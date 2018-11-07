from PyQt4 import QtGui
from PyQt4 import QtCore
from ui_oscilla import Ui_OscillaWindow
from lib_icepapcms import Collector  # Todo: Cannot find reference 'Collector' in '__init__.py
import pyqtgraph as pg
from collections import namedtuple
import time


class AxisTime(pg.AxisItem):
    """
    Formats axis labels to human readable time.
    values  - List of time values (Format: Seconds since 1970).
    scale   - Not used.
    spacing - Not used.
    """
    def tickStrings(self, values, scale, spacing):
        strings = []
        for x in values:
            try:
                strings.append(time.strftime("%H:%M:%S", time.gmtime(x)))
            except ValueError:  # Windows can't handle dates before 1970.
                strings.append('')
        return strings


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
        self.array_time = []  # Todo: Protect from simultaneous writing?
        self.array_val = []
        self.val_min = 0  # Todo: Maybe never have smaller.
        self.val_max = 0  # Todo: Maybe never have bigger.
        sig_vals = self.signals[str(sig_name)]
        self.color = sig_vals.pen_color
        self.pen = {'color': sig_vals.pen_color, 'width': sig_vals.pen_width, 'style': sig_vals.pen_style}
        self.curve = None
        self.signature = ''
        self.update_signature()

    def update_signature(self):
        """Sets the new value of the signature string."""
        self.signature = '{}:{}:{}'.format(self.driver_addr, self.signal_name, self.y_axis)

    def create_curve(self):
        self.curve = pg.PlotCurveItem(x=self.array_time, y=self.array_val, pen=self.pen)
        return self.curve

    def update_curve(self):
        self.curve.setData(x=self.array_time, y=self.array_val)

    def get_y(self, t_val):
        """
        Retrieve the signal value corresponding to the provided time value.

        t_val - Time value.
        Return: Signal value corresponding to an adjacent sample in time.
        """
        for x, v in zip(self.array_time, self.array_val):
            if x > t_val:
                return v


class OscillaWindow(QtGui.QMainWindow):
    """A dialog for plotting IcePAP signals."""

    def __init__(self, host, port, selected_driver=None):
        """
        Initializes an instance of class OscillaWindow.

        host - IcePAP system address.
        port - IcePAP system port number.
        """
        QtGui.QMainWindow.__init__(self, None)

        try:
            self.collector = Collector(host, port, self.callback_plot)
        except Exception as e:
            msg = 'Failed to create main window.\n{}'.format(e)
            print(msg)
            QtGui.QMessageBox.critical(None, 'Create Main Window', msg)  # Todo: Fix warning.
            return

        self.subscriptions = {}
        self.curve_items = []
        self._paused = False

        self.ui = Ui_OscillaWindow()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.ui.setupUi(self)
        self.setWindowTitle('Oscilla  |  ' + host)

        self.plot_widget = pg.PlotWidget()
        self._plot_item = self.plot_widget.getPlotItem()
        self.view_boxes = [self.plot_widget.getViewBox(), pg.ViewBox(), pg.ViewBox()]
        self.ui.vloCurves.setDirection(QtGui.QBoxLayout.BottomToTop)
        self.ui.vloCurves.addWidget(self.plot_widget)

        # Set up the X-axis.
        self._plot_item.getAxis('bottom').hide()  # Hide the old x-axis.
        self._axisTime = AxisTime(orientation='bottom')  # Create a new X-axis with human readable time labels.
        self._axisTime.linkToView(self.view_boxes[0])
        self._plot_item.layout.addItem(self._axisTime, 3, 1)
        self._initial_x_range = 30  # [seconds]
        self.now = self.collector.get_current_time()
        self.view_boxes[0].setXRange(self.now - self._initial_x_range, self.now, padding=0)

        # Set up the three Y-axes.
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
        self.view_boxes[0].addItem(self.label)

        self.vertical_line = pg.InfiniteLine(angle=90, movable=False)
        self.view_boxes[0].addItem(self.vertical_line, ignoreBounds=True)

        self._fill_combo_box_driver_ids(selected_driver)
        self._fill_combo_box_signals()
        self._select_axis_1()
        self._update_button_status()

        self._connect_signals()
        self.proxy = pg.SignalProxy(self.plot_widget.scene().sigMouseMoved, rateLimit=60, slot=self._mouse_moved)

    def _fill_combo_box_driver_ids(self, selected_driver):
        driver_ids = self.collector.get_available_drivers()
        for driver_id in driver_ids:
            self.ui.cbDrivers.addItem(str(driver_id))
        start_index = 0
        if selected_driver is not None:
            start_index = self.ui.cbDrivers.findText(str(selected_driver))
        self.ui.cbDrivers.setCurrentIndex(start_index)

    def _fill_combo_box_signals(self):
        sig_items = []
        for sig_name, sig_vals in CurveItem.signals.items():
            sig_items.append((sig_vals.drop_down_list_pos, sig_name))
        sig_items.sort()
        for i in sig_items:
            self.ui.cbSignals.addItem(i[1])
        self.ui.cbSignals.setCurrentIndex(0)

    def _connect_signals(self):
        self.ui.rbAxis1.clicked.connect(self._select_axis_1)
        self.ui.rbAxis2.clicked.connect(self._select_axis_2)
        self.ui.rbAxis3.clicked.connect(self._select_axis_3)
        self.ui.btnAdd.clicked.connect(self._add_button_clicked)
        self.ui.btnShift.clicked.connect(self._shift_button_clicked)
        self.ui.btnRemoveSel.clicked.connect(self._remove_selected_signal)
        self.ui.btnRemoveAll.clicked.connect(self._remove_all_signals)
        self.ui.btnClearSignal.clicked.connect(self._clear_selected_signal)
        self.ui.btnClearAll.clicked.connect(self._clear_all_signals)
        self.ui.btnCLoop.clicked.connect(self._prepare_closed_loop)
        self.ui.btnCurrents.clicked.connect(self._prepare_currents)
        self.ui.btnTarget.clicked.connect(self._prepare_target)
        self.ui.btnPause.clicked.connect(self._pause_button_clicked)
        self.ui.btnNow.clicked.connect(self._now_button_clicked)
        self.view_boxes[0].sigResized.connect(self._update_views)

    def _update_views(self):
        """Updates the geometry of the view boxes."""
        self.view_boxes[1].setGeometry(self.view_boxes[0].sceneBoundingRect())
        self.view_boxes[2].setGeometry(self.view_boxes[0].sceneBoundingRect())
        self.view_boxes[1].linkedViewChanged(self.view_boxes[0], self.view_boxes[1].XAxis)
        self.view_boxes[2].linkedViewChanged(self.view_boxes[0], self.view_boxes[2].XAxis)

    def _update_button_status(self):
        val = self.ui.lvActiveSig.count() == 0
        self.ui.btnShift.setDisabled(val)
        self.ui.btnRemoveSel.setDisabled(val)
        self.ui.btnRemoveAll.setDisabled(val)
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
        self._add_signal(addr, my_signal_name, my_axis)

    def _add_signal(self, driver_addr, signal_name, y_axis):
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
        self._add_curve(ci)
        self.curve_items.append(ci)
        self.ui.lvActiveSig.addItem(ci.signature)
        index = len(self.curve_items) - 1
        self.ui.lvActiveSig.setCurrentRow(index)
        self.ui.lvActiveSig.item(index).setForeground(ci.color)
        self.ui.lvActiveSig.item(index).setBackground(QtGui.QColor(0, 0, 0))
        self._update_plot_axes_labels()
        self._update_button_status()

    def _remove_selected_signal(self):
        index = self.ui.lvActiveSig.currentRow()
        ci = self.curve_items[index]
        self.collector.unsubscribe(ci.subscription_id)
        self._remove_curve_plot(ci)
        self.ui.lvActiveSig.takeItem(index)
        self.curve_items.remove(ci)
        self._update_plot_axes_labels()
        self._update_button_status()

    def _remove_all_signals(self):
        """Removes all signals."""
        for ci in self.curve_items:
            self.collector.unsubscribe(ci.subscription_id)
            self._remove_curve_plot(ci)
        self.ui.lvActiveSig.clear()
        self.curve_items = []
        self._update_plot_axes_labels()
        self._update_button_status()

    def _clear_selected_signal(self):
        """Remove the visible data for a signal."""
        index = self.ui.lvActiveSig.currentRow()
        self.curve_items[index].array_time = []
        self.curve_items[index].array_val = []

    def _clear_all_signals(self):
        """Remove the visible data for all signals."""
        for ci in self.curve_items:
            ci.array_time = []
            ci.array_val = []

    def _shift_button_clicked(self):
        """Assign a curve to a different y axis."""
        index = self.ui.lvActiveSig.currentRow()
        ci = self.curve_items[index]
        self._remove_curve_plot(ci)
        ci.y_axis = (ci.y_axis % 3) + 1
        ci.update_signature()
        self._add_curve(ci)
        self.ui.lvActiveSig.takeItem(index)
        self.ui.lvActiveSig.insertItem(index, ci.signature)
        self.ui.lvActiveSig.item(index).setForeground(ci.color)
        self.ui.lvActiveSig.item(index).setBackground(QtGui.QColor(0, 0, 0))
        self.ui.lvActiveSig.setCurrentRow(index)
        self._update_plot_axes_labels()

    def _add_curve(self, ci):
        """
        Create a new curve and add it to a viewbox.

        ci - Curve item that will be the owner.
        """
        my_curve = ci.create_curve()
        self.view_boxes[ci.y_axis - 1].addItem(my_curve)

    def _mouse_moved(self, evt):  # Todo: Review this.
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

    def _remove_curve_plot(self, ci):
        """
        Remove a curve from the plot area.

        ci - Curve item to remove.
        """
        self.view_boxes[ci.y_axis - 1].removeItem(ci.curve)

    def _prepare_closed_loop(self):
        """Display a specific set of curves."""
        self._remove_all_signals()
        drv_addr = int(self.ui.cbDrivers.currentText())
        self._add_signal(drv_addr, 'PosAxis', 1)
        self._add_signal(drv_addr, 'DifAxTgtenc', 2)
        self._add_signal(drv_addr, 'DifAxMotor', 2)
        self._add_signal(drv_addr, 'StatReady', 3)
        self._add_signal(drv_addr, 'StatMoving', 3)
        self._add_signal(drv_addr, 'StatSettling', 3)
        self._add_signal(drv_addr, 'StatOutofwin', 3)

    def _prepare_currents(self):
        """Display a specific set of curves."""
        self._remove_all_signals()
        drv_addr = int(self.ui.cbDrivers.currentText())
        self._add_signal(drv_addr, 'PosAxis', 1)
        self._add_signal(drv_addr, 'MeasI', 2)
        self._add_signal(drv_addr, 'MeasVm', 3)

    def _prepare_target(self):
        """Display a specific set of curves."""
        self._remove_all_signals()
        drv_addr = int(self.ui.cbDrivers.currentText())
        self._add_signal(drv_addr, 'PosAxis', 1)
        self._add_signal(drv_addr, 'EncTgtenc', 2)

    def _now_button_clicked(self):
        """Pan X axis to display newest values."""
        self.now = self.collector.get_current_time()
        x_small = self.view_boxes[0].viewRange()[0][0]
        x_big = self.view_boxes[0].viewRange()[0][1]
        self.view_boxes[0].setXRange(self.now - (x_big - x_small), self.now, padding=0)

    def _pause_button_clicked(self):
        """Freeze the X axis."""
        if self._paused:
            self._paused = False
            self.ui.btnPause.setText('Pause')
        else:
            self._paused = True
            self.ui.btnPause.setText('Run')

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
        if not self._paused:
            self._update_view()

    def _update_view(self):
        # Update the X-axis.
        x_small = self.view_boxes[0].viewRange()[0][0]
        x_big = self.view_boxes[0].viewRange()[0][1]
        now_in_range = self.now <= x_big
        self.now = self.collector.get_current_time()
        if now_in_range:
            self.view_boxes[0].setXRange(self.now - (x_big - x_small), self.now, padding=0)
        self.ui.btnNow.setDisabled(now_in_range)

        # Update the curves.
        for ci in self.curve_items:
            ci.update_curve()
