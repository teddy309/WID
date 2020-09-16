import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pprint import PrettyPrinter as pp
import collections

from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score

from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from sklearn_extra.cluster import KMedoids

import os,sys
import math,random
from ctypes import * #for unsigned int32
import warnings

warnings.filterwarnings(action='ignore')
np.set_printoptions(threshold=sys.maxsize)

def index_of(val, in_list):
    try:
        return in_list.index(val)
    except ValueError:
        return -1
def result_section(cluster):
    list_60 = []
    list_70 = []
    list_80 = []
    list_90 = []
    list_00 = []
    list_10 = []

    for i in cluster:
        if index_of(1960, i) != -1:
            for j in i[index_of(1960, i) + 1]:
                list_60.append(j)
        if index_of(1970, i) != -1:
            for j in i[index_of(1970, i) + 1]:
                list_70.append(j)
        if index_of(1980, i) != -1:
            for j in i[index_of(1980, i) + 1]:
                list_80.append(j)
        if index_of(1990, i) != -1:
            for j in i[index_of(1990, i) + 1]:
                list_90.append(j)
        if index_of(2000, i) != -1:
            for j in i[index_of(2000, i) + 1]:
                list_00.append(j)
        if index_of(2010, i) != -1:
            for j in i[index_of(2010, i) + 1]:
                list_10.append(j)
    #print(list_60)
    if len(list_60) != 0:
        cc_60 =collections.Counter(list_60)
        tmp = cc_60.most_common(6)
        print("1960s Indicator number = " + str(tmp[0][1]) + " , Relative Nation top 5 : " + str(tmp[1][0]) + ", " + str(tmp[2][0])
              + ", " + str(tmp[3][0]) + ", " + str(tmp[4][0]) + ", " + str(tmp[5][0]))
    else:
        print("1960s no Indicator")

    if len(list_70) != 0:
        cc_70 =collections.Counter(list_70)
        tmp = cc_70.most_common(6)
        print("1970s Indicator number = " + str(tmp[0][1]) + " , Relative Nation top 5 : " + str(tmp[1][0]) + ", " + str(tmp[2][0])
              + ", " + str(tmp[3][0]) + ", " + str(tmp[4][0]) + ", " + str(tmp[5][0]))
    else:
        print("1970s no Indicator")

    if len(list_80) != 0:
        cc_80 =collections.Counter(list_80)
        tmp = cc_80.most_common(6)
        print("1980s Indicator number = " + str(tmp[0][1]) + " , Relative Nation top 5 : " + str(tmp[1][0]) + ", " + str(tmp[2][0])
              + ", " + str(tmp[3][0]) + ", " + str(tmp[4][0]) + ", " + str(tmp[5][0]))
    else:
        print("1980s no Indicator")

    if len(list_90) != 0:
        cc_90 =collections.Counter(list_90)
        tmp = cc_90.most_common(6)
        print("1990s Indicator number = " + str(tmp[0][1]) + " , Relative Nation top 5 : " + str(tmp[1][0]) + ", " + str(tmp[2][0])
              + ", " + str(tmp[3][0]) + ", " + str(tmp[4][0]) + ", " + str(tmp[5][0]))
    else:
        print("1990s no Indicator")


    if len(list_00) != 0:
        cc_00 =collections.Counter(list_00)
        tmp = cc_00.most_common(6)
        print("2000s Indicator number = " + str(tmp[0][1]) + " , Relative Nation top 5 : " + str(tmp[1][0]) + ", " + str(tmp[2][0])
              + ", " + str(tmp[3][0]) + ", " + str(tmp[4][0]) + ", " + str(tmp[5][0]))
    else:
        print("2000s no Indicator")


    if len(list_10) != 0:
        cc_10 =collections.Counter(list_10)
        tmp = cc_10.most_common(6)
        print("2010s Indicator number = " + str(tmp[0][1]) + " , Relative Nation top 5 : " + str(tmp[1][0]) + ", " + str(tmp[2][0])
              + ", " + str(tmp[3][0]) + ", " + str(tmp[4][0]) + ", " + str(tmp[5][0]))
    else:
        print("2010s no Indicator")

def index_to_county_code(list_clsuter,dataset):#list = result_list , dataset = preprocessing_dataset
    country_list = []
    country_list.clear()
    tmp = []
    if index_of(1960,list_clsuter) != -1:
        tmp.clear()
        for i in list_clsuter[index_of(1960,list_clsuter)+1]:
            tmp.append(dataset["Country Code"].iloc[i])
        country_list.append(1960)
        country_list.append(list(tmp))

    if index_of(1970,list_clsuter) != -1:
        tmp.clear()
        for i in list_clsuter[index_of(1970, list_clsuter) + 1]:
            tmp.append(dataset["Country Code"].iloc[i])
        country_list.append(1970)
        country_list.append(list(tmp))

    if index_of(1980,list_clsuter) != -1:
        tmp.clear()
        for i in list_clsuter[index_of(1980, list_clsuter) + 1]:
            tmp.append(dataset["Country Code"].iloc[i])
        country_list.append(1980)
        country_list.append(list(tmp))

    if index_of(1990,list_clsuter) != -1:
        tmp.clear()
        for i in list_clsuter[index_of(1990, list_clsuter) + 1]:
            tmp.append(dataset["Country Code"].iloc[i])
        country_list.append(1990)
        country_list.append(list(tmp))

    if index_of(2000,list_clsuter) != -1:
        tmp.clear()
        for i in list_clsuter[index_of(2000,list_clsuter)+1]:
            tmp.append(dataset["Country Code"].iloc[i])
        country_list.append(2000)
        country_list.append(list(tmp))

    if index_of(2010,list_clsuter) != -1:
        tmp.clear()
        for i in list_clsuter[index_of(2010, list_clsuter) + 1]:
            tmp.append(dataset["Country Code"].iloc[i])
        country_list.append(2010)
        country_list.append(list(tmp))

    return country_list


def calculate_cluster(c1,c2,kor_index):
    result_list = []
    if 1960 in c1.columns:
        new_df1 = c1[c1[1960].isin(c1[1960][kor_index])]
        new_df2 = c2[c2[1960].isin(c2[1960][kor_index])]
        result_list.append(1960)
        result_list.append(list(set(new_df1.index).intersection(new_df2.index)))
    if 1970 in c1.columns:
        new_df1 = c1[c1[1970].isin(c1[1970][kor_index])]
        new_df2 = c2[c2[1970].isin(c2[1970][kor_index])]
        result_list.append(1970)
        result_list.append(list(set(new_df1.index).intersection(new_df2.index)))
    if 1980 in c1.columns:
        new_df1 = c1[c1[1980].isin(c1[1980][kor_index])]
        new_df2 = c2[c2[1980].isin(c2[1980][kor_index])]
        result_list.append(1980)
        result_list.append(list(set(new_df1.index).intersection(new_df2.index)))

    if 1990 in c1.columns:
        new_df1 = c1[c1[1990].isin(c1[1990][kor_index])]
        new_df2 = c2[c2[1990].isin(c2[1990][kor_index])]
        result_list.append(1990)
        result_list.append(list(set(new_df1.index).intersection(new_df2.index)))

    if 2000 in c1.columns:
        new_df1 = c1[c1[2000].isin(c1[2000][kor_index])]
        new_df2 = c2[c2[2000].isin(c2[2000][kor_index])]
        result_list.append(2000)
        result_list.append(list(set(new_df1.index).intersection(new_df2.index)))

    if 2010 in c1.columns:
        new_df1 = c1[c1[2010].isin(c1[2010][kor_index])]
        new_df2 = c2[c2[2010].isin(c2[2010][kor_index])]
        result_list.append(2010)
        result_list.append(list(set(new_df1.index).intersection(new_df2.index)))


    return result_list
def k_Means(dataset):
    kor = dataset[dataset["Country Code"].isin(["KOR"])]
    result = []
    list = []
    if dataset['1960s'].count() != 0:# 1960s all nan
        year_list = []
        for i in range(len(dataset)):
            year_list.append(int(1960))
        data_60 = dataset[['1960s']].fillna(0)
        data_60['year'] = year_list
        # n-clusters = 3
        kmeans = KMeans(n_clusters=10)
        kmeans.fit(data_60)
        KMeans(algorithm='auto', copy_x=True, init='k-means++',
               max_iter=50, n_clusters=10, n_init=10, n_jobs=1,
               precompute_distances='auto ', random_state=None,
               tol=0.0001, verbose=0)
        cluster = kmeans.fit_predict(data_60)
        result.append(cluster)
        list.append(1960)
        """plt.scatter(data_60['1960s'], data_60['year'], c=cluster, s=60, edgecolors='black')
        plt.title("K-Means 1960s")
        plt.xlabel("Year")
        plt.ylabel("Value")
        plt.show()"""

    if dataset['1970s'].count() != 0:
        year_list = []
        for i in range(len(dataset)):
            year_list.append(int(1970))
        data_70 = dataset[['1970s']].fillna(0)
        data_70['year'] = year_list
        # n-clusters = 3
        kmeans = KMeans(n_clusters=10)
        kmeans.fit(data_70)
        KMeans(algorithm='auto', copy_x=True, init='k-means++',
               max_iter=50, n_clusters=10, n_init=10, n_jobs=1,
               precompute_distances='auto ', random_state=None,
               tol=0.0001, verbose=0)
        cluster = kmeans.fit_predict(data_70)
        result.append(cluster)
        list.append(1970)


        """plt.scatter(data_70['1970s'], data_70['year'], c=cluster, s=60, edgecolors='black')
        plt.title("K-Means 1970s")
        plt.xlabel("Value")
        plt.ylabel("Year")
        plt.show()"""

    if dataset['1980s'].count() != 0:
        year_list = []
        for i in range(len(dataset)):
            year_list.append(int(1980))
        data_80 = dataset[['1980s']].fillna(0)
        data_80['year'] = year_list
        # n-clusters = 3
        kmeans = KMeans(n_clusters=10)
        kmeans.fit(data_80)

        KMeans(algorithm='auto', copy_x=True, init='k-means++',
               max_iter=50, n_clusters=10, n_init=10, n_jobs=1,
               precompute_distances='auto ', random_state=None,
               tol=0.0001, verbose=0)
        cluster = kmeans.fit_predict(data_80)
        result.append(cluster)
        list.append(1980)

        """plt.scatter(data_80['1980s'], data_80['year'], c=cluster, s=60, edgecolors='black')
        plt.title("K-Means 1980s")
        plt.xlabel("Value")
        plt.ylabel("Year")
        plt.show()"""
    if dataset['1990s'].count() != 0:
        year_list = []
        for i in range(len(dataset)):
            year_list.append(int(1990))
        data_90 = dataset[['1990s']].fillna(0)
        data_90['year'] = year_list
        # n-clusters = 3
        kmeans = KMeans(n_clusters=10)
        kmeans.fit(data_90)

        KMeans(algorithm='auto', copy_x=True, init='k-means++',
               max_iter=50, n_clusters=10, n_init=10, n_jobs=1,
               precompute_distances='auto ', random_state=None,
               tol=0.0001, verbose=0)
        cluster = kmeans.fit_predict(data_90)
        result.append(cluster)
        list.append(1990)

        """plt.scatter(data_80['1990s'], data_80['year'], c=cluster, s=60, edgecolors='black')
        plt.title("K-Means 1990s")
        plt.xlabel("Value")
        plt.ylabel("Year")
        plt.show()"""
    if dataset['2000s'].count() != 0:
        year_list = []
        for i in range(len(dataset)):
            year_list.append(int(2000))
        data_00 = dataset[['2000s']].fillna(0)
        data_00['year'] = year_list
        # n-clusters = 3
        kmeans = KMeans(n_clusters=10)
        kmeans.fit(data_00)

        KMeans(algorithm='auto', copy_x=True, init='k-means++',
               max_iter=50, n_clusters=10, n_init=10, n_jobs=1,
               precompute_distances='auto ', random_state=None,
               tol=0.0001, verbose=0)
        cluster = kmeans.fit_predict(data_00)
        result.append(cluster)
        list.append(2000)

        """plt.scatter(data_80['2000s'], data_80['year'], c=cluster, s=60, edgecolors='black')
        plt.title("K-Means 2000s")
        plt.xlabel("Value")
        plt.ylabel("Year")
        plt.show()"""
    if dataset['2010s'].count() != 0:
        year_list = []
        for i in range(len(dataset)):
            year_list.append(int(2000))
        data_10 = dataset[['2010s']].fillna(0)
        data_10['year'] = year_list
        # n-clusters = 3
        kmeans = KMeans(n_clusters=10)
        kmeans.fit(data_10)

        KMeans(algorithm='auto', copy_x=True, init='k-means++',
               max_iter=50, n_clusters=10, n_init=10, n_jobs=1,
               precompute_distances='auto ', random_state=None,
               tol=0.0001, verbose=0)
        cluster = kmeans.fit_predict(data_10)
        result.append(cluster)
        list.append(2010)

        """plt.scatter(data_80['2010s'], data_80['year'], c=cluster, s=60, edgecolors='black')
        plt.title("K-Means 2010s")
        plt.xlabel("Value")
        plt.ylabel("Year")
        plt.show()"""

    result_list = np.array(result)
    cluster_result = pd.DataFrame(data = result_list.T,columns=list)
    #print(result)
    return cluster_result,kor.index
def k_Medoids(dataset):
    kor = dataset[dataset["Country Code"].isin(["KOR"])]
    result = []
    list = []
    if dataset['1960s'].count() != 0:
        year_list = []
        for i in range(len(dataset)):
            year_list.append(int(1960))
        data_60 = dataset[['1960s']].fillna(0)
        data_60['year'] = year_list
        # n-clusters = 5
        kmedoids = KMedoids(n_clusters=10, random_state=0)
        kmedoids.fit(data_60)

        cluster = kmedoids.labels_
        result.append(cluster)
        list.append(1960)
        """plt.scatter(data_60['1960s'], data_60['year'], c=cluster, s=60, edgecolors='black')
        plt.title("K-Means 1960s")
        plt.xlabel("Year")
        plt.ylabel("Value")
        plt.show()"""
    if dataset['1970s'].count() != 0:
        year_list = []
        for i in range(len(dataset)):
            year_list.append(int(1970))
        data_70 = dataset[['1970s']].fillna(0)
        data_70['year'] = year_list
        # n-clusters = 5
        kmedoids = KMedoids(n_clusters=10, random_state=0)
        kmedoids.fit(data_70)

        cluster = kmedoids.labels_
        result.append(cluster)
        list.append(1970)
        """plt.scatter(data_60['1960s'], data_60['year'], c=cluster, s=60, edgecolors='black')
        plt.title("K-Means 1960s")
        plt.xlabel("Year")
        plt.ylabel("Value")
        plt.show()"""
    if dataset['1980s'].count() != 0:
        year_list = []
        for i in range(len(dataset)):
            year_list.append(int(1980))
        data_80 = dataset[['1980s']].fillna(0)
        data_80['year'] = year_list
        # n-clusters = 5
        kmedoids = KMedoids(n_clusters=10, random_state=0)
        kmedoids.fit(data_80)

        cluster = kmedoids.labels_
        result.append(cluster)
        list.append(1980)
        """plt.scatter(data_60['1960s'], data_60['year'], c=cluster, s=60, edgecolors='black')
        plt.title("K-Means 1960s")
        plt.xlabel("Year")
        plt.ylabel("Value")
        plt.show()"""
    if dataset['1990s'].count() != 0:
        year_list = []
        for i in range(len(dataset)):
            year_list.append(int(1990))
        data_90 = dataset[['1990s']].fillna(0)
        data_90['year'] = year_list
        # n-clusters = 5
        kmedoids = KMedoids(n_clusters=10, random_state=0)
        kmedoids.fit(data_90)

        cluster = kmedoids.labels_
        result.append(cluster)
        list.append(1990)
        """plt.scatter(data_60['1960s'], data_60['year'], c=cluster, s=60, edgecolors='black')
        plt.title("K-Means 1960s")
        plt.xlabel("Year")
        plt.ylabel("Value")
        plt.show()"""

    if dataset['2000s'].count() != 0:
        year_list = []
        for i in range(len(dataset)):
            year_list.append(int(2000))
        data_00 = dataset[['2000s']].fillna(0)
        data_00['year'] = year_list
        # n-clusters = 5
        kmedoids = KMedoids(n_clusters=10, random_state=0)
        kmedoids.fit(data_00)

        cluster = kmedoids.labels_
        result.append(cluster)
        list.append(2000)
        """plt.scatter(data_60['1960s'], data_60['year'], c=cluster, s=60, edgecolors='black')
        plt.title("K-Means 1960s")
        plt.xlabel("Year")
        plt.ylabel("Value")
        plt.show()"""
    if dataset['2010s'].count() != 0:
        year_list = []
        for i in range(len(dataset)):
            year_list.append(int(2010))
        data_10 = dataset[['2010s']].fillna(0)
        data_10['year'] = year_list
        # n-clusters = 5
        kmedoids = KMedoids(n_clusters=10, random_state=0)
        kmedoids.fit(data_10)

        cluster = kmedoids.labels_
        result.append(cluster)
        list.append(2010)
        """plt.scatter(data_60['1960s'], data_60['year'], c=cluster, s=60, edgecolors='black')
        plt.title("K-Means 1960s")
        plt.xlabel("Year")
        plt.ylabel("Value")
        plt.show()"""
    result_list = np.array(result)
    cluster_result = pd.DataFrame(data = result_list.T,columns=list)
    #print(result)
    return cluster_result,kor.index


def DBScan(dataset):
    from sklearn.preprocessing import LabelEncoder
    from sklearn.preprocessing import MinMaxScaler
    # from sklearn.preprocessing import RobustScaler
    from sklearn.cluster import DBSCAN

    kor = dataset[dataset["Country Code"].isin(["KOR"])]  # row of "KOR"(dataframe)
    koreaIndex = kor.index.values.astype(int)[0]  # index of row(int)
    # print('koreaIndex: ',koreaIndex) #int
    # print('koreaRowCountry:',dataset.loc[koreaIndex,"Country Code"]) #Country Code
    numDatasets = len(dataset)

    enc = LabelEncoder()
    for col in dataset.columns:
        dataset[col] = dataset[col].fillna(0)
        if col == 'Country Code' or col == 'Indicator Code':
            # dataset[i][col]=enc.fit_transform(dataset[i][col]) #OK
            if col == 'Country Code':
                # print('[{}]dropped'.format(col))#
                dataset = dataset.drop(columns=[col])
            elif col == 'Indicator Code':
                # print('[{}]dropped'.format(col))#
                dataset = dataset.drop(columns=[col])

    ##minmax scaling
    scaler = MinMaxScaler(copy=True, feature_range=(0, 1))  # RobustScaler()
    dataset_normalized = scaler.fit_transform(dataset)
    #print('OK1')
    #print(type(dataset_normalized))
   # print(dataset_normalized)
    # EPS_population=[1.0,0.7,0.5,0.45,0.4,0.35,0.3,0.1,0.05,0.02,0.01,0.005]
    # EPS_economy=[1.0,0.7,0.65,0.6,0.55,0.5,0.45,0.4,0.35,0.3,0.1,0.05,0.02,0.01,0.005,0.001]
    EPS = [1.0, 0.7, 0.65, 0.6, 0.55, 0.5, 0.45, 0.4, 0.35, 0.3, 0.1, 0.05, 0.02, 0.01, 0.005, 0.001]
    MS = range(2, 10)
    for MSi in MS:
        for EPi in EPS:
            DBscan = DBSCAN(eps=EPi, min_samples=MSi)
            cluster_dbscan = DBscan.fit_predict(dataset_normalized)
            koreaClusterNum = cluster_dbscan[koreaIndex]
            if list(cluster_dbscan).count(koreaClusterNum) < 10:  # korea cluster has under 10 nations
                clusterList = []
                for i in range(len(cluster_dbscan)):
                    if cluster_dbscan[i] == koreaClusterNum:
                        clusterList.append(i)
                #print('EPS:', EPi, 'MS:', MSi)
                #print('Korea index:', koreaIndex)
                #print('cluster of KoreaS indices:', clusterList)
                #print(type(clusterList))
                return cluster_dbscan
    print('DBSCAN HyperParameter cannot Found!!!!')
    return np.ones(len(dataset))

def Preprocessing(indi_codeSet, dataset):
    if len(indi_codeSet) == 3:  # 3 indicators
        return Preprocessing_type3(indi_codeSet[0], indi_codeSet[1], indi_codeSet[2], dataset)
    elif len(indi_codeSet) == 2:  # 2 indicators
        return Preprocessing_type2(indi_codeSet[0], indi_codeSet[1], dataset)
    else:  # 1 indicators
        return Preprocessing_type1(indi_codeSet, dataset)


def Preprocessing_type1(indi_code, dataset):
    new_df = dataset
    new_df = new_df[new_df["Indicator Code"].isin([indi_code])]
    # set_avg_1960
    # mean_list = []
    mean_60 = []
    mean_70 = []
    mean_80 = []
    mean_90 = []
    mean_00 = []
    mean_10 = []
    tmp = []
    for i in new_df.index:
        tmp = list(new_df.loc[i])
        mean_60.append(np.mean(tmp[4:14]))  # 60~69
        mean_70.append(np.mean(tmp[14:24]))  # 70~79
        mean_80.append(np.mean(tmp[24:34]))  # 80~89
        mean_90.append(np.mean(tmp[34:44]))  # 90~99
        mean_00.append(np.mean(tmp[44:54]))  # 00~09
        mean_10.append(np.mean(tmp[54:63]))  # 10~18

    targer_df = new_df[['Country Code', 'Indicator Code']]
    targer_df['1960s'] = mean_60
    targer_df['1970s'] = mean_70
    targer_df['1980s'] = mean_80
    targer_df['1990s'] = mean_90
    targer_df['2000s'] = mean_00
    targer_df['2010s'] = mean_10
    targer_df = targer_df.reset_index()

    return targer_df


def Preprocessing_type2(indi_code1, indi_code2, dataset):  # return Preprocessing(code1/code2)
    df = dataset
    new_df1 = df[df["Indicator Code"].isin([indi_code1])]
    new_df2 = df[df["Indicator Code"].isin([indi_code2])]
    indexFrom = np.where(new_df1.columns == "1960")[0][0]
    indexTo = np.where(new_df1.columns == "2019")[0][0]
    values1 = new_df1.iloc[:, indexFrom:indexTo]
    values2 = new_df2.iloc[:, indexFrom:indexTo]

    index1 = list(values1.index)
    index2 = list(values2.index)
    new_df = new_df1
    new_df.reset_index()

    for i in range(len(new_df)):
        new_df.loc[index1[i], "Indicator Code"] = indi_code1 + '/' + indi_code2
        for col in values1.columns:  # for i in range(len(new_df))
            val1 = values1.loc[index1[i], col]
            val2 = values2.loc[index2[i], col]
            new_df.loc[index1[i], col] = val1 / val2

    mean_60 = []
    mean_70 = []
    mean_80 = []
    mean_90 = []
    mean_00 = []
    mean_10 = []
    for i in new_df.index:
        tmp = list(new_df.loc[i])
        mean_60.append(np.mean(tmp[4:14]))  # 60~69
        mean_70.append(np.mean(tmp[14:24]))  # 70~79
        mean_80.append(np.mean(tmp[24:34]))  # 80~89
        mean_90.append(np.mean(tmp[34:44]))  # 90~99
        mean_00.append(np.mean(tmp[44:54]))  # 00~09
        mean_10.append(np.mean(tmp[54:63]))  # 10~18

    targer_df = new_df[['Country Code', 'Indicator Code']]
    targer_df['1960s'] = mean_60
    targer_df['1970s'] = mean_70
    targer_df['1980s'] = mean_80
    targer_df['1990s'] = mean_90
    targer_df['2000s'] = mean_00
    targer_df['2010s'] = mean_10
    targer_df = targer_df.reset_index()

    return targer_df


def Preprocessing_type3(indi_code1, indi_code2, indi_code3, dataset):  # return Preprocessing(code1/(code2+code3)
    df = dataset
    new_df1 = df[df["Indicator Code"].isin([indi_code1])]
    new_df2 = df[df["Indicator Code"].isin([indi_code2])]
    new_df3 = df[df["Indicator Code"].isin([indi_code3])]
    indexFrom = np.where(new_df1.columns == "1960")[0][0]
    indexTo = np.where(new_df1.columns == "2019")[0][0]
    values1 = new_df1.iloc[:, indexFrom:indexTo]
    values2 = new_df2.iloc[:, indexFrom:indexTo]
    values3 = new_df3.iloc[:, indexFrom:indexTo]

    index1 = list(values1.index)
    index2 = list(values2.index)
    index3 = list(values3.index)
    new_df = new_df1
    new_df.reset_index()

    for i in range(len(new_df)):
        new_df.loc[index1[i], "Indicator Code"] = indi_code1 + '/' + indi_code2 + '/' + indi_code3
        for col in values1.columns:  # for i in range(len(new_df))
            val1 = values1.loc[index1[i], col]
            val2 = values2.loc[index2[i], col]
            val3 = values3.loc[index3[i], col]
            new_df.loc[index1[i], col] = val1 / (val2 + val3)

    mean_60 = []
    mean_70 = []
    mean_80 = []
    mean_90 = []
    mean_00 = []
    mean_10 = []
    for i in new_df.index:
        tmp = list(new_df.loc[i])
        mean_60.append(np.mean(tmp[4:14]))  # 60~69
        mean_70.append(np.mean(tmp[14:24]))  # 70~79
        mean_80.append(np.mean(tmp[24:34]))  # 80~89
        mean_90.append(np.mean(tmp[34:44]))  # 90~99
        mean_00.append(np.mean(tmp[44:54]))  # 00~09
        mean_10.append(np.mean(tmp[54:63]))  # 10~18

    targer_df = new_df[['Country Code', 'Indicator Code']]
    targer_df['1960s'] = mean_60
    targer_df['1970s'] = mean_70
    targer_df['1980s'] = mean_80
    targer_df['1990s'] = mean_90
    targer_df['2000s'] = mean_00
    targer_df['2010s'] = mean_10
    targer_df = targer_df.reset_index()

    return targer_df

##read&plot dataset: 'Series.csv'
readDt=pd.read_csv(os.getcwd()+'\\Indicators_bindWithYear.csv')
seriesCode=readDt['Indicator Code']


#indi_code
#indi_code = "NY.GDP.MKTP.KD.ZG"
#target_dataset = Preprocessing(indi_code, readDt)


#Economic/Financial:all 1960~2018
economy_code=['DC.DAC.TOTL.CD','FM.AST.DOMS.CN','NV.IND.MANF.ZS','BX.KLT.DINV.WD.GD.ZS']
#Infrastructure/Trade: 1960~:index0,1, 1980~:index2,3, 2000~:index4
infra_code=[['TX.VAL.FUEL.ZS.UN','TM.VAL.FUEL.ZS.UN'],['TX.VAL.MANF.ZS.UN','TM.VAL.MANF.ZS.UN'],'IS.AIR.PSGR','IT.CEL.SETS.P2','IT.NET.USER.ZS',]
#Agriculture/Environment/Health: 1960~:index0~3
env_code=['AG.LND.AGRI.ZS','AG.PRD.LVSK.XD','EN.ATM.CO2E.KT','EN.POP.DNST']
#Welfare/Labor/Population: 1960~:index0~2 ,1980~:index3~5 ,2000~: index6
wlfr_code=['SE.SEC.CUAT.LO.ZS','SH.DTH.IMRT','SL.UEM.TOTL.NE.ZS','SH.IMM.IDPT','SL.AGR.EMPL.ZS','SL.GDP.PCAP.EM.KD','SH.XPD.CHEX.PC.CD']
#Population: 1960~:index0~3
popu_code=['SP.POP.TOTL',['SP.POP.TOTL.FE.IN','SP.POP.TOTL.MA.IN'],['SP.POP.1564.TO','SP.POP.0014.TO','SP.POP.65UP.TO']]

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



#economy

print("\n---------------------------------------------------\n")
print("Economic/Financial Section")
cluster4 = []
cluster4.clear()
for i in range(len(dataset_economy)):
    cluster1, kor_index = k_Means(dataset_economy[i])
    #print(cluster1, kor_index)
    cluster2, kor_index = k_Medoids(dataset_economy[i])
    #print(cluster2, kor_index)
    result_list = calculate_cluster(cluster1,cluster2,kor_index)
    print(economy_code[i])
    cluster3 = DBScan(dataset_economy[i])
   # print(all(cluster3))#True = Not Found False = Found
    result_list = index_to_county_code(result_list,dataset_economy[i])
    cluster4.append(result_list)
    print(result_list)
    if all(cluster3) == False:
        dbscan_result = []
        dbscan_result.clear()
        for j in range(0, len(cluster3)):
            if cluster3[j] == cluster3[kor_index]:
                dbscan_result.append(j)
        tmp = []
        tmp.clear()
        for j in dbscan_result:
            tmp.append(dataset_economy[i]["Country Code"].iloc[j])
        print("DBSCAN Result : ")
        print(tmp)

result_section(cluster4)
print("\n---------------------------------------------------\n")
#infra_code
print("Infrastructure/Trade Section")
cluster4 = []
cluster4.clear()
for i in range(len(dataset_infra)):
    cluster1, kor_index = k_Means(dataset_infra[i])
    #print(cluster1, kor_index)
    cluster2, kor_index = k_Medoids(dataset_infra[i])
    #print(cluster2, kor_index)
    result_list = calculate_cluster(cluster1,cluster2,kor_index)
    print(infra_code[i])
    cluster3 = DBScan(dataset_infra[i])
   # print(all(cluster3))#True = Not Found False = Found
    result_list = index_to_county_code(result_list,dataset_infra[i])
    cluster4.append(result_list)
    print(result_list)
    if all(cluster3) == False:
        dbscan_result = []
        dbscan_result.clear()
        for j in range(0, len(cluster3)):
            if cluster3[j] == cluster3[kor_index]:
                dbscan_result.append(j)
        tmp = []
        tmp.clear()
        for j in dbscan_result:
            tmp.append(dataset_infra[i]["Country Code"].iloc[j])
        print("DBSCAN Result : ")
        print(tmp)

result_section(cluster4)

print("\n---------------------------------------------------\n")

#env_code
print("Agriculture/Environment/Health Section")

cluster4 = []
cluster4.clear()
for i in range(len(dataset_environment)):
    cluster1, kor_index = k_Means(dataset_environment[i])
    #print(cluster1, kor_index)
    cluster2, kor_index = k_Medoids(dataset_environment[i])
    #print(cluster2, kor_index)
    result_list = calculate_cluster(cluster1,cluster2,kor_index)
    print(env_code[i])
    cluster3 = DBScan(dataset_environment[i])
   # print(all(cluster3))#True = Not Found False = Found
    result_list = index_to_county_code(result_list,dataset_environment[i])
    cluster4.append(result_list)
    print(result_list)
    if all(cluster3) == False:
        dbscan_result = []
        dbscan_result.clear()
        for j in range(0, len(cluster3)):
            if cluster3[j] == cluster3[kor_index]:
                dbscan_result.append(j)
        tmp = []
        tmp.clear()
        for j in dbscan_result:
            tmp.append(dataset_environment[i]["Country Code"].iloc[j])
        print("DBSCAN Result : ")
        print(tmp)

result_section(cluster4)
print("\n---------------------------------------------------\n")
print("Welfare/Labor/Population Section")

#wlfr_code
cluster4 = []
cluster4.clear()
for i in range(len(dataset_welfare)):
    cluster1, kor_index = k_Means(dataset_welfare[i])
    #print(cluster1, kor_index)
    cluster2, kor_index = k_Medoids(dataset_welfare[i])
    #print(cluster2, kor_index)
    result_list = calculate_cluster(cluster1,cluster2,kor_index)
    print(wlfr_code[i])
    cluster3 = DBScan(dataset_welfare[i])
   # print(all(cluster3))#True = Not Found False = Found
    result_list = index_to_county_code(result_list,dataset_welfare[i])
    cluster4.append(result_list)
    print(result_list)
    if all(cluster3) == False:
        dbscan_result = []
        dbscan_result.clear()
        for j in range(0, len(cluster3)):
            if cluster3[j] == cluster3[kor_index]:
                dbscan_result.append(j)
        tmp = []
        tmp.clear()
        for j in dbscan_result:
            tmp.append(dataset_welfare[i]["Country Code"].iloc[j])
        print("DBSCAN Result : ")
        print(tmp)

result_section(cluster4)

print("\n---------------------------------------------------\n")
print("Population Section")

#popu_code
cluster4 = []
cluster4.clear()
for i in range(len(dataset_population)):
    cluster1, kor_index = k_Means(dataset_population[i])
    #print(cluster1, kor_index)
    cluster2, kor_index = k_Medoids(dataset_population[i])
    #print(cluster2, kor_index)
    result_list = calculate_cluster(cluster1,cluster2,kor_index)
    print(popu_code[i])
    cluster3 = DBScan(dataset_population[i])
   # print(all(cluster3))#True = Not Found False = Found
    result_list = index_to_county_code(result_list,dataset_population[i])
    cluster4.append(result_list)
    print(result_list)
    if all(cluster3) == False:
        dbscan_result = []
        dbscan_result.clear()
        for j in range(0, len(cluster3)):
            if cluster3[j] == cluster3[kor_index]:
                dbscan_result.append(j)
        tmp = []
        tmp.clear()
        for j in dbscan_result:
            tmp.append(dataset_population[i]["Country Code"].iloc[j])
        print("DBSCAN Result : ")
        print(tmp)

result_section(cluster4)