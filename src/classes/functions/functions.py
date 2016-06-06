import numpy as np
# TODO make the path changed when installing the program
# instaled_path="/home/hadrian/Documentos/github/Physical-Data-Analyzer/classes/"

def linear(x,a,b):
    return a+b*x

def cuadratic(x,a,b,c):
    return a+b*x+c*x**2


def exponential_decay(x,c,tau):
    return c*np.e**(-tau*x)
