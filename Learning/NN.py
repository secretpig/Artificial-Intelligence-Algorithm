import pandas as pd
import math
import numpy as np
import random

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

#unit class, network
class NNUnit:
    def __init__(self,weights=None,inputs=None):
        self.weights=[]
        self.inputs=[]
        self.value=None
        
def network(input_units,hidden_layer_sizes,output_units):
    if hidden_layer_sizes:
        layers_sizes=[input_units]+hidden_layer_sizes+[output_units]
    else:
        layer_sizes=[input_units]+[output_units]
        
    net=[[NNUnit() for n in range(size)] for size in layers_sizes]
    n_layers=len(net)
    
    #Connection
    for i in range(1,n_layers):
        for n in net[i]:
            for k in net[i-1]:
                n.inputs.append(k)
                n.weights.append(0)
    return net

# NNLearner    
    
def NeuralNetLearner(dataset,hidden_layer_sizes=[3],learning_rate=0.1,epochs=500):
    i_units=len(dataset.attributes.keys())-1
    o_units=len(dataset.attributes[classifier])
    y_label=list(dataset.attributes[classifier])
    x_col=list(dataset.attributes.keys())
    x_col.remove(classifier)
    
    raw_net=network(i_units,hidden_layer_sizes,o_units)
    learned_net=BackPropagationLearner(dataset,raw_net,learning_rate,epochs,y_label,x_col)
    def predict(example):
        i_val=[example[x_col[i]] for i in range(len(x_col))]
        i_nodes=learned_net[0]
        for v,n in zip(i_val,i_nodes):
            n.value=v 
        for layer in learned_net[1:]:
            for node in layer:
                inc=[n.value for n in node.inputs]
                in_val=np.dot(inc,node.weights)
                node.value=1/(1+math.exp(-in_val))
        
        o_nodes=learned_net[-1]
        temp=0
        for node in o_nodes:
            if node.value>temp:                
                prediction=y_label[o_nodes.index(node)]
                temp=node.value

        return prediction
    return predict

    
def BackPropagationLearner(dataset,net,learning_rate,epochs,y_label,x_col):
    for layer in net:
        for node in layer:
            node.weights=[random.uniform(-0.5,0.5) for i in range(len(node.weights))]
    #assign small random number to weights
    
    examples=dataset.examples
    
    o_nodes=net[-1]
    i_nodes=net[0]
    o_units=len(o_nodes)
    n_layers=len(net)   
    

    for epoch in range(epochs):
        for e in examples:
            i_val=[e[x_col[i]] for i in range(len(x_col))]
            t_val=[]
            for y in y_label:
                if e[classifier]==y:
                    t_val.append(1)
                else:
                    t_val.append(0)
            
            #activate input layer
            for v,n in zip(i_val,i_nodes):
                n.value=v
                
            #forward pass
            for layer in net[1:]:
                for node in layer:
                    inc=[n.value for n in node.inputs]
                    in_val=np.dot(inc,node.weights)
                    node.value=1/(1+math.exp(-in_val))
                    
            #initialize delta
            delta=[[] for i in range(n_layers)]
            
            #compute output layer delta
            err=[t_val[i]-o_nodes[i].value for i in range(o_units)]
            delta[-1]=[(o_nodes[i].value*(1-o_nodes[i].value))*err[i] for i in range(o_units)]      
            #Backwaard pass
            h_layers=n_layers-2
            for i in range(h_layers,0,-1):
                layer=net[i]
                h_units=len(layer)
                nx_layer=net[i+1]
                w=[[node.weights[k] for node in nx_layer] for k in range(h_units)]
                delta[i]=[(layer[j].value*(1-layer[j].value))*np.dot(w[j],delta[i+1]) for j in range(h_units)]
            #update weights
            for i in range(1,n_layers):
                layer=net[i]
                inc=[node.value for node in net[i-1]]
                units=len(layer)
                for j in range(units):
                    for w in range(len(layer[j].weights)):
                        layer[j].weights[w]=layer[j].weights[w]+learning_rate*delta[i][j]*inc[w]
                  
                    
                    
    return net
#training function
def training(source,hidden_layer_sizes,epochs):
    data=DataSet(source)
    data1,data2=Divide(data,0.9)
    Net=NeuralNetLearner(data1,hidden_layer_sizes,0.1,epochs)
    total1=len(data1.examples)
    total2=len(data2.examples)
    count1=0
    count2=0
    for e in data1.examples:
        y=e[classifier]
        del e[classifier]
        if y==Net(e):
            count1+=1
   
                
    for e in data2.examples:
        y=e[classifier]
        del e[classifier]
        if y==Net(e):
            count2+=1
    print("Accuracy for training data is %3f" %(count1/total1))
    print("Accuracy for test data is %3f" %(count2/total2))
    return Net    

    
#classifier='class'
#source='Iris.csv'
#classifier='class'
#source='wine2.csv'   
#Result=training(source)
#example={'sepal length': 6.0, 'sepal width': 2, 'petal length': 5.0, 'petal width': 1.5}
#print(Result(example))

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
    
    print('input units for hidden layer, times of iteration')
    para=input()
    if para=="end":
        break
    para=para.split(',')
    hidden_layer_sizes=[]
    for i in para[:len(para)-1]:
        hidden_layer_sizes.append(int(i))

    epochs=int(para[-1])
    result=training(source,hidden_layer_sizes,epochs)
    print('input example that you want to classify')
    e=input()
    if e=="end":
        break
    e=e.split(',')
    i=0
    dict={}
    while i<len(e):
        dict[e[i]]=float(e[i+1])
        i+=2
    print(result(dict))
    end=input('Do you want to exit? Y or N:    ')
    if end=='Y' or end=='y':
        over=True