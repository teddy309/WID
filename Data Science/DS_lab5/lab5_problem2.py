from sklearn import datasets

import pandas as pd
import warnings
from math import *
import numpy as np
import matplotlib.pyplot as plt
import os,random,math
warnings.filterwarnings(action='ignore')


#return euclidean distance between (x1,y1) and (x2,y2)
def EuclideanDistance(aSL,aSW,aPL,aPW,bSL,bSW,bPL,bPW):
    distance=math.sqrt((aSL-bSL)**2+(aSW-bSW)**2+(aPL-bPL)**2+(aPW-bPW)**2)
    return distance

#return list of distance from (x,y) to elements in dataframe D, using EuclideanDistance()
def getEuclideanDistance(dataframe,A,i):
    irisI=[dataframe['SepalLengthCm'][i],dataframe['SepalWidthCm'][i],dataframe['PetalLengthCm'][i],dataframe['PetalWidthCm'][i]]
    irisA=[dataframe['SepalLengthCm'][A],dataframe['SepalWidthCm'][A],dataframe['PetalLengthCm'][A],dataframe['PetalWidthCm'][A]]
    return EuclideanDistance(irisA[0],irisA[1],irisA[2],irisA[3],irisI[0],irisI[1],irisI[2],irisI[3])

def moveCluster(clusterFrom,i,clusterTo):
    #clusterTo=clusterTo.append(pd.Series(clusterFrom.loc[fromIndex,:]))
    #clusterFrom=clusterFrom.drop(fromIndex,axis=0)
    clusterTo=clusterTo.append(pd.Series(clusterFrom.loc[i,:]))
    clusterFrom=clusterFrom.drop(i,axis=0)

readDt=pd.read_csv(os.getcwd()+'\\iris.csv')
iris=readDt.iloc[:,0:6]
iris['Species']=iris.Species.astype('category')

index=list(range(len(iris)))
centroidIndex=random.sample(index,3)
print(centroidIndex)
print(iris.loc[centroidIndex[0]])
print(iris.loc[centroidIndex[1]])
print(iris.loc[centroidIndex[2]])



#print(centroid)
#print(centroid[1])
#EuclideanDistance(iris[i]['SepalLengthCm'],iris[i]['SepalWidth'],iris[centroidIndex[j]]['SepalLengthCm'],iris[centroidIndex[j]]['SepalWidthCm'])
print("")
#print(pd.Series(iris.loc[0]))
cluster1=pd.DataFrame({'Id':[],'SepalLengthCm':[],'SepalWidthCm':[],'PetalLengthCm':[],'PetalWidthCm':[],'Species':[]})
cluster2=pd.DataFrame({'Id':[],'SepalLengthCm':[],'SepalWidthCm':[],'PetalLengthCm':[],'PetalWidthCm':[],'Species':[]})
cluster3=pd.DataFrame({'Id':[],'SepalLengthCm':[],'SepalWidthCm':[],'PetalLengthCm':[],'PetalWidthCm':[],'Species':[]})
#clusterIndex1,clusterIndex2,clusterIndex3=[],[],[]
for i in range(len(iris)):
    if min(getEuclideanDistance(iris,i,centroidIndex[0]),getEuclideanDistance(iris,i,centroidIndex[1]),getEuclideanDistance(iris,i,centroidIndex[2]))==getEuclideanDistance(iris,i,centroidIndex[0]):
        cluster1=cluster1.append(pd.Series(iris.loc[i]))#pd.DataFrame([s.to_dict() for s in iris.loc[i]])#cluster1.append(pd.DataFrame(iris.loc[i]))
    elif min(getEuclideanDistance(iris,i,centroidIndex[0]),getEuclideanDistance(iris,i,centroidIndex[1]),getEuclideanDistance(iris,i,centroidIndex[2]))==getEuclideanDistance(iris,i,centroidIndex[1]):
        cluster2=cluster2.append(pd.Series(iris.loc[i]))#cluster2.append(pd.Series(iris.loc[i]))
    elif min(getEuclideanDistance(iris,i,centroidIndex[0]),getEuclideanDistance(iris,i,centroidIndex[1]),getEuclideanDistance(iris,i,centroidIndex[2]))==getEuclideanDistance(iris,i,centroidIndex[2]):
        cluster3=cluster3.append(pd.Series(iris.loc[i]))#cluster3.append(pd.Series(iris.loc[i]))
print("cluster1")
print(cluster1)
print(cluster2)
#print(cluster3)


def getCentroid(clst):
    Centroid=pd.DataFrame({'SepalLengthCm':[np.mean(clst['SepalLengthCm'])],'SepalWidthCm':[np.mean(clst['SepalWidthCm'])],'PetalLengthCm':[np.mean(clst['PetalLengthCm'])],'PetalWidthCm':[np.mean(clst['PetalLengthCm'])]})
    return Centroid
def getCentroidDistance(dataframe,i,Centroid):
    irisI=[dataframe['SepalLengthCm'][i],dataframe['SepalWidthCm'][i],dataframe['PetalLengthCm'][i],dataframe['PetalWidthCm'][i]]
    irisA=[Centroid['SepalLengthCm'][0],Centroid['SepalWidthCm'][0],Centroid['PetalLengthCm'],Centroid['PetalWidthCm'][0]]
    return EuclideanDistance(irisA[0],irisA[1],irisA[2],irisA[3],irisI[0],irisI[1],irisI[2],irisI[3])

#print(cluster1['SepalLengthCm'][0])

prevC1=cluster3
prevC2=cluster1
prevC3=cluster2
#prevC1=pd.DataFrame({'Id':[],'SepalLengthCm':[],'SepalWidthCm':[],'PetalLengthCm':[],'PetalWidthCm':[],'Species':[]})
#prevC2=pd.DataFrame({'Id':[],'SepalLengthCm':[],'SepalWidthCm':[],'PetalLengthCm':[],'PetalWidthCm':[],'Species':[]})
#prevC3=pd.DataFrame({'Id':[],'SepalLengthCm':[],'SepalWidthCm':[],'PetalLengthCm':[],'PetalWidthCm':[],'Species':[]})
#print(bufC1.equals(bufC1))
cent=getCentroid(cluster1)
#print(getCentroidDistance(cluster1,0,cent))#getCentroid(cluster1)))

x=pd.DataFrame({'k':[0]})
y=pd.DataFrame({'k':[1]})
print("SAME?: ",x.equals(y))

while(True):
    centroid1,centroid2,centroid3=getCentroid(cluster1),getCentroid(cluster2),getCentroid(cluster3)
    if prevC1.equals(cluster1) and prevC2.equals(cluster2) and prevC3.equals(cluster3):
        break
    prevC1,prevC2,prevC3=centroid1,centroid2,centroid3
    print(centroid1)
    print(centroid2)
    print(centroid3)
    print(prevC1)
    print(prevC2)
    print(prevC3)
    print("--------------------------",prevC1.equals(cluster1),prevC2.equals(cluster2),prevC3.equals(cluster3))





print(cluster1.drop(cluster1.index[0]))
      

for i in range(10):
    cluster2=cluster2.append(pd.Series(cluster1.loc[i,:]))
    cluster1=cluster1.drop(i,axis=0)
print("will be moved")
#moveCluster(cluster1,0,cluster2)
#print(cluster1.loc[0])
#cluster2=cluster2.append(pd.Series(cluster1.loc[0,:]))
print("OK")
#cluster1=cluster1.drop(0,axis=0)
#cluster2=cluster2.append(moveCluster(cluster1,0,cluster2))

print("deleted cluster1")
print(cluster1)
print(cluster2)

        

