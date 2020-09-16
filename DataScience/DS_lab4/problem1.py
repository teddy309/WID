import numpy as np
import pandas as pd
from sklearn import linear_model
import matplotlib.pyplot as plt
from sklearn import preprocessing
import math,os,random


#read datas from csv file
readDt=pd.read_csv(os.getcwd()+'\\linear_regression_data.csv',encoding='utf-8')
#store 'Distance','Delivery Time' attributes into dataframe df
df=readDt.iloc[:,0:2]

#generate index list and shuffle for sampling
index=list(range(len(df)))#index 0~29
random.shuffle(index)#shuffle index array randomly
testD=df.iloc[index[0:6]].copy()#take 6 for test set
trainingD=df.iloc[index[6:30]].copy()#take rest 24 for training set
print("training Set----------------------------")
print(trainingD)

sumX=0#sum of Distance values of training set
sumY=0#sum of Delivery Time values of training set
sumXY=0#sum of Distance*Delivery Time values of training set
sumXpow=0#sum of Distance^2 values of training set
#calculate training set's values for get linear regression from training set
for i in range(len(trainingD)):
    sumX=sumX+trainingD['Distance'].iloc[i]
    sumY=sumY+trainingD['Delivery Time'].iloc[i]
    sumXY=sumXY+trainingD['Distance'].iloc[i]*trainingD['Delivery Time'].iloc[i]
    sumXpow=sumXpow+(trainingD['Distance'].iloc[i])**2
numTrain=len(trainingD)
meanX=sumX/numTrain#mean of Distance values of training set
meanY=sumY/numTrain#mean of Delivery Time values of training set
print("sum(X):",sumX," sum(Y): ",sumY," sum(X*Y): ",sumXY,"sum(X^2):",sumXpow)
print("mean(X):",meanX," mean(Y):",meanY)

#calculate A,B to get linear regression equation(predictY=B(X-meanX)+meanY)
B=(sumXY-(sumX*sumY)/numTrain)/(sumXpow-(sumX**2)/numTrain)
A=meanY-meanX*B#a=-b*mean(x)+mean(y)

#print regression equation, test case output
testOutput=B*testD['Distance']+A#y=bx+a
print("Regression Equation: Y=",B,"X+",A)
print("Test Set-------------------------------------")
print(pd.DataFrame({'Distance':testD['Distance'],
                    'Real Time':testD['Delivery Time'],
                    'Regression Output':testOutput}))

#Calculating Sum of Squares of Regression
regressionOutput=B*trainingD['Distance']+A
SSE=sum((regressionOutput-trainingD['Delivery Time'])**2)
print("Sum of Squares of Error is ",SSE)
SSR=sum((regressionOutput-meanY)**2)
print("Sum of Squares of Regression is ",SSR)
SST=sum((trainingD['Delivery Time']-meanY)**2)
print("Total Sum of Squares is ",SST)#SST=SSR+SSE: result is same as below
#print("Total Sum of Squares is ",SSR+SSE)


#print scatter plot: 24 training set(blue), 6 test set(red)
plt.scatter(trainingD['Distance'],trainingD['Delivery Time'],color='blue')
plt.scatter(testD['Distance'],testOutput,color='red')#Y factor is predicted by linear regression
plt.xlabel('Distance')
plt.ylabel('Delivery Time')
plt.title('Linear Regression: test(red),training(blue)')
plt.show()
