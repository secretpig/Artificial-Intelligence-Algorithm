#import labs
import sys
import xml.dom.minidom
from xml.dom.minidom import parse
#define helpers
def match(event,variables):#event is a dictionary,variables are list of variables, return tuple(T,F)
    return tuple(event[i] for i in variables)
def parser(fname):
    Filename=fname+'.xml'
    DOMTree = xml.dom.minidom.parse(Filename)
    collection = DOMTree.documentElement
    nodes=collection.getElementsByTagName("DEFINITION")
    Bayesnet=[]
    for node in nodes:
        Bayesnode=[]
        name=node.getElementsByTagName('FOR')[0]
        Bayesnode.append(name.childNodes[0].data)
    
        parents=node.getElementsByTagName('GIVEN')
        temp=[j.childNodes[0].data for j in parents]
        Bayesnode.append(temp)

        
        table=node.getElementsByTagName('TABLE')
        if table[0].childNodes.length==1:
            temp=float(table[0].childNodes[0].nodeValue.split()[0])
        elif table[0].childNodes.length==7:
            temp={}
            temp[(T,)]=float(table[0].childNodes[4].nodeValue.split()[0])
            temp[(F,)]=float(table[0].childNodes[6].nodeValue.split()[0])
        elif table[0].childNodes.length==11:
            temp={}
            temp[T,T]=float(table[0].childNodes[4].nodeValue.split()[0])
            temp[T,F]=float(table[0].childNodes[6].nodeValue.split()[0])
            temp[F,T]=float(table[0].childNodes[8].nodeValue.split()[0])
            temp[F,F]=float(table[0].childNodes[10].nodeValue.split()[0])
        Bayesnode.append(temp)
        Bayesnode=tuple(Bayesnode)
        Bayesnet.append(Bayesnode)
    for i in Bayesnet:
        print(i)
    return Bayesnet
#define important class
class BayesNode:
    def __init__(self,name,parents,cpt):
        if isinstance(cpt,(float,int)):# if no parents
            cpt={():cpt}
        self.variable=name
        self.parents=parents
        self.cpt=cpt
        self.children=[]
        
    def prob(self,value,event):#return the conditional probability
        ptrue=self.cpt[match(event,self.parents)]
        return ptrue if value else 1-ptrue
        
    def __repr__(self):
        return repr((self.variable, ' '.join(self.parents)))
    
class BayesNet:
    def __init__(self,nodes=[]):
        self.nodes=[]
        self.variables=[]
        for node in nodes:
            self.add(node)
            
    def add(self,nodes):
        node=BayesNode(*nodes)
        self.nodes.append(node)
        self.variables.append(node.variable)
        for i in node.parents:
            self.variable_node(i).children.append(node)

    def variable_node(self,name):#return the node of variable with name
        for i in self.nodes:
            if i.variable==name:
                return i
    def __repr__(self):
        return 'BayesNet({0!r})'.format(self.nodes)                  
            
#Core functions
def enumeration_ask(X,e,bn):# suppose X=true
    Xtrue=enumerate_all(bn.variables,dict(e, **{X:True}),bn)
    Xfalse=enumerate_all(bn.variables,dict(e, **{X:False}),bn)
    Xtrue=Xtrue/(Xtrue+Xfalse)
    Xfalse=1-Xtrue
    print('Distribution of %s:<T: %f,F: %f>' % (X,Xtrue,Xfalse))
def enumerate_all(variables,e,bn):
    if not variables:
        return 1.0
    Y,rest=variables[0],variables[1:]
    Ynode=bn.variable_node(Y)
    if Y in e:
        return Ynode.prob(e[Y],e)*enumerate_all(rest,e,bn)
    else:
        return sum(Ynode.prob(y,e)*enumerate_all(rest,dict(e, **{Y:y}),bn) for y in [True, False])
     

#Main function
T,F=True, False
over=False
while not over:
    print('Please input the name of xml file')
    name=input()    
    netlist=parser(name)
    bn=BayesNet(netlist)
    
    print('Upload complete!')
    print('input variable that you want to ask')
    X=input()
    print('input evidence variable')
    e=input()
    e=e.split()
    print('input value of evidence variable')
    v=input()
    v=v.split()
    evidence={}
    for i,j in zip(e,v):
        evidence[i]=j
    print(X,evidence)
    enumeration_ask(X,evidence,bn)
    end=input('Do you want to exit? Y or N:    ')
    if end=='Y':
        over=True




