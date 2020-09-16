import numpy as np
import pandas as pd
from sklearn import linear_model
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.impute import SimpleImputer
import os
#read csv file and read height,weight columns
filepath='DS-minilab-2-dataset.csv'
arr=pd.read_csv(os.getcwd()+'\\DS-minilab-2-dataset.csv')
data=arr.loc[:,['Height','Weight']]#store 'Height','Weight' columns into dataframe
height=data.loc[:,'Height']
weight=data.loc[:,'Weight']

#set outlier ranges of weight and height
outHMin=np.mean(height)-0.4*np.std(height);#'Height' outlier from outHMin(141)
outHMax=np.mean(height)+0.2*np.std(height)#to outHMax(206)
outWMin=np.mean(weight)-1*np.std(weight)#'Weight' outlier from outWMin(48)
outWMax=np.mean(weight)+0.1*np.std(weight)#to outWMax(116)
print("heigth outlier under: ",outHMin)
print("height outlier over=",outHMax)
print("weigth outlier under: ",outWMin)
print("weight outlier over=",outWMax)

#mark outliers with NaN and gather their index for scatter plotting
indexH=[]
indexW=[]
for i in range(len(weight)):
    if weight[i]<outWMin or outWMax<weight[i]:
        data.iat[i,1]=np.nan#if weight outlier, fix weight to NaN and gather index
        indexW.append(i)
    if height[i]<outHMin or outHMax<height[i]:
        data.iat[i,0]=np.nan#if height outlier, fix height to NaN and gather index
        indexH.append(i)
        
#plot scatter plot of normal data in blue color before imputation
plt.scatter(np.array(data['Height']),np.array(data['Weight']),color='b')

#impute NaN into mean values with Simpleimputer()
imp=SimpleImputer(missing_values=np.nan,strategy='mean')
data=imp.fit_transform(data)#fit and transform data itself withimputer
print(data.astype(int))#print imputed result in int values

#collect dirty datas indices into index list and put each estimated height,weight into list
estHeight=[]
estWeight=[]
index=list(set(indexW+indexH))
for i in index:
    estHeight.append(data[i,0])
for i in index:
    estWeight.append(data[i,1])
    
#plot scatter plot of abnormal data in red color after imputation and show it
plt.scatter(np.array(estHeight),np.array(estWeight),color='r')
plt.xlabel('height')
plt.ylabel('weight')
plt.title('Scatter plot: mean-value estimation')
plt.show()
