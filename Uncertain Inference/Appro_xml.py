#import labs
import sys
import time
import random
from numpy import product
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
    
    def sample(self,event):
        p=self.prob(True,event)
        if p>random.uniform(0.0, 1.0):
            return True
        else:
            return False
        
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
            
#Core functions/rejection sampling
def prio_sample(bn):# generate event according to CPT, sequence of nodes are important
    x={}
    for node in bn.nodes:
        x[node.variable]=node.sample(x)
    return x

def consistent(x,e):
    return all(e.get(k,v)==v for k,v in x.items())

def rejection_sample(X,e,bn,N):
    # N is the total number of samples
    count={T:0,F:0}
    for j in range(N):
        x=prio_sample(bn)
        if consistent(x,e):
            count[x[X]]+=1
    Xtrue=count[T]/(count[T]+count[F])
    Xfalse=1-Xtrue
    print('Rejection:distribution of %s:<T: %f,F: %f>' % (X,Xtrue,Xfalse))
#Core functions/likelihood weighting
def likelihood(X,e,bn,N):
    w={T:0,F:0}
    for j in range(N):
        sample,weight=weighted_sample(bn,e)
        w[sample[X]]+=weight
    Xtrue=w[T]/(w[T]+w[F])
    Xfalse=1-Xtrue
    return print('Likelihood:distribution of %s:<T: %f,F: %f>' % (X,Xtrue,Xfalse))

def weighted_sample(bn,e):
    w=1
    x=dict(e)
    for node in bn.nodes:
        Xi=node.variable
        if Xi in e.keys():
            if node.parents!=[]:                
                 w*=node.prob(e[Xi],x)           
        else:
            x[Xi]=node.sample(x)
    return x,w
#Core functions/gibbs
def gibbs_ask(X,e,bn,N):
    counts={T:0,F:0}
    Z=[var for var in bn.variables if var not in e]
    state=dict(e)
    for Zi in Z:
        state[Zi]=random.choice([True,False])
    for j in range(N):
        for Zi in Z:
            state[Zi]=marcov_blanket(Zi,state,bn)
            counts[state[X]]+=1
    Xtrue=counts[T]/(counts[T]+counts[F])
    Xfalse=1-Xtrue
    print('Gibbs:distribution of %s:<T: %f,F: %f>' % (X,Xtrue,Xfalse))
    
def marcov_blanket(X,e,bn):
    Xnode=bn.variable_node(X)
    P={T:0,F:0}
    for xi in [True,False]:
        ei=dict(e, **{X:xi})
        P[xi]=Xnode.prob(xi,e)*product([Yj.prob(ei[Yj.variable],ei) for Yj in Xnode.children])    
    if P[T]/(P[T]+P[F])>random.uniform(0.0, 1.0):
        return True
    else:
        return False
           

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
    temp=[eval(i) for i in v]
    evidence={}
    for i,j in zip(e,temp):
        evidence[i]=j
    print(X,evidence)
    print('input sample size')
    M=int(input())
    print('1: Rejection sampling')
    random.seed(47)
    rejection_sample(X,evidence,bn,M)
    print('2: Likelihood weighting')
    random.seed(47)
    likelihood(X,evidence,bn,M)
    print('3: Gibbs sampling')
    random.seed(47)
    gibbs_ask(X,evidence,bn,M)
    end=input('Do you want to exit? Y or N:    ')
    if end=='Y':
        over=True
