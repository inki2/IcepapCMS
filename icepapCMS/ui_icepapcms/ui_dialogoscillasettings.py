# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogoscillasettings.ui'
#
# Created: Thu Nov 15 13:04:50 2018
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
        DialogOscillaSettings.resize(450, 429)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DialogOscillaSettings.sizePolicy().hasHeightForWidth())
        DialogOscillaSettings.setSizePolicy(sizePolicy)
        DialogOscillaSettings.setModal(True)
        self.bbOscillaSettings = QtGui.QDialogButtonBox(DialogOscillaSettings)
        self.bbOscillaSettings.setGeometry(QtCore.QRect(20, 380, 171, 32))
        self.bbOscillaSettings.setOrientation(QtCore.Qt.Horizontal)
        self.bbOscillaSettings.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.bbOscillaSettings.setObjectName(_fromUtf8("bbOscillaSettings"))
        self.gbSampling = QtGui.QGroupBox(DialogOscillaSettings)
        self.gbSampling.setGeometry(QtCore.QRect(10, 10, 391, 181))
        self.gbSampling.setObjectName(_fromUtf8("gbSampling"))
        self.sbSampleRate = QtGui.QSpinBox(self.gbSampling)
        self.sbSampleRate.setGeometry(QtCore.QRect(300, 30, 71, 24))
        self.sbSampleRate.setPrefix(_fromUtf8(""))
        self.sbSampleRate.setMinimum(10)
        self.sbSampleRate.setMaximum(1000)
        self.sbSampleRate.setSingleStep(10)
        self.sbSampleRate.setProperty("value", 50)
        self.sbSampleRate.setObjectName(_fromUtf8("sbSampleRate"))
        self.sbDumpRate = QtGui.QSpinBox(self.gbSampling)
        self.sbDumpRate.setGeometry(QtCore.QRect(300, 80, 71, 24))
        self.sbDumpRate.setMinimum(1)
        self.sbDumpRate.setMaximum(20)
        self.sbDumpRate.setProperty("value", 2)
        self.sbDumpRate.setObjectName(_fromUtf8("sbDumpRate"))
        self.label = QtGui.QLabel(self.gbSampling)
        self.label.setGeometry(QtCore.QRect(18, 30, 241, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.gbSampling)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 211, 20))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_4 = QtGui.QLabel(self.gbSampling)
        self.label_4.setGeometry(QtCore.QRect(20, 140, 221, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.leGuiUpdateRate = QtGui.QLineEdit(self.gbSampling)
        self.leGuiUpdateRate.setEnabled(False)
        self.leGuiUpdateRate.setGeometry(QtCore.QRect(302, 140, 71, 23))
        self.leGuiUpdateRate.setReadOnly(False)
        self.leGuiUpdateRate.setObjectName(_fromUtf8("leGuiUpdateRate"))
        self.groupBox = QtGui.QGroupBox(DialogOscillaSettings)
        self.groupBox.setGeometry(QtCore.QRect(10, 220, 391, 71))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(20, 30, 211, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.spLenAxisX = QtGui.QSpinBox(self.groupBox)
        self.spLenAxisX.setGeometry(QtCore.QRect(296, 30, 71, 24))
        self.spLenAxisX.setMinimum(10)
        self.spLenAxisX.setMaximum(3600)
        self.spLenAxisX.setSingleStep(10)
        self.spLenAxisX.setProperty("value", 30)
        self.spLenAxisX.setObjectName(_fromUtf8("spLenAxisX"))
        self.btnOK = QtGui.QPushButton(DialogOscillaSettings)
        self.btnOK.setGeometry(QtCore.QRect(350, 360, 80, 23))
        self.btnOK.setObjectName(_fromUtf8("btnOK"))
        self.btnCancel = QtGui.QPushButton(DialogOscillaSettings)
        self.btnCancel.setGeometry(QtCore.QRect(350, 390, 80, 23))
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))

        self.retranslateUi(DialogOscillaSettings)
        QtCore.QObject.connect(self.bbOscillaSettings, QtCore.SIGNAL(_fromUtf8("accepted()")), DialogOscillaSettings.accept)
        QtCore.QObject.connect(self.bbOscillaSettings, QtCore.SIGNAL(_fromUtf8("rejected()")), DialogOscillaSettings.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogOscillaSettings)

    def retranslateUi(self, DialogOscillaSettings):
        DialogOscillaSettings.setWindowTitle(_translate("DialogOscillaSettings", "Oscilloscope Settings", None))
        self.gbSampling.setTitle(_translate("DialogOscillaSettings", "Data Collection", None))
        self.label.setText(_translate("DialogOscillaSettings", "Sample Rate [ms between samples]", None))
        self.label_2.setText(_translate("DialogOscillaSettings", "GUI Dump Rate [samples/dump]", None))
        self.label_4.setText(_translate("DialogOscillaSettings", "Resulting GUI Update Rate [ms]", None))
        self.groupBox.setTitle(_translate("DialogOscillaSettings", "X-axis", None))
        self.label_3.setText(_translate("DialogOscillaSettings", "Default length [seconds]", None))
        self.btnOK.setText(_translate("DialogOscillaSettings", "OK", None))
        self.btnCancel.setText(_translate("DialogOscillaSettings", "Cancel", None))

