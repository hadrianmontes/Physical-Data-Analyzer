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

        # Status of he fit
        #  0-> not fitted
        #  1-> fiited and converged
        # -1-> fitted but not converged
        self.status=0

    def save(self,f):
        # Save the function if configured
        if self.fitting_function:
            f.write("function "+self.fitting_function["name"]+"\n")
        # Save the limits of the fit if configured
        if self.xmax and self.xmin:
            f.write("xmin "+str(self.xmin)+"\n")
            f.write("xmax "+str(self.xmax)+"\n")

        if len(self.parameters)!=0:
            f.write("parameters")
            for parameter in self.parameters:
                f.write(" "+str(parameter))
            f.write("\n")
            
        # If using uncertainties, save it
        if self.uncertainties:
            f.write("Uncertainties True\n")
        f.write("END FIT\n")

    def load(self,f):
        # Initiate an instance of the function manager
        # to load the used functions
        manager=function_manager()
        manager.load_fits()

        for l in f:
            l=l.strip()

            if l.startswith("function"):
                self.set_fitting_function(manager[l.split()[1]])

            elif l.startswith("parameters"):
                self.parameters=np.array([float(i) for i in l.split()[1:]])

            elif l.startswith("xmin"):
                self.xmin=float(l.split()[1])

            elif l.startswith("xmax"):
                self.xmax=float(l.split()[1])

            elif l.startswith("Uncertainties"):
                self.uncertainties=bool(l.split()[1])

            elif l.startswith("END FIT"):
                break

    def set_fitting_function(self,dictionary):
        self.fitting_function=dictionary
        self.set_paramaters()

    def set_paramaters(self,values=None):
        if not values:
            self.parameters=self.fitting_function["initial_values"]
        elif len(values)==len(self.fitting_function["initial_values"]):
            self.parameters=values
        else:
            return "error"
        self.parameters=np.array(self.parameters)

    def use_uncertainties(self,boolean):
        self.uncertainties=boolean

    def start_fit(self):
        if not self.fitting_function:
            return

        # Load the values of x and y from de dataset
        info=self.listdata[self.datafile_index][self.dataset_index].info
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
