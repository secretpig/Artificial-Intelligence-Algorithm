#import labs
import sys
import time
import random
from numpy import *
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
        
    def sample(self,event):
        Q=ProbDist(self.variable)
        for xi in bn.variable_values(self.variable):
            Q.prob[xi]=self.prob(xi,event)
        Q.normalize()
        p=random.uniform(0.0, 1.0)
        dic={}
        temp=0
        for x in Q.prob.keys():
            dic[x]=[temp,Q.prob[x]+temp]
            temp=Q.prob[x]+temp
        for x in dic.keys():
            if p>=dic[x][0] and p<=dic[x][1]:
                return x     
        

        
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
                self.prob[v]=p
            self.normalize()
    def normalize(self):
        temp=list(self.prob.values())
        total=sum(temp)
        for var in self.prob:
            temp=self.prob[var]
            self.prob[var]/=total
        return self    
    
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
    count={x:0 for x in bn.variable_values(X)}
    for j in range(N):
        x=prio_sample(bn)
        if consistent(x,e):
            count[x[X]]+=1
    Q=ProbDist(X,count)
    Q.normalize()
    print('Distribution of %s:' % X)
    print(Q.prob)
#Core functions/likelihood weighting
def likelihood(X,e,bn,N):
    w={x:0 for x in bn.variable_values(X)}
    for j in range(N):
        sample,weight=weighted_sample(bn,e)
        w[sample[X]]+=weight
    Q=ProbDist(X,w)
    Q.normalize()
    print('Distribution of %s:' % X)
    print(Q.prob)

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
    counts={x:0 for x in bn.variable_values(X)}
    Z=[var for var in bn.variables if var not in e]
    state=dict(e)
    for Zi in Z:
        state[Zi]=random.choice(bn.variable_values(Zi))
    for j in range(N):
        for Zi in Z:
            state[Zi]=marcov_blanket(Zi,state,bn)
            counts[state[X]]+=1
    Q=ProbDist(X,counts)
    Q.normalize()
    print('Distribution of %s:' % X)
    print(Q.prob)
    
def marcov_blanket(X,e,bn):
    Xnode=bn.variable_node(X)
    P=ProbDist(X)
    for xi in bn.variable_values(X):
        ei=dict(e, **{X:xi})
        P.prob[xi]=Xnode.prob(xi,e)*product([Yj.prob(ei[Yj.variable],ei) for Yj in Xnode.children])
    P.normalize()
    p=random.uniform(0.0, 1.0)
    dic={}
    temp=0
    for x in P.prob.keys():
        dic[x]=[temp,P.prob[x]+temp]
        temp+=P.prob[x]
    for x in dic.keys():
        if p>=dic[x][0] and p<=dic[x][1]:
            return x
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
    print('input sample size')
    M=int(input())
    print(X,evidence,M)
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