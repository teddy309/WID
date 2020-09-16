#_*_coding:utf-8_*_
import numpy as np
import pandas as pd
import os
import math
import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
#print(sys.stdin.encoding) #cp949



def findF1score(table):
    ConfusionMatrix=np.zeros((2,2))#index:0=False,1=True
    for i in range(len(table)):
        if table.loc[i,'answer']==0:
            if table.loc[i,'prediction']==0:#TN
                ConfusionMatrix[0][0]=ConfusionMatrix[0][0]+1
            if table.loc[i,'prediction']==1:#FP
                ConfusionMatrix[0][1]=ConfusionMatrix[0][1]+1
        if table.loc[i,'answer']==1:
            if table.loc[i,'prediction']==0:#FN
                ConfusionMatrix[1][0]=ConfusionMatrix[1][0]+1
            if table.loc[i,'prediction']==1:#TP
                ConfusionMatrix[1][1]=ConfusionMatrix[1][1]+1
    TP=ConfusionMatrix[1][1]
    FN=ConfusionMatrix[1][0]
    FP=ConfusionMatrix[0][1]
    TN=ConfusionMatrix[0][0]
    
    accuracy=(TP+TN)/1000
    precision=TP/(TP+FP)
    recall=TP/(TP+FN)
    F1score=2*precision*recall/(precision+recall)
    print('F1-score: ',F1score,', accuracy: ',accuracy)
    print('precision: ',precision,', recall: ',recall)
    return F1score

'''
write TF-IDF values on files with tab
'''
def make_output_file(output, TFIDF): ## write 10000 features(TFIDF) on each file path(output)
    f=open(output,'w',encoding='utf-8')   #open file
    f.write(str(TFIDF).replace(' ','\t'))   #write TFIDF result on each output files
    f.close()  #close file
	
def main():
    DF=pd.DataFrame(columns=['answer','prediction'])

    answer_set = "answer.txt"   	# the result of implement #1
    file=open(answer_set,'r',encoding='UTF8')
    index=0
    while True:
        line=file.readline()
        if not line:
            break
        DF.loc[index,'answer']=int(line)
        index=index+1
    print('lenAnswer: ',index)

    result_set = "result.txt"   	# the result of implement #1
    file=open(result_set,'r',encoding='UTF8')
    index=0
    while True:
        line=file.readline()
        if not line:
            break
        line=line.split('\t')
        line[0]=float(line[0])
        line[1]=float(line[1].strip('\n'))
        maxIndex=line.index(max(line))
        if maxIndex==1:#Positive
            DF.loc[index,'prediction']=1
        elif maxIndex==0:#Negative
            DF.loc[index,'prediction']=0
        else:
            print(DF.loc[index,'PoS'],' ',line)
        index=index+1
    print('lenResult: ',index)
    print(DF)

    findF1score(DF)
        
if __name__ == "__main__":
    main()
