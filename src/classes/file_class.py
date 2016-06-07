import os
from dataset_class import dataset
import numpy as np
class data_file:
    '''
    This is a class created for the management of files woth multiple
    datasets to be analysed
    '''
    def __init__(self,ldat,filename,index=0,coma_separator=False):
        '''
        Init function, takes as argument the path to a file (absolute
        or relative) and reads the data
        '''
        # Global index to indentify the file
        self.index=index
        self.coma_separator=coma_separator
        self.list_datafiles=ldat
        # Creates an empty dictionary with some keys to be used by a parser
        self.parameters=dict()
        if filename:
            self.initialize_file(filename)

    def initialize_file(self,filename):
        self.path=os.path.abspath(filename)
        # Read the data from the file
        self.data=self.read_file()
        self.total_colums=np.shape(self.data)[1]

        # Initialice the parameters dictionary with the preset values
        for i in range(self.total_colums):
            self.add_parameter("C"+str(i+1),i)
        if self.total_colums>=2:
            self.add_parameter("x",0)
            self.add_parameter("y",1)

        # Create a list to store datasets
        self.datasets=dict()
        self.number_datasets=0
        self.list_of_keys=[]

    def read_file(self):
        '''
        This function reads the data from a file and returns a matrix with them'''
        data=[]
        with open(self.path) as f:
            for l in f:
                l=l.strip()
                if self.coma_separator:
                    l=l.replace(",",".")
                try:
                    data.append(np.float_(l.split()))
                except:
                    pass
        return np.matrix(data)

    def add_parameter(self,name,column):
        '''
        Adds a key to the dictionary for the parser
        '''
        self.parameters[name]="np.array(data[:,"+str(column)+"].T)[0]"

    def add_constant(self,name,value):
        self.parameters[name]=str(value)

    def add_dataset(self):
        '''
        This function will add a dataset to the file
        '''
        self.datasets[self.number_datasets]=dataset(self.list_datafiles,self.number_datasets,self.index)
        self.list_of_keys=sorted(self.datasets.keys())
        self.number_datasets+=1

    def __getitem__(self,index):
        return self.datasets[index]

    def reload(self):
        self.data=self.read_file()

    def remove_dataset(self,index):
        self.datasets.pop(index)
        self.list_of_keys=sorted(self.datasets.keys())

    def save(self,f):
        f.write("path ")
        f.write(self.path+"\n")
        f.write("BEGIN PARAMETERS\n")

        for parameter in self.parameters:
            f.write(parameter+"\t"+self.parameters[parameter]+"\n")
        f.write("END PARAMETERS\n")

        for key in self.list_of_keys:
            f.write("DATASET "+str(key)+"\n")
            self.datasets[key].save(f)
        f.write("END DATAFILE\n")

    def load(self,f):
        for l in f:
            l=l.strip()
            if l.startswith("path"):
                self.initialize_file(l[5:])
            elif l.startswith("BEGIN PARAMETERS"):
                self.load_parameters(f)
            elif l.startswith("DATASET"):
                key=int(l.split()[1])
                self.list_of_keys.append(key)
                self.datasets[key]=dataset(self.list_datafiles,key,self.index)
                self.datasets[key].load(f)
                self.number_datasets=max(self.number_datasets,key+1)
            elif l.startswith("END DATAFILE"):
                break
        self.list_of_keys=sorted(self.datasets.keys())

    def load_parameters(self,f):
        for l in f:
            l=l.strip()
            if l.startswith("END PARAMETERS"):
                break
            else:
                self.parameters[l.split()[0]]=l.split()[1]

    def remove_datafile(self,index):
        self.datasets.pop(index)
        self.list_of_keys=sorted(self.datasets.keys())
