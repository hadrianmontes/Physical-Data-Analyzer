class dataset:
    '''
    This class will define a dataset. THis is a set of data that will
    be analyzd later
    '''
    def __init__(self,ldat,index,datafile_index):
        # Set an index for the dataset
        self.index=index
        self.strings={"x":"","y":"","sx":"","sy":""}
        self.data={"x":[],"y":[],"sx":[],"sy":[]}
        self.list_datafiles=ldat
