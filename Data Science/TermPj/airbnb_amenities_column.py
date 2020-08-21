import numpy as np
import pandas as pd
from sklearn import linear_model
import matplotlib.pyplot as plt
from sklearn import preprocessing
import math,os,random
import re
import warnings
import operator

warnings.filterwarnings(action='ignore')


def trimming(strList):
    for i in range(len(strList)):
        #trim(strList[i])
        strList[i]=splitString(strList[i])
#str양끝에 특수기호가 있으면 벗겨줌
def trim(str):
    while(not(str.isalnum()) and not(splitString(str).isalnum())):
        str=str.strip()
        str=str.strip(']')
        str=str.strip('[')
        str=str.strip(':')
        str=str.strip('{')
        str=str.strip('}')
        str=str.strip('\'')
        str=str.strip('"')
        str=str.strip('_')
        str=str.strip('-')
        str=str.strip('\"')
        str=str.strip('}')
#str을에서 특수기호 기준으로 분리해줌 
def splitString(str):
    tmp=str
    tmp="".join(tmp.split())
    tmp="".join(tmp.split('/'))
    tmp="".join(tmp.split('-'))
    tmp="".join(tmp.split(':'))
    tmp="".join(tmp.split('.'))
    tmp="".join(tmp.split('_'))
    tmp="".join(tmp.split('#'))
    tmp="".join(tmp.split('"'))
    tmp="".join(tmp.split('\''))
    tmp="".join(tmp.split('{'))
    tmp="".join(tmp.split('}'))
    tmp="".join(tmp.split('['))
    tmp="".join(tmp.split(']'))
    tmp="".join(tmp.split('('))
    tmp="".join(tmp.split(')'))
    tmp="".join(tmp.split('<'))
    tmp="".join(tmp.split('>'))
    return tmp


readDt=pd.read_csv(os.getcwd()+'\\data.csv',encoding = "ISO-8859-1")
column=readDt[['id','host_id','amenities']]
testSize=250
column=column.iloc[0:testSize,:]#일단 100개 row만 받아옴
column['amenities']=column.amenities.astype('category')


 

#유니크한 amenity들의 개수 세기 
def findAmenities():
    amenitycount={colCat[0]:0}
    for i in range(len(colCat)):
        amenitycount[colCat[i]]=0
    for i in range(len(column)):
        for x in amenitycount:
            if str(column['amenities'][i]).find(x)>0:
                amenitycount[x]=amenitycount[x]+1
    return amenitycount;#return: {'amenity이름':amenity의 전체빈도수}


#dic(dictionary) 중에서 빈도수가 가장높은 n개만 뽑아서 큰순서로 리턴
def topNfromDict(dic,n):
    topN=[]
    sortedDict=sorted(dic.items(),key=operator.itemgetter(1),reverse=True)#sort by value in reverse
    for i in range(n):
        item=sortedDict[i]
        topN.append(item)
    return topN #return[('key',value)*n]array



#각 방마다 amenDic의 물건들있는지 count리스트에 표시해줌
def oneHotAmenities():
    OneHotAmenities=[]
    for i in range(len(column)):
        count=[0,0,0,0,0]
        if re.search('Wifi'or'Internet',column['amenities'].iloc[i],re.IGNORECASE):
            count[0]=count[0]+1
        if re.search('Heating',column['amenities'].iloc[i],re.IGNORECASE):
            count[1]=count[1]+1
        if re.search('essentials'or'shampoo'or'dryer',column['amenities'].iloc[i],re.IGNORECASE):
            count[2]=count[2]+1
        if re.search('kitchen',column['amenities'].iloc[i],re.IGNORECASE):
            count[3]=count[3]+1
        if re.search('elevator',column['amenities'].iloc[i],re.IGNORECASE):
            count[4]=count[4]+1
        OneHotAmenities.append(count)
    return OneHotAmenities


#amenity를 한줄로 정렬(colCat)하고 ,단위로 끊음.
colCat=column['amenities'].as_matrix().reshape(-1)
colCat=str(colCat).split(',')
#좌우의 특수기호, 중복 제거
trimming(colCat)#특수기호 제거
colCat=list(dict.fromkeys(colCat))#eliminate duplicated
amenityCount=findAmenities()
#amenity 중에 12개 뽑아서 관련된 것끼리 합침
amenSize=25
topTen=topNfromDict(amenityCount,amenSize)
amenX,amenY=[],[]
for i in range(amenSize):
    amenX.append(topTen[i][0])
    amenY.append(topTen[i][1])
#[['Wifi','Internet'],['Heating'],['essentials','shampoo','dryer'],['kitchen'],['elevator']]
#위에처럼 묶어서 대표값으로 합친걸 amenDic
'''
amenDic={'Wifi':0,'Heating':0,'Showering':0,'Kitchen':0,'Elevator':0}
amenDic['Wifi']=amenY[0]+amenY[9]#Wifi+Internet
amenDic['Heating']=amenY[1]
amenDic['Showering']=amenY[2]+amenY[7]+amenY[8]#Essentials+Shampoo+Dryer
amenDic['Kitchen']=amenY[3]
amenDic['Elevator']=amenY[10]
'''
OHamenity=oneHotAmenities()
OH=pd.DataFrame(np.array(OHamenity),columns=['Wifi','Heating','Shower','Kitchen','Elevator'])
#column=pd.concat(['Wifi':OH[0],'Heating':OH[1],'Shower':OH[2],'Kitchen':OH[3],'Elevator':OH[4]])
print(np.array(OHamenity).T)
OH.to_excel(os.getcwd()+'\\amenToExcel.xlsx',sheet_name='first')

#print(oneHotAmenities())
plt.title("amenities count(testSize:{0},amenity selected:{1})".format(testSize,amenSize))
plt.barh(amenX,amenY)
plt.show()
