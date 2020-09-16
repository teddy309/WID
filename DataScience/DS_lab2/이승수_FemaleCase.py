from matplotlib import pyplot as plt
import numpy as np
import math
import sys
import statistics

filepath='DS-minilab-2-dataset.csv'

heightVal=1000
weightVal=2000


#start
arr=list(np.genfromtxt(filepath,delimiter=',',dtype=str))
arr.pop(0)

for i in range(len(arr)):
    for j in range(4):
        if arr[i][j]=='':
            arr[i][j]=0 #fill empty data

femIndex=[]
for i in range(len(arr)):
    if(str(arr[i][0])=="Female"):
        femIndex.append(i)


countH=0
countW=0
for i in range(len(arr)): #mark dirty data
    if(int(arr[i][1])<140 or 200<int(arr[i][1])):
        arr[i][1]=heightVal
        countH=countH+1
    if(150<int(arr[i][2]) or int(arr[i][2])<40):
        arr[i][2]=weightVal
        countW=countW+1
        

CDheight=[]
CDweight=[]
for i in femIndex: #get clean dataset
    if(int(arr[i][1])!=heightVal and int(arr[i][2])!=weightVal):
        CDheight.append(int(arr[i][1]))
        CDweight.append(int(arr[i][2]))


#linear regression
meanCDH=sum(CDheight)/len(CDheight)
meanCDW=sum(CDweight)/len(CDweight)
up=sum((CDheight[i]-meanCDH)*(CDweight[i]-meanCDW) for i in range(len(CDheight)))
down=sum((CDheight[i]-meanCDH)**2 for i in range(len(CDheight)))
A=up/down
B=meanCDW-(meanCDH*A)


estimIndex=[]
for i in femIndex: #get outlier's indexs
    if(int(arr[i][1])==heightVal):
        estimIndex.append(i)
    if(int(arr[i][2])==weightVal):
        estimIndex.append(i)

        
estimH=[float(arr[i][1]) for i in estimIndex]
estimW=[A*estimH[i]+B for i in range(len(estimH))]

plt.scatter(CDheight,CDweight,color='b') #clean dataset
plt.scatter(estimH,estimW,color='r') #estimated dataset
plt.xlabel('height')
plt.ylabel('weight')
plt.xlim([135,210])
plt.ylim([40,160])
plt.title('Scatter plot_case:female estimation')
plt.show()
