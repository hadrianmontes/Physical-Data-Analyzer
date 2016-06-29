import numpy as np
from numpy import sin,cos,tan,log,exp
# TODO make the path changed when installing the program
# instaled_path="/home/hadrian/Documentos/github/Physical-Data-Analyzer/classes/"

def linear(x,a,b):
    return a+b*x

def cuadratic(x,a,b,c):
    return a+b*x+c*x**2


def exponential_decay(x,c,tau):
    return c*np.e**(-tau*x)

def cubic(x,a,b,c,d):
    return a+b*x+c*x**2+d*x**3

def logaritmo(x,a,b,tau):
    return np.log(a+b*x)+tau



def potencial(x,a,b):
    return x**a+b
