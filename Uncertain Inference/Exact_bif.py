#import labs
import sys
import time
import random
from numpy import product
import xml.dom.minidom
from xml.dom.minidom import parse
import re
####define helpers
def parse_bif(filename):
    readfile = open(filename+'.bif')
    readfile.readline()
    readfile.readline()    
    prior_probability_pattern_1 = re.compile(r"probability \( ([^|]+) \) \{\s*")
    prior_probability_pattern_2 = re.compile(r"  table (.+);\s*")
    conditional_probability_pattern_1 = (re.compile(r"probability \( (.+) \| (.+) \) \{\s*"))
    conditional_probability_pattern_2 = re.compile(r"  \((.+)\) (.+);\s*")    
    variables = {}    
    bayes_net = []    
    while True:        
        line = readfile.readline()
        # print(line)        
        if not line:
            break            
        if line.startswith("variable"):            
            var = line[9:-3]
            new_line = readfile.readline()
            indexa = new_line.find("{")
            indexb = new_line.find("}")
            new_line = new_line[indexa+2:indexb-1]
            variables[var] = new_line.split(", ")            
            readfile.readline()        
        elif line.startswith("probability"):            
            match = prior_probability_pattern_1.match(line)            
            if match:                
                # prior probabilities:
                variable = match.group(1)
                parents = []
                line = readfile.readline()
                match = prior_probability_pattern_2.match(line)
                p = [float(i) for i in match.group(1).split(', ')]
                table = {}
                for i in range(len(variables[variable])):
                    value = variables[variable][i]
                    table[tuple([value])] = {():p[i]}                
                readfile.readline()                  
            else:
                match = conditional_probability_pattern_1.match(line)
                if match:
                    variable = match.group(1)
                    parents = match.group(2).split(', ')
                    table = {}
                    for value in variables[variable]:
                        table[tuple([value])] = {}                    
                    while True:
                        line = readfile.readline()
                        if line.startswith("}"):
                            break
                        match = conditional_probability_pattern_2.match(line)
                        given = match.group(1).split(', ')
                        p = [float(i) for i in match.group(2).split(', ')]
                        for i in range(len(variables[variable])):
                            value = variables[variable][i]
                            table[tuple([value])][tuple(given)] = p[i]                            
            bayes_net.append([variable,variables[variable],parents,table])
    return bayes_net
def match(event,variables):#event is a dictionary,variables are list of variables, return tuple(T,F)
    return tuple(event[i] for i in variables)
####define class
class BayesNode:
    def __init__(self,name,domain,parents,cpt):
        if isinstance(cpt,(float,int)):# if no parents
            cpt={():cpt}
        self.variable=name
        self.domain=domain
        self.parents=parents
        self.children=[]
        self.cpt=cpt
        
    def prob(self,value,event):#return the conditional probability  
        ptrue=self.cpt[(value,)][match(event,self.parents)]
        return ptrue    
        
    #def sample(self,event):

        
    def __repr__(self):
        return repr((self.variable, ' '.join(self.parents)))
    
class BayesNet:
    def __init__(self,nodes=[]):
        self.nodes=[]
        self.variables=[]
        for node in nodes:
            self.add(tuple(node))
        #add children
        for node in self.nodes:
            self.variables.append(node.variable)
            for i in node.parents:
                self.variable_node(i).children.append(node)
        #sort
        self.sort()
                                   
    def sort(self):
        i=0
        for i in range(len(self.nodes)):
            if self.nodes[i].parents:
                for j in range(i,len(self.nodes)):
                    node=self.nodes[j]
                    find=True
                    for p in self.nodes[j].parents:
                        if p not in self.variables[:i]:
                            find=False
                            break
                    if find:
                        del self.nodes[j]
                        del self.variables[j]
                        self.nodes.insert(i,node)
                        self.variables.insert(i,node.variable)
                        break
         
   
    def add(self,nodes):
        node=BayesNode(*nodes)
        if nodes[2]==[]:
            self.nodes.insert(0,node)
        else:
            self.nodes.append(node)               
             
             

           
    def variable_node(self,name):#return the node of variable with name
        for i in self.nodes:
            if i.variable==name:
                return i
            
    def variable_values(self,var):# return the domain of var
        node=self.variable_node(var)
        return node.domain
    
    def __repr__(self):
        return 'BayesNet({0!r})'.format(self.nodes)
    
class ProbDist: #p=ProbDist('X',{'lo':25,'med':75,'hi':100})
    def __init__(self,varname='?',freqs=None):
        self.prob={}
        self.varname=varname
        self.values=[]
        if freqs:
            for (v,p) in freqs.items():
                self[v]=p
            self.normalize()
    def normalize(self):
        total=sum(self.prob.values())
        for var in self.prob:
            self.prob[var]/=total
        return self    
    
#Core functions
def enumeration_ask(X,e,bn):# 
    Q=ProbDist(X)
    for xi in bn.variable_values(X):
        Q.prob[xi]=enumerate_all(bn.variables,dict(e, **{X:xi}),bn)
    Q.normalize()
    print('Distribution of %s:' % X)
    print(Q.prob)

def enumerate_all(variables,e,bn):
    if not variables:
        return 1.0
    Y,rest=variables[0],variables[1:]
    Ynode=bn.variable_node(Y)
    if Y in e:
        return Ynode.prob(e[Y],e)*enumerate_all(rest,e,bn)
    else:
        return sum(Ynode.prob(y,e)*enumerate_all(rest,dict(e, **{Y:y}),bn) for y in bn.variable_values(Y))

#main
T,F=True, False
over=False
while not over:
    print('Please input the name of bif file')
    name=input()    
    bnlist=parse_bif(name)
    bn=BayesNet(bnlist)
    for i in bn.nodes:
        print(i)       
        
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
