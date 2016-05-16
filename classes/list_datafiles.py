from file_class import data_file

class list_datafiles():
    '''
    This class will act as a container of datafiles
    '''

    def __init__(self):
        self.datafiles=dict()
        self.number_datafiles=0
        self.list_of_keys=[]

    def add_datafile(self,path):
        self.datafiles[self.number_datafiles]=data_file(path,self.number_datafiles)
        self.number_datafiles+=1
        self.list_of_keys=sorted(self.datafiles.keys())

    def remove_datafile(self,index):
        self.datafiles.pop(index)
        self.list_of_keys=sorted(self.datafiles.keys())

    def __getitem__(self,index):
        return self.datafiles[index]
