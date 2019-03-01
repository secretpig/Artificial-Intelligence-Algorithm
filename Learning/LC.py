import pandas as pd
import math
import numpy as np
import random
import matplotlib.pyplot as plt
#dataset class
class DataSet():
    def __init__(self,source='',examples=[],attributes={}):
        self.source=source
        self.examples=examples
        self.attributes=attributes
        if source!='':
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
# devide dataset into 2 parts
def Divide(dataset,p):
    dataset1=DataSet('',[],dataset.attributes)
    dataset2=DataSet('',[],dataset.attributes)
    size=len(dataset.examples)
    for e in dataset.examples:
        if len(dataset1.examples)>size*p:
            dataset2.examples.append(e)
        elif len(dataset2.examples)>size*(1-p):
            dataset1.examples.append(e)
        else:
            if random.uniform(0,1)<0.2:
                dataset2.examples.append(e)
            else:
                dataset1.examples.append(e)    
    return dataset1,dataset2        
#classifier class
class Perceptron():
    def __init__(self,dataset,target):
        self.xcol=list(dataset.attributes.keys())
        self.xcol.remove(target)
        self.y=[]
        self.x=[]
        dummy={c:0 for c in dataset.attributes[target]}
        for e in dataset.examples:
            temp=[e[i] for i in self.xcol]
            self.x.append(temp)
            temp=dict(dummy)
            temp[e[target]]=1
            self.y.append(temp)
        self.w={c:[random.uniform(-0.5,0.5) for i in range(len(self.xcol)+1)] for c in dataset.attributes[target]}
        self.size=len(self.x)
        self.classes=dict(dummy)
        
    def update_w(self,rate,w):
        e=random.randint(0, self.size-1)
        for i in range(len(self.xcol)+1):
            learning=0
            x=[1]+self.x[e]
            y=self.y[e]
            for c in sorted(y.keys()):
                if np.dot(w[c],x)>0:hw=1
                else:hw=0
                learning=(y[c]-hw)*x[i]
                w[c][i]+=rate*learning
        return w
    
    def Logupdate_w(self,rate,w):
        e=random.randint(0, self.size-1)
        for i in range(len(self.xcol)+1):
            learning=0
            x=[1]+self.x[e]
            y=self.y[e]
            for c in sorted(y.keys()):
                hw=1/(1+math.exp(-np.dot(w[c],x)))
                learning=(y[c]-hw)*x[i]*hw*(1-hw)
                w[c][i]+=rate*learning
        return w
    
    def predict(self,example,w):
        output=dict(self.classes)
        x=[1]+example
        for c in sorted(output.keys()):
            if np.dot(w[c],x)>0:output[c]=1
            else:output[c]=0
        for k,v in output.items():
            if v==1:
                return k
        return k
            
    def Logpredict(self,example,w):
        output=dict(self.classes)
        x=[1]+example
        for c in sorted(output.keys()):
            hw=1/(1+math.exp(-np.dot(w[c],x)))
            if hw>=0.5:output[c]=1
            else:output[c]=0
        output=dict(sorted(output.items(),key=lambda item:item[1],reverse = True))
        for k,v in output.items():
            if v==1:
                return k        
        return k
 
            
        
    def correctrate(self,w):
        count=0
        for x,y in zip(self.x,self.y):
            label=self.predict(x,w)
            if y[label]==1:
                count+=1
        return count/self.size
    
    def Logcorrectrate(self,w):
        count=0
        for x,y in zip(self.x,self.y):
            label=self.Logpredict(x,w)
            if y[label]==1:
                count+=1
        return count/self.size
         

#test function
def training1(source,epochs):
    data=DataSet(source)
    data1,data2=Divide(data,0.9)
    Linear1=Perceptron(data1,classifier)
    Linear2=Perceptron(data2,classifier)
    
    w=Linear1.w
    for t in range(epochs):
        rate=1000/(1000+t)
        w=Linear1.update_w(rate,w)
    
    c1=Linear1.correctrate(w)
    c2=Linear2.correctrate(w)

    print("Accuracy for training data is %3f" %(c1))
    print("Accuracy for test data is %3f" %(c2))
    return Linear1,w

def training2(source,epochs):
    data=DataSet(source)
    data1,data2=Divide(data,0.9)
    Linear1=Perceptron(data1,classifier)
    Linear2=Perceptron(data2,classifier)
    
    w=Linear1.w
    for t in range(epochs):
        rate=1000/(1000+t)
        w=Linear1.Logupdate_w(rate,w)
    
    c1=Linear1.Logcorrectrate(w)
    c2=Linear2.Logcorrectrate(w)

    print("Accuracy for training data is %3f" %(c1))
    print("Accuracy for test data is %3f" %(c2))
    return Linear1,w


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
    
    print('input times of iteration')
    epochs=input()
    if epochs=="end":
        break
    epochs=int(epochs)
    
    print('input method you want to use 1:perception, 2:logistic')
    method=input()
    if method=="end":
        break
    if method=='1':
        result,w=training1(source,epochs)
        print('input example that you want to classify')
        e=input()
        if e=="end":
            break
        e=e.split(',')
        example=[float(i) for i in e]
        print(result.predict(example,w))
    else:
        result,w=training2(source,epochs)
        print('input example that you want to classify')
        e=input()
        if e=="end":
            break
        e=e.split(',')
        example=[float(i) for i in e]
        print(result.Logpredict(example,w))   

    end=input('Do you want to exit? Y or N:    ')
    if end=='Y' or end=='y':
        over=True




