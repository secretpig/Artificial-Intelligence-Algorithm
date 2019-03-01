#import
import pandas as pd
import math


#dataset class
class DataSet():
    def __init__(self,source='',examples=[],attributes={}):
        self.source=source
        self.examples=examples
        self.attributes=attributes
        self.upload()
    
    def upload(self):
        dataframe=pd.read_csv(self.source,sep=',')
        row,col=dataframe.shape
        for i in list(dataframe.columns):
            self.attributes[i]=tuple(dataframe[i].unique())
        for i in range(row):
            dict={}
            for j in range(col):
                dict[dataframe.columns[j]]=dataframe.iloc[i,j]
            self.examples.append(dict)            
        
    def __repr__(self):
        return '<dataset({}):{:d} examples, {:d} attributes>'.format(
            self.name, len(self.examples),len(self.attributes))

# class for decision tree
class DecisionLeaf():
    def __init__(self,name):
        self.name=name
    def display(self,indent=0):
        print('Class=',self.name)    
    def __repr__(self):
        return repr(self.name)
    def __call__(self,example):
        return self.name
class DecisionTree():
    def __init__(self,name,default_child=None,branches=None):
        self.name=name
        self.branches=branches or {}
        self.default_child=default_child
    def add(self,val,subtree):
        self.branches[val]=subtree
        
    def display(self,indent=0):
        name=self.name
        print('Attribute:',name)
        for (val,subtree) in self.branches.items():
            print(' '*4*indent,name,'=',val,'==>',end=' ')
            subtree.display(indent+1)
    def __call__(self,example):
        attrvalue=example[self.name]
        if attrvalue in self.branches:
            return self.branches[attrvalue](example)
        else:
            return self.default_child(example)        
            
    def __repr__(self):
        return ('DecisionTree({0!r},{1!r})'
                .format(self.name,self.branches))


#functions
def DTL(dataset):

    def DecisionTL(examples,attributes,p_examples=[]):
        if len(examples)==0:
            return plurality_value(p_examples)
        elif same_class(examples):
            return DecisionLeaf(examples[0][classifier])
        elif len(attributes)==0:
            return plurality_value(examples)
        else:
            A=choose_attribute(attributes,examples)
            tree=DecisionTree(A,plurality_value(examples))
            attributes.remove(A)
            for vk in dataset.attributes[A]:
                exs=split_by(A,vk,examples)
                subtree=DecisionTL(exs,attributes,examples)
                tree.add(vk,subtree)
            return tree
    def plurality_value(examples):
        count={}
        for e in examples:
            if e[classifier] not in count.keys():
                count[e[classifier]]=1
            else:
                count[e[classifier]]+=1
        popular=max(count.items(),key=lambda x:x[1])[0]
        return DecisionLeaf(popular)
    
    def same_class(examples):
        class0=examples[0][classifier]
        return all(e[classifier]==class0 for e in examples)
    
    def choose_attribute(attributes,examples):
        DI=Prob(examples)
        dict={}
        for A in attributes:
            dict[A]=DI-information(A,examples)
        return max(dict.items(),key=lambda x:x[1])[0]
        
    def information(attr,examples):
        sums=0
        for val in dataset.attributes[attr]:
            es=split_by(attr,val,examples)
            sums+=(len(es)/len(examples))*Prob(es)
        return sums           
    
    def split_by(attr,val,examples):
        return list(filter(lambda x:x[attr]==val, examples)) 
    def Prob(examples):
        count={c:0 for c in dataset.attributes[classifier]}
        total=len(examples)
        sums=0    
        for e in examples:
            count[e[classifier]]+=1            
        for v in count.values():
            if v!=0:
                sums-=(v/total)*math.log2(v/total)           
        return sums
            
    pureattr=list(dataset.attributes.keys())
    pureattr.remove(classifier)
    result=DecisionTL(dataset.examples,pureattr,p_examples=[])
    result.display()
    return result
    
#main
#classifier='WillWait'
#source='WillWait-data.csv'
#classifier='class'
#source='iris.data.discrete.csv'
#data=DataSet(source)

#A=DTL(data)
#print(A({'sepal length': 'S', 'sepal width': 'S', 'petal length': 'ML', 'petal width': 'ML'}))

#main
T,F=True, False
over=False
while not over:
    print('Please input the name of file')
    source=input()
    if source=="end":
        break
    data=DataSet(source) 
    print('Upload complete!')
    print('input the name of classifier')
    classifier=input()
    if classifier=="end":
        break
    result=DTL(data)
    print('input example that you want to classifiy')
    e=input()
    if e=="end":
        break
    e=e.split(',')
    i=0
    dict={}
    while i<len(e):
        dict[e[i]]=e[i+1]
        i+=2
    print(result(dict))
    end=input('Do you want to exit? Y or N:    ')
    if end=='Y' or end=='y:
        over=True
