import functions.functions as functions
class function_manager():
    def __init__(self):
        self.names=[]
        self.funct=dict()

    def load_fits(self):
        '''
        Load the information about the functions from the info file'''
        f=open(functions.instaled_path+"functions/info")
        for l in f:
            l=l.strip()
            if l.startswith("Function:"):
                name=l[10:]
                self.names.append(name)
                self.funct[name]=dict()
                self.funct[name]["name"]=name
                self.funct[name]["function"]=eval("functions."+name)

            elif l.startswith("Parameters:"):
                self.funct[name]["parameters"]=l[12:].split(",")
                self.funct[name]["number_parameters"]=len(self.funct[name]["parameters"])

            elif l.startswith("initial_values"):
                val=l[16:].split(",")
                val=[float(i) for i in val]
                self.funct[name]["initial_values"]=val

            elif l.startswith("string"):
                self.funct[name]["string"]=l[7:]
