from src.main_window import pda_window
from PyQt4 import QtGui
import sys
app = QtGui.QApplication(sys.argv)
MainWindow = QtGui.QMainWindow()
ui = pda_window()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())
