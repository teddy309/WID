import numpy as np
import pandas as pd
from sklearn import linear_model
import matplotlib.pyplot as plt
from sklearn import preprocessing
import os

#read Excel File
readDt=pd.read_excel(os.getcwd()+'\\DS-lab-3-dataset.xlsx','Dataset',index_col=None)

Df=readDt.iloc[:,0:3]#get 'Gender','Height','Weight' columns
#select by columns and put Gender,Height,Weight column into dG,lX,lY
dG=np.array(Df['Gender'])
lX=np.array(Df['Height']).tolist()
lY=np.array(Df['Weight']).tolist()
BMI=np.array([])
#get only female datas into dX,dY from lX,lY
dX=np.array([])
dY=np.array([])
for i in range(len(dG)):
    if dG[i]=="Female":#if 'Gender' column is 'Female', append to array dX,dY
        dX=np.append(dX,lX[i])
        dY=np.append(dY,lY[i])

#with linear regression E study from (dX,dY), predict pY with dX
linRegE=linear_model.LinearRegression()
linRegE.fit(dX[:,np.newaxis],dY)
py=linRegE.predict(dX[:,np.newaxis])#py=w'
#make e array and standardize to e_zscore
e=np.array(dY)-np.array(py)#e=w-w'
e_zscore=preprocessing.scale(e)

#alpha=np.mean(e_zscore)+1.5*np.std(e_zscore)

#set alpha to 1.5 and set BMI 0 or 5 which surpass alpha
alpha=1.5#set alpha 1.5
for i in range(len(e_zscore)):
    if e_zscore[i]<(-alpha):
        BMI=np.append(BMI,0)#set underfitting outlier to 0
    elif alpha<e_zscore[i]:
        BMI=np.append(BMI,5)#set overfitting outlier to 5
    else:
        BMI=np.append(BMI,3)#set normal persons 3
resultDF=pd.DataFrame({'Height':np.array(dX,dtype='float32'),
                       'Weight':np.array(dY,dtype='float32'),
                       'BMI':np.array(BMI,dtype='int32')})
print(resultDF)

#devide into 9 bins and show histogram
bin=np.linspace(e_zscore.min(),e_zscore.max(),10) #9bins
plt.hist(e_zscore,bins=bin)
plt.xticks(bin)#mark x ticks with bins
plt.title("histogram of z-scores of female")
plt.xlabel('z_scores')
plt.ylabel('Frequency')
plt.show()
