from parser import parser
from fit import fit
from function_manager import function_manager
import numpy as np
class dataset:
    '''
    This class will define a dataset. THis is a set of data that will
    be analyzd later
    '''
    def __init__(self,ldat,index,datafile_index):
        # Set an index for the dataset
        self.index=index
        self.datafile=datafile_index
        # Each element is string_to_evaluate, list_of_data,calculated
        self.info={"x":["",[],False],
                   "y":["",[],False],
                   "sx":["",[],False],
                   "sy":["",[],False]}
        self.list_datafiles=ldat

        # Create a list to store fits
        self.fits=dict()
        self.number_fits=0
        self.list_of_keys=[]

    def add_fit(self):
        self.fits[self.number_fits]=fit(self.list_datafiles,self.datafile,self.index,self.number_fits)
        self.list_of_keys=sorted(self.fits.keys())
        self.number_fits+=1
        
    def calculate(self):
        data=self.list_datafiles[self.datafile].data
        parameters=self.list_datafiles[self.datafile].parameters
        for variable in self.info:
            lista=self.info[variable]
            if (not lista[2]) and lista[0]:
                string=lista[0].replace(" ","")
                self.info[variable][1]=np.array(eval(parser(string,parameters)).T)[0]

    def save(self,f):
        for variable in self.info:
            f.write(variable+" "+self.info[variable][0]+"\n")
        f.write("END DATASET\n")

    def load(self,f):
        for l in f:
            l=l.strip()
            if l.startswith("END DATASET"):
                break
            else:
                if len(l.split())>1:
                    variable=l.split()[0]
                    self.info[variable][0]=l[len(variable)+1:]
        self.calculate()

    def set_value(self,key,string):
        self.info[key][0]=string
        self.info[key][2]=False
        self.calculate()

if __name__=="__main__":
    from list_datafiles import list_datafiles
    a=list_datafiles()
    a.add_datafile("test")
    a[0].add_dataset()
    a[0][0].info["x"][0]="x"
    a[0][0].info["y"][0]="y"
    a[0][0].calculate()
    a[0][0].add_fit()
    b=b=a[0][0].fits[0]
    c=function_manager()
    c.load_fits()
    b.set_fitting_function(c["cuadratic"])
    b.start_fit()
