from PyQt4.QtGui import QDialog
from ui_dialogoscillasettings import Ui_DialogOscillaSettings


class DialogOscillaSettings(QDialog):

    def __init__(self, parent, settings):
        QDialog.__init__(self, parent)
        self.ui = Ui_DialogOscillaSettings()
        self.ui.setupUi(self)
        self._connect_signals()
        self._update_gui_rate()
        self.settings = settings
        self.ui.sbSampleRate.setMinimum(self.settings.sample_rate_min)
        self.ui.sbSampleRate.setMaximum(self.settings.sample_rate_max)
        self.ui.sbSampleRate.setValue(self.settings.sample_rate)
        self.ui.sbDumpRate.setMinimum(self.settings.dump_rate_min)
        self.ui.sbDumpRate.setMaximum(self.settings.dump_rate_max)
        self.ui.sbDumpRate.setValue(self.settings.dump_rate)
        self.ui.sbLenAxisX.setMinimum(self.settings.default_x_axis_length_min)
        self.ui.sbLenAxisX.setMaximum(self.settings.default_x_axis_length_max)
        self.ui.sbLenAxisX.setValue(self.settings.default_x_axis_length)

    def _connect_signals(self):
        self.ui.sbSampleRate.valueChanged.connect(self._update_gui_rate)
        self.ui.sbDumpRate.valueChanged.connect(self._update_gui_rate)
        self.ui.bbOscillaSettings.accepted.connect(self._settings_accepted)
        self.ui.bbOscillaSettings.rejected.connect(self.close)

    def _settings_accepted(self):
        self.settings.sample_rate = self.ui.sbSampleRate.value()
        self.settings.dump_rate = self.ui.sbDumpRate.value()
        self.settings.default_x_axis_length = self.ui.sbLenAxisX.value()
        self.settings.announce_update()
        self.close()

    def _update_gui_rate(self):
        self.ui.leGuiUpdateRate.setText(str(self.ui.sbSampleRate.value() * self.ui.sbDumpRate.value()))
