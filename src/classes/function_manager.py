import functions.functions as functions
import os
import inspect


class function_manager():
    filename = inspect.getframeinfo(inspect.currentframe()).filename
    instaled_path = os.path.dirname(os.path.abspath(filename))

    def __init__(self):
        self.names=[]
        self.funct=dict()
        self.load_fits()

    def load_fits(self):
        '''
        Load the information about the functions from the info file'''
        self.names=[]
        self.funct=dict()
        f=open(self.instaled_path+"/functions/info")
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

    def list_functions(self):
        return self.names

    def new_function(self,dictionary):
        '''Takes as input a dictionary with the keys:
        name: name of the fit
        parameters: parameters of the fit (in a list)
        initial_values: (optional) initial values for the parameters, if none
        defaults are 0
        string: string with the function in python format
        '''

        # Write the function in info file
        f=open(self.instaled_path+"/functions/info","a")
        f.write("\n")
        f.write("Function: ")
        f.write(dictionary["name"])
        f.write("\n")

        f.write("Parameters: ")
        number_parameters=len(dictionary["parameters"])

        if number_parameters>1:
            for parameter in dictionary["parameters"][:-1]:
                f.write(parameter+",")
        f.write(dictionary["parameters"][-1]+"\n")

        f.write("initial_values: ")

        if "initial_values" not in dictionary:
            dictionary["initial_values"]=[0 for i in range(number_parameters)]

        if number_parameters>1:
            for parameter in dictionary["initial_values"][:-1]:
                f.write(str(parameter)+",")
        f.write(str(dictionary["initial_values"][-1])+"\n")

        f.write("string ")
        f.write(dictionary["string"])
        f.write("\n")
        f.close()

        # write information of the function in the functions module

        f=open(self.instaled_path+"/functions/functions.py","a")
        f.write("\n")

        f.write("def "+dictionary["name"]+"(x")
        for i in dictionary["parameters"]:
            f.write(","+i)
        f.write("):\n")
        f.write("    return "+dictionary["string"]+"\n")
        f.close()

        reload(functions)
        self.load_fits()

    def __getitem__(self,string):
        return self.funct[string]

if __name__=="__main__":
    manager=function_manager()
