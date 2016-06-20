# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fits.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_fitmanager(object):
    def setupUi(self, fitmanager):
        fitmanager.setObjectName(_fromUtf8("fitmanager"))
        fitmanager.resize(591, 303)
        self.gridLayout_2 = QtGui.QGridLayout(fitmanager)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.combo_list = QtGui.QComboBox(fitmanager)
        self.combo_list.setObjectName(_fromUtf8("combo_list"))
        self.gridLayout_2.addWidget(self.combo_list, 0, 0, 1, 5)
        self.new_button = QtGui.QPushButton(fitmanager)
        self.new_button.setObjectName(_fromUtf8("new_button"))
        self.gridLayout_2.addWidget(self.new_button, 0, 5, 1, 1)
        self.scrollArea = QtGui.QScrollArea(fitmanager)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 453, 217))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.gridLayout = QtGui.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.table_values = QtGui.QTableWidget(self.scrollAreaWidgetContents)
        self.table_values.setRowCount(2)
        self.table_values.setColumnCount(2)
        self.table_values.setObjectName(_fromUtf8("table_values"))
        self.gridLayout.addWidget(self.table_values, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 1, 0, 1, 5)
        self.label = QtGui.QLabel(fitmanager)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 2, 0, 1, 1)
        self.string_val = QtGui.QLineEdit(fitmanager)
        self.string_val.setObjectName(_fromUtf8("string_val"))
        self.gridLayout_2.addWidget(self.string_val, 2, 1, 1, 4)
        self.save_button = QtGui.QPushButton(fitmanager)
        self.save_button.setEnabled(False)
        self.save_button.setObjectName(_fromUtf8("save_button"))
        self.gridLayout_2.addWidget(self.save_button, 2, 5, 1, 1)

        self.retranslateUi(fitmanager)
        QtCore.QMetaObject.connectSlotsByName(fitmanager)

    def retranslateUi(self, fitmanager):
        fitmanager.setWindowTitle(_translate("fitmanager", "Dialog", None))
        self.new_button.setText(_translate("fitmanager", "Add Function", None))
        self.label.setText(_translate("fitmanager", "function y=", None))
        self.save_button.setText(_translate("fitmanager", "Save Function", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    fitmanager = QtGui.QDialog()
    ui = Ui_fitmanager()
    ui.setupUi(fitmanager)
    fitmanager.show()
    sys.exit(app.exec_())

