import numpy as np
import pandas as pd
from sklearn import linear_model
import matplotlib.pyplot as plt
from sklearn import preprocessing
import math,os

#return euclidean distance between (x1,y1) and (x2,y2)
def EuclideanDistance(x1,y1,x2,y2):
    distance=math.sqrt((x1-x2)**2+(y1-y2)**2)
    return distance

#return list of distance from (x,y) to elements in dataframe D, using EuclideanDistance()
def getEuclideanDistances(x,y):
    dist=[]
    for i in range(len(D)):
        dist.append(EuclideanDistance(x,y,D.iloc[i,0],D.iloc[i,1]))
    return dist

#read datas from excel file
readDt=pd.read_excel(os.getcwd()+'\\dataset-lab4-problem2.xlsx','Sheet1',index_col=None)
#store 'Height','Weigth','Size' into dataframe D
#Then set column 'Size' as categorical data['M','L']
D=readDt.iloc[:,0:3]
D['Size']=D.Size.astype('category')

#put new input
print("new input: (161cm,61kg)")
newInput=[161.0,61.0]

#Step 0: Normaliztion of dataframe D for better prediction.
height=preprocessing.scale(np.append(D['Height'],newInput[0]))#normalize D with new input together
weight=preprocessing.scale(np.append(D['Weight'],newInput[1]))
newInput[0]=height[len(height)-1]#update new input to normalized values
newInput[1]=weight[len(weight)-1]
height=np.delete(height,len(height)-1)#delete normalized new input from height array
weight=np.delete(weight,len(weight)-1)
print("normalized new input: ",newInput)
D['Height']=pd.Series(height)#update dataframe D with normalized values
D['Weight']=pd.Series(weight)

#Step 1: Compute Euclidean Distance of new input with existing datas
ED=getEuclideanDistances(newInput[0],newInput[1])
D['Distance']=pd.Series(ED)
tmpD=D.sort_values(by='Distance')

#Step 2: Set K size with 7,
#assume new input's T-shirt size by comparing to relatives selected by tmpD in size K
K=7
print(tmpD.head(K))#
countL=tmpD.head(K)['Size'].value_counts('L').to_dict()['L']
countM=tmpD.head(K)['Size'].value_counts('L').to_dict()['M']
if countL>countM:
    print("new data({0}cm,{1}kg) is predicted to T-shirt size L".format(161,61))
else:
    print("new data({0}cm,{1}kg) is predicted to T-shirt size M".format(161,61))

#seperate 'M' and 'L' size into array for scatter plot
mX=np.array(D.loc[D['Size']=='M']['Weight'])
mY=np.array(D.loc[D['Size']=='M']['Height'])
lX=np.array(D.loc[D['Size']=='L']['Weight'])
lY=np.array(D.loc[D['Size']=='L']['Height'])
#show scatter plot(blue:size'M', orange:size'L', yellow:new input)
plt.scatter(mX,mY,color='blue')
plt.scatter(lX,lY,color='orange')
plt.scatter(newInput[1],newInput[0],color='yellow')#newInput[1]=weight,newInput[0]=height
plt.title("scatter plot with normalization")
plt.xlabel('Weight(kg)')
plt.ylabel('Height(cm)')
plt.show()
