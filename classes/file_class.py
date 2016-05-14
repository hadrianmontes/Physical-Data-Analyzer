import os
from dataset_class import dataset
import numpy as np
class data_file:
    '''
    This is a class created for the management of files woth multiple
    datasets to be analysed
    '''
    # Initialize a global index to count
    # the nuber of opened files (maybe it is worthless)
    total_numner_files=0

    def __init__(self,filename,coma_separator=False):
        '''
        Init function, takes as argument the path to a file (absolute
        or relative) and reads the data
        '''
        # Global index to indentify the file
        self.global_index=data_file.total_numner_files
        data_file.total_numner_files+=1

        self.coma_separator=coma_separator

        # Creates an empty dictionary with some keys to be used by a parser
        self.parameters=dict()

        # Read the data from the file
        self.data=self.read_file(filename)
        self.total_colums=np.shape(self.data)[1]

        # Initialice the parameters dictionary with the preset values
        for i in range(self.total_colums):
            self.add_parameter("C"+str(i+1),i)
        if self.total_colums>=2:
            self.add_parameter("x",0)
            self.add_parameter("y",1)

        # Create a list to store datasets
        self.datasets=[]

    def read_file(self,filename):
        '''
        This function reads the data from a file and returns a matrix with them'''
        data=[]
        with open(filename) as f:
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
        self.parameters[name]="data[:,"+str(column)+"]"

    def add_dataset(self):
        '''
        This function will add a dataset to the file
        '''
        self.datasets.append(dataset(self))
