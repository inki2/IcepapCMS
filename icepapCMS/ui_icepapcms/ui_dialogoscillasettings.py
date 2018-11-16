# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogoscillasettings.ui'
#
# Created: Fri Nov 16 13:05:27 2018
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_DialogOscillaSettings(object):
    def setupUi(self, DialogOscillaSettings):
        DialogOscillaSettings.setObjectName(_fromUtf8("DialogOscillaSettings"))
        DialogOscillaSettings.resize(601, 395)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DialogOscillaSettings.sizePolicy().hasHeightForWidth())
        DialogOscillaSettings.setSizePolicy(sizePolicy)
        DialogOscillaSettings.setModal(False)
        self.bbOscillaSettings = QtGui.QDialogButtonBox(DialogOscillaSettings)
        self.bbOscillaSettings.setGeometry(QtCore.QRect(100, 350, 171, 32))
        self.bbOscillaSettings.setOrientation(QtCore.Qt.Horizontal)
        self.bbOscillaSettings.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.bbOscillaSettings.setObjectName(_fromUtf8("bbOscillaSettings"))
        self.gbSampling = QtGui.QGroupBox(DialogOscillaSettings)
        self.gbSampling.setGeometry(QtCore.QRect(50, 20, 391, 181))
        self.gbSampling.setObjectName(_fromUtf8("gbSampling"))
        self.sbSampleRate = QtGui.QSpinBox(self.gbSampling)
        self.sbSampleRate.setGeometry(QtCore.QRect(300, 30, 71, 24))
        self.sbSampleRate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sbSampleRate.setPrefix(_fromUtf8(""))
        self.sbSampleRate.setMinimum(1)
        self.sbSampleRate.setMaximum(2)
        self.sbSampleRate.setSingleStep(1)
        self.sbSampleRate.setProperty("value", 2)
        self.sbSampleRate.setObjectName(_fromUtf8("sbSampleRate"))
        self.sbDumpRate = QtGui.QSpinBox(self.gbSampling)
        self.sbDumpRate.setGeometry(QtCore.QRect(260, 80, 71, 24))
        self.sbDumpRate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sbDumpRate.setMinimum(1)
        self.sbDumpRate.setMaximum(20)
        self.sbDumpRate.setProperty("value", 2)
        self.sbDumpRate.setObjectName(_fromUtf8("sbDumpRate"))
        self.labelSampleRate = QtGui.QLabel(self.gbSampling)
        self.labelSampleRate.setGeometry(QtCore.QRect(18, 30, 241, 20))
        self.labelSampleRate.setObjectName(_fromUtf8("labelSampleRate"))
        self.labelDumpRate = QtGui.QLabel(self.gbSampling)
        self.labelDumpRate.setGeometry(QtCore.QRect(40, 80, 211, 20))
        self.labelDumpRate.setObjectName(_fromUtf8("labelDumpRate"))
        self.labelGuiRate = QtGui.QLabel(self.gbSampling)
        self.labelGuiRate.setGeometry(QtCore.QRect(70, 150, 221, 16))
        self.labelGuiRate.setObjectName(_fromUtf8("labelGuiRate"))
        self.leGuiUpdateRate = QtGui.QLineEdit(self.gbSampling)
        self.leGuiUpdateRate.setEnabled(False)
        self.leGuiUpdateRate.setGeometry(QtCore.QRect(302, 140, 71, 23))
        self.leGuiUpdateRate.setReadOnly(False)
        self.leGuiUpdateRate.setObjectName(_fromUtf8("leGuiUpdateRate"))
        self.groupBox = QtGui.QGroupBox(DialogOscillaSettings)
        self.groupBox.setGeometry(QtCore.QRect(180, 220, 391, 71))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.labelXAxisLength = QtGui.QLabel(self.groupBox)
        self.labelXAxisLength.setGeometry(QtCore.QRect(20, 30, 211, 16))
        self.labelXAxisLength.setObjectName(_fromUtf8("labelXAxisLength"))
        self.sbLenAxisX = QtGui.QSpinBox(self.groupBox)
        self.sbLenAxisX.setGeometry(QtCore.QRect(240, 30, 71, 24))
        self.sbLenAxisX.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sbLenAxisX.setMinimum(1)
        self.sbLenAxisX.setMaximum(2)
        self.sbLenAxisX.setSingleStep(1)
        self.sbLenAxisX.setProperty("value", 2)
        self.sbLenAxisX.setObjectName(_fromUtf8("sbLenAxisX"))

        self.retranslateUi(DialogOscillaSettings)
        QtCore.QObject.connect(self.bbOscillaSettings, QtCore.SIGNAL(_fromUtf8("accepted()")), DialogOscillaSettings.accept)
        QtCore.QObject.connect(self.bbOscillaSettings, QtCore.SIGNAL(_fromUtf8("rejected()")), DialogOscillaSettings.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogOscillaSettings)

    def retranslateUi(self, DialogOscillaSettings):
        DialogOscillaSettings.setWindowTitle(_translate("DialogOscillaSettings", "Oscilloscope Settings", None))
        self.gbSampling.setTitle(_translate("DialogOscillaSettings", "Data Collection", None))
        self.labelSampleRate.setText(_translate("DialogOscillaSettings", "Sample Rate [ms between samples]", None))
        self.labelDumpRate.setText(_translate("DialogOscillaSettings", "GUI Dump Rate [samples/dump]", None))
        self.labelGuiRate.setText(_translate("DialogOscillaSettings", "Resulting GUI Update Rate [ms]", None))
        self.groupBox.setTitle(_translate("DialogOscillaSettings", "X-axis", None))
        self.labelXAxisLength.setText(_translate("DialogOscillaSettings", "Default/Reset Length [seconds]", None))

