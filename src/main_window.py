from window_ui.geometry import Ui_MainWindow
from PyQt4 import QtCore, QtGui
from list_datafiles import list_datafiles

class pda_window(Ui_MainWindow):

    def __init__(self):
        self.file_list=list_datafiles()

    def setupUi(self,MainWindow):
        super(pda_window, self).setupUi(MainWindow)
        self.variable_list.setColumnCount(2)
        self.actionSave.triggered.connect(self.save)
        self.setup_files()

    def setup_files(self):
        self.add_button.clicked.connect(self.add_file)
        self.update_combo()

    def add_file(self):
        text=str(QtGui.QFileDialog.getOpenFileName())
        self.file_list.add_datafile(text)
        self.update_combo()

    def update_combo(self):
        self.combo_file.clear()
        lista=[self.file_list[i].path for i in self.file_list.list_of_keys]
        self.combo_file.addItems(lista)

    def save(self):
        print "hola"

if __name__=="__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = pda_window()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
