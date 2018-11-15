from PyQt4 import QtGui
from ui_dialogoscillasettings import Ui_DialogOscillaSettings


class DialogOscillaSettings(QtGui.QDialog):

    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_DialogOscillaSettings()
        self.ui.setupUi(self)
        self._connect_signals()
        self.sample_rate = 0
        self.dump_rate = 0
        self.default_x_axis_len = 0

    def _connect_signals(self):
        self.ui.sbSampleRate.editingFinished.connect(self._set_sample_rate)
        self.ui.sbDumpRate.editingFinished.connect(self._set_dump_rate)
        self.ui.btnOK.clicked.connect(self._clicked_ok)
        self.ui.btnCancel.clicked.connect(self.close)
        self.ui.bbOscillaSettings.clicked.connect(self._button_box_clicked)

    def _set_sample_rate(self):
        self._update_gui_rate()

    def _set_dump_rate(self):
        self._update_gui_rate()

    #def _set_default_x_axis_len(self):
    #    msg = 'Freetext field does not work with pyIcePAP API v2.'
    #    print(msg)
    #    MessageDialogs.showErrorMessage(None, 'Freetest Box', msg)

    def _button_box_clicked(self):
        pass

    def _clicked_ok(self):
        self.sample_rate = self.ui.sbSampleRate.value()
        self.dump_rate = self.ui.sbDumpRate.value()
        self.default_x_axis_len = self.ui.spLenAxisX.value()
        self.close()

    def _update_gui_rate(self):
        self.ui.leGuiUpdateRate.setText(str(self.ui.sbSampleRate.value() * self.ui.sbDumpRate.value()))
