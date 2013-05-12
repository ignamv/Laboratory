# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'channel_controls.ui'
#
# Created: Sat May 11 11:05:48 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_channel_controls(object):
    def setupUi(self, channel_controls):
        channel_controls.setObjectName(_fromUtf8("channel_controls"))
        channel_controls.resize(400, 300)
        self.formLayout = QtGui.QFormLayout(channel_controls)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(channel_controls)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.range = QtGui.QDoubleSpinBox(channel_controls)
        self.range.setObjectName(_fromUtf8("range"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.range)
        self.label_2 = QtGui.QLabel(channel_controls)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.offset = QtGui.QDoubleSpinBox(channel_controls)
        self.offset.setObjectName(_fromUtf8("offset"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.offset)
        self.visible = QtGui.QCheckBox(channel_controls)
        self.visible.setObjectName(_fromUtf8("visible"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.visible)

        self.retranslateUi(channel_controls)
        QtCore.QMetaObject.connectSlotsByName(channel_controls)

    def retranslateUi(self, channel_controls):
        channel_controls.setWindowTitle(QtGui.QApplication.translate("channel_controls", "Channel", None, QtGui.QApplication.UnicodeUTF8))
        channel_controls.setTitle(QtGui.QApplication.translate("channel_controls", "GroupBox", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("channel_controls", "Range", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("channel_controls", "Offset", None, QtGui.QApplication.UnicodeUTF8))
        self.visible.setText(QtGui.QApplication.translate("channel_controls", "Visible", None, QtGui.QApplication.UnicodeUTF8))

