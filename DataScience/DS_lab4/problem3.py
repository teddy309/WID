import numpy as np
import pandas as pd
from sklearn import linear_model
import matplotlib.pyplot as plt
from sklearn import preprocessing
import math,os,random
import warnings
warnings.filterwarnings(action='ignore')

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

def printScatterplot(listX,listY,c):
    plt.scatter(listX,listY,color=c)
    plt.xlabel('longitude')
    plt.ylabel('latitude')
    plt.show()

def testCase(startIndex,N,numK,testFrom,testTo):
    #Step 1: Compute Euclidean Distance of new input with existing datas
    testcase=D.loc[index[startIndex],['longitude','latitude']]
    tmpD=D.copy()#deep copy
    ED=getEuclideanDistances(testcase['longitude'],testcase['latitude'])
    tmpD['Distance']=pd.Series(ED)#put *********
    
    trainingD=tmpD.drop([index[i] for i in range(testFrom,testTo)])#D.iloc[index-index[startIndex:endIndex]]
    testD=tmpD.iloc[index[testFrom:testTo]]
    testD.loc[index[15:30],'lang']=np.nan
   
    tmpDsorted=trainingD.sort_values(by='Distance')
    #Step 2: Set K size with 8,
    #assume new input's T-shirt size by comparing to relatives selected by tmpD in size K
    K=numK
    countPython=tmpDsorted.head(K)['lang'].value_counts().to_dict().get(' Python')
    countJava=tmpDsorted.head(K)['lang'].value_counts().to_dict().get(' Java')
    countR=tmpDsorted.head(K)['lang'].value_counts().to_dict().get(' R')
    if countPython==max(countPython,countJava,countR):
        return pd.DataFrame({'longitude':[testcase['longitude']],'latitude':[testcase['latitude']],'lang':['python']})#[testcase['longitude'],testcase['latitude'],'python']#print("test data{0}(longitude:{1},latitude:{2}) is predicted to use Python language".format(startIndex,testcase['longitude'],testcase['latitude']))
    elif countJava==max(countPython,countJava,countR):
        return pd.DataFrame({'longitude':[testcase['longitude']],'latitude':[testcase['latitude']],'lang':['java']})#[testcase['longitude'],testcase['latitude'],'java']#print("test data{0}(longitude:{1},latitude:{2}) is predicted to use Java language".format(startIndex,testcase['longitude'],testcase['latitude']))
    elif countR==max(countPython,countJava,countR):
        return pd.DataFrame({'longitude':[testcase['longitude']],'latitude':[testcase['latitude']],'lang':['R']})#[testcase['longitude'],testcase['latitude'],'R']#print("test data{0}(longitude:{1},latitude:{2}) is predicted to use R language".format(startIndex,testcase['longitude'],testcase['latitude']))

def testNfoldEach(N,numK):
    subLength=int(len(D)/N)#N=5, length=15
    trainLength=subLength*4#length=60
    
    for i in range(N):
        meanRlongtd=0
        meanRlatd=0
        langCount=[0,0,0]
        for j in range(subLength):
            testResult=pd.DataFrame({'longitude':[],'latitude':[],'lang':[]})
            result=testCase(j,N,numK,(subLength*i)%trainLength,(subLength*(i+1))%trainLength)
            testResult.append(result)
            print(testResult)
            #meanRlongtd=meanRlongtd+result[0]
            #meanRlatd=meanRlatd+result[1]
            #for q in range(trainLength):
                #result=testCase(q,N,numK,subLength*(i+1)%trainLength,(subLength*(i+2))%trainLength)
                #testResult.append(result)
                #print(result)
            #print("test[",i,j,"]-------------")
            #print(testResult)
        print("N ",i,"-----------------")
        print(meanRlongtd/subLength)
        print(meanRlatd/subLength)
        print()


#read datas from csv file
readDt=pd.read_csv(os.getcwd()+'\\knn_data.csv')
D=readDt.iloc[:,0:3]
D['lang']=D.lang.astype('category')

#put new input
newInput=[-85.5,38.5]
#print("new input: (longitude: {0}, latitude: {1})".format(newInput[0],newInput[1]))
#print(D.loc[D['lang'].isin(['Python','R'])])##왜 Empty?????????


index=list(range(len(D)))
random.shuffle(index)

#for i in range(0,15):
    #testCase(i,8,15,30)
#testCase(40,5,8,15,30)
testNfoldEach(5,8)

#Step 1: Compute Euclidean Distance of new input with existing datas
ED=getEuclideanDistances(newInput[0],newInput[1])
D['Distance']=pd.Series(ED)#put *********
trainingD=pd.concat([D.iloc[index[0:15]],D.iloc[index[30:75]]]).copy()#test sample2
print("trainingD index: ",trainingD.index[0])###############

testD=D.iloc[index[15:30]]#test sample2
testD.loc[index[15:30],'lang']=np.nan
print("D---------------")
#print(D)
print("trainingD---------------")
#print(trainingD)
print("testD---------------")
#print(testD)
tmpD=trainingD.sort_values(by='Distance')



    
#Step 2: Set K size with 8,
#assume new input's T-shirt size by comparing to relatives selected by tmpD in size K
K=8
print(K,"tmpD-----------------")
#print(tmpD.head(K))#
countPython=tmpD.head(K)['lang'].value_counts().to_dict().get(' Python')
countJava=tmpD.head(K)['lang'].value_counts().to_dict().get(' Java')
countR=tmpD.head(K)['lang'].value_counts().to_dict().get(' R')
#print(countPython)
if countPython==max(countPython,countJava,countR):
    print("new data(longitude:{0},latitude:{1}) is predicted to use Python language".format(newInput[0],newInput[1]))
elif countJava==max(countPython,countJava,countR):
    print("new data(longitude:{0},latitude:{1}) is predicted to use Java language".format(newInput[0],newInput[1]))
elif countR==max(countPython,countJava,countR):
    print("new data(longitude:{0},latitude:{1}) is predicted to use R language".format(newInput[0],newInput[1]))

#seperate 'M' and 'L' size into array for scatter plot
sampleX_Python=np.array(trainingD.loc[trainingD['lang']==' Python']['longitude'])
sampleY_Python=np.array(trainingD.loc[trainingD['lang']==' Python']['latitude'])
sampleX_Java=np.array(trainingD.loc[trainingD['lang']==' Java']['longitude'])
sampleY_Java=np.array(trainingD.loc[trainingD['lang']==' Java']['latitude'])
sampleX_R=np.array(trainingD.loc[trainingD['lang']==' R']['longitude'])
sampleY_R=np.array(trainingD.loc[trainingD['lang']==' R']['latitude'])

tmpX_Python=np.array(tmpD.head(K).loc[tmpD.head(K)['lang']==' Python']['longitude'])
tmpY_Python=np.array(tmpD.head(K).loc[tmpD.head(K)['lang']==' Python']['latitude'])
tmpX_Java=np.array(tmpD.head(K).loc[tmpD.head(K)['lang']==' Java']['longitude'])
tmpY_Java=np.array(tmpD.head(K).loc[tmpD.head(K)['lang']==' Java']['latitude'])
tmpX_R=np.array(tmpD.head(K).loc[tmpD.head(K)['lang']==' R']['longitude'])
tmpY_R=np.array(tmpD.head(K).loc[tmpD.head(K)['lang']==' R']['latitude'])

plt.scatter(sampleX_Python,sampleY_Python,color='green')
plt.scatter(sampleX_Java,sampleY_Java,color='orange')
plt.scatter(sampleX_R,sampleY_R,color='black')
plt.scatter(testD['longitude'],testD['latitude'],color='blue')
plt.xlabel('longitude')
plt.ylabel('latitude')
plt.title('Python:Java:R trainingSet(green,orange,black), testSet=blue')
plt.show()
