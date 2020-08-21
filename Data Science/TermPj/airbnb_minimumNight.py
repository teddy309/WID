#minimum night
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
pd.options.mode.chained_assignment = None

data = pd.read_csv(os.getcwd()+'\\data.csv',encoding = "ISO-8859-1")

def dropna(origin,feacture):
    origin=origin.dropna(how="all",subset=[feacture])
    return origin

#city가 nan인경우 drop, 하고 암스트레담이 아닌 경우도 드랍..
def cityPreprocess(data):
    data_dropna=dropna(data,"city")
    data_city=data_dropna[data_dropna["city"]=="Amsterdam"]
    #print(data_dropna.head())
    #print(data_city.iloc[30:40,4:7])
    return data_city

data=cityPreprocess(data)
datat=data.reset_index(drop=True)
night = datat["minimum_nights"]

temp=(datat.iloc[:,22].to_numpy())#22='minimum_nights'
temp=temp.astype(np.float32)
print("mean night: ",np.mean(temp))
for i in range(len(night)): # outlier detection
    if((float(night[i]) > np.mean(temp) + 3 * np.std(temp)) or (float(night[i]) < np.mean(temp) -  3 * np.std(temp))):
        night[i] = np.mean(temp)
# print(night)
night = pd.DataFrame({'minimum_nights': night, 'minimum_nights_check': 0})
night["minimum_nights_check"] = 0

# print(night)
for i in range(len(night)):
    if(float(night.iloc[i,0]) >= 5):#5일 이상이면 1(장기) 아니면 0(단기)
        night.iloc[i,1] = 1
    else:
        night.iloc[i,1] = 0

print(night)#64 line
print(datat)#64 line
print(np.mean(temp))#3.289...
print(np.std(temp))#12.324...
