import numpy as np
import pandas as pd
from sklearn import linear_model
import matplotlib.pyplot as plt
from sklearn import preprocessing
import math,os

#return frequency of key in each categories(cat)
def getRate(dataframe,cat,key):
    return dataframe[cat].value_counts(key).to_dict()[key]
#return entropy of each attributes(node) with values.
def entropy(dataframe,n,node,value):
    sum=0
    for i in range(n):
        sum=sum+getRate(dataframe,node,value)*math.log10(getRate(dataframe,node,value))#Pi*logPi(following latest ppt)
    return -sum #return negative of total integral 
#return entropy of root node
def entropy_root(dataframe,n,node):#entropy_root(dataframe,n)
    sum=0
    for i in range(n):
        sum=sum+getRate(dataframe,node,'Respond')*math.log10(getRate(dataframe,node,'Nothing'))#Pi*logPi(following latest ppt)
    return -sum#return negative of total integral 
#return information gain of each attributes(node)
def infoGain(dataframe,node,leftValue,rightValue):#entropy_root - sum(getRate(child)*entropy(child))
    return entropy_root(dataframe,2,'Outcome')-(getRate(dataframe,node,leftValue)*entropy(dataframe,2,node,leftValue)+getRate(dataframe,node,rightValue)*entropy(dataframe,2,node,rightValue))

#read datas from excel file
readDt=pd.read_excel(os.getcwd()+'\\dataset-lab4-problem1.xlsx','Sheet1',index_col=None)
#store 'District','HouseType','Income','PreviousCustomer','Outcome' attributes into dataframe df
df=readDt.iloc[:,0:5]
#Then set column 'District' as categorical data['Urban','Suburban','Rural']
#set column 'HouseType' as categorical data['Detached','Semi-detached']
#set column 'Income' as categorical data['High','Low']
#set column 'PreviousCustomer' as categorical data['Yes','No']
#set column 'Outcome' as categorical data['Respond','Nothing']
df['District']=df.District.astype('category')#
df['HouseType']=df.HouseType.astype('category')
df['Income']=df.Income.astype('category')
df['PreviousCustomer']=df.PreviousCustomer.astype('category')
df['Outcome']=df.Outcome.astype('category')
print(df)#print dataframe

#calculate entropies of 'HouseType' attribute and print it. Use entropy() for childs and entropy_root() for root
print("HouseType Node---------------")
HouseType_leftChild=entropy(df,2,'HouseType','Detached')
HouseType_rightChild=entropy(df,2,'HouseType','Semi-detached')
HouseType_root=entropy_root(df,2,'Outcome')#put 'Outcome' attribute for calculate root entropy
print("entropy of left-child: ",HouseType_leftChild)
print("entropy of right-child: ",HouseType_rightChild)
print("entropy of root node: ",HouseType_root)
#calculate entropies of 'PreviousCustomer' attribute and print it. Use entropy() for childs and entropy_root() for root
print("PreviousCustomer Node---------------")
PreviousCustomer_leftChild=entropy(df,2,'PreviousCustomer','Yes')
PreviousCustomer_rightChild=entropy(df,2,'PreviousCustomer','No')
PreviousCustomer_root=entropy_root(df,2,'Outcome')#put 'Outcome' attribute for calculate root entropy
print("entropy of left-child: ",PreviousCustomer_leftChild)
print("entropy of right-child: ",PreviousCustomer_rightChild)
print("entropy of root node: ",PreviousCustomer_root)
#calculate entropies of 'Income' attribute and print it. Use entropy() for childs and entropy_root() for root
print("Income Node---------------")
Income_leftChild=entropy(df,2,'Income','High')
Income_rightChild=entropy(df,2,'Income','Low')
Income_root=entropy_root(df,2,'Outcome')#put 'Outcome' attribute for calculate root entropy
print("entropy of left-child: ",PreviousCustomer_leftChild)
print("entropy of right-child: ",PreviousCustomer_rightChild)
print("entropy of root node: ",PreviousCustomer_root)

print("")
#calculate information gain with root node-entropies of each attributes.
#Use infoGain() function to calculate each information gain.
#Then print the result, attribute which has the largest information gain value.
infoGain_HouseType=infoGain(df,'HouseType','Detached','Semi-detached')
infoGain_PreviousCustomer=infoGain(df,'PreviousCustomer','Yes','No')
infoGain_Income=infoGain(df,'Income','High','Low')
print("information gain for House type: ",infoGain_HouseType)
print("information gain for Previous: ",infoGain_PreviousCustomer)
print("information gain for Income: ",infoGain_Income)
if(infoGain_HouseType==max(infoGain_HouseType,infoGain_PreviousCustomer,infoGain_Income)):
    print("Result: 'HouseType' attribute is chosen!!")
if(infoGain_PreviousCustomer==max(infoGain_HouseType,infoGain_PreviousCustomer,infoGain_Income)):
     print("Result: 'PreviousCustomer' attribute is chosen!!")
if(infoGain_Income==max(infoGain_HouseType,infoGain_PreviousCustomer,infoGain_Income)):
     print("Result: 'Income' attribute is chosen!!")
