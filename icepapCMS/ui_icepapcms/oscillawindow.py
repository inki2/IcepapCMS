try:
    from PyQt5 import QtGui
    from PyQt5 import QtCore
    from PyQt5 import Qt
except ImportError as ie:
    from PyQt4 import QtGui
    from PyQt4 import QtCore
    from PyQt4 import Qt
from ui_oscilla import Ui_OscillaWindow
from lib_icepapcms.oscillacollector import Collector
import pyqtgraph as pg
from collections import namedtuple
import time


class CurveItem:
    """Represents a curve to be plotted in a diagram."""

    SignalAppearance = namedtuple('SignalAppearance', ['pen_color', 'pen_width', 'pen_style', 'drop_down_list_pos'])

    signals = {'PosAxis': SignalAppearance(QtGui.QColor(255, 255, 0), 1, QtCore.Qt.SolidLine, 0),
               'PosTgtenc': SignalAppearance(QtGui.QColor(255, 0, 0), 1, QtCore.Qt.SolidLine, 1),
               'PosShftenc': SignalAppearance(QtGui.QColor(0, 255, 0), 1, QtCore.Qt.SolidLine, 2),
               'PosEncin': SignalAppearance(QtGui.QColor(255, 255, 255), 1, QtCore.Qt.SolidLine, 3),
               'PosAbsenc': SignalAppearance(QtGui.QColor(51, 153, 255), 1, QtCore.Qt.SolidLine, 4),
               'PosInpos': SignalAppearance(QtGui.QColor(0, 255, 255), 1, QtCore.Qt.SolidLine, 5),
               'PosMotor': SignalAppearance(QtGui.QColor(255, 0, 255), 1, QtCore.Qt.SolidLine, 6),
               'PosCtrlenc': SignalAppearance(QtGui.QColor(204, 153, 102), 1, QtCore.Qt.SolidLine, 7),
               'PosMeasure': SignalAppearance(QtGui.QColor(0, 0, 255), 1, QtCore.Qt.SolidLine, 8),
               'DifAxMeasure': SignalAppearance(QtGui.QColor(0, 255, 0), 1, QtCore.Qt.SolidLine, 9),
               'DifAxMotor': SignalAppearance(QtGui.QColor(255, 204, 0), 1, QtCore.Qt.SolidLine, 10),
               'DifAxTgtenc': SignalAppearance(QtGui.QColor(153, 255, 153), 3, QtCore.Qt.DotLine, 11),
               'DifAxShftenc': SignalAppearance(QtGui.QColor(255, 170, 0), 2, QtCore.Qt.DashLine, 12),
               'DifAxCtrlenc': SignalAppearance(QtGui.QColor(255, 0, 0), 3, QtCore.Qt.DashLine, 13),
               'EncEncin': SignalAppearance(QtGui.QColor(0, 255, 255), 1, QtCore.Qt.DotLine, 14),
               'EncAbsenc': SignalAppearance(QtGui.QColor(255, 170, 255), 1, QtCore.Qt.DashLine, 15),
               'EncTgtenc': SignalAppearance(QtGui.QColor(127, 255, 127), 1, QtCore.Qt.DashLine, 16),
               'EncInpos': SignalAppearance(QtGui.QColor(255, 255, 127), 1, QtCore.Qt.DashLine, 17),
               'StatReady': SignalAppearance(QtGui.QColor(255, 0, 0), 5, QtCore.Qt.DotLine, 18),
               'StatMoving': SignalAppearance(QtGui.QColor(255, 0, 0), 1, QtCore.Qt.DashLine, 19),
               'StatSettling': SignalAppearance(QtGui.QColor(0, 255, 0), 3, QtCore.Qt.DotLine, 20),
               'StatOutofwin': SignalAppearance(QtGui.QColor(255, 255, 255), 2, QtCore.Qt.SolidLine, 21),
               'StatStopcode': SignalAppearance(QtGui.QColor(51, 153, 255), 1, QtCore.Qt.DashLine, 22),
               'StatWarning': SignalAppearance(QtGui.QColor(255, 0, 255), 1, QtCore.Qt.DashLine, 23),
               'StatLim+': SignalAppearance(QtGui.QColor(255, 153, 204), 1, QtCore.Qt.DashLine, 24),
               'StatLim-': SignalAppearance(QtGui.QColor(204, 153, 102), 1, QtCore.Qt.DashLine, 25),
               'StatHome': SignalAppearance(QtGui.QColor(255, 204, 0), 1, QtCore.Qt.DashLine, 26),
               'MeasI': SignalAppearance(QtGui.QColor(255, 0, 255), 1, QtCore.Qt.DashLine, 27),
               'MeasIa': SignalAppearance(QtGui.QColor(255, 153, 204), 1, QtCore.Qt.DashLine, 28),
               'MeasIb': SignalAppearance(QtGui.QColor(204, 153, 102), 1, QtCore.Qt.DashLine, 29),
               'MeasVm': SignalAppearance(QtGui.QColor(255, 204, 0), 1, QtCore.Qt.DashLine, 30)}

    def __init__(self, subscription_id, driver_addr, sig_name, y_axis):
        """
        Initializes an instance of class CurveItem.

        driver_addr - IcePAP driver address.
        sig_name    - Signal name.
        y_axis      - Y axis to plot against.
        """
        self.subscription_id = subscription_id
        self.driver_addr = driver_addr
        self.signal_name = sig_name
        self.y_axis = y_axis
        self.start_over = True
        self.array_time = []
        self.array_val = []
        self.val_min = 0
        self.val_max = 0
        sig_vals = self.signals[str(sig_name)]
        self.color = sig_vals.pen_color
        self.pen = {'color': sig_vals.pen_color, 'width': sig_vals.pen_width, 'style': sig_vals.pen_style}
        self.curve_plot = None
        self.signature = ''
        self.update_signature()

    def update_signature(self):
        """Sets the new value of the signature string."""
        self.signature = '{}:{}:{}'.format(self.driver_addr, self.signal_name, self.y_axis)

    def get_y(self, t):
        """
        Retrieve the signal value corresponding to the provided time value.

        t - Time value.
        Return: Signal value corresponding to an adjacent sample in time.
        """
        for x, v in zip(self.array_time, self.array_val):
            if x > t:
                return v


class OscillaWindow(QtGui.QMainWindow):
    """A dialog for plotting IcePAP signals."""

    def __init__(self, host, port):
        """
        Initializes an instance of class OscillaWindow.

        host - IcePAP system address.
        port - IcePAP system port number.
        """
        QtGui.QMainWindow.__init__(self, None)
        self.ui = Ui_OscillaWindow()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        try:
            self.collector = Collector(host, port, self.callback_plot)
        except Exception as e:
            msg = 'Failed to create main window.\n{}'.format(e)
            print(msg)
            QtGui.QMessageBox.critical(None, 'Create Main Window', msg)
            return

        self.subscriptions = {}

        self.ui.setupUi(self)
        self.setWindowTitle('Oscilla  |  ' + host)
        self.curve_items = []

        self.plot_widget = pg.PlotWidget()
        self.view_boxes = [self.plot_widget.getViewBox(), pg.ViewBox(), pg.ViewBox()]
        self.view_boxes[0].setXRange(time.time() - 30, time.time(), padding=0)
        self._plot_item = self.plot_widget.getPlotItem()
        self.ui.vloCurves.setDirection(QtGui.QBoxLayout.BottomToTop)
        self.ui.vloCurves.addWidget(self.plot_widget)
        self._plot_item.showAxis('right')
        self._plot_item.scene().addItem(self.view_boxes[1])
        self._plot_item.scene().addItem(self.view_boxes[2])
        ax3 = pg.AxisItem(orientation='right', linkView=self.view_boxes[2])
        self.axes = [self._plot_item.getAxis('left'), self._plot_item.getAxis('right'), ax3]
        self.axes[1].linkToView(self.view_boxes[1])
        self.view_boxes[1].setXLink(self.view_boxes[0])
        self.view_boxes[2].setXLink(self.view_boxes[0])
        self._plot_item.layout.addItem(self.axes[2], 2, 3)
        self.view_boxes[0].disableAutoRange(axis=self.view_boxes[0].XAxis)
        self.view_boxes[0].enableAutoRange(axis=self.view_boxes[0].YAxis)
        self.view_boxes[1].disableAutoRange(axis=self.view_boxes[1].XAxis)
        self.view_boxes[1].enableAutoRange(axis=self.view_boxes[1].YAxis)
        self.view_boxes[2].disableAutoRange(axis=self.view_boxes[2].XAxis)
        self.view_boxes[2].enableAutoRange(axis=self.view_boxes[2].YAxis)
        self.label = pg.LabelItem(justify='right')
        self.vertical_line = pg.InfiniteLine(angle=90, movable=False)
        self.view_boxes[0].addItem(self.vertical_line, ignoreBounds=True)
        self.view_boxes[0].addItem(self.label)

        self._fill_combo_box_driver_ids()
        self._fill_combo_box_signals()
        self._select_axis_1()
        self._update_button_status()

        self.ref_time = time.time()
        self.last_now = None
        self.ticker = Qt.QTimer(self)
        self.tick_interval = 1000  # [milliseconds]

        self._connect_signals()
        self.proxy = pg.SignalProxy(self.plot_widget.scene().sigMouseMoved, rateLimit=60, slot=self.mouse_moved)

        self.ticker.start(self.tick_interval)

    def _fill_combo_box_driver_ids(self):
        driver_ids = self.collector.get_available_drivers()
        for driver_id in driver_ids:
            self.ui.cbDrivers.addItem(str(driver_id))
        self.ui.cbDrivers.setCurrentIndex(0)

    def _fill_combo_box_signals(self):
        sig_items = []
        for sig_name, sig_vals in CurveItem.signals.items():
            sig_items.append((sig_vals.drop_down_list_pos, sig_name))
        sig_items.sort()
        for i in sig_items:
            self.ui.cbSignals.addItem(i[1])
        self.ui.cbSignals.setCurrentIndex(0)

    def _connect_signals(self):
        QtCore.QObject.connect(self.ticker, QtCore.SIGNAL("timeout()"), self._tick)
        self.ui.rbAxis1.clicked.connect(self._select_axis_1)
        self.ui.rbAxis2.clicked.connect(self._select_axis_2)
        self.ui.rbAxis3.clicked.connect(self._select_axis_3)
        self.ui.btnAdd.clicked.connect(self._add_button_clicked)
        self.ui.btnShift.clicked.connect(self.shift_button_clicked)
        self.ui.btnRemove.clicked.connect(self._remove_button_clicked)
        self.ui.btnClearSignal.clicked.connect(self.clear_signal)
        self.ui.btnClearAll.clicked.connect(self.clear_all_signals)
        self.ui.btnCLoop.clicked.connect(self.prepare_closed_loop)
        self.ui.btnCurrents.clicked.connect(self.prepare_currents)
        self.ui.btnTarget.clicked.connect(self.prepare_target)
        self.ui.btnPause.clicked.connect(self.pause_button_clicked)
        self.ui.btnNow.clicked.connect(self.now_button_clicked)
        self.view_boxes[0].sigResized.connect(self.update_views)

    def update_views(self):
        """Updates the geometry of the view boxes."""
        self.view_boxes[1].setGeometry(self.view_boxes[0].sceneBoundingRect())
        self.view_boxes[2].setGeometry(self.view_boxes[0].sceneBoundingRect())
        self.view_boxes[1].linkedViewChanged(self.view_boxes[0], self.view_boxes[1].XAxis)
        self.view_boxes[2].linkedViewChanged(self.view_boxes[0], self.view_boxes[2].XAxis)

    def _update_button_status(self):
        val = self.ui.lvActiveSig.count() == 0
        self.ui.btnShift.setDisabled(val)
        self.ui.btnRemove.setDisabled(val)
        self.ui.btnClearSignal.setDisabled(val)
        self.ui.btnClearAll.setDisabled(val)

    def _update_plot_axes_labels(self):
        txt = ['', '', '']
        for ci in self.curve_items:
            t = "<span style='font-size: 8pt; color: %s;'>%s</span>" % (ci.color.name(), ci.signature)
            txt[ci.y_axis - 1] += t
        for i in range(0, len(self.axes)):
            self.axes[i].setLabel(txt[i])

    def _select_axis_1(self):
        self.ui.rbAxis1.setChecked(True)
        self.ui.rbAxis2.setChecked(False)
        self.ui.rbAxis3.setChecked(False)

    def _select_axis_2(self):
        self.ui.rbAxis1.setChecked(False)
        self.ui.rbAxis2.setChecked(True)
        self.ui.rbAxis3.setChecked(False)

    def _select_axis_3(self):
        self.ui.rbAxis1.setChecked(False)
        self.ui.rbAxis2.setChecked(False)
        self.ui.rbAxis3.setChecked(True)

    def _add_button_clicked(self):
        addr = int(self.ui.cbDrivers.currentText())
        my_signal_name = self.ui.cbSignals.currentText()
        my_axis = 1
        if self.ui.rbAxis2.isChecked():
            my_axis = 2
        elif self.ui.rbAxis3.isChecked():
            my_axis = 3
        self.add_curve(addr, my_signal_name, my_axis)

    def callback_plot(self, subscription_id, value_list):
        for ci in self.curve_items:
            if ci.subscription_id == subscription_id:
                for t, v in value_list:
                    ci.array_time.append(t)
                    ci.array_val.append(v)
                    if v > ci.val_max:
                        ci.val_max = v
                    elif v < ci.val_min:
                        ci.val_min = v

    def add_curve(self, driver_addr, signal_name, y_axis):
        """
        Adds a new curve to the plot area.

        driver_addr - IcePAP driver address.
        signal_name - Signal name.
        y_axis      - Y axis to plot against.
        """
        try:
            subscription_id = self.collector.subscribe(driver_addr, signal_name)
        except Exception as e:
            msg = 'Failed to add curve.\n{}'.format(e)
            print(msg)
            QtGui.QMessageBox.critical(None, 'Add Curve', msg)
            return
        ci = CurveItem(subscription_id, driver_addr, signal_name, y_axis)
        self.collector.start(subscription_id)
        self.plot_curve(ci)
        self.curve_items.append(ci)
        self.ui.lvActiveSig.addItem(ci.signature)
        index = len(self.curve_items) - 1
        self.ui.lvActiveSig.setCurrentRow(index)
        self.ui.lvActiveSig.item(index).setForeground(ci.color)
        self.ui.lvActiveSig.item(index).setBackground(QtGui.QColor(0, 0, 0))
        self._update_plot_axes_labels()
        self._update_button_status()

    def clear_all_signals(self):
        """Remove the visible data for all signals."""
        self.ref_time = time.time()
        for ci in self.curve_items:
            ci.start_over = True

    def shift_button_clicked(self):
        """Assign a curve to a different y axis."""
        index = self.ui.lvActiveSig.currentRow()
        ci = self.curve_items[index]
        self.remove_curve_plot(ci)
        ci.y_axis = (ci.y_axis % 3) + 1  # Todo: Have bug in IcePAPcms.
        ci.update_signature()
        self.plot_curve(ci)
        self.ui.lvActiveSig.takeItem(index)
        self.ui.lvActiveSig.insertItem(index, ci.signature)
        self.ui.lvActiveSig.item(index).setForeground(ci.color)
        self.ui.lvActiveSig.item(index).setBackground(QtGui.QColor(0, 0, 0))
        self.ui.lvActiveSig.setCurrentRow(index)
        self._update_plot_axes_labels()

    def plot_curve(self, ci):
        """
        Plot a curve.

        ci - Curve item to plot.
        """
        ci.curve_plot = pg.PlotCurveItem(x=ci.array_time, y=ci.array_val, pen=ci.pen)
        self.view_boxes[ci.y_axis - 1].addItem(ci.curve_plot)

    def clear_signal(self):
        """Remove the visible data for a signal."""
        index = self.ui.lvActiveSig.currentRow()
        self.curve_items[index].start_over = True

    def _remove_button_clicked(self):
        index = self.ui.lvActiveSig.currentRow()
        ci = self.curve_items[index]
        self.collector.unsubscribe(ci.subscription_id)
        self.remove_curve_plot(ci)
        self.ui.lvActiveSig.takeItem(index)
        self.curve_items.remove(ci)
        self._update_plot_axes_labels()
        self._update_button_status()

    def remove_all_signals(self):
        """Removes all signals."""
        for ci in self.curve_items:
            self.collector.unsubscribe(ci.subscription_id)
            self.remove_curve_plot(ci)
        self.ui.lvActiveSig.clear()
        self.curve_items = []
        self._update_plot_axes_labels()
        self._update_button_status()

    def mouse_moved(self, evt):
        """
        Acts om mouse move.

        evt - Event containing the position of the mouse pointer.
        """
        pos = evt[0]  # The signal proxy turns original arguments into a tuple.
        if self.plot_widget.sceneBoundingRect().contains(pos):
            mouse_point = self.view_boxes[0].mapSceneToView(pos)
            time_value = mouse_point.x()
            txt = "<span style='font-size: 8pt; color: white;'>" + "%0.2f" % time_value + "</span>"
            txtmax = ''
            txtmin = ''
            for ci in self.curve_items:
                if ci.array_time and ci.array_time[0] < time_value < ci.array_time[-1]:
                    txt1 = "<span style='font-size: 8pt; color: %s;'>" % ci.color.name() + '|'
                    txt += txt1 + str(ci.get_y(time_value)) + "</span>"
                    txtmin += txt1 + str(ci.val_min) + "</span>"
                    txtmax += txt1 + str(ci.val_max) + "</span>"
            self.plot_widget.setTitle("<br>%s<br>%s<br>%s" % (txtmax, txt, txtmin))
            self.vertical_line.setPos(mouse_point.x())

    def remove_curve_plot(self, ci):
        """
        Remove a curve from the plot area.

        ci - Curve item to remove.
        """
        self.view_boxes[ci.y_axis - 1].removeItem(ci.curve_plot)

    def prepare_closed_loop(self):
        """Display a specific set of curves."""
        self.remove_all_signals()
        drv_addr = int(self.ui.cbDrivers.currentText())
        self.add_curve(drv_addr, 'PosAxis', 1)
        self.add_curve(drv_addr, 'DifAxTgtenc', 2)
        self.add_curve(drv_addr, 'DifAxMotor', 2)
        self.add_curve(drv_addr, 'StatReady', 3)
        self.add_curve(drv_addr, 'StatMoving', 3)
        self.add_curve(drv_addr, 'StatSettling', 3)
        self.add_curve(drv_addr, 'StatOutofwin', 3)

    def prepare_currents(self):
        """Display a specific set of curves."""
        self.remove_all_signals()
        drv_addr = int(self.ui.cbDrivers.currentText())
        self.add_curve(drv_addr, 'PosAxis', 1)
        self.add_curve(drv_addr, 'MeasI', 2)
        self.add_curve(drv_addr, 'MeasVm', 3)

    def prepare_target(self):
        """Display a specific set of curves."""
        self.remove_all_signals()
        drv_addr = int(self.ui.cbDrivers.currentText())
        self.add_curve(drv_addr, 'PosAxis', 1)
        self.add_curve(drv_addr, 'EncTgtenc', 2)

    def now_button_clicked(self):
        """Pan X axis to display newest values."""
        #now = time.time() - self.ref_time
        now = time.time()
        x_small = self.view_boxes[0].viewRange()[0][0]
        x_big = self.view_boxes[0].viewRange()[0][1]
        self.view_boxes[0].setXRange(now - (x_big - x_small), now, padding=0)

    def pause_button_clicked(self):
        """Freeze the X axis."""
        if self.ticker.isActive():
            self.ticker.stop()
            self.ui.btnPause.setText('Run')
        else:
            self.ticker.start(self.tick_interval)
            self.ui.btnPause.setText('Pause')

    def _tick(self):
        #now = time.time() - self.ref_time
        now = time.time()
        x_small = self.view_boxes[0].viewRange()[0][0]
        x_big = self.view_boxes[0].viewRange()[0][1]
        now_in_range = self.last_now <= x_big
        if now_in_range:
            self.view_boxes[0].setXRange(now - (x_big - x_small), now, padding=0)
        self.ui.btnNow.setDisabled(now_in_range)
        for ci in self.curve_items:
            ci.curve_plot.setData(x=ci.array_time, y=ci.array_val)
        self.last_now = now
        self.ticker.start(self.tick_interval)
