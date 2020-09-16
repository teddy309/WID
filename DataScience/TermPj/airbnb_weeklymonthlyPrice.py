#weekly & montly price
import numpy as np
import pandas as pd
from sklearn import linear_model
import matplotlib.pyplot as plt
from sklearn import preprocessing
import math,os,random
import re
import warnings
import operator
import sys
warnings.filterwarnings(action='ignore')
pd.options.mode.chained_assignment = None 

data = pd.read_csv(os.getcwd()+'\\data.csv',encoding = "ISO-8859-1")

def dropna(origin,feature):
    origin=origin.dropna(how="all",subset=[feature])
    return origin

#city가 nan인경우 drop, 하고 암스트레담이 아닌 경우도 드랍..
def cityPreprocess(data):
    data_dropna=dropna(data,"city")
    data_city=data_dropna[data_dropna["city"]=="Amsterdam"]#==?
    #print(data_dropna.head())
    #print(data_city.iloc[30:40,4:7])
    return data_city

data=cityPreprocess(data)
datat=data.reset_index(drop=True)
datat=datat.loc[:,'price':'cleaning_fee']
print(datat)##select only price columns

price_week = datat[["price", "weekly_price"]]
price_month = datat[["price", "monthly_price"]]

price_origin = datat["price"]
week_origin = datat["weekly_price"]
month_origin = datat["monthly_price"]

price_week_noNan = price_week.dropna() # drop nan from week
price1 = price_week_noNan["price"]
week = price_week_noNan["weekly_price"]

price_month_noNan = price_month.dropna() # drop nan from month
price2 = price_month_noNan["price"]
month = price_month_noNan["monthly_price"]

##reg,reg2 학습
reg = linear_model.LinearRegression() # price and week linear regression
reg.fit(price1[:, np.newaxis], week) 
reg2 = linear_model.LinearRegression() # price and month linear regression
reg2.fit(price2[:, np.newaxis], month)


pw = reg.predict(price_origin[:,np.newaxis]) #predicted week_price
pm = reg2.predict(price_origin[:,np.newaxis]) #predicted month_price

for i in range(len(price_origin)):  # enter week nan data to predicted data
    w = float(week_origin[i])
    if(np.isnan(w)):
        week_origin[i] = int(pw[i])
for i in range(len(price_origin)):  # enter month nan data to predicted data
    m = float(month_origin[i])
    if(np.isnan(m)):
        month_origin[i] = int(pm[i])

print(week_origin)
print(month_origin)
