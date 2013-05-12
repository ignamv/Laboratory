# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created: Sat May 11 11:04:56 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName(_fromUtf8("main_window"))
        main_window.resize(487, 312)
        self.gridLayout = QtGui.QGridLayout(main_window)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.controlBox = QtGui.QVBoxLayout()
        self.controlBox.setObjectName(_fromUtf8("controlBox"))
        self.timebaseBox = QtGui.QGroupBox(main_window)
        self.timebaseBox.setObjectName(_fromUtf8("timebaseBox"))
        self.formLayout = QtGui.QFormLayout(self.timebaseBox)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_2 = QtGui.QLabel(self.timebaseBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.timebase_mode = QtGui.QComboBox(self.timebaseBox)
        self.timebase_mode.setObjectName(_fromUtf8("timebase_mode"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.timebase_mode)
        self.label_3 = QtGui.QLabel(self.timebaseBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_3)
        self.timebase_delay = QtGui.QDoubleSpinBox(self.timebaseBox)
        self.timebase_delay.setObjectName(_fromUtf8("timebase_delay"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.timebase_delay)
        self.label = QtGui.QLabel(self.timebaseBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label)
        self.timebase_range = QtGui.QDoubleSpinBox(self.timebaseBox)
        self.timebase_range.setObjectName(_fromUtf8("timebase_range"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.timebase_range)
        self.controlBox.addWidget(self.timebaseBox)
        self.gridLayout.addLayout(self.controlBox, 0, 0, 2, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.plot = QtGui.QPushButton(main_window)
        self.plot.setObjectName(_fromUtf8("plot"))
        self.horizontalLayout.addWidget(self.plot)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.refreshAuto = QtGui.QCheckBox(main_window)
        self.refreshAuto.setObjectName(_fromUtf8("refreshAuto"))
        self.horizontalLayout.addWidget(self.refreshAuto)
        self.refreshDelay = QtGui.QSpinBox(main_window)
        self.refreshDelay.setMaximum(525600)
        self.refreshDelay.setObjectName(_fromUtf8("refreshDelay"))
        self.horizontalLayout.addWidget(self.refreshDelay)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 1)
        self.plotBox = QtGui.QVBoxLayout()
        self.plotBox.setObjectName(_fromUtf8("plotBox"))
        self.gridLayout.addLayout(self.plotBox, 0, 1, 1, 1)

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        main_window.setWindowTitle(QtGui.QApplication.translate("main_window", "HP54616B Oscilloscope", None, QtGui.QApplication.UnicodeUTF8))
        self.timebaseBox.setTitle(QtGui.QApplication.translate("main_window", "Time base", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("main_window", "Mode", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("main_window", "Delay", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("main_window", "Range", None, QtGui.QApplication.UnicodeUTF8))
        self.plot.setText(QtGui.QApplication.translate("main_window", "Plot", None, QtGui.QApplication.UnicodeUTF8))
        self.refreshAuto.setText(QtGui.QApplication.translate("main_window", "Refresh every", None, QtGui.QApplication.UnicodeUTF8))
        self.refreshDelay.setSuffix(QtGui.QApplication.translate("main_window", "ms", None, QtGui.QApplication.UnicodeUTF8))

