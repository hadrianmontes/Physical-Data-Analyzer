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

    def save(self,path):
        f=open(path,"w")
        for key in self.list_of_keys:
            f.write("datafile "+str(key)+"\n")
            self.datafiles[key].save(f)
        f.close()

    def load(self,path):
        f=open(path,"r")
        for l in f:
            if l.strip().startswith("datafile"):
                key=int(l.split()[1])
                self.list_of_keys.append(key)
                self.datafiles[key]=data_file("",key)
                self.datafiles[key].load(f)
                self.number_datafiles=max(self.number_datafiles,key+1)
        f.close()

        self.list_of_keys=sorted(self.list_of_keys)
