import numpy as np
import pandas as pd
from sklearn import linear_model
import matplotlib.pyplot as plt
from sklearn import preprocessing
import math,os,random

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
        sum=sum+getRate(dataframe,node,True)*math.log10(getRate(dataframe,node,False))#Pi*logPi(following latest ppt)
    return -sum#return negative of total integral 
#return information gain of each attributes(node)
def infoGain(dataframe,node,n):#entropy_root - sum(getRate(child)*entropy(child))
    child=[]
    entropyChild=[]
    for i in range(n):
        child.append(trainingD[node].unique()[i])
        entropyChild.append(entropy(dataframe,n,node,child[i]))
        return entropy_root(dataframe,n,'interview')-sum(entropyChild)


#read datas from excel file
readDt=pd.read_csv(os.getcwd()+'\\decision_tree_data.csv',encoding='utf-8')
#store 'District','HouseType','Income','PreviousCustomer','Outcome' attributes into dataframe df
df=readDt.iloc[:,0:5]
#Then set column 'level' as categorical data['senior','mid','junior']
#set column 'lang' as categorical data['java','python','R']
#set column 'tweets' as categorical data['no','yes']
#set column 'phd' as categorical data['no','yes']
#set column 'interview' as categorical data['FALSE','TRUE']
df['level']=df.level.astype('category')#['senior','mid','junior']
df['lang']=df.lang.astype('category')
df['tweets']=df.tweets.astype('category')
df['phd']=df.phd.astype('category')
df['interview']=df.interview.astype('category')

index=list(range(len(df)))
random.shuffle(index)

testD=df.iloc[index[0:3]].copy()#take 1/10 for testing set
trainingD=df.iloc[index[3:30]].copy()#take 9/10 for training set
print(testD)

#calculate entropies of 'tweets' attribute and print it. Use entropy() for childs and entropy_root() for root
print("tweets---------------")
tweets_leftChild=entropy(trainingD,2,'tweets','no')
tweets_rightChild=entropy(trainingD,2,'tweets','yes')
tweets_root=entropy_root(trainingD,2,'interview')#put 'interview' attribute for calculate root entropy
print("entropy of left-child: ",tweets_leftChild)
print("entropy of right-child: ",tweets_rightChild)
print("entropy of root node: ",tweets_root)
#calculate entropies of 'phd' attribute and print it. Use entropy() for childs and entropy_root() for root
print("phd---------------")
phd_leftChild=entropy(trainingD,2,'phd','no')
phd_rightChild=entropy(trainingD,2,'phd','yes')
phd_root=entropy_root(trainingD,2,'interview')#put 'interview' attribute for calculate root entropy
print("entropy of left-child: ",phd_leftChild)
print("entropy of right-child: ",phd_rightChild)
print("entropy of root node: ",phd_root)
#calculate entropies of 'lang' attribute and print it. Use entropy() for childs and entropy_root() for root
print("lang---------------")
lang_javaChild=entropy(trainingD,3,'lang','java')
lang_RChild=entropy(trainingD,3,'lang','R')
lang_PythonChild=entropy(trainingD,3,'lang','python')
lang_root=entropy_root(trainingD,3,'interview')#put 'interview' attribute for calculate root entropy
print("entropy of java-child: ",lang_javaChild)
print("entropy of R-child: ",lang_RChild)
print("entropy of Pyton-child: ",lang_PythonChild)
print("entropy of root node: ",lang_root)
print("")

#calculate information gain with root node-entropies of each attributes.
#Use infoGain() function to calculate each information gain.
#Then print the result, attribute which has the largest information gain value.
infoGain_tweets=infoGain(df,'tweets',2)
infoGain_phd=infoGain(df,'phd',2)
infoGain_lang=infoGain(df,'lang',3)
print("information gain for tweets: ",infoGain_tweets)
print("information gain for phd: ",infoGain_phd)
print("information gain for lang: ",infoGain_lang)

decisionRoot=''
if(infoGain_tweets==max(infoGain_tweets,infoGain_phd,infoGain_lang)):
    print("Result: 'tweets' attribute is chosen!!")
    decisionRoot='tweets'
if(infoGain_phd==max(infoGain_tweets,infoGain_phd,infoGain_lang)):
     print("Result: 'phd' attribute is chosen!!")
     decisionRoot='phd'
if(infoGain_lang==max(infoGain_tweets,infoGain_phd,infoGain_lang)):
     print("Result: 'lang' attribute is chosen!!")
     decisionRoot='lang'



print("       ")
print("decision tree for test set Start!!----------------------------")
print("       ")


#calculate entropies of 'tweets' attribute and print it. Use entropy() for childs and entropy_root() for root
print("tweets---------------")
tweets_leftChild=entropy(testD,2,'tweets','no')
tweets_rightChild=entropy(testD,2,'tweets','yes')
tweets_root=entropy_root(testD,2,'interview')#put 'interview' attribute for calculate root entropy
print("entropy of left-child: ",tweets_leftChild)
print("entropy of right-child: ",tweets_rightChild)
print("entropy of root node: ",tweets_root)
#calculate entropies of 'phd' attribute and print it. Use entropy() for childs and entropy_root() for root
print("phd---------------")
phd_leftChild=entropy(testD,2,'phd','no')
phd_rightChild=entropy(testD,2,'phd','yes')
phd_root=entropy_root(testD,2,'interview')#put 'interview' attribute for calculate root entropy
print("entropy of left-child: ",phd_leftChild)
print("entropy of right-child: ",phd_rightChild)
print("entropy of root node: ",phd_root)
#calculate entropies of 'lang' attribute and print it. Use entropy() for childs and entropy_root() for root
print("lang---------------")
lang_javaChild=entropy(testD,3,'lang','java')
lang_RChild=entropy(testD,3,'lang','R')
lang_PythonChild=entropy(testD,3,'lang','python')
lang_root=entropy_root(testD,3,'interview')#put 'interview' attribute for calculate root entropy
print("entropy of java-child: ",lang_javaChild)
print("entropy of R-child: ",lang_RChild)
print("entropy of Pyton-child: ",lang_PythonChild)
print("entropy of root node: ",lang_root)
print("")


#calculate information gain with root node-entropies of each attributes.
#Use infoGain() function to calculate each information gain.
#Then print the result, attribute which has the largest information gain value.
infoGain_tweets=infoGain(df,'tweets',2)
infoGain_phd=infoGain(df,'phd',2)
infoGain_lang=infoGain(df,'lang',3)
print("information gain for tweets: ",infoGain_tweets)
print("information gain for phd: ",infoGain_phd)
print("information gain for lang: ",infoGain_lang)


if(infoGain_tweets==max(infoGain_tweets,infoGain_phd,infoGain_lang)):
    print("Result: 'tweets' attribute is chosen!!")
    if DecisionRoot=='tweets':
        print("prediction correct!!")
if(infoGain_phd==max(infoGain_tweets,infoGain_phd,infoGain_lang)):
     print("Result: 'phd' attribute is chosen!!")
     if DecisionRoot=='phd':
        print("prediction correct!!")
if(infoGain_lang==max(infoGain_tweets,infoGain_phd,infoGain_lang)):
     print("Result: 'lang' attribute is chosen!!")
     if DecisionRoot=='lang':
        print("prediction correct!!")




