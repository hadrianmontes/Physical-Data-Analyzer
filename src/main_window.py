from window_ui.geometry import Ui_MainWindow
from PyQt4 import QtCore, QtGui
from classes.list_datafiles import list_datafiles
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class pda_window(Ui_MainWindow):

    def __init__(self):
        self.file_list=list_datafiles()

        # Lists for the combobox
        self.list_files=None
        self.list_sets=None
        self.list_fits=None

        # Store the current object open
        self.current_file=None
        self.current_set=None
        self.current_fit=None

    def setupUi(self,MainWindow):
        super(pda_window, self).setupUi(MainWindow)
        self.actionSave.triggered.connect(self.save)
        self.actionOpen.triggered.connect(self.load)
        self.setup_files()
        self.setup_data()

########################
# FILE RELATED METHODS #
########################

    def setup_files(self):
        # Actions
        self.add_button.clicked.connect(self.add_file)
        self.combo_file.activated.connect(self.select_file)
        self.remove_button.clicked.connect(self.remove)
        self.parameter_add.clicked.connect(self.add_parameter)

        self.update_combo()
        self.variable_list.setHorizontalHeaderLabels(["Parameter","Row(Column)"])
        self.variable_list.setColumnCount(2)

    def add_file(self):
        text=str(QtGui.QFileDialog.getOpenFileName())
        self.file_list.add_datafile(text)
        self.update_combo()
        self.combo_file.setCurrentIndex(len(self.list_files)-1)
        self.select_file()

    def update_combo(self):
        self.combo_file.clear()
        self.list_files=[self.file_list[i].path for i in self.file_list.list_of_keys]
        self.combo_file.addItems(self.list_files)

    def select_file(self):
        '''This funciton reads the selected file and loads all the properties'''
        # Index inside the hte file_list
        file_index=self.file_list.list_of_keys[self.combo_file.currentIndex()]
        self.current_file=self.file_list[file_index]

        print "Changed to file "+self.current_file.path
        # Reset the other properties
        self.current_set=None
        self.current_fit=None

        # Set the parameters
        self.update_variable_list()
        # set the max row in the box for parameters
        self.parameter_column.setMaximum(self.current_file.total_colums)

        self.update_combo_data()

        self.select_data()

    def remove(self):
        """removes a datafile form the list"""
        file_index=self.file_list.list_of_keys[self.combo_file.currentIndex()]
        self.file_list.remove_datafile(file_index)
        self.update_combo()
        self.select_file()

    def update_variable_list(self):
        ui.variable_list.setRowCount(len(self.current_file.parameters))
        self.variable_list.clear()
        row=0
        for parameter in sorted(self.current_file.parameters):
            para=QtGui.QTableWidgetItem(parameter)
            colum=str(int(self.current_file.parameters[parameter][16:][:-7])+1)
            colum=QtGui.QTableWidgetItem(colum)
            self.variable_list.setItem(row,0,para)
            self.variable_list.setItem(row,1,colum)
            row+=1

    def add_parameter(self):
        self.current_file.add_parameter(str(self.parameter_name.text()),
                                        self.parameter_column.value()-1)
        self.update_variable_list()

    ###################
    # DATASET METHODS #
    ###################

    def setup_data(self):
        # Prepare the canvas for the plot
        fig = Figure()
        self.axes_preview=fig.add_subplot(111)
        self.simple_plot_data = FigureCanvas(fig)
        self.toolbar_preview = NavigationToolbar(self.simple_plot_data,
                                                 self.matplotlib_grid.widget())
        self.matplotlib_grid.addWidget(self.toolbar_preview,1,0)
        self.matplotlib_grid.addWidget(self.simple_plot_data,2,0,8,1)

        # Connect the buttons
        self.add_dataset.clicked.connect(self.new_dataset)
        self.data_save.clicked.connect(self.save_dataset)
        self.plot_button.clicked.connect(self.plot_simple_plot_data)
        self.reset_plot_preview.clicked.connect(self.reset_preview)

        # Connect the combo
        self.combo_set.activated.connect(self.select_data)

        self.select_data()

    def update_combo_data(self):
        self.combo_set.clear()
        self.list_sets=[self.current_file[i].label for i in self.current_file.list_of_keys]
        self.combo_set.addItems(self.list_sets)

    def new_dataset(self):
        if not self.current_file:
            return
        self.current_file.add_dataset()
        last_index=self.current_file.list_of_keys[-1]
        self.current_file[last_index].label="New Dataset"
        self.update_combo_data()
        self.combo_set.setCurrentIndex(len(self.current_file.list_of_keys)-1)
        self.select_data()

    def select_data(self):
        if not self.current_file:
            return
        elif len(self.current_file.list_of_keys)==0:
            return
        data_index=self.current_file.list_of_keys[self.combo_set.currentIndex()]
        self.current_set=self.current_file[data_index]
        print "Changed to set "+self.current_set.label
        # Reset the other properties
        self.current_fit=None
        self.update_set_parameters()

    def update_set_parameters(self):
        self.label_data.setText(self.current_set.label)
        self.x_data.setText(self.current_set.info["x"][0])
        self.y_data.setText(self.current_set.info["y"][0])
        self.sx_data.setText(self.current_set.info["sx"][0])
        self.sy_data.setText(self.current_set.info["sy"][0])

    def save_dataset(self):
        if not self.current_set:
            return

        # Save the index to restore the combobox
        current_index=self.combo_set.currentIndex()
        
        self.current_set.label=str(self.label_data.text())
        x=str(self.x_data.text())
        if x:
            self.current_set.info["x"][0]=x
        y=str(self.y_data.text())
        if y:
            self.current_set.info["y"][0]=y
        sx=str(self.sx_data.text())
        if sx:
            self.current_set.info["sx"][0]=sx
        sy=str(self.sy_data.text())
        if sy:
            self.current_set.info["sy"][0]=sy
        
        self.update_combo_data()
        self.combo_set.setCurrentIndex(current_index)
        self.current_set.calculate()
        self.select_data()

    def plot_simple_plot_data(self):
        if not self.current_set:
            print "No set selected"
            return
        self.current_set.calculate()
        if self.current_set.info["x"][1]!=[]:
            if self.current_set.info["y"][1]!=[]:
                x=self.current_set.info["x"][1]
                y=self.current_set.info["y"][1]
                self.axes_preview.plot(x,y)
                self.simple_plot_data.draw()
            else:
                print "No values for y"
        else:
            print "No values for x"

    def reset_preview(self):
        self.axes_preview.clear()
        self.simple_plot_data.draw()
            

    #########
    # Menus #
    #########

    def save(self):
        text=str(QtGui.QFileDialog.getSaveFileName())
        self.file_list.save(text)

    def load(self):
        test=str(QtGui.QFileDialog.getOpenFileName())
        self.file_list.load(test)
        self.update_combo()
        self.select_file()


# Execution of the main window
if __name__=="__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = pda_window()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
