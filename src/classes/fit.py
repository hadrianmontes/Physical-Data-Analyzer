import matplotlib.pyplot as plt
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
        self.label=""

        # Status of he fit
        #  0-> not fitted
        #  1-> fiited and converged
        # -1-> fitted but not converged
        self.status=0

    def set_label(self,string):
        self.label=string

    def save(self,f):
        # Save the function if configured
        f.write("Label: "+self.label+"\n")
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

            elif l.startswith("Label:"):
                self.label=l[7:]

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
        self.erros=[]
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
            y=y[np.logical_and(x>self.xmin,x<self.xmax)]
            if self.uncertainties:
                sy=sy[np.logical_and(x>self.xmin,x<self.xmax)]
                sx=sx[np.logical_and(x>self.xmin,x<self.xmax)]
            x=x[np.logical_and(x>self.xmin,x<self.xmax)]
        # Do the fits
        if not self.uncertainties:
            self.parameters, self.errors=curve_fit(self.fitting_function["function"],x,y,p0=self.parameters)

        else:
            self.parameters, self.errors=curve_fit(self.fitting_function["function"],x,y,p0=self.parameters,sigma=sy)
        self.errors=np.diag(self.errors)**0.5

    def print_parameters(self):
        string=""
        for i in range(self.fitting_function["number_parameters"]):
            string+=self.fitting_function["parameters"][i]+"="+str(self.parameters[i])+", "
        string=string[:-2]
        return string

    def print_errors(self):
        string=""
        if self.errors==[]:
            return string
        for i in range(self.fitting_function["number_parameters"]):
            string+=self.fitting_function["parameters"][i]+"="+str(self.errors[i])+", "
        string=string[:-2]
        return string

    def save_parameters(self,string):
        parameters=string.split(",")
        for parameter in parameters:
            para,val=parameter.split("=")
            para=para.strip()
            val=val.strip()
            index=self.fitting_function["parameters"].index(para)
            self.parameters[index]=float(val)

    def plot(self,axis):
        info=self.listdata[self.datafile_index][self.dataset_index].info
        x=info["x"][1]
        y=info["y"][1]
        axis.plot(x,y)
        maximun=max(x)
        minimun=min(x)
        x=np.linspace(minimun,maximun,100000)
        y=self.fitting_function["function"](x,*self.parameters)
        axis.plot(x,y)

    def set_graphic_range(self):
        info=self.listdata[self.datafile_index][self.dataset_index].info
        x=info["x"][1]
        y=info["y"][1]
        fig,axis=plt.subplots()
        axis.plot(x,y)
        self.xmin,self.xmax=plt.ginput(2)
        self.xmin=self.xmin[0]
        self.xmax=self.xmax[0]
        axis.clear()
        plt.close(fig)
