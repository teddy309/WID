import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix
import os
import warnings
warnings.filterwarnings(action='ignore')

#read original iris.csv data into iris
iris=pd.read_csv(os.getcwd()+'\\Iris.csv',encoding='utf-8')
labels=iris['Species']

#read 10 bagging datasets into samples list
samples=[]
sample=pd.read_csv("Iris_bagging_datasets/Iris_bagging_dataset (1).csv")
samples.append(sample)
sample=pd.read_csv("Iris_bagging_datasets/Iris_bagging_dataset (2).csv")
samples.append(sample)
sample=pd.read_csv("Iris_bagging_datasets/Iris_bagging_dataset (3).csv")
samples.append(sample)
sample=pd.read_csv("Iris_bagging_datasets/Iris_bagging_dataset (4).csv")
samples.append(sample)
sample=pd.read_csv("Iris_bagging_datasets/Iris_bagging_dataset (5).csv")
samples.append(sample)
sample=pd.read_csv("Iris_bagging_datasets/Iris_bagging_dataset (6).csv")
samples.append(sample)
sample=pd.read_csv("Iris_bagging_datasets/Iris_bagging_dataset (7).csv")
samples.append(sample)
sample=pd.read_csv("Iris_bagging_datasets/Iris_bagging_dataset (8).csv")
samples.append(sample)
sample=pd.read_csv("Iris_bagging_datasets/Iris_bagging_dataset (9).csv")
samples.append(sample)
sample=pd.read_csv("Iris_bagging_datasets/Iris_bagging_dataset (10).csv")
samples.append(sample)


#make majority voting from each prediction cases at index
#return elected result in String
def vote(index):
    count={'Iris-setosa':0,'Iris-versicolor':0,'Iris-virginica':0}
    for i in range(len(irisPrediction)):
        for x in count:
            if(irisPrediction[i][index]==x):
                count[x]=count[x]+1
    if max(count['Iris-setosa'],count['Iris-versicolor'],count['Iris-virginica'])==count['Iris-setosa']:
        return "Iris-setosa"
    elif max(count['Iris-setosa'],count['Iris-versicolor'],count['Iris-virginica'])==count['Iris-versicolor']:
        return "Iris-versicolor"
    elif max(count['Iris-setosa'],count['Iris-versicolor'],count['Iris-virginica'])==count['Iris-virginica']:
        return "Iris-virginica"
         


#make 10 decision trees with samples
tree_clf = DecisionTreeClassifier(criterion="entropy",random_state=42)
tree_clf.fit(iris.drop('Species',axis=1), iris['Species'])
tree_clf=[]
for i in range(len(samples)):
    tree_clf.append(DecisionTreeClassifier(criterion="entropy",random_state=42))
    tree_clf[i].fit(samples[i].drop('Species',axis=1), samples[i]['Species'])
    
#predict from original iris data with each 10 decision trees
irisPrediction=[]
for i in range(len(samples)):
    irisPrediction.append(tree_clf[i].predict(iris.drop('Species',axis=1)))

#vote from each 10 samples's index i
print("[original Iris data], [predicted Iris data]")
predictionVoted=[]
for i in range(len(iris)):
    predictionVoted.append(vote(i))
    print(iris['Species'][i],predictionVoted[i])

#print confusion matrix
cm=confusion_matrix(iris['Species'],predictionVoted)
print("            Iris-setosa  Iris-versicolor  Iris-virginica")
print("Iris-setosa    ",cm[0,0],"           ",cm[0,1],"         ",cm[0,2])
print("Iris-versicolor",cm[1,0],"           ",cm[1,1],"         ",cm[2,2])
print("Iris-virginica ",cm[2,0],"           ",cm[2,1],"         ",cm[2,2])

#print precision
print("Accuracy is",100*(cm[0,0]+cm[1,1]+cm[2,2])/sum(sum(cm)),"%")
