from window_ui.geometry import Ui_MainWindow
from dialog import Dialog
from PyQt4 import QtGui, QtCore
from classes.list_datafiles import list_datafiles
from classes.function_manager import function_manager
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class pda_window(Ui_MainWindow):

    def __init__(self):
        self.file_list=list_datafiles()
        self.function_manager=function_manager()

        # Lists for the combobox
        self.list_files=None
        self.list_sets=None
        self.list_fits=None

        # Store the current object open
        self.current_file=None
        self.current_set=None
        self.current_fit=None

        self.activated_file=False
        self.activated_set=False
        self.activated_fit=False

    def setupUi(self,MainWindow):
        super(pda_window, self).setupUi(MainWindow)
        self.actionSave.triggered.connect(self.save)
        self.actionOpen.triggered.connect(self.load)
        self.setup_files()
        self.setup_data()
        self.setup_fit()

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
        self.toogle_file()

    def toogle_file(self):
        self.parameter_name.setEnabled(self.activated_file)
        self.parameter_column.setEnabled(self.activated_file)
        self.parameter_add.setEnabled(self.activated_file)
        self.add_dataset.setEnabled(self.activated_file)
        self.remove_dataset.setEnabled(self.activated_file)

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
        self.activated_file=True
        self.activated_set=False
        self.activated_fit=False

        # Set the parameters
        self.update_variable_list()
        # set the max row in the box for parameters
        self.parameter_column.setMaximum(self.current_file.total_colums)

        self.update_combo_data()

        self.select_data()
        self.toogle_file()

    def remove(self):
        """removes a datafile form the list"""
        file_index=self.file_list.list_of_keys[self.combo_file.currentIndex()]
        self.file_list.remove_datafile(file_index)
        self.update_combo()
        self.select_file()

    def update_variable_list(self):
        self.variable_list.setRowCount(len(self.current_file.parameters))
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
        self.remove_dataset.clicked.connect(self.remove_data)
        # Connect the combo
        self.combo_set.activated.connect(self.select_data)

        self.select_data()
        self.toogle_data()

    def toogle_data(self):
        self.label_data.setEnabled(self.activated_set)
        self.x_data.setEnabled(self.activated_set)
        self.y_data.setEnabled(self.activated_set)
        self.sx_data.setEnabled(self.activated_set)
        self.sy_data.setEnabled(self.activated_set)
        self.data_save.setEnabled(self.activated_set)
        self.plot_button.setEnabled(self.activated_set)
        self.add_fit.setEnabled(self.activated_set)
        self.delete_fit.setEnabled(self.activated_set)

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

    def remove_data(self):
        """removes a dataset form the list"""
        data_index=self.current_file.list_of_keys[self.combo_set.currentIndex()]
        self.current_file.remove_datafile(data_index)
        self.update_combo_data()
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
        self.activated_set=True
        self.activated_fit=False
        self.update_set_parameters()
        self.toogle_data()
        self.update_combo_fit()
        self.select_fit()

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
        self.save_dataset()
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

    #######################
    # Fit related methods #
    #######################

    def setup_fit(self):
        # Prepare the canvas for the plot
        fig = Figure()
        self.axes_view_fit=fig.add_subplot(111)
        self.view_fit = FigureCanvas(fig)
        self.toolbar_view_fit = NavigationToolbar(self.view_fit,
                                                  self.fit_plot_grid.widget())
        self.fit_plot_grid.addWidget(self.toolbar_view_fit,2,0)
        self.fit_plot_grid.addWidget(self.view_fit,3,0,8,1)

        # connect the buttons
        self.add_fit.clicked.connect(self.new_fit)
        self.save_fit.clicked.connect(self.save_fit_parameters)
        self.graphic_range.clicked.connect(self.set_graphic_range)
        self.manage_functions.clicked.connect(self.fit_manager)
        # Connect the combobox
        self.combo_fit.activated.connect(self.select_fit)
        self.fit_function.addItems(self.function_manager.names)
        self.fit_function.activated.connect(self.save_fit_function)

        self.start_fit.clicked.connect(self.start_fitting)
        self.toogle_fit()

    def toogle_fit(self):
        self.fit_label.setEnabled(self.activated_fit)
        self.fit_function.setEnabled(self.activated_fit)
        self.check_uncertainties.setEnabled(self.activated_fit)
        self.min_range.setEnabled(self.activated_fit)
        self.max_range.setEnabled(self.activated_fit)
        self.graphic_range.setEnabled(self.activated_fit)
        self.param_val.setEnabled(self.activated_fit)
        self.param_uncert.setEnabled(self.activated_fit)
        self.save_fit.setEnabled(self.activated_fit)
        self.start_fit.setEnabled(self.activated_fit)

    def set_graphic_range(self):
        if self.current_fit is None:
            return
        self.current_fit.set_graphic_range()
        self.update_fit_parameters()

    def save_fit_function(self):
        self.param_val.setText("")
        self.param_uncert.setText("")
        self.current_fit.errors=[]
        self.save_fit_parameters()
        self.update_fit_parameters()

    def update_combo_fit(self):
        self.combo_fit.clear()
        self.list_fits=[self.current_set[i].label for i in self.current_set.list_of_keys]
        self.combo_fit.addItems(self.list_fits)

    def new_fit(self):
        self.current_set.add_fit()
        last_index=self.current_set.list_of_keys[-1]
        self.current_set[last_index].label="New Fit"
        self.update_combo_fit()
        self.combo_fit.setCurrentIndex(len(self.current_file.list_of_keys)-1)
        self.select_fit()

    def select_fit(self):
        if not self.current_set:
            return
        elif len(self.current_set.list_of_keys)==0:
            return
        set_index=self.current_set.list_of_keys[self.combo_fit.currentIndex()]
        self.current_fit=self.current_set[set_index]
        print "Changed to fit "+self.current_fit.label
        # Reset the other properties
        self.update_fit_parameters()
        self.activated_fit=True
        self.toogle_fit()

    def update_fit_parameters(self):

        self.fit_label.setText(self.current_fit.label)
        if self.current_fit.fitting_function is not None:
            index=self.function_manager.names.index(self.current_fit.fitting_function["name"])
            self.fit_function.setCurrentIndex(index)

            text=self.current_fit.print_parameters()
            self.param_val.setText(text)

            text=self.current_fit.print_errors()
            self.param_uncert.setText(text)
        if self.current_fit.xmax is not None:
            if self.current_fit.xmin is not None:
                self.min_range.setText(str(self.current_fit.xmin))
                self.max_range.setText(str(self.current_fit.xmax))

        self.check_uncertainties.setChecked(self.current_fit.uncertainties)

    def save_fit_parameters(self):
        self.current_fit.set_label(str(self.fit_label.text()))

        fit_index=self.fit_function.currentIndex()
        function=self.function_manager.funct[self.function_manager.names[fit_index]]
        self.current_fit.set_fitting_function(function)

        if self.param_val.text():
            text=str(self.param_val.text())
            self.current_fit.save_parameters(text)

        if str(self.max_range.text())!="":
            self.current_fit.xmax=float(str(self.max_range.text()))
        else:
            self.current_fit.xmax=None

        if str(self.min_range.text())!="":
            self.current_fit.xmin=float(str(self.min_range.text()))
        else:
            self.current_fit.xmin=None

        self.current_fit.use_uncertainties(self.check_uncertainties.isChecked())

        current_index=self.combo_fit.currentIndex()
        self.update_combo_fit()
        self.combo_fit.setCurrentIndex(current_index)
        self.select_fit()

    def start_fitting(self):
        if not self.current_fit:
            return
        elif self.current_fit.fitting_function is None:
            return

        self.current_fit.start_fit()
        self.plot_fit()
        self.update_fit_parameters()

    def plot_fit(self):
        self.axes_view_fit.clear()
        self.current_fit.plot(self.axes_view_fit)
        self.view_fit.draw()

    def fit_manager(self):
        dialog = QtGui.QDialog()
        dialog.ui = Dialog()
        dialog.ui.setupUi(dialog)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.exec_()
        self.function_manager=function_manager()
        self.fit_function.clear()
        self.fit_function.addItems(self.function_manager.names)

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
