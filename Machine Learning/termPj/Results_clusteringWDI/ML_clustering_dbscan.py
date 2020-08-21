import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pprint import PrettyPrinter as pp

from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score

#from sklearn.preprocessing import LabelEncoder
#from sklearn.preprocessing import OneHotEncoder
#from sklearn.preprocessing import MinMaxScaler
#from sklearn.preprocessing import StandardScaler
#from sklearn.preprocessing import MaxAbsScaler
#from sklearn.preprocessing import RobustScaler

from sklearn.cluster import KMeans
import os,sys
import math,random
from ctypes import * #for unsigned int32
import warnings

warnings.filterwarnings(action='ignore')
np.set_printoptions(threshold=sys.maxsize)


def findHyperParams(cluster):
    count=0
    for i in range(len(target)):
        if target[i]==num:
            count=count+1

def DBScan(dataset):
    from sklearn.preprocessing import LabelEncoder
    from sklearn.preprocessing import MinMaxScaler
    #from sklearn.preprocessing import RobustScaler
    from sklearn.cluster import DBSCAN
    
    kor = dataset[dataset["Country Code"].isin(["KOR"])]#row of "KOR"(dataframe)
    koreaIndex=kor.index.values.astype(int)[0] #index of row(int)
    #print('koreaIndex: ',koreaIndex) #int
    #print('koreaRowCountry:',dataset.loc[koreaIndex,"Country Code"]) #Country Code
    numDatasets=len(dataset)

    enc=LabelEncoder()
    for col in dataset.columns:
        dataset[col]=dataset[col].fillna(0)
        if col=='Country Code' or col=='Indicator Code':
            #dataset[i][col]=enc.fit_transform(dataset[i][col]) #OK
            if col=='Country Code':
                #print('[{}]dropped'.format(col))#
                dataset=dataset.drop(columns=[col])
            elif col=='Indicator Code':
                #print('[{}]dropped'.format(col))#
                dataset=dataset.drop(columns=[col])

    ##minmax scaling
    scaler=MinMaxScaler(copy=True, feature_range=(0,1))#RobustScaler()
    dataset_normalized=scaler.fit_transform(dataset)
    print('OK1')
    print(type(dataset_normalized))
    print(dataset_normalized)
    #EPS_population=[1.0,0.7,0.5,0.45,0.4,0.35,0.3,0.1,0.05,0.02,0.01,0.005]
    #EPS_economy=[1.0,0.7,0.65,0.6,0.55,0.5,0.45,0.4,0.35,0.3,0.1,0.05,0.02,0.01,0.005,0.001]
    EPS=[1.0,0.7,0.65,0.6,0.55,0.5,0.45,0.4,0.35,0.3,0.1,0.05,0.02,0.01,0.005,0.001]
    MS=range(2,10)
    for MSi in MS:
        for EPi in EPS:
            DBscan=DBSCAN(eps=EPi,min_samples=MSi)
            cluster_dbscan=DBscan.fit_predict(dataset_normalized)
            koreaClusterNum=cluster_dbscan[koreaIndex]
            if list(cluster_dbscan).count(koreaClusterNum)<10: #korea cluster has under 10 nations
                clusterList=[]
                for i in range(len(cluster_dbscan)):
                    if cluster_dbscan[i]==koreaClusterNum:
                        clusterList.append(i)
                print('EPS:',EPi,'MS:',MSi)
                print('Korea index:',koreaIndex)
                print('cluster of KoreaS indices:',clusterList)
                print(type(clusterList))
                return cluster_dbscan
    print('HyperParameter cannot Found!!!!')
    DBscan=DBSCAN(eps=0.5,min_samples=10)
    return cluster_dbscan=DBscan.fit_predict(dataset_normalized)


def Preprocessing(indi_codeSet,dataset):
    resultDF=pd.DataFrame()
    if len(indi_codeSet)==3: #3 indicators
        return Preprocessing_type3(indi_codeSet[0],indi_codeSet[1],indi_codeSet[2],dataset)
    elif len(indi_codeSet)==2: #2 indicators
        return Preprocessing_type2(indi_codeSet[0],indi_codeSet[1],dataset)
    else: #1 indicators
        return Preprocessing_type1(indi_codeSet,dataset)

    
def Preprocessing_type1(indi_code, dataset):
    new_df = dataset
    new_df = new_df[new_df["Indicator Code"].isin([indi_code])]
    #set_avg_1960
    #mean_list = []
    mean_60 = []
    mean_70 = []
    mean_80 = []
    mean_90 = []
    mean_00 = []
    mean_10 = []
    tmp = []
    for i in new_df.index:
        tmp = list(new_df.loc[i])
        mean_60.append(np.mean(tmp[4:14]))   # 60~69
        mean_70.append(np.mean(tmp[14:24]))  # 70~79
        mean_80.append(np.mean(tmp[24:34]))  # 80~89
        mean_90.append(np.mean(tmp[34:44]))  # 90~99
        mean_00.append(np.mean(tmp[44:54]))  # 00~09
        mean_10.append(np.mean(tmp[54:63]))  # 10~18

    targer_df = new_df[['Country Code','Indicator Code']]
    targer_df['1960s'] = mean_60
    targer_df['1970s'] =mean_70
    targer_df['1980s'] =mean_80
    targer_df['1990s'] =mean_90
    targer_df['2000s'] =mean_00
    targer_df['2010s'] =mean_10
    targer_df = targer_df.reset_index()

    return targer_df

def Preprocessing_type2(indi_code1,indi_code2, dataset): #return Preprocessing(code1/code2)
    df = dataset    
    new_df1=df[df["Indicator Code"].isin([indi_code1])]
    new_df2 = df[df["Indicator Code"].isin([indi_code2])]
    indexFrom=np.where(new_df1.columns=="1960")[0][0]
    indexTo=np.where(new_df1.columns=="2019")[0][0]
    values1=new_df1.iloc[:,indexFrom:indexTo]
    values2=new_df2.iloc[:,indexFrom:indexTo]

    index1=list(values1.index)
    index2=list(values2.index)
    new_df=new_df1
    new_df.reset_index()
    
    for i in range(len(new_df)):
        new_df.loc[index1[i],"Indicator Code"] = indi_code1+'/'+indi_code2
        for col in values1.columns:# for i in range(len(new_df))
            val1=values1.loc[index1[i],col]
            val2=values2.loc[index2[i],col]
            new_df.loc[index1[i],col] = val1/val2

    mean_60 = []
    mean_70 = []
    mean_80 = []
    mean_90 = []
    mean_00 = []
    mean_10 = []
    for i in new_df.index:
        tmp = list(new_df.loc[i])
        mean_60.append(np.mean(tmp[4:14]))   # 60~69
        mean_70.append(np.mean(tmp[14:24]))  # 70~79
        mean_80.append(np.mean(tmp[24:34]))  # 80~89
        mean_90.append(np.mean(tmp[34:44]))  # 90~99
        mean_00.append(np.mean(tmp[44:54]))  # 00~09
        mean_10.append(np.mean(tmp[54:63]))  # 10~18

    targer_df = new_df[['Country Code','Indicator Code']]
    targer_df['1960s'] = mean_60
    targer_df['1970s'] =mean_70
    targer_df['1980s'] =mean_80
    targer_df['1990s'] =mean_90
    targer_df['2000s'] =mean_00
    targer_df['2010s'] =mean_10
    targer_df = targer_df.reset_index()
    return targer_df

def Preprocessing_type3(indi_code1,indi_code2, indi_code3, dataset): #return Preprocessing(code1/(code2+code3)
    df = dataset    
    new_df1=df[df["Indicator Code"].isin([indi_code1])]
    new_df2 = df[df["Indicator Code"].isin([indi_code2])]
    new_df3 = df[df["Indicator Code"].isin([indi_code3])]
    indexFrom=np.where(new_df1.columns=="1960")[0][0]
    indexTo=np.where(new_df1.columns=="2019")[0][0]
    values1=new_df1.iloc[:,indexFrom:indexTo]
    values2=new_df2.iloc[:,indexFrom:indexTo]
    values3=new_df3.iloc[:,indexFrom:indexTo]

    index1=list(values1.index)
    index2=list(values2.index)
    index3=list(values3.index)
    new_df=new_df1
    new_df.reset_index()
    
    for i in range(len(new_df)):
        new_df.loc[index1[i],"Indicator Code"] = indi_code1+'/'+indi_code2+'/'+indi_code3
        for col in values1.columns:# for i in range(len(new_df))
            val1=values1.loc[index1[i],col]
            val2=values2.loc[index2[i],col]
            val3=values3.loc[index3[i],col]
            new_df.loc[index1[i],col] = val1/(val2+val3)

    mean_60 = []
    mean_70 = []
    mean_80 = []
    mean_90 = []
    mean_00 = []
    mean_10 = []
    for i in new_df.index:
        tmp = list(new_df.loc[i])
        mean_60.append(np.mean(tmp[4:14]))   # 60~69
        mean_70.append(np.mean(tmp[14:24]))  # 70~79
        mean_80.append(np.mean(tmp[24:34]))  # 80~89
        mean_90.append(np.mean(tmp[34:44]))  # 90~99
        mean_00.append(np.mean(tmp[44:54]))  # 00~09
        mean_10.append(np.mean(tmp[54:63]))  # 10~18

    targer_df = new_df[['Country Code','Indicator Code']]
    targer_df['1960s'] = mean_60
    targer_df['1970s'] =mean_70
    targer_df['1980s'] =mean_80
    targer_df['1990s'] =mean_90
    targer_df['2000s'] =mean_00
    targer_df['2010s'] =mean_10
    targer_df = targer_df.reset_index()
    return targer_df

def sepIndicatorCode(indicCode):
    indicCode_split=[] #[industry,measureUnit,code]*numIndicators
    for i in range(len(indicCode)):
        split=indicCode.loc[i,].split('.')
        industry=split[0]
        measureUnit=split[len(split)-1]
        code=''
        for i in range(1,len(split)-1):
            code=code+split[i]+'.'
        code=code.strip('.')
        indicCode_split.append([industry,measureUnit,code])
    return indicCode_split #list

def make_output_file(output,DF): ## write 10000 features(TFIDF) on each file path(output)
    f=open(output,'w',encoding='utf-8')   #open file
    #pd.set_option('display.max_columns')
    f.write(str(DF))#.replace(' ','\t'))   #write TFIDF result on each output files
    f.close()  #close file

##read&plot dataset: 'Series.csv'
readDt=pd.read_csv(os.getcwd()+'\\Indicators_bindWithYear.csv')
seriesCode=readDt['Indicator Code']

#toCSVDF=readDt
#toCSVDF['industryCode']=pd.Series([seriesCode_split[col][0] for col in range(len(seriesCode_split))])
#toCSVDF['measureUnit']=pd.Series([seriesCode_split[col][2] for col in range(len(seriesCode_split))])
#toCSVDF['code']=pd.Series([seriesCode_split[col][1] for col in range(len(seriesCode_split))])
#print(toCSVDF)
#toCSVDF.to_csv(os.getcwd()+'\\Indicators_split.csv',index=False) #to csv file




#Economic/Financial:all 1960~2018
economy_code=['DC.DAC.TOTL.CD','FM.AST.DOMS.CN','NV.IND.MANF.ZS','BX.KLT.DINV.WD.GD.ZS']
#Infrastructure/Trade: 1960~:index0,1, 1980~:index2,3, 2000~:index4
infra_code=[['TX.VAL.FUEL.ZS.UN','TM.VAL.FUEL.ZS.UN'],['TX.VAL.MANF.ZS.UN','TM.VAL.MANF.ZS.UN'],'IS.AIR.PSGR','IT.CEL.SETS.P2','IT.NET.USER.ZS',]
#Agriculture/Environment/Health: 1960~:index0~3
env_code=['AG.LND.AGRI.ZS','AG.PRD.LVSK.XD','EN.ATM.CO2E.KT','EN.POP.DNST']
#Welfare/Labor/Population: 1960~:index0~2 ,1980~:index3~5 ,2000~: index6
wlfr_code=['SE.SEC.CUAT.LO.ZS','SH.DTH.IMRT','SL.UEM.TOTL.NE.ZS','SH.IMM.IDPT','SL.AGR.EMPL.ZS','SL.GDP.PCAP.EM.KD','SH.XPD.CHEX.PC.CD']
#Population: 1960~:index0~3
popu_code=['SP.POP.TOTL',['SP.POP.TOTL.FE.IN','SP.POP.TOTL.MA.IN'],['SP.POP.1564.TO','SP.POP.0014.TO','SP.POP.65UP.TO'],['SP.URB.TOTL.IN.ZS','SP.RUR.TOTL.ZS']]

dataset_economy=[]
for i in range(len(economy_code)):
    dataset_economy.append(Preprocessing(economy_code[i],readDt))
dataset_infra=[]
for i in range(len(infra_code)):
    dataset_infra.append(Preprocessing(infra_code[i],readDt))
dataset_environment=[]
for i in range(len(env_code)):
    dataset_environment.append(Preprocessing(env_code[i],readDt))
dataset_welfare=[]
for i in range(len(wlfr_code)):
    dataset_welfare.append(Preprocessing(wlfr_code[i],readDt))
dataset_population=[]
for i in range(len(popu_code)):
    dataset_population.append(Preprocessing(popu_code[i],readDt))

#popu_code[2]: 3 indicators
target2=Preprocessing_type3(popu_code[2][0],popu_code[2][1],popu_code[2][2],readDt)
#print(target2)

#infra_code[0,1],popu_code[1,3]: 2 indicators
target1=Preprocessing_type2(infra_code[0][0],infra_code[0][1],readDt)
#print(target1)

#else: 1 indiators
indi_code = "NY.GDP.MKTP.KD.ZG"
target_dataset = Preprocessing_type1(indi_code, readDt)
#print(target_dataset)

#indexKor_population=[]
for i in range(len(dataset_population)):
    #print(dataset_population[i].columns)
    print('population dataset:',i)#
    print(dataset_population[i])

    #datasetI=dataset_population[i]
    #kor=datasetI[datasetI["Country Code"].isin(["KOR"])] #row of "KOR"(dataframe)
    #index=kor.index.values.astype(int)[0] #index of row(int)
    #indexKor_population.append(index)
    

dataset_population[0]=dataset_population[0].drop(columns=['index'])
#print(dataset_population[3])
#print(dataset_population[0].columns)
'''
# dataset_economy 4   dataset_infra
dataset=dataset_economy
for i in range(len(dataset)):
    cluster_DBSCAN=DBScan(dataset[i])
    print('economy',i,'OK')
dataset=dataset_economy
for i in range(len(dataset)):
    cluster_DBSCAN=DBScan(dataset[i])
    print('economy',i,'OK')
dataset=dataset_economy
for i in range(len(dataset)):
    cluster_DBSCAN=DBScan(dataset[i])
    print('economy',i,'OK')
dataset=dataset_economy
for i in range(len(dataset)):
    cluster_DBSCAN=DBScan(dataset[i])
    print('economy',i,'OK')
'''
targetFactorSet=dataset_economy
print('[Population Factors]')
stddevDF=pd.DataFrame()
for i in range(len(targetFactorSet)):
    columnName=str(i)+"th"#+str(targetFactorSet[i].loc[0,"Indicator Code"])
    stddevDF[columnName]=targetFactorSet[i].std(axis=0)
print('Stddev:')
print(stddevDF)
make_output_file("stddevPopulation.txt",stddevDF)
for i in range(len(targetFactorSet)):
    print('Indicator {}th[{}] cluster result:'.format(i,targetFactorSet[i].loc[0,"Indicator Code"]))
    cluster_DBSCAN=DBScan(targetFactorSet[i])
    print(cluster_DBSCAN)
#print('len column:',len(dataset_population[0]))
#print(len(cluster_DBSCAN))

#cluster, kor_index = k_Means(Preprocessing_type1("NY.GDP.MKTP.KD.ZG", readDt))
#print(cluster, kor_index)
