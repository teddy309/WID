import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#from sklearn import preprocessing
#from sklearn.preprocessing import MinMaxScaler
#from sklearn.preprocessing import LabelEncoder
#from sklearn.preprocessing import StandardScaler
#from sklearn.preprocessing import normalize
#from sklearn.decomposition import PCA

from sklearn.model_selection import cross_val_score#
from sklearn.metrics import accuracy_score

import seaborn as sns
import os,sys
import math,random
from ctypes import * #for unsigned int32
import warnings

warnings.filterwarnings(action='ignore')
np.set_printoptions(threshold=sys.maxsize)

##function: to plot Yes/No histogram in one plot, distribute categorical values into continuous xrange to each features.
##input: X:list, vals: np.Series, width: float
##output: plotting frame
def subcategorybar(X, vals, width=0.8):
    n = len(vals)
    _X = np.arange(len(X))
    for i in range(n):
        plt.bar(_X - width/2. + i/float(n)*width, vals[i], 
                width=width/float(n), align="edge")   
    plt.xticks(_X, X)
##function: plot categorical features
##input: col(string)
##output: subcategorybar() result
def plotColNY_categorical(DF,col):
    selectCol=DF[[col,'y']]
    indexList=list(set(DF[col].values))
    
    numCol=pd.DataFrame({col:indexList},columns=[col,'countY','countN','nyRatio'])
    
    for i in range(len(numCol)):
        countI_yesno=selectCol.loc[selectCol[col]==numCol.iloc[i][col]]['y'].value_counts()
        if 'yes' in countI_yesno:
            numCol.loc[i,'countY']=countI_yesno['yes']
        else:
            numCol.loc[i,'countY']=0
        if 'no' in countI_yesno:
            numCol.loc[i,'countN']=countI_yesno['no']
        else:
            numCol.loc[i,'countN']=0
        numCol.loc[i,'nyRatio']=float(numCol.loc[i,'countY']/(numCol.loc[i,'countY']+numCol.loc[i,'countN']))
    pd.set_option('display.max_rows',numCol.shape[0]+1)#elaborate dataframe numCol
    print(numCol)
    print('average nyRatio: ',np.mean(numCol['nyRatio'].values))
    
    plt.title(" bank.csv(feature:{0}), [orange:no, blue:yes]".format(col))
    plt.xlabel(col)
    #plt.xticks(rotation=90) #used for xticks name rotation
    plt.ylabel('frequency')
    X=numCol[col]
    subcategorybar(X,[numCol['countY'],numCol['countN']])
    plt.show()
##function: plot numeric features
##input: col(string)
##output: plotting frame
def plotColNY(DF,col):
    selectCol=DF[[col,'y']]
    indexList=list(set(DF[col].values))

    numCol=pd.DataFrame({col:indexList},columns=[col,'countY','countN','nyRatio'])
    for i in range(len(numCol)):
        countI_yesno=selectCol.loc[selectCol[col]==numCol.iloc[i][col]]['y'].value_counts()
        if 'yes' in countI_yesno:
            numCol.loc[i,'countY']=countI_yesno['yes']
        else:
            numCol.loc[i,'countY']=0
        if 'no' in countI_yesno:
            numCol.loc[i,'countN']=countI_yesno['no']
        else:
            numCol.loc[i,'countN']=0
        numCol.loc[i,'nyRatio']=float(numCol.loc[i,'countY']/(numCol.loc[i,'countY']+numCol.loc[i,'countN']))
    pd.set_option('display.max_rows',numCol.shape[0]+1)#elaborate dataframe numCol
    print(numCol)
    print('average nyRatio: ',np.mean(numCol['nyRatio'].values))
    
    plt.title(" bank.csv(feature:{0}), [red:yes, blue:no]".format(col))
    plt.xlabel(col)
    plt.xticks(rotation=90)#xticks name rotation
    plt.ylabel('frequency')
    X=numCol[col]
    plt.bar(X-0.25,numCol['countY'],width=0.25,color='r')
    plt.bar(X+0.25,numCol['countN'],width=0.25,color='b')
    plt.show()
##function: 
##input:
##output:
def plotXY(col):
    ##categorical/binary feature
    count=pd.Series(readDt[col].value_counts())
    countIndex=list(count.index.values.tolist())
    plt.title("distribution of bank.csv(feature:{0})".format(count.name))
    plt.xlabel(count.name)
    plt.xticks(rotation=90)#xticks name rotation
    plt.ylabel('frequency')
    plt.bar(countIndex,count)
    for x,y in zip(countIndex,count):
        plt.text(x,y,str(y))
    plt.show()
    ##numeric feature
##function: plot by each features
##input: DF(dataframe), boolNum(boolean):whether plot numeric features, boolCat(boolean):whether plot categorical features
##output: plotting frames(8 plots for numeric, 8 plots for categorical features)
def plotByColumns(DF,boolNum,boolCat):
    columns=list(DF.columns)
    numericColIndex=[0,5,9,10,11,12,13,14]
    categoricalColIndex=[1,2,3,4,6,7,8,15]
    binaryColIndex=[]
    if boolNum is True:
        for i in numericColIndex:
            print('feature[{}]: {}'.format(i,columns[i]))
            plotColNY(DF,str(columns[i]))
    if boolCat is True:
        for i in categoricalColIndex:
            print('feature[{}]: {}'.format(i,columns[i]))
            plotColNY_categorical(DF,str(columns[i]))


##function: run Decision Tree Classifier
##input: K_fold(int), critIndex(int:0~1):index to select hyper-parameter
##output: mean score of DT classifier(float)
def runDecisionTree(K_fold,critIndex,X_train,X_test,y_train,y_test):
    score=np.empty([K_fold]) #10-folds
    predY=[pd.Series([]) for i in range(K_fold)]
    ##Model's Parameters:stored in an array##
    pCriterion=['gini','entropy']
    ##Algorithm 1: Decision Tree
    from sklearn.tree import DecisionTreeClassifier
    clf_DT=DecisionTreeClassifier(random_state=0,criterion=pCriterion[critIndex])#Parameters:criterion(gini,entropy)
    for i in range(K_fold):
        clf_DT.fit(X_train[i],y_train[i])
        predY[i]=clf_DT.predict(X_test[i])
        score[i]=clf_DT.score(X_test[i],y_test[i]).astype('float64')
    return np.mean(score)
##function: run Logistic Regression
##input: K_fold(int), critIndex(int:0~2),critIndex(int:0~2):index to select hyper-parameter
##output: mean score of Logistic Regression(float)
def runLogisticRegression(K_fold,solverIndex,iterIndex,X_train,X_test,y_train,y_test):
    score=np.empty([K_fold]) #10-folds
    predY=[pd.Series([]) for i in range(K_fold)]
    ##Algorithm 2: Logistic Regression
    from sklearn.linear_model import LogisticRegression
    ##Model's Parameters:stored in an array##
    pSolver=['liblinear','lbfgs','sag']
    pMax_iter=[50,100,200]
    logisticRegr=LogisticRegression(solver=pSolver[solverIndex],max_iter=pMax_iter[iterIndex])#Parameters:solver(liblinear,lbfgs,sag),max_iter(50,100,200)
    for i in range(K_fold):
        logisticRegr.fit(X_train[i],y_train[i])
        predY[i]=logisticRegr.predict(X_test[i])
        score[i]=logisticRegr.score(X_test[i],y_test[i]).astype('float64')
    return np.mean(score)
##function: run Support Vector Machine
##input: K_fold(int), kernelIndex(int:0~2),gammaIndex(int:0~2),cIndex(int:0~2):index to select hyper-parameter
##output: mean score of SVM(float)
def runSVM(K_fold,kernelIndex,gammaIndex,cIndex,X_train,X_test,y_train,y_test):
    score=np.empty([K_fold]) #10-folds
    predY=[pd.Series([]) for i in range(K_fold)]
    ##Algorithm 3: SVM
    from sklearn.svm import SVC
    ##Model's Parameters:stored in an array##
    pCvalues=[0.1,1.0,10.0]
    pKernel=['linear','poly','rbf','sigmoid']
    pGamma=['auto',10,100]
    clf_SVC=SVC(C=pCvalues[cIndex],kernel=pKernel[kernelIndex],gamma=pGamma[gammaIndex],degree=3,tol=0.001)#Parameters:C(0.1,1.0,10.0),kernel(linear,poly,rbf,sigmoid),gamma(0,10,100)
    for i in range(K_fold):
        clf_SVC.fit(X_train[i],y_train[i])
        predY[i]=clf_SVC.predict(X_test[i])
        score[i]=clf_SVC.score(X_test[i],y_test[i]).astype('float64')
    return np.mean(score)
    

##function: do SVM for return prediction of algorithm
##input: K_fold(int), kernelIndex(int:0~2),gammaIndex(int:0~2),cIndex(int:0~2):index to select hyper-parameter
##output: predY(list):prediction of SVM algorithm
def doSVM(K_fold,kernelIndex,gammaIndex,cIndex,X_train,X_test,y_train,y_test):
    score=np.empty([K_fold]) #10-folds
    pred=np.empty([K_fold]) #10-folds
    predY=[pd.Series([]) for i in range(K_fold)]
    ##Algorithm 3: SVM
    from sklearn.svm import SVC
    ##Model's Parameters:stored in an array##
    pCvalues=[0.1,1.0,10.0]
    pKernel=['linear','poly','rbf','sigmoid']
    pGamma=['auto',10,100]
    clf_SVC=SVC(C=pCvalues[cIndex],kernel=pKernel[kernelIndex],gamma=pGamma[gammaIndex],degree=3,tol=0.001)#Parameters:C(0.1,1.0,10.0),kernel(linear,poly,rbf,sigmoid),gamma(0,10,100)
    for i in range(K_fold):
        clf_SVC.fit(X_train[i],y_train[i])
        predY[i]=clf_SVC.predict(X_test[i])
        score[i]=clf_SVC.score(X_test[i],y_test[i]).astype('float64')
    return predY
##function: split 'bank.csv' to 'bank_preprocessed.csv'
##input: none
##output: none
def csvSplit():
    ##read Dataset'bank.csv' & store to 'bank_preprocessed.csv'##
    #read&split dataset: 'bank.csv'
    readDt=pd.read_csv(os.getcwd()+'\\bank.csv',encoding = "ISO-8859-1",sep=';')
    print(readDt)
    readDt.to_csv(os.getcwd()+'\\bank_preprocessed.csv',index=False)
##function: LabelEncoding DF dataframe for categorical features into numeric features
##input: DF(dataframe)
##output: encodedDF(labelEncoded DF)
def labelEncoding(DF):
    from sklearn.preprocessing import LabelEncoder
    encodedDF=DF
    columns=list(DF.columns)
    categoricalColIndex=[1,2,3,4,6,7,8,15]
    for i in categoricalColIndex:
        encodedDF[columns[i]]=LabelEncoder().fit_transform(encodedDF[columns[i]])
    return encodedDF

def main():
    ##read&plot dataset: 'bank_preprocessed.csv'
    #csvSplit() #do it before run this main() function
    readDt=pd.read_csv(os.getcwd()+'\\bank_preprocessed.csv')

    ##Feature Engineering: month(str2int),balance(devide by 50)
    #feature discretization: binning correlated features&change 'month'(categorical->numeric)
    import calendar
    for i in range(len(readDt['age'].values)):
        readDt.loc[i,'month']=int(list(calendar.month_abbr).index(str(readDt.loc[i,'month']).capitalize()))
        readDt.loc[i,'balance']=int(readDt.loc[i,'balance']/50)
        readDt.loc[i,'duration']=int(readDt.loc[i,'duration']/100)
        readDt.loc[i,'duration']=int(readDt.loc[i,'pdays']/7)
    #print(readDt)#print binned data

    ##plotting categorical/binary/numeric featurescolumns=list(readDt.columns)
    plotByColumns(readDt,True,True) #plotNumeric features? no, plotCategorical features? no
    
    ##Train/Test datasets
    encodedDF=labelEncoding(readDt)
    
    X=encodedDF.drop(columns=['y'])  #drop continuous
    y=encodedDF['y'].values
    ##Test/Train Split: split into 10-Folds##
    K_fold=10 #K-size
    from sklearn.model_selection import train_test_split
    X_train=[pd.DataFrame(columns=X.columns) for i in range(K_fold)]
    X_test=[pd.DataFrame(columns=X.columns) for i in range(K_fold)]
    y_train=[pd.Series([]) for i in range(K_fold)]
    y_test=[pd.Series([]) for i in range(K_fold)]
    for i in range(K_fold):#
        trainX,testX,trainY,testY=train_test_split(X,y,test_size=0.2,random_state=None,stratify=y)
        X_train[i]=trainX
        X_test[i]=testX
        y_train[i]=trainY
        y_test[i]=testY
    ##print Algorithm accuracy score: DecisionTree, LogisticRegression, SVM
    print('DT_scores average:{}'.format(runDecisionTree(K_fold,1,X_train,X_test,y_train,y_test)))
    print('LR_scores average:{}'.format(runLogisticRegression(K_fold,2,0,X_train,X_test,y_train,y_test)))
    print('SVM_scores average:{}'.format(runSVM(K_fold,3,1,1,X_train,X_test,y_train,y_test)))

    ##Plot confusion matrix
    predY=doSVM(K_fold,3,1,1,X_train,X_test,y_train,y_test)
    nfold=1
    #confusion_matrix=pd.crosstab(y[bestIndexDT],predY[bestIndexDT],rownames=['Actual'],colnames=['Predicted'],margins=True)
    confusion_matrix=pd.crosstab(y_test[nfold][0:500],predY[nfold][0:500],rownames=['Actual'],colnames=['Predicted'],margins=False)
    sns.heatmap(confusion_matrix,annot=True,fmt='d')
    plt.title("ConfusionMatrix(model:{})".format('SVM'))
    plt.show()


if __name__ == "__main__":
    main()
