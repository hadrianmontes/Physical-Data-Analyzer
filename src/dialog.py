from PyQt4 import QtGui
from window_ui.manager import Ui_fitmanager
from classes.function_manager import function_manager

class Dialog(Ui_fitmanager):
    def __init__(self):
        self.function_manager=function_manager()
        return

    def setupUi(self,MainWindow):
        super(Dialog, self).setupUi(MainWindow)
        self.combo_list.addItems(self.function_manager.names)
        self.combo_list.activated.connect(self.update_parameters)
        self.new_button.clicked.connect(self.start_new)
        self.update_parameters()
        self.table_values.cellClicked.connect(self.update_spaces)
        self.table_values.cellChanged.connect(self.update_spaces)
        self.save_button.clicked.connect(self.save_function)

    def update_parameters(self):
        self.save_button.setEnabled(False)
        index=self.combo_list.currentIndex()
        name=self.function_manager.names[index]
        function=self.function_manager[name]
        self.name_val.setText(name)
        self.table_values.clear()
        self.table_values.setRowCount(function["number_parameters"])
        self.table_values.setHorizontalHeaderLabels(["Parameter","Inital Value"])
        for i in range(function["number_parameters"]):
            parameter=function["parameters"][i]
            parameter=QtGui.QTableWidgetItem(parameter)
            # parameter.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table_values.setItem(i,0,parameter)
            initial_value=str(function["initial_values"][i])
            initial_value=QtGui.QTableWidgetItem(initial_value)
            # initial_value.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table_values.setItem(i,1,initial_value)
        self.table_values.setEnabled(False)
        self.string_val.setText(function["string"])
        self.string_val.setReadOnly(True)
        self.name_val.setEnabled(False)
        # self.string_val.setEnabled(False)

    def update_spaces(self,row,col):
        rows=self.table_values.rowCount()
        max_used=0

        for i in range(rows):
            if self.table_values.item(i,0):
                string=str(self.table_values.item(i,0).text())
            else:
                string=""
            if string!="":
                max_used=i+1
        self.table_values.setRowCount(max_used+2)

    def start_new(self):
        self.table_values.clear()
        self.table_values.setRowCount(2)
        self.table_values.setColumnCount(2)
        self.table_values.setEnabled(True)
        self.string_val.setReadOnly(False)
        self.string_val.setText("")
        self.save_button.setEnabled(True)
        self.name_val.setText("")
        self.name_val.setEnabled(True)

    def save_function(self):
        rows=self.table_values.rowCount()
        parameters=[]
        initial=[]
        for i in range(rows):
            if self.table_values.item(i,0):
                string=str(self.table_values.item(i,0).text())
            else:
                string=""

            if string!="":
                parameters.append(string)
                try:
                    val=float(str(self.table_values.item(i,1).text()))
                except:
                    val=0
                initial.append(val)

        function=dict()
        if str(self.name_val.text())!="":
            function["name"]=str(self.name_val.text())
        else:
            print "No name provided"
            return
        if parameters==[]:
            print "No parameters provided"
            return
        else:
            function["parameters"]=parameters
            function["initial_values"]=initial

        if str(self.string_val.text())=="":
            print "No function provided"
        else:
            function["string"]=str(self.string_val.text())

        self.function_manager.new_function(function)
        self.function_manager=function_manager()
        self.combo_list.clear()
        self.combo_list.addItems(self.function_manager.names)
        self.combo_list.setCurrentIndex(len(self.function_manager.names)-1)
        self.update_parameters()
