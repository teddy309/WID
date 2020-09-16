# -*- coding: utf-8 -*-
"""
Created on Sun May 26 14:56:57 2019

@author: 김진겸
"""
import pandas as pd
import numpy as np
from sklearn import preprocessing
import math
import os
data=pd.read_csv(os.getcwd()+'\\data.csv',encoding = "ISO-8859-1")
#print(data.columns)
column=data.columns[:29]

#인덱스 찾는 함수 -1이면 없는 거 
def findIndex(target):
    for i in range(len(column)):
        if column[i]==target:
            return i
    return -1
#target column이 숫자이면(True일 때) data에서 drop해줌.
def dropDigit(data,target,what):
    index=findIndex(target)
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
    return data
    
#숫자가 아닌지 판단하는 함
def is_digit(temp):
    temp=str(temp)
    try:
        float(temp)
        return True
    except ValueError:
        return False

def dropna(origin,feacture):
    origin=origin.dropna(how="all",subset=[feacture])
    origin=origin.reset_index(drop=True)
    return origin
#city가 nan인경우 drop, 하고 암스트레담이 아닌 경우도 드랍..
def cityPreprocess(data):
    data_dropna=dropna(data,"city")
    data_city=data_dropna[data_dropna["city"]=="Amsterdam"]
    data_city=data_city.reset_index(drop=True)
    #print(data_city[160:165]) 
    #print(data_dropna.head())
    #print(data_city.iloc[30:40,4:7])
    return data_city

#일단 먼저 그 영어있으면 때주는것    
def zipcodePreprocess(origin):
    index_zipcode=findIndex("zipcode")
    
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
    index_latitude=findIndex("latitude")
    index_longitude=findIndex("longitude")
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

#
def zipcodeLocationPreprocess(data):
    index_zipcode=findIndex("zipcode")
    index_latitude=findIndex("latitude")
    index_longitude=findIndex("longitude")
    list_drop=[]
    for i in range((len(data))):
        #zipcode=data.iloc[i,index_zipcode]
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
    data=data.drop(list_drop)#데이터 drop
    data=data.reset_index(drop=True)
    return data
    #어떤 row 기준으로 어떤 target으로 고를건지
def fillLocation(data): #
    
    index_zipcode=findIndex("zipcode")
    index_latitude=findIndex("latitude")
    index_longitude=findIndex("longitude")
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
    target_index=findIndex(target)
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
    feature_index=findIndex(feature)
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

def OneHotPreprocessing(data,target):
    

    drop_na_property=dropna(data,target)
    drop_na_property=dropDigit(drop_na_property, target,True)
    if target=="property_type":
        one_hot=pd.get_dummies(drop_na_property.property_type)
    elif target=="room_type":
        one_hot=pd.get_dummies(drop_na_property.room_type)
    elif target=="bed_type":
        one_hot=pd.get_dummies(drop_na_property.bed_type)
        
    return one_hot

def convertFloat(data, target):
    index=findIndex(target)
    for i in range(len(data)):
        if float(data.iloc[i,index]).is_integer()==False:
            data.iat[i,index]=round(float(data.iloc[i,index]))
    return data

def roomPreprocess(data):
    index_bath=findIndex("bathrooms")
    #index_room=findIndex("bedrooms")
    index_bed=findIndex("beds")
    index_acom=findIndex("accommodates")
    list_type=["bathrooms","bedrooms","beds","accommodates"]
    #na인 경우 버림...
    data=data.dropna(subset=["bathrooms","bedrooms","beds","accommodates"])
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
        
data=cityPreprocess(data)
#zipcode, 위도 경도 프리프로세싱
data=zipcodePreprocess(data)
data=locationPreprocess(data)
data=zipcodeLocationPreprocess(data)
#fillLocation(data)

#room type, property type의 프리 프로세싱
bathroom, beds= roomPreprocess(data)
onehot_property=OneHotPreprocessing(data,"property_type")
onehot_room_type=OneHotPreprocessing(data,"room_type")
onehot_bed_type=OneHotPreprocessing(data,"bed_type")






print(onehot_room_type)





















