# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'homing.ui'
#
# Created: Tue Aug  4 15:08:47 2009
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_homing(object):
    def setupUi(self, homing):
        homing.setObjectName("homing")
        homing.resize(250, 329)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(homing.sizePolicy().hasHeightForWidth())
        homing.setSizePolicy(sizePolicy)
        homing.setMinimumSize(QtCore.QSize(250, 250))
        self.gridlayout = QtGui.QGridLayout(homing)
        self.gridlayout.setObjectName("gridlayout")
        self.homing_frame = QtGui.QFrame(homing)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.homing_frame.sizePolicy().hasHeightForWidth())
        self.homing_frame.setSizePolicy(sizePolicy)
        self.homing_frame.setMinimumSize(QtCore.QSize(182, 260))
        self.homing_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.homing_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.homing_frame.setObjectName("homing_frame")
        self.vboxlayout = QtGui.QVBoxLayout(self.homing_frame)
        self.vboxlayout.setObjectName("vboxlayout")
        self.gridlayout1 = QtGui.QGridLayout()
        self.gridlayout1.setObjectName("gridlayout1")
        self.label_9 = QtGui.QLabel(self.homing_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QtCore.QSize(100, 16))
        self.label_9.setMaximumSize(QtCore.QSize(16777215, 22))
        self.label_9.setObjectName("label_9")
        self.gridlayout1.addWidget(self.label_9, 0, 0, 1, 1)
        self.cfgHOMESRC = QtGui.QComboBox(self.homing_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cfgHOMESRC.sizePolicy().hasHeightForWidth())
        self.cfgHOMESRC.setSizePolicy(sizePolicy)
        self.cfgHOMESRC.setMinimumSize(QtCore.QSize(70, 16))
        self.cfgHOMESRC.setMaximumSize(QtCore.QSize(16777215, 22))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.cfgHOMESRC.setFont(font)
        self.cfgHOMESRC.setObjectName("cfgHOMESRC")
        self.gridlayout1.addWidget(self.cfgHOMESRC, 0, 1, 1, 1)
        self.label_10 = QtGui.QLabel(self.homing_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setMinimumSize(QtCore.QSize(100, 16))
        self.label_10.setMaximumSize(QtCore.QSize(16777215, 22))
        self.label_10.setObjectName("label_10")
        self.gridlayout1.addWidget(self.label_10, 1, 0, 1, 1)
        self.cfgHOMETYPE = QtGui.QComboBox(self.homing_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cfgHOMETYPE.sizePolicy().hasHeightForWidth())
        self.cfgHOMETYPE.setSizePolicy(sizePolicy)
        self.cfgHOMETYPE.setMinimumSize(QtCore.QSize(70, 16))
        self.cfgHOMETYPE.setMaximumSize(QtCore.QSize(16777215, 22))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.cfgHOMETYPE.setFont(font)
        self.cfgHOMETYPE.setObjectName("cfgHOMETYPE")
        self.gridlayout1.addWidget(self.cfgHOMETYPE, 1, 1, 1, 1)
        self.vboxlayout.addLayout(self.gridlayout1)
        spacerItem = QtGui.QSpacerItem(370, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.vboxlayout.addItem(spacerItem)
        self.label_4 = QtGui.QLabel(self.homing_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(150, 16))
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 22))
        self.label_4.setObjectName("label_4")
        self.vboxlayout.addWidget(self.label_4)
        self.line_2 = QtGui.QFrame(self.homing_frame)
        self.line_2.setMinimumSize(QtCore.QSize(150, 0))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.vboxlayout.addWidget(self.line_2)
        self.cfgHOMEFLAGS = QtGui.QFrame(self.homing_frame)
        self.cfgHOMEFLAGS.setFrameShape(QtGui.QFrame.NoFrame)
        self.cfgHOMEFLAGS.setFrameShadow(QtGui.QFrame.Plain)
        self.cfgHOMEFLAGS.setObjectName("cfgHOMEFLAGS")
        self.gridlayout2 = QtGui.QGridLayout(self.cfgHOMEFLAGS)
        self.gridlayout2.setObjectName("gridlayout2")
        spacerItem1 = QtGui.QSpacerItem(50, 20, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem1, 0, 0, 1, 1)
        self.cfgHOMEFLAGS_AUTODIR = QtGui.QCheckBox(self.cfgHOMEFLAGS)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cfgHOMEFLAGS_AUTODIR.sizePolicy().hasHeightForWidth())
        self.cfgHOMEFLAGS_AUTODIR.setSizePolicy(sizePolicy)
        self.cfgHOMEFLAGS_AUTODIR.setMinimumSize(QtCore.QSize(150, 16))
        self.cfgHOMEFLAGS_AUTODIR.setMaximumSize(QtCore.QSize(16777215, 22))
        self.cfgHOMEFLAGS_AUTODIR.setObjectName("cfgHOMEFLAGS_AUTODIR")
        self.gridlayout2.addWidget(self.cfgHOMEFLAGS_AUTODIR, 0, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(50, 20, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem2, 1, 0, 1, 1)
        self.cfgHOMEFLAGS_REVERSE = QtGui.QCheckBox(self.cfgHOMEFLAGS)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cfgHOMEFLAGS_REVERSE.sizePolicy().hasHeightForWidth())
        self.cfgHOMEFLAGS_REVERSE.setSizePolicy(sizePolicy)
        self.cfgHOMEFLAGS_REVERSE.setMinimumSize(QtCore.QSize(150, 16))
        self.cfgHOMEFLAGS_REVERSE.setMaximumSize(QtCore.QSize(16777215, 22))
        self.cfgHOMEFLAGS_REVERSE.setObjectName("cfgHOMEFLAGS_REVERSE")
        self.gridlayout2.addWidget(self.cfgHOMEFLAGS_REVERSE, 1, 1, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(50, 20, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem3, 2, 0, 1, 1)
        self.cfgHOMEFLAGS_SETPOS = QtGui.QCheckBox(self.cfgHOMEFLAGS)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cfgHOMEFLAGS_SETPOS.sizePolicy().hasHeightForWidth())
        self.cfgHOMEFLAGS_SETPOS.setSizePolicy(sizePolicy)
        self.cfgHOMEFLAGS_SETPOS.setMinimumSize(QtCore.QSize(150, 16))
        self.cfgHOMEFLAGS_SETPOS.setMaximumSize(QtCore.QSize(16777215, 22))
        self.cfgHOMEFLAGS_SETPOS.setObjectName("cfgHOMEFLAGS_SETPOS")
        self.gridlayout2.addWidget(self.cfgHOMEFLAGS_SETPOS, 2, 1, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(50, 20, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem4, 3, 0, 1, 1)
        self.cfgHOMEFLAGS_SLOW = QtGui.QCheckBox(self.cfgHOMEFLAGS)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cfgHOMEFLAGS_SLOW.sizePolicy().hasHeightForWidth())
        self.cfgHOMEFLAGS_SLOW.setSizePolicy(sizePolicy)
        self.cfgHOMEFLAGS_SLOW.setMinimumSize(QtCore.QSize(150, 16))
        self.cfgHOMEFLAGS_SLOW.setMaximumSize(QtCore.QSize(16777215, 22))
        self.cfgHOMEFLAGS_SLOW.setObjectName("cfgHOMEFLAGS_SLOW")
        self.gridlayout2.addWidget(self.cfgHOMEFLAGS_SLOW, 3, 1, 1, 1)
        self.vboxlayout.addWidget(self.cfgHOMEFLAGS)
        spacerItem5 = QtGui.QSpacerItem(370, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.vboxlayout.addItem(spacerItem5)
        self.gridlayout3 = QtGui.QGridLayout()
        self.gridlayout3.setObjectName("gridlayout3")
        self.label_7 = QtGui.QLabel(self.homing_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMinimumSize(QtCore.QSize(100, 16))
        self.label_7.setMaximumSize(QtCore.QSize(16777215, 22))
        self.label_7.setObjectName("label_7")
        self.gridlayout3.addWidget(self.label_7, 0, 0, 1, 1)
        self.cfgHOMEPOS = QtGui.QSpinBox(self.homing_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cfgHOMEPOS.sizePolicy().hasHeightForWidth())
        self.cfgHOMEPOS.setSizePolicy(sizePolicy)
        self.cfgHOMEPOS.setMinimumSize(QtCore.QSize(70, 16))
        self.cfgHOMEPOS.setMaximumSize(QtCore.QSize(16777215, 22))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.cfgHOMEPOS.setFont(font)
        self.cfgHOMEPOS.setProperty("text", QtCore.QVariant(QtGui.QApplication.translate("homing", "0", None, QtGui.QApplication.UnicodeUTF8)))
        self.cfgHOMEPOS.setMaximum(999999999)
        self.cfgHOMEPOS.setObjectName("cfgHOMEPOS")
        self.gridlayout3.addWidget(self.cfgHOMEPOS, 0, 1, 1, 1)
        self.label_8 = QtGui.QLabel(self.homing_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMinimumSize(QtCore.QSize(100, 16))
        self.label_8.setMaximumSize(QtCore.QSize(16777215, 22))
        self.label_8.setObjectName("label_8")
        self.gridlayout3.addWidget(self.label_8, 1, 0, 1, 1)
        self.cfgHOMEVEL = QtGui.QDoubleSpinBox(self.homing_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cfgHOMEVEL.sizePolicy().hasHeightForWidth())
        self.cfgHOMEVEL.setSizePolicy(sizePolicy)
        self.cfgHOMEVEL.setMinimumSize(QtCore.QSize(70, 16))
        self.cfgHOMEVEL.setMaximumSize(QtCore.QSize(16777215, 22))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.cfgHOMEVEL.setFont(font)
        self.cfgHOMEVEL.setProperty("text", QtCore.QVariant(QtGui.QApplication.translate("homing", "0.00", None, QtGui.QApplication.UnicodeUTF8)))
        self.cfgHOMEVEL.setMaximum(999999999.0)
        self.cfgHOMEVEL.setSingleStep(0.01)
        self.cfgHOMEVEL.setObjectName("cfgHOMEVEL")
        self.gridlayout3.addWidget(self.cfgHOMEVEL, 1, 1, 1, 1)
        self.vboxlayout.addLayout(self.gridlayout3)
        self.gridlayout.addWidget(self.homing_frame, 0, 0, 1, 1)

        self.retranslateUi(homing)
        QtCore.QMetaObject.connectSlotsByName(homing)

    def retranslateUi(self, homing):
        homing.setWindowTitle(QtGui.QApplication.translate("homing", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("homing", "Reference signal", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("homing", "Signal type", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("homing", "Flags", None, QtGui.QApplication.UnicodeUTF8))
        self.cfgHOMEFLAGS_AUTODIR.setText(QtGui.QApplication.translate("homing", "auto direction", None, QtGui.QApplication.UnicodeUTF8))
        self.cfgHOMEFLAGS_REVERSE.setText(QtGui.QApplication.translate("homing", "reverse search", None, QtGui.QApplication.UnicodeUTF8))
        self.cfgHOMEFLAGS_SETPOS.setText(QtGui.QApplication.translate("homing", "set axis position", None, QtGui.QApplication.UnicodeUTF8))
        self.cfgHOMEFLAGS_SLOW.setText(QtGui.QApplication.translate("homing", "slow search mode", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("homing", "Home position", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("homing", "search velocity", None, QtGui.QApplication.UnicodeUTF8))
