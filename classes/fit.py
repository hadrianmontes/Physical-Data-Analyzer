from scipy.optimize import curve_fit
# Import the functions to use for the fits
import functions.functions as functions

# Define the fit class
class fit:
    def __init__(self,listdata,datafile_index,dataset_index,index):
        self.listdata=listdata
        self.datafile_index=datafile_index
        self.dataset_index=dataset_index
        self.index=index
        self.load_fits()

