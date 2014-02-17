# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created: Thu Jul 11 15:23:15 2013
#      by: PyQt4 UI code generator 4.10
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

class Ui_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName(_fromUtf8("main_window"))
        main_window.resize(687, 603)
        self.gridLayout = QtGui.QGridLayout(main_window)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.plotBox = QtGui.QVBoxLayout()
        self.plotBox.setObjectName(_fromUtf8("plotBox"))
        self.gridLayout.addLayout(self.plotBox, 1, 1, 1, 1)
        self.controlBox = QtGui.QVBoxLayout()
        self.controlBox.setObjectName(_fromUtf8("controlBox"))
        self.groupBox = QtGui.QGroupBox(main_window)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.save = QtGui.QPushButton(self.groupBox)
        self.save.setObjectName(_fromUtf8("save"))
        self.verticalLayout.addWidget(self.save)
        self.controlBox.addWidget(self.groupBox)
        self.timebaseBox = QtGui.QGroupBox(main_window)
        self.timebaseBox.setObjectName(_fromUtf8("timebaseBox"))
        self.formLayout = QtGui.QFormLayout(self.timebaseBox)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
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
        self.gridLayout.addLayout(self.controlBox, 1, 0, 2, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.plot = QtGui.QPushButton(main_window)
        self.plot.setObjectName(_fromUtf8("plot"))
        self.horizontalLayout.addWidget(self.plot)
        self.refreshAuto = QtGui.QCheckBox(main_window)
        self.refreshAuto.setObjectName(_fromUtf8("refreshAuto"))
        self.horizontalLayout.addWidget(self.refreshAuto)
        self.refreshDelay = QtGui.QSpinBox(main_window)
        self.refreshDelay.setMaximum(525600)
        self.refreshDelay.setObjectName(_fromUtf8("refreshDelay"))
        self.horizontalLayout.addWidget(self.refreshDelay)
        self.checkMosaic = QtGui.QCheckBox(main_window)
        self.checkMosaic.setObjectName(_fromUtf8("checkMosaic"))
        self.horizontalLayout.addWidget(self.checkMosaic)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 1, 1, 1)

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        main_window.setWindowTitle(_translate("main_window", "HP54616B Oscilloscope", None))
        self.groupBox.setTitle(_translate("main_window", "Save plot", None))
        self.save.setText(_translate("main_window", "Save", None))
        self.timebaseBox.setTitle(_translate("main_window", "Time base", None))
        self.label_2.setText(_translate("main_window", "Mode", None))
        self.label_3.setText(_translate("main_window", "Delay", None))
        self.label.setText(_translate("main_window", "Range", None))
        self.plot.setText(_translate("main_window", "Plot", None))
        self.refreshAuto.setText(_translate("main_window", "Refresh every", None))
        self.refreshDelay.setSuffix(_translate("main_window", "ms", None))
        self.checkMosaic.setText(_translate("main_window", "MOSAIC", None))

