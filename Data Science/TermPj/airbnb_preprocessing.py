# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 02:51:30 2019

@author: 김진겸, 정유지, 이승수
"""

import warnings
warnings.filterwarnings(action="ignore")
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsRegressor

import seaborn as sns
from sklearn import linear_model
import math,os,re,random
import operator
pd.options.mode.chained_assignment = None 

original=pd.read_csv("data_select1000.csv",encoding = "ISO-8859-1")#파일명 바꾸기
column=original.columns[:29]

#프리프로세싱 순서(먼저 데이터 관련 되어서 보는거 작업 필요 그다음에 drop할 거 부타 먼저 하기)
#1. city가 asterdam인지 판별
#2. id, host id가 null값인 경우 인증 되지 않았다고 판단 dropna
#3. np.nan일때 drop시킬것 먼저 drop
#4. zipcode and latitude longitude preprocessing
#5. One-hot encoder,(property, room_type,bedtype)
#6. room, bedroom, bed....
#7. amenties: 빈도수가 높거나 중요한 것들 5개로 묶어서 One-hot encoding('Wifi','Heating','Shower','Kitchen','Elevator')
#8.price, weekly price, monlty price
def preprocessingData(data):
    data=cityPreprocess(data)
    data=idPreprocess(data)
    data=dropna(data,"property_type")
    data=dropna(data,"room_type")
    data=dropna(data,"bed_type")
    data=data.dropna(subset=["bathrooms","bedrooms","beds","accommodates"])
    data=zipcodePreprocess(data)
    data=locationPreprocess(data)
    data=zipcodeLocationPreprocess(data)
    fillLocation(data)
    bathroom, beds= roomPreprocess(data)
    onehot_property_label, onehot_property=OneHotPreprocessing(data,"property_type")
    onehot_roomtype_label,onehot_roomtype=OneHotPreprocessing(data,"room_type")
    onehot_bedtype_label,onehot_bedtype=OneHotPreprocessing(data,"bed_type")
    minimumNightNewFeature = minimumNightPreprocess(data)
    global preprocessed_data   
    delete_list=[]
    delete_list.append(1)
    preprocessed_data=data.iloc[:,:]
    preprocessed_data["property_type"]=onehot_property
    preprocessed_data["room_type"]=onehot_roomtype
    preprocessed_data["bed_type"]=onehot_bedtype
    preprocessed_data["beds"]=beds
    preprocessed_data["bathrooms"]=bathroom
    colCat=preprocessed_data['amenities'].as_matrix().reshape(-1)
    colCat=str(colCat).split(',')
    trimming(colCat)#특수기호 제거
    colCat=list(dict.fromkeys(colCat))#eliminate duplicated
    amenityCount=findAmenities(colCat)
    amenSize=12
    topTwelve=topNfromDict(amenityCount,amenSize)
    amenX,amenY=[],[]#생략하기..
    for i in range(amenSize):
        amenX.append(topTwelve[i][0])
        amenY.append(topTwelve[i][1])
    #[['Wifi','Internet'],['Heating'],['essentials','shampoo','dryer'],['kitchen'],['elevator']]
    amenDic={'Wifi':0,'Heating':0,'Showering':0,'Kitchen':0,'Elevator':0}
    amenDic['Wifi']=amenY[0]+amenY[9]#Wifi+Internet
    amenDic['Heating']=amenY[1]
    amenDic['Showering']=amenY[2]+amenY[7]+amenY[8]#Essentials+Shampoo+Dryer
    amenDic['Kitchen']=amenY[3]
    amenDic['Elevator']=amenY[10]
    OHamenity=oneHotAmenities()
    OH=['Wifi','Heating','Shower','Kitchen','Elevator']
    revOHamenity=np.array(OHamenity).T
    for i in range(len(revOHamenity)):
        preprocessed_data[OH[i]]=pd.Series(revOHamenity[i])
    preprocessed_data=pd.concat([preprocessed_data, minimumNightNewFeature], axis = 1)
    preprocessed_data=preprocessed_data.drop(["guests_included","number_of_reviews_ltm","last_review","reviews_per_month","minimum_nights","maximum_nights","latitude","longitude","host_response_time","host_response_rate","amenities"],axis=1)
    preprocessed_data=weekPricePredict(preprocessed_data)
    preprocessed_data=monthPricePredict(preprocessed_data)
    print(preprocessed_data.head())

    return onehot_property_label,onehot_roomtype_label,onehot_bedtype_label,preprocessed_data
    

def cityPreprocess(data):
    data_dropna=dropna(data,"city")
    data_city=data_dropna[data_dropna["city"]=="Amsterdam"]
    data_city=data_city.reset_index(drop=True)
    #print(data_city[160:165]) 
    #print(data_dropna.head())
    #print(data_city.iloc[30:40,4:7])
    return data_city

def idPreprocess(data):
    data=dropna(data,"id")
    data=dropna(data,"host_id")
    data=dropDigit(data,"id",False)
    data=dropDigit(data,"host_id",False)
    return data

def zipcodePreprocess(origin):
    index_zipcode=findIndex("zipcode",origin)
    
    for i in range(len(origin)):
        list_temp=[]
        zipcode=str(origin.iloc[i,index_zipcode])
        if zipcode=="nan":
            continue;
            
        else:
            for j in range(len(zipcode)):
              
                if ord(zipcode[j])>=48 and ord(zipcode[j])<=57:
                    list_temp.append(j)
                    
                if j==len(zipcode)-1 and len(list_temp)>0:
                    zipcode=zipcode[:len(list_temp)]
                    
        origin.iat[i,index_zipcode]=zipcode
    
    for i in range(len(origin)):
        list_temp=[]
        zipcode=str(origin.iloc[i,index_zipcode])
        if zipcode=="nan":
            continue;
            
        else:
            if is_digit(zipcode)==False:
                zipcode="nan"                    
        origin.iat[i,index_zipcode]=zipcode       
    origin=origin.reset_index(drop=True)
    return origin

        
#위도 경도 프리프로세싱(범위 보고 그거 넘어가면 아웃라이더 판단. np.nan일단 냅두기) 
#나중 처리를 위해, 위도,경도 이상한건 np.nan처리--> 나중에 zip code와 분석하여 채울예정
def locationPreprocess(data):
    index_latitude=findIndex("latitude",data)
    index_longitude=findIndex("longitude",data)
    for i in range(len(data)):
        latitude=(data.iloc[i,index_latitude])
        
        if is_digit(latitude)==False:
            latitude=np.NAN
            latitude=float(latitude)
            data.iat[i,index_latitude]=latitude
            #print(latitude)
        
        else:
            latitude=float(latitude)
            if latitude<52.28 or latitude>54:
                latitude=float(latitude)
                data.iat[i,index_latitude]=latitude
            

    for i in range(len(data)):
        longitude=(data.iloc[i,index_longitude])
        if is_digit(longitude)==False:
            longitude=np.NAN
            longitude=float(longitude)
            data.iat[i,index_longitude]=longitude
       
        else:
            longitude=float(longitude)
            if longitude<4.7 or longitude>5.0:
                data.iat[i,index_longitude]=longitude
        
         
    data=data.reset_index(drop=True)
    return data

def zipcodeLocationPreprocess(data):
    index_zipcode=findIndex("zipcode",data)
    index_latitude=findIndex("latitude",data)
    index_longitude=findIndex("longitude",data)
    list_drop=[]
    for i in range((len(data))):
        zipcode=data.iloc[i,index_zipcode]
        zipcode=str(data.iloc[i,index_zipcode])
        latitude=data.iloc[i,index_latitude]
        longitude=data.iloc[i,index_longitude]
        latitude=float(latitude)
        longitude=float(longitude)
        #모두가 null일때는 dropna처리.
        if zipcode=="nan":
            if np.isnan(latitude):
                if np.isnan(longitude):
                    print("drop")
                    list_drop.append(i)
    data=data.drop(list_drop)
    data=data.reset_index(drop=True)
    return data
    #어떤 row 기준으로 어떤 target으로 고를건지 
def fillLocation(data):
    
    index_zipcode=findIndex("zipcode",data)
    index_latitude=findIndex("latitude",data)
    index_longitude=findIndex("longitude",data)
    for i in range(len(data)):
        zipcode=data.iloc[i,index_zipcode]
        zipcode=str(data.iloc[i,index_zipcode])
        latitude=data.iloc[i,index_latitude]
        longitude=data.iloc[i,index_longitude]
        latitude=float(latitude)
        longitude=float(longitude)
        list_temp=[i]
        if zipcode=="nan":    
            if np.isnan(latitude):
                near_index=findNearst(data,i,"longitude",list_temp)
                data=fill(data,i,"longitude","zipcode",near_index)
            else:

                near_index=findNearst(data,i,"latitude",list_temp)
                data=fill(data,i,"latitude","zipcode",near_index)
                
    for i in range(len(data)):
        latitude=data.iloc[i,index_latitude]
        longitude=data.iloc[i,index_longitude]
        latitude=float(latitude)
        longitude=float(longitude)
        list_temp=[i]
        if np.isnan(latitude):
                near_index=findNearst(data,i,"zipcode",list_temp)
                data=fill(data,i,"zipcode","latitude",near_index)
        if np.isnan(longitude):
                near_index=findNearst(data,i,"zipcode",list_temp)
                data=fill(data,i,"zipcode","latitude",near_index)

 
def findNearst(data,index,target,list_temp):
    target_index=findIndex(target,data)
    nearset_target=float(data.iloc[index,target_index])
    diff=1000
    index_near=0
    for i in range(len(data)):
        
        if np.isnan(float(data.iloc[i,target_index])):
            continue;
        elif i in list_temp:
            continue;
            
        else:
            #print(np.abs(float(data.iloc[i,target_index])-nearset_target))
            if np.abs(float(data.iloc[i,target_index])-nearset_target)<diff:
                index_near=i
                diff=np.abs(float(data.iloc[i,target_index])-nearset_target)
    
    return index_near
    #fill(data,index, "zipcode",index_near)

def fill(data, index, target,feature,index_near):
    feature_index=findIndex(feature,data)
    if np.isnan(float(data.iloc[index_near,feature_index])):
        list_temp=[index_near]
        while(True):
            index_near=findNearst(data,index,target,list_temp)
            if np.isnan(float(data.iloc[index_near,feature_index])):
                list_temp.append(index_near)
            else:
                break;
    data.iat[index,feature_index]=data.iloc[index_near,feature_index]
    print(index," ",data.iloc[index,feature_index])
    return data


def dropna(origin,feacture):
    origin=origin.dropna(how="all",subset=[feacture])
    origin=origin.reset_index(drop=True)
    return origin
def dropDigit(data,target,what):
    index=findIndex(target,data)
    list_digit=[]
    if what==True:
        for i in range(len(data)):
            if is_digit(data.iloc[i,index])==True:
                list_digit.append(i)
    else:
        for i in range(len(data)):
            if is_digit(data.iloc[i,index])==False:
                list_digit.append(i)
    data=data.drop(list_digit)
    data=data.reset_index(drop=True)
    return data

def findIndex(target,data):
    column_list=data.columns
    for i in range(len(column_list)):
        if column_list[i]==target:
            return i
    return -1

def is_digit(temp):
    temp=str(temp)
    try:
        float(temp)
        return True
    except ValueError:
        return False
def OneHotPreprocessing(data,target):
    

    drop_na_property=dropna(data,target)
    drop_na_property=dropDigit(drop_na_property, target,True)

    if target=="property_type":
        one_hot=pd.get_dummies(drop_na_property.property_type)
        #print(one_hot,one_hot.columns)
    elif target=="room_type":
        one_hot=pd.get_dummies(drop_na_property.room_type)
    elif target=="bed_type":
        one_hot=pd.get_dummies(drop_na_property.bed_type)     
    
    lis=index(one_hot,one_hot.columns)
    return one_hot.columns,lis 
def index(data,column):
    index=[]
    for i in range(len(data)):
        for j in range(len(column)):
            if data.iloc[i,j]==1:
                index.append(j)
    return index
def convertFloat(data, target):
    index=findIndex(target,data)
    for i in range(len(data)):
        if float(data.iloc[i,index]).is_integer()==False:
            data.iat[i,index]=round(float(data.iloc[i,index]))
    return data

def roomPreprocess(data):
    index_bath=findIndex("bathrooms",data)
    #index_room=findIndex("bedrooms",data)
    index_bed=findIndex("beds",data)
    index_acom=findIndex("accommodates",data)
    list_type=["bathrooms","bedrooms","beds","accommodates"]
    
    #na인 경우 버림...
    for i in range(len(list_type)):
        data=dropDigit(data,list_type[i],False)
    
     # 그 데이터가 flaot인 경우가 있어서 그거 내림 해서 인수로 만들기...
    for i in range(len(list_type)):
        data=convertFloat(data,list_type[i])
    bathrooms_accom=[]
    for i in range(len(data)):
        bathrooms_accom.append(int(int(data.iloc[i,index_bath])/int(data.iloc[i,index_acom])))
    beds_accom=[]
    for i in range(len(data)):
        beds_accom.append(int(int(data.iloc[i,index_bed])/int(data.iloc[i,index_acom])))
    return bathrooms_accom, beds_accom
def minimumNightPreprocess(data):
    night = data["minimum_nights"]

    temp=(data.iloc[:,22].to_numpy())
    temp=temp.astype(np.float32)

    for i in range(len(night)): # outlier detection
        if((float(night[i]) > np.mean(temp) + 3 * np.std(temp)) or (float(night[i]) < np.mean(temp) -  3 * np.std(temp))):
            night[i] = np.mean(temp)
    # print(night)
    night = pd.DataFrame({'minimum_nights': night, 'minimum_nights_check': 0})
    night["minimum_nights_check"] = 0

    for i in range(len(night)): # minimum night가 작으면 0 크면 1로 feature creation
        if(float(night.iloc[i,0]) >= 5):
            night.iloc[i,1] = 1
        else:
            night.iloc[i,1] = 0

    return night["minimum_nights_check"]


def weekPricePredict(datat):
    price_week = datat[["price", "weekly_price"]]
    price_origin = datat["price"]
    week_origin = datat["weekly_price"]
    
    price_week_noNan = price_week.dropna() # drop nan from week
    price1 = price_week_noNan["price"]
    week = price_week_noNan["weekly_price"]

    reg = linear_model.LinearRegression() # price and week linear regression
    reg.fit(price1[:, np.newaxis], week)

    pw = reg.predict(price_origin[:,np.newaxis]) #predicted week_price
    
    for i in range(len(price_origin)):  # enter predicted data at week nan data
        w = float(week_origin[i])
        if(np.isnan(w)):
            datat["weekly_price"][i] = int(pw[i])

    return datat

# month 가격 채워넣기
def monthPricePredict(datat):
    price_month = datat[["price", "monthly_price"]]
    price_origin = datat["price"]
    month_origin = datat["monthly_price"]

    price_month_noNan = price_month.dropna() # drop nan from month
    price2 = price_month_noNan["price"]
    month = price_month_noNan["monthly_price"]

    reg2 = linear_model.LinearRegression() # price and month linear regression
    reg2.fit(price2[:, np.newaxis], month)

    pm = reg2.predict(price_origin[:,np.newaxis]) #predicted month_price

    for i in range(len(price_origin)):  # enter month nan data to predicted data
        m = float(month_origin[i])
        if(np.isnan(m)):
            datat["monthly_price"][i] = int(pm[i])

    return datat
#####'amenities'분리해주는 functions######
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
#유니크한 amenity들의 개수 세기 
def findAmenities(colCat):
    amenitycount={colCat[0]:0}
    for i in range(len(colCat)):
        amenitycount[colCat[i]]=0
    for i in range(len(preprocessed_data)):
        for x in amenitycount:
            if str(preprocessed_data['amenities'][i]).find(x)>0:
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
def oneHotAmenities():
    OneHotAmenities=[]
    for i in range(len(preprocessed_data)):
        count=[0,0,0,0,0]
        if re.search('Wifi'or'Internet',preprocessed_data['amenities'].iloc[i],re.IGNORECASE):
            count[0]=count[0]+1
        if re.search('Heating',preprocessed_data['amenities'].iloc[i],re.IGNORECASE):
            count[1]=count[1]+1
        if re.search('essentials'or'shampoo'or'dryer',preprocessed_data['amenities'].iloc[i],re.IGNORECASE):
            count[2]=count[2]+1
        if re.search('kitchen',preprocessed_data['amenities'].iloc[i],re.IGNORECASE):
            count[3]=count[3]+1
        if re.search('elevator',preprocessed_data['amenities'].iloc[i],re.IGNORECASE):
            count[4]=count[4]+1
        OneHotAmenities.append(count)
    return OneHotAmenities

#lable1,labe2,label3,preprocessed_data=preprocessingData(original)

#print(preprocessed_data.columns)

#preprocessed_data.to_excel("preprocess.xlsx",sheet_name="first")

#KNN###
from sklearn.neighbors import KNeighborsRegressor

preprocessed_data=pd.read_excel("preprocess.xlsx",encoding = "ISO-8859-1")
index=list(range(len(preprocessed_data)))
random.shuffle(index)
trainingSize,testSize=5000,450

#preprocessed_X=preprocessed_data.drop(['id','host_id','neighbourhood_cleansed','city','price','weekly_price','cleaning_fee'],axis=1)
#preprocessed_X=preprocessed_data.drop(['zipcode','accommodates','beds','review_scores_rating','id','host_id','neighbourhood_cleansed','city','price','weekly_price','cleaning_fee'],axis=1)
preprocessed_X=preprocessed_data[['zipcode','accommodates','beds','review_scores_rating']]

trainingX=preprocessed_X.iloc[index[0:trainingSize]]
preprocessed_Y=preprocessed_data["price"]
testX=[]
for i in range(10):
    testX.append(preprocessed_X.iloc[index[trainingSize+i*testSize:trainingSize+(i+1)*testSize-1]])
trainingY=preprocessed_Y.iloc[index[0:trainingSize]]
testY=[]
for i in range(10):
    testY.append(preprocessed_Y.iloc[index[trainingSize+i*testSize:trainingSize+(i+1)*testSize-1]])
clf=KNeighborsRegressor(n_neighbors=5)
clf.fit(trainingX,trainingY)

accuracy=[]
print("Considered data columns: ")
print(preprocessed_X.columns)
print("K-neighbor accuracy: ",clf.score(trainingX,trainingY))

#for i in range(10):
    #accuracy.append(clf.score(testX[0],testY[0]))
#print("accuracy: ",np.mean(accuracy))

#Bagging##
from sklearn.ensemble import BaggingRegressor
regressor=BaggingRegressor(random_state=0)
regressor.fit(trainingX,trainingY)
predY=[]
scoreBagging=[]
for i in range(10):
    predY.append(regressor.predict(testX[i]))
    scoreBagging.append(regressor.score(testX[i],testY[i]))
print("Bagging score: ",np.mean(scoreBagging))
print(predY)
print(testY)

def RMSE(n,p,a):
    for i in range(n):
        a=0

