from scipy.optimize import curve_fit
from function_manager import function_manager
import numpy as np

# Define the fit class
class fit:
    def __init__(self,listdata,datafile_index,dataset_index,index):
        # Set al the parameters to locate the fit
        self.listdata=listdata
        self.datafile_index=datafile_index
        self.dataset_index=dataset_index
        self.index=index

        # Fitting related atributes
        self.fitting_function=None
        self.xmax=None
        self.xmin=None
        self.parameters=[]
        self.errors=[]
        self.uncertainties=False

    def set_fitting_function(self,dictionary):
        self.fitting_function=dictionary

    def set_paramaters(self,values=None):
        if not values:
            self.parameters=self.fitting_function["initial_values"]
        elif len(values)==len(self.fitting_function["initial_values"]):
            self.parameters=values
        else:
            return "error"

    def use_uncertainties(self,boolean):
        self.uncertainties=boolean

    def start_fit(self):
        if not self.fitting_function:
            return

        # Load the values of x and y from de dataset
        info=self.listadata[self.datafile][self.dataset][self.index].info
        x=info["x"][1]
        y=info["y"][1]
        sx=info["sx"][1]
        sy=info["sy"][1]
        # select the data in the data range
        if self.xmin and self.xmax:
            y=y[np.logical_and(x>self.xmin,x>self.xmax)]
            sy=sy[np.logical_and(x>self.xmin,x>self.xmax)]
            sx=sx[np.logical_and(x>self.xmin,x>self.xmax)]
            x=x[np.logical_and(x>self.xmin,x>self.xmax)]
        # Do the fits
        if not self.uncertainties:
            self.parameters, self.errors=curve_fit(self.fitting_function["function"],x,y,p0=self.parameters)

        else:
            self.parameters, self.errors=curve_fit(self.fitting_function["function"],x,y,p0=self.parameters,sigma=sy)

    
