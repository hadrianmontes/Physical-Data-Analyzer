def parser(instring,parameters):
    out=[]
    parentesis=instring.split("(")
    for ip in range(len(parentesis)):
        parentesis2=parentesis[ip].split(")")
        for ip2 in range(len(parentesis2)):
            suma=parentesis2[ip2].split("+")
            for s in range(len(suma)):
                resta=suma[s].split("-")
                for r in range(len(resta)):
                    po=resta[r].split("**")
                    for p in range(len(po)):
                        mul=po[p].split("*")
                        for m in range(len(mul)):
                            div=mul[m].split("/")
                            div=replacer(div,parameters)
                            mul[m]=joiner(div,"/")
                        po[p]=joiner(mul,"*")
                    resta[r]=joiner(po,"**")
                suma[s]=joiner(resta,"-")
            parentesis2[ip2]=joiner(suma,"+")
        parentesis[ip]=joiner(parentesis2,")")
    out=joiner(parentesis,"(")
    return out

def joiner(lista,operand):
    if len(lista)==1:
        return lista[0]
    else:
        out=lista[0]
        for i in lista[1:]:
            out+=operand
            out+=i
    return out

def replacer(lista,parameters):
    for i in range(len(lista)):
        if lista[i] in parameters:
            lista[i]=parameters[lista[i]]
    return lista


if __name__=="__main__":
    parameters={'x':'data[1]','y':'data[2]'}
    string='x*y+cos(x-y)-x+x**y-x/y'
    parser(string,parameters)
