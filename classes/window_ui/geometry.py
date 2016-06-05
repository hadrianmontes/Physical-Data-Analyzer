# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1045, 701)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.main_grid = QtGui.QGridLayout(self.centralwidget)
        self.main_grid.setObjectName(_fromUtf8("main_grid"))
        self.main_tabs = QtGui.QTabWidget(self.centralwidget)
        self.main_tabs.setObjectName(_fromUtf8("main_tabs"))
        self.file_tab = QtGui.QWidget()
        self.file_tab.setObjectName(_fromUtf8("file_tab"))
        self.main_file_grid = QtGui.QGridLayout(self.file_tab)
        self.main_file_grid.setObjectName(_fromUtf8("main_file_grid"))
        self.file_show_grid = QtGui.QGridLayout()
        self.file_show_grid.setObjectName(_fromUtf8("file_show_grid"))
        self.label = QtGui.QLabel(self.file_tab)
        self.label.setObjectName(_fromUtf8("label"))
        self.file_show_grid.addWidget(self.label, 0, 0, 1, 1)
        self.scrollArea = QtGui.QScrollArea(self.file_tab)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scroll_grid = QtGui.QWidget()
        self.scroll_grid.setGeometry(QtCore.QRect(0, 0, 662, 523))
        self.scroll_grid.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.scroll_grid.setObjectName(_fromUtf8("scroll_grid"))
        self.gridLayout_5 = QtGui.QGridLayout(self.scroll_grid)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.plainTextEdit = QtGui.QPlainTextEdit(self.scroll_grid)
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.gridLayout_5.addWidget(self.plainTextEdit, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scroll_grid)
        self.file_show_grid.addWidget(self.scrollArea, 1, 0, 1, 1)
        self.main_file_grid.addLayout(self.file_show_grid, 1, 1, 1, 2)
        self.variable_grid = QtGui.QGridLayout()
        self.variable_grid.setObjectName(_fromUtf8("variable_grid"))
        self.label_2 = QtGui.QLabel(self.file_tab)
        self.label_2.setMaximumSize(QtCore.QSize(331, 16777215))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.variable_grid.addWidget(self.label_2, 0, 0, 1, 1)
        self.variable_list = QtGui.QTableWidget(self.file_tab)
        self.variable_list.setObjectName(_fromUtf8("variable_list"))
        self.variable_list.setColumnCount(0)
        self.variable_list.setRowCount(0)
        self.variable_grid.addWidget(self.variable_list, 1, 0, 1, 1, QtCore.Qt.AlignLeft)
        self.main_file_grid.addLayout(self.variable_grid, 1, 0, 1, 1)
        self.file_choosing_grid = QtGui.QHBoxLayout()
        self.file_choosing_grid.setObjectName(_fromUtf8("file_choosing_grid"))
        self.combo_file = QtGui.QComboBox(self.file_tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_file.sizePolicy().hasHeightForWidth())
        self.combo_file.setSizePolicy(sizePolicy)
        self.combo_file.setObjectName(_fromUtf8("combo_file"))
        self.file_choosing_grid.addWidget(self.combo_file)
        self.add_button = QtGui.QPushButton(self.file_tab)
        self.add_button.setObjectName(_fromUtf8("add_button"))
        self.file_choosing_grid.addWidget(self.add_button)
        self.remove_button = QtGui.QPushButton(self.file_tab)
        self.remove_button.setObjectName(_fromUtf8("remove_button"))
        self.file_choosing_grid.addWidget(self.remove_button)
        self.main_file_grid.addLayout(self.file_choosing_grid, 0, 0, 1, 3)
        self.main_tabs.addTab(self.file_tab, _fromUtf8(""))
        self.dataset_tab = QtGui.QWidget()
        self.dataset_tab.setObjectName(_fromUtf8("dataset_tab"))
        self.main_tabs.addTab(self.dataset_tab, _fromUtf8(""))
        self.main_grid.addWidget(self.main_tabs, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1045, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.main_tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "File Content", None))
        self.label_2.setText(_translate("MainWindow", "Set Variables", None))
        self.add_button.setText(_translate("MainWindow", "Add", None))
        self.remove_button.setText(_translate("MainWindow", "Delete", None))
        self.main_tabs.setTabText(self.main_tabs.indexOf(self.file_tab), _translate("MainWindow", "Files", None))
        self.main_tabs.setTabText(self.main_tabs.indexOf(self.dataset_tab), _translate("MainWindow", "Data sets", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

