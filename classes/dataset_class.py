class dataset:
    '''
    This class will define a dataset. THis is a set of data that will
    be analyzd later
    '''
    # Global index of the dataset
    total_dataset=0

    def __init__(self,datafile):
        # Set an index for the dataset
        self.index=dataset.total_dataset
        dataset.total_dataset+=1
        self.data_file=datafile
        self.x=[]
        self.y=[]
        self.sx=False
        self.sy=False
        self.histogramlike=False

    def setx(self,expresion):
        '''
        Loads data from the data_file for the x values
        '''
        data=self.data_file.data
        
