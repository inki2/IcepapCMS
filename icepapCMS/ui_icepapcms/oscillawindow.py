from PyQt4 import QtGui
from PyQt4 import QtCore
from ui_oscilla import Ui_OscillaWindow
from lib_icepapcms import Collector
from collections import namedtuple
from threading import RLock
import pyqtgraph as pg
import time


class _AxisTime(pg.AxisItem):
    """
    Formats axis labels to human readable time.
    values  - List of time values (Format: Seconds since 1970).
    scale   - Not used.
    spacing - Not used.
    """
    def tickStrings(self, values, scale, spacing):
        """We override this function to have the X-axis labels display our way."""
        strings = []
        for x in values:
            try:
                strings.append(time.strftime("%H:%M:%S", time.gmtime(x)))
            except ValueError:  # Time out of range.
                strings.append('')
        return strings


class CurveItem:  # Todo: Move to its own file?
    """Represents a curve to be plotted in a diagram."""

    SignalAppearance = namedtuple('SignalAppearance', ['pen_color', 'pen_width', 'pen_style'])

    colors = [SignalAppearance(QtGui.QColor(255, 255, 0), 1, QtCore.Qt.SolidLine),
              SignalAppearance(QtGui.QColor(255, 0, 0), 1, QtCore.Qt.SolidLine),
              SignalAppearance(QtGui.QColor(0, 255, 0), 1, QtCore.Qt.SolidLine),
              SignalAppearance(QtGui.QColor(255, 255, 255), 1, QtCore.Qt.SolidLine),
              SignalAppearance(QtGui.QColor(51, 153, 255), 1, QtCore.Qt.SolidLine),
              SignalAppearance(QtGui.QColor(0, 255, 255), 1, QtCore.Qt.SolidLine),
              SignalAppearance(QtGui.QColor(255, 0, 255), 1, QtCore.Qt.SolidLine),
              SignalAppearance(QtGui.QColor(204, 153, 102), 1, QtCore.Qt.SolidLine),
              SignalAppearance(QtGui.QColor(0, 0, 255), 1, QtCore.Qt.SolidLine),
              SignalAppearance(QtGui.QColor(0, 255, 0), 1, QtCore.Qt.SolidLine),
              SignalAppearance(QtGui.QColor(255, 204, 0), 1, QtCore.Qt.SolidLine),
              SignalAppearance(QtGui.QColor(153, 255, 153), 2, QtCore.Qt.DotLine),
              SignalAppearance(QtGui.QColor(255, 170, 0), 2, QtCore.Qt.DashLine),
              SignalAppearance(QtGui.QColor(255, 0, 0), 2, QtCore.Qt.DashLine),
              SignalAppearance(QtGui.QColor(0, 255, 255), 1, QtCore.Qt.DotLine),
              SignalAppearance(QtGui.QColor(255, 170, 255), 1, QtCore.Qt.DashLine),
              SignalAppearance(QtGui.QColor(127, 255, 127), 1, QtCore.Qt.DashLine),
              SignalAppearance(QtGui.QColor(255, 255, 127), 1, QtCore.Qt.DashLine),
              SignalAppearance(QtGui.QColor(255, 0, 0), 2, QtCore.Qt.DotLine),
              SignalAppearance(QtGui.QColor(255, 0, 0), 1, QtCore.Qt.DashLine),
              SignalAppearance(QtGui.QColor(0, 255, 0), 2, QtCore.Qt.DotLine),
              SignalAppearance(QtGui.QColor(255, 255, 255), 2, QtCore.Qt.SolidLine),
              SignalAppearance(QtGui.QColor(51, 153, 255), 1, QtCore.Qt.DashLine),
              SignalAppearance(QtGui.QColor(255, 0, 255), 1, QtCore.Qt.DashLine),
              SignalAppearance(QtGui.QColor(255, 153, 204), 1, QtCore.Qt.DashLine),
              SignalAppearance(QtGui.QColor(204, 153, 102), 1, QtCore.Qt.DashLine),
              SignalAppearance(QtGui.QColor(255, 204, 0), 1, QtCore.Qt.DashLine),
              SignalAppearance(QtGui.QColor(255, 0, 255), 1, QtCore.Qt.DashLine),
              SignalAppearance(QtGui.QColor(255, 153, 204), 1, QtCore.Qt.DashLine),
              SignalAppearance(QtGui.QColor(204, 153, 102), 1, QtCore.Qt.DashLine),
              SignalAppearance(QtGui.QColor(255, 204, 0), 1, QtCore.Qt.DashLine)]

    def __init__(self, subscription_id, driver_addr, sig_name, y_axis, color_idx):
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
        self.array_time = []
        self.array_val = []
        self.val_min = 0
        self.val_max = 0
        col_item = self.colors[color_idx]
        self.color = col_item.pen_color
        self.pen = {'color': col_item.pen_color, 'width': col_item.pen_width, 'style': col_item.pen_style}
        self.curve = None
        self.lock = RLock()
        self.signature = ''
        self.update_signature()

    def update_signature(self):
        """Sets the new value of the signature string."""
        self.signature = '{}:{}:{}'.format(self.driver_addr, self.signal_name, self.y_axis)

    def create_curve(self):
        """Creates a new plot item."""
        with self.lock:
            self.curve = pg.PlotCurveItem(x=self.array_time, y=self.array_val, pen=self.pen)
        return self.curve

    def update_curve(self, time_min, time_max):
        """Updates the curve with recent collected data."""
        with self.lock:
            idx_min = self._get_time_index(time_min)
            idx_max = self._get_time_index(time_max)
            self.curve.setData(x=self.array_time[idx_min:idx_max], y=self.array_val[idx_min:idx_max])

    def in_range(self, t):
        """
        Check to see if time is within range of collected data.

        t - Time value.
        Return: True if time is within range of collected data. Otherwise False.
        """
        with self.lock:
            if self.array_time and self.array_time[0] < t < self.array_time[-1]:
                return True
        return False

    def start_time(self):
        """
        Get time for first data sample.

        Return: Time of the first collected data sample. -1 if none.
        """
        with self.lock:
            if self.array_time:
                return self.array_time[0]
        return -1

    def collect(self, new_data):
        """Store new collected data."""
        with self.lock:
            if not self.array_val:
                self.val_min = self.val_max = new_data[0][1]
            for t, v in new_data:
                self.array_time.append(t)
                self.array_val.append(v)
                if v > self.val_max:
                    self.val_max = v
                elif v < self.val_min:
                    self.val_min = v

    def get_y(self, time_val):
        """
        Retrieve the signal value corresponding to the provided time value.

        t_val - Time value.
        Return: Signal value corresponding to an adjacent sample in time.
        """
        with self.lock:
            idx = self._get_time_index(time_val)
            return self.array_val[idx]

    def _get_time_index(self, time_val):
        """
        Retrieve the sample index corresponding to the provided time value.

        t_val - Time value.
        Return: Index of a sample adjacent to the provided time value.
        """
        with self.lock:
            if not self.array_time:
                return -1
            if len(self.array_time) == 1:
                return 0
            time_min = self.array_time[0]
            time_max = self.array_time[-1]
            if time_val < time_min:
                return 0
            elif time_val > time_max:
                return len(self.array_time)
            idx = int(((time_val - time_min) / (time_max - time_min)) * len(self.array_time))
            while self.array_time[idx] > time_val:
                idx -= 1
            while self.array_time[idx] < time_val:
                idx += 1
            return idx


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
            self.collector = Collector(host, port, self.callback_collect)
        except Exception as e:
            msg = 'Failed to create main window.\n{}'.format(e)
            print(msg)
            QtGui.QMessageBox.critical(None, 'Create Main Window', msg)
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
        self._plot_item.getAxis('bottom').hide()  # Hide the original x-axis.
        self._axisTime = _AxisTime(orientation='bottom')  # Create a new X-axis with human readable time labels.
        self._axisTime.linkToView(self.view_boxes[0])
        self._plot_item.layout.removeItem(self._plot_item.getAxis('bottom'))
        self._plot_item.layout.addItem(self._axisTime, 3, 1)
        self.now = self.collector.get_current_time()
        self._view_last_30_seconds()

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
        self._plot_item.hideButtons()

        self.view_boxes[0].disableAutoRange(axis=self.view_boxes[0].XAxis)
        self.view_boxes[1].disableAutoRange(axis=self.view_boxes[1].XAxis)
        self.view_boxes[2].disableAutoRange(axis=self.view_boxes[2].XAxis)
        self._enable_auto_range_y()

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
        signals = self.collector.get_available_signals()
        num_colors = len(CurveItem.colors)
        if num_colors < len(signals):
            msg = 'Internal error!\nNew signals added.\nAdd more colors and pens.'
            print(msg)
            QtGui.QMessageBox.warning(None, 'Available Signals', msg)
            for i in range(num_colors):
                self.ui.cbSignals.addItem(signals[i])
        else:
            for sig in signals:
                self.ui.cbSignals.addItem(sig)
        self.ui.cbSignals.setCurrentIndex(0)

    def _connect_signals(self):
        self.ui.rbAxis1.clicked.connect(self._select_axis_1)
        self.ui.rbAxis2.clicked.connect(self._select_axis_2)
        self.ui.rbAxis3.clicked.connect(self._select_axis_3)
        self.ui.btnAdd.clicked.connect(self._add_button_clicked)
        self.ui.btnShift.clicked.connect(self._shift_button_clicked)
        self.ui.btnRemoveSel.clicked.connect(self._remove_selected_signal)
        self.ui.btnRemoveAll.clicked.connect(self._remove_all_signals)
        self.ui.btnCLoop.clicked.connect(self._setup_signal_set_closed_loop)
        self.ui.btnCurrents.clicked.connect(self._setup_signal_set_currents)
        self.ui.btnTarget.clicked.connect(self._setup_signal_set_target)
        self.ui.btnSeeAll.clicked.connect(self._view_all_data)
        self.ui.btn30sec.clicked.connect(self._view_last_30_seconds)
        self.ui.btnResetY.clicked.connect(self._enable_auto_range_y)
        self.ui.btnPause.clicked.connect(self._pause_x_axis)
        self.ui.btnNow.clicked.connect(self._goto_now)
        self.view_boxes[0].sigResized.connect(self._update_views)

    def closeEvent(self, event):
        self._remove_all_signals()
        event.accept()

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

    def _update_plot_axes_labels(self):
        txt = ['', '', '']
        for ci in self.curve_items:
            t = "<span style='font-size: 8pt; color: {};'>{}</span>".format(ci.color.name(), ci.signature)
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
        my_signal_name = str(self.ui.cbSignals.currentText())
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
            msg = 'Failed to subscribe to signal {} from driver {}.\n{}'.format(signal_name, driver_addr, e)
            print(msg)
            QtGui.QMessageBox.critical(None, 'Add Curve', msg)
            return
        try:
            color_idx = self.collector.get_signal_index(signal_name)
        except ValueError as e:
            msg = 'Internal error. Failed to retrieve index for signal {}.\n{}'.format(signal_name, e)
            print(msg)
            QtGui.QMessageBox.critical(None, 'Add Curve', msg)
            return
        ci = CurveItem(subscription_id, driver_addr, signal_name, y_axis, color_idx)
        self._add_curve(ci)
        self.curve_items.append(ci)
        self.collector.start(subscription_id)
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

    def _mouse_moved(self, evt):
        """
        Acts om mouse move.

        evt - Event containing the position of the mouse pointer.
        """
        pos = evt[0]  # The signal proxy turns original arguments into a tuple.
        if self.plot_widget.sceneBoundingRect().contains(pos):
            mouse_point = self.view_boxes[0].mapSceneToView(pos)
            time_value = mouse_point.x()
            try:
                pretty_time = time.strftime("%H:%M:%S", time.gmtime(time_value))
            except ValueError:  # Time out of range.
                return
            txtmax = ''
            txtnow = ''
            txtmin = ''
            for ci in self.curve_items:
                txt1 = "<span style='font-size: 8pt; color: {};'>|".format(ci.color.name())
                if ci.in_range(time_value):
                    txtmax += "{}{}</span>".format(txt1, ci.val_max)
                    txtnow += "{}{}</span>".format(txt1, ci.get_y(time_value))
                    txtmin += "{}{}</span>".format(txt1, ci.val_min)
            txtnow += "|<span style='font-size: 8pt; color: white;'>{}</span>".format(pretty_time)
            self.plot_widget.setTitle("<br>{}<br>{}<br>{}".format(txtmax, txtnow, txtmin))
            self.vertical_line.setPos(mouse_point.x())

    def _remove_curve_plot(self, ci):
        """
        Remove a curve from the plot area.

        ci - Curve item to remove.
        """
        self.view_boxes[ci.y_axis - 1].removeItem(ci.curve)

    def _setup_signal_set_closed_loop(self):
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

    def _setup_signal_set_currents(self):
        """Display a specific set of curves."""
        self._remove_all_signals()
        drv_addr = int(self.ui.cbDrivers.currentText())
        self._add_signal(drv_addr, 'PosAxis', 1)
        self._add_signal(drv_addr, 'MeasI', 2)
        self._add_signal(drv_addr, 'MeasVm', 3)

    def _setup_signal_set_target(self):
        """Display a specific set of curves."""
        self._remove_all_signals()
        drv_addr = int(self.ui.cbDrivers.currentText())
        self._add_signal(drv_addr, 'PosAxis', 1)
        self._add_signal(drv_addr, 'EncTgtenc', 2)

    def _view_all_data(self):
        """Adjust X axis to view all collected data."""
        time_start = self.collector.get_current_time()
        for ci in self.curve_items:
            t = ci.start_time()
            if 0 < t < time_start:
                time_start = t
        self.view_boxes[0].setXRange(time_start, self.collector.get_current_time(), padding=0)

    def _view_last_30_seconds(self):
        """Adjust X axis to view the last 30 seconds."""
        now = self.collector.get_current_time()
        self.view_boxes[0].setXRange(now - 30, now, padding=0)

    def _enable_auto_range_y(self):
        self.view_boxes[0].enableAutoRange(axis=self.view_boxes[0].YAxis)
        self.view_boxes[1].enableAutoRange(axis=self.view_boxes[1].YAxis)
        self.view_boxes[2].enableAutoRange(axis=self.view_boxes[2].YAxis)

    def _pause_x_axis(self):
        """Freeze the X axis."""
        if self._paused:
            self._paused = False
            self.ui.btnPause.setText('Pause')
        else:
            self._paused = True
            self.ui.btnPause.setText('Run')

    def _goto_now(self):
        """Pan X axis to display newest values."""
        now = self.collector.get_current_time()
        x_min = self.view_boxes[0].viewRange()[0][0]
        x_max = self.view_boxes[0].viewRange()[0][1]
        self.view_boxes[0].setXRange(now - (x_max - x_min), now, padding=0)

    def callback_collect(self, subscription_id, value_list):
        """
        Callback function that stores the data collected from IcePAP.

        subscription_id - Subscription id.
        value_list - List of tuples (time, value).
        """
        for ci in self.curve_items:
            if ci.subscription_id == subscription_id:
                ci.collect(value_list)
        if not self._paused:
            self._update_view()

    def _update_view(self):
        x_min = self.view_boxes[0].viewRange()[0][0]
        x_max = self.view_boxes[0].viewRange()[0][1]

        # Update the X-axis.
        now_in_range = self.now <= x_max
        self.now = self.collector.get_current_time()
        if now_in_range:
            self.view_boxes[0].setXRange(self.now - (x_max - x_min), self.now, padding=0)
        self.ui.btnNow.setDisabled(now_in_range)

        # Update the curves.
        for ci in self.curve_items:
            ci.update_curve(x_min, x_max)
