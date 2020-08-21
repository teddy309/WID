#!/usr/bin/env python
# coding: utf-8

# # FIT5202 Data processing for big data
# 
# ##  Activity: MongoDB and Apache Spark Data Visualization (Titanic Dataset)
# 
# Last week we looked into MongoDB - a NoSQL database and how Apache Spark can extend MongoDB's analytics capabilities. We used **MongoDB Connector for Apache Spark** for this activity. 
# 
# Today we are going to learn visualisation of our data stored in MongoDB. We will take the **Titanic Dataset** to analyze the data and use data visualization to get a deeper understanding. But before that let's learn some basics of data visualisation.
# 
# ## What is data visualization?
# Data visualization is presenting data into an appropriate pictorial or graphical form.
# For example, if we want to understand how the area of the house has an influence on the price of the house. A scatter plot between the area of the house and price of the house would quickly help us gain the understanding.
# 
# ## Why data visualization is useful?
# A picture says a thousand words. Our brains process pictures and colors better than numbers or text. When we see the data related to area of the house and its prices, we take time to process the information and come to a conclusion. However, when we have a scatter plot, with a glance we are able to understand the relationship, identify trends and also spot the outliers.
# This visualization of data becomes even more important when we have large datasets. It is difficult for human brain to analyze the massive amount of data without any pictorial representation and that’s when data visualization becomes important.
# 
# 
# 

# ## SparkContext and SparkSession
# We will use and import **`SparkContext`** from **`pyspark`**, which is the main entry point for Spark Core functionality. The **`SparkSession`** object provides methods used to create DataFrames from various input sources. 
# A [DataFrame](https://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.DataFrame) is equivalent to a relational table in Spark SQL, and can be created using various functions in SparkSession. Once created, it can be manipulated using the various domain-specific-language (DSL) functions defined in: [DataFrame](https://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.DataFrame), [Column](https://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.Column).
# 
# 

# In[ ]:


import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.0 pyspark-shell'
# create entry points to spark
from pyspark import SparkContext # Spark
from pyspark.sql import SparkSession # Spark SQL

# We add this line to avoid an error : "Cannot run multiple SparkContexts at once". 
# If there is an existing spark context, we will reuse it instead of creating a new context.
sc = SparkContext.getOrCreate()

# local[*]: run Spark locally with as many working processors as logical cores on your machine.
# In the field of `master`, we use a local server with as many working processors (or threads) as possible (i.e. `local[*]`). 
# If we want Spark to run locally with 'k' worker threads, we can specify as `local[k]`.
# The `appName` field is a name to be shown on the Sparking cluster UI. 

# If there is no existing spark context, we now create a new context
if (sc is None):
    sc = SparkContext(master="local[*]")
spark = SparkSession(sparkContext=sc)        .builder        .appName("MongoDB and Apache Spark Data Visualization")        .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.11:2.4.0")        .config("spark.mongodb.input.uri", "mongodb://127.0.0.1/fit5202_db.wk05_titanic_coll")        .config("spark.mongodb.output.uri", "mongodb://127.0.0.1/fit5202_db.wk05_titanic_coll")        .getOrCreate()


# ### Write to MongoDB
# We will use MongoDB as our datasource. Therefore, as a data loading step we read the csv file using spark session and insert all the records into MongoDB similar to what we did last week.

# In[ ]:


titanic_df = spark.read.csv('titanic_passenger_list.csv', header=True, inferSchema=True)
# Write to MongoDB
titanic_df.write.format("com.mongodb.spark.sql.DefaultSource").mode("overwrite").save()


# ### Read from MongoDB
# You can create a Spark DataFrame to hold data from the MongoDB collection specified in the `spark.mongodb.input.uri` option which your SparkSession option is using. Assign the collection to a DataFrame with `spark.read()`.

# In[ ]:


titanic_mongodb_df = spark.read.format("com.mongodb.spark.sql.DefaultSource").load()


# To read the contents of the DataFrame, use the `show()` method. The description of the data columns are as follows:
# - survival - Survival (0 = No; 1 = Yes)
# - class - Passenger Class (1 = 1st; 2 = 2nd; 3 = 3rd)
# - name - Name
# - sex - Sex
# - age - Age
# - sibsp - Number of Siblings/Spouses Aboard
# - parch - Number of Parents/Children Aboard
# - ticket - Ticket Number
# - fare - Passenger Fare
# - cabin - Cabin
# - embarked - Port of Embarkation (C = Cherbourg; Q = Queenstown; S = Southampton)
# - boat - Lifeboat (if survived)
# - body - Body number (if did not survive and body was recovered)
# 

# In[ ]:


titanic_mongodb_df.show(5)


# Spark samples the records to infer the schema of the collection. The `printSchema()` method prints out the DataFrame’s schema.

# In[ ]:


titanic_mongodb_df.printSchema()


# ### Data visualization using Matplotlib
# `Matplotlib` is a Python 2D plotting library which produces publication quality figures in a variety of hardcopy formats and interactive environments across platforms. Matplotlib can be used in Python scripts, the Python and IPython shells, the Jupyter notebook, web application servers, and four graphical user interface toolkits. Matplotlib tries to make easy things easy and hard things possible. You can generate plots, histograms, power spectra, bar charts, errorcharts, scatterplots, etc., with just a few lines of code. 

# In[ ]:


# Uncomment the command below to install matplotlib library
# !pip install matplotlib
import matplotlib.pyplot as plt
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')


# #### 1.  Bar chart

# In[ ]:


# How many male and female passengers in the Titanic?
gender_count = titanic_mongodb_df.groupBy('sex').count().sort('sex', ascending=False).collect()


# In[ ]:


# prepare data
y_axis = [row['count'] for row in gender_count]

# plot
bar_width = 0.5
objects= ('Male', 'Female')
y_pos = np.arange(len(objects))

plt.bar(y_pos, y_axis, bar_width, align='center', color='C0')
plt.xticks(y_pos, objects)
plt.xlabel('Sex')
plt.ylabel('Count of Passengers')
plt.title('How many male and female passengers in the Titanic?')
plt.tight_layout()
plt.show()
# We see more male passenger than female


# In[ ]:


gender_count_sampled = titanic_mongodb_df.sample(False, 0.5, seed=123).groupBy('sex').count().sort('sex', ascending=False).collect()


# In[ ]:


# Sampling or No Sampling?

# prepare data
y_axis_no_sampling = [row['count'] for row in gender_count]
y_axis_sampling = [row['count'] for row in gender_count_sampled]

# plot
bar_width = 0.5
objects= ('Male', 'Female')
y_pos = np.arange(len(objects))
f, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,5), tight_layout=True, sharey=True)


ax1.bar(y_pos, y_axis_no_sampling, bar_width, align='center', color='C0')
ax1.set_xticks(y_pos)
ax1.set_xticklabels(objects)
ax1.set_xlabel('Sex')
ax1.set_ylabel('Count of Passengers')
ax1.set_title('No Sampling')

ax2.bar(y_pos, y_axis_sampling, bar_width, align='center', color='C0')
ax2.set_xticks(y_pos)
ax2.set_xticklabels(objects)
ax2.set_xlabel('Sex')
ax2.set_title('Sampling')

plt.tight_layout()
plt.show()


# In[ ]:


# Passengers based on the class in the Titanic
class_count = titanic_mongodb_df.groupBy('pclass').count().sort('pclass').collect()


# In[ ]:


# prepare data
y_axis = [row['count'] for row in class_count]

# plot
bar_width = 0.5
objects= ('1', '2', '3')
y_pos = np.arange(len(objects))

plt.bar(y_pos, y_axis, bar_width, align='center', color='C0')
plt.xticks(y_pos, objects)
plt.xlabel('Class')
plt.ylabel('Count of Passengers')
plt.title('Passengers based on the class in the Titanic')
plt.tight_layout()
plt.show()
# We see more passengers from class 3.


# In[ ]:


# Gender ratio among classes
grc_count = titanic_mongodb_df.groupBy('pclass', 'sex').count().sort('pclass').collect()


# In[ ]:


# prepare data
male = [row['count'] for row in grc_count if row['sex'] == 'male']
female = [row['count'] for row in grc_count if row['sex'] == 'female']

# plot
bar_width = 0.4
plt.bar(y_pos, male, bar_width, align='center', color='C0', label='Male')
plt.bar(y_pos + bar_width, female, bar_width, align='center', color='C1', label='Female')
plt.xticks(y_pos + 0.5 * bar_width, [1,2,3])
plt.xlabel('Class')
plt.ylabel('Count of Passengers')
plt.legend(loc='upper left')
plt.title('Gender ratio among the classes')
plt.tight_layout()
plt.show()


# ### Histogram

# In[ ]:


# Age distribution
df = titanic_mongodb_df.select('age').collect()


# In[ ]:


# prepare data
age = [row['age'] for row in df if row['age'] != None]
minm = min(age)
maxm = max(age)

# plot
plt.hist(age, bins = 10, range = (minm, maxm))
plt.title('Age distribution')
plt.xlabel('Age')
plt.ylabel('Count of Passengers')
plt.show()


# In[ ]:


df = titanic_mongodb_df.select('age', 'survived', 'sex').collect()


# In[ ]:


# prepare data
age_m_0=[row['age'] for row in df if row['sex'] == 'male' and row['survived'] == 0 and row['age'] != None]
age_m_1=[row['age'] for row in df if row['sex'] == 'male' and row['survived'] == 1 and row['age'] != None]
age_f_0=[row['age'] for row in df if row['sex'] == 'female' and row['survived'] == 0 and row['age'] != None]
age_f_1=[row['age'] for row in df if row['sex'] == 'female' and row['survived'] == 1 and row['age'] != None]

# plot
n_bins = 12
f, ax = plt.subplots(2, 2, figsize=(10,6), tight_layout=True,sharex=True, sharey=True)

ax[0][0].hist(age_m_0, bins=n_bins, color='C3', label='Deceased')
ax[0][0].set_title('Male')
ax[0][0].set_ylabel('Count of Passengers')

ax[0][1].hist(age_f_0, bins=n_bins, color='C3',  label='Deceased')
ax[0][1].set_title('Female')
ax[0][1].legend()

ax[1][0].hist(age_m_1, bins=n_bins, color='C0',  label='Survived')
ax[1][0].set_ylabel('Count of Passengers')
ax[1][0].set_xlabel('Age')

ax[1][1].hist(age_f_1, bins=n_bins, color='C0', label='Survived')
ax[1][1].set_xlabel('Age')
ax[1][1].legend()
plt.tight_layout()
plt.show()


# #### Scatter Plot

# In[ ]:


# Fare based on Age
df = titanic_mongodb_df.select('fare','age', 'survived' ).collect()


# In[ ]:


# prepare data
fare_1 = [row['fare'] for row in df if row['survived'] == 1]
age_1 = [row['age'] for row in df if row['survived'] == 1]
fare_0 = [row['fare'] for row in df if row['survived'] == 0]
age_0 = [row['age'] for row in df if row['survived'] == 0]

# plot
plt.scatter(fare_1, age_1, c='C0', label='Survived')
plt.scatter(fare_0, age_0, c='C1', label='Ceased')
plt.xlabel('Fare')
plt.ylabel('Age')
plt.legend(loc='upper right')
plt.title('Fare based on Age')
plt.tight_layout()
plt.show()


# In[ ]:


# Sampling or No Sampling?

# Approximate Sampling

age_fare = titanic_mongodb_df.select('fare','age', 'survived' ).collect()

age_fare_sampled_50 = titanic_mongodb_df.sample(False, 0.5, seed=123).select('fare','age', 'survived' ).collect()

age_fare_sampled_25 = titanic_mongodb_df.sample(False, 0.25, seed=123).select('fare','age', 'survived' ).collect()


# In[ ]:


# prepare data
fare_1 = [row['fare'] for row in age_fare if row['survived'] == 1]
age_1 = [row['age'] for row in age_fare if row['survived'] == 1]
fare_0 = [row['fare'] for row in age_fare if row['survived'] == 0]
age_0 = [row['age'] for row in age_fare if row['survived'] == 0]

fare_s50_1 = [row['fare'] for row in age_fare_sampled_50 if row['survived'] == 1]
age_s50_1 = [row['age'] for row in age_fare_sampled_50 if row['survived'] == 1]
fare_s50_0 = [row['fare'] for row in age_fare_sampled_50 if row['survived'] == 0]
age_s50_0 = [row['age'] for row in age_fare_sampled_50 if row['survived'] == 0]

fare_s25_1 = [row['fare'] for row in age_fare_sampled_25 if row['survived'] == 1]
age_s25_1 = [row['age'] for row in age_fare_sampled_25 if row['survived'] == 1]
fare_s25_0 = [row['fare'] for row in age_fare_sampled_25 if row['survived'] == 0]
age_s25_0 = [row['age'] for row in age_fare_sampled_25 if row['survived'] == 0]


# In[ ]:


# plot
f, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12,4), sharey=True)
ax1.scatter(fare_1, age_1, c='C0', label='Survived')
ax1.scatter(fare_0, age_0, c='C1', label='Ceased')
ax1.set_xlabel('Fare')
ax1.set_ylabel('Age')
ax1.legend(loc='upper right')
ax1.set_title('No Sampling')

ax2.scatter(fare_s50_1, age_s50_1, c='C0', label='Survived')
ax2.scatter(fare_s50_0, age_s50_0, c='C1', label='Ceased')
ax2.set_xlabel('Fare')
ax2.legend(loc='upper right')
ax2.set_title('Sampling (50% data returned)')

ax3.scatter(fare_s25_1, age_s25_1, c='C0', label='Survived')
ax3.scatter(fare_s25_0, age_s25_0, c='C1', label='Ceased')
ax3.set_xlabel('Fare')
ax3.legend(loc='upper right')
ax3.set_title('Sampling (25% data returned)')

f.suptitle('Survival by Gender, Age and Fare', size= 16, y=1.05)
plt.tight_layout()
plt.show()


# In[ ]:


# Survival by Gender, Age and Fare
df = titanic_mongodb_df.select('fare', 'age', 'survived', 'sex').collect()


# In[ ]:


# prepare data
fare_1_f = [row['fare'] for row in df if row['survived'] == 1 and row['sex']== 'female']
age_1_f = [row['age'] for row in df if row['survived'] == 1 and row['sex']== 'female']
fare_0_f = [row['fare'] for row in df if row['survived'] == 0 and row['sex']== 'female']
age_0_f = [row['age'] for row in df if row['survived'] == 0 and row['sex']== 'female']

fare_1_m = [row['fare'] for row in df if row['survived'] == 1 and row['sex']== 'male']
age_1_m = [row['age'] for row in df if row['survived'] == 1 and row['sex']== 'male']
fare_0_m = [row['fare'] for row in df if row['survived'] == 0 and row['sex']== 'male']
age_0_m = [row['age'] for row in df if row['survived'] == 0 and row['sex']== 'male']

# plot
f, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,4), sharey=True)
ax1.scatter(fare_1_m, age_1_m, c='C0', label='Survived')
ax1.scatter(fare_0_m, age_0_m, c='C1', label='Ceased')
ax1.set_xlabel('Fare')
ax1.set_ylabel('Age')
ax1.legend(loc='upper right')
ax1.set_title('Male')

ax2.scatter(fare_1_f, age_1_f, c='C0', label='Survived')
ax2.scatter(fare_0_f, age_0_f, c='C1', label='Ceased')
ax2.set_xlabel('Fare')
ax2.legend(loc='upper right')
ax2.set_title('Female')

f.suptitle('Survival by Gender, Age and Fare', size= 16, y=1.05)
plt.tight_layout()
plt.show()


# ### Exercise: Survival by class, Age and Fare

# In[ ]:


# Write your code here


# ### Box Plot

# In[ ]:


# Survival by Age
df = titanic_mongodb_df.select('age','survived').collect()


# In[ ]:


# prepare data
age_0 = [row['age'] for row in df if row['survived'] == 0 and row['age'] != None]
age_1 = [row['age'] for row in df if row['survived'] == 1 and row['age'] != None]
age = [age_0, age_1]

# plot
plt.boxplot(age)
plt.xticks([1,2], ['Ceased', 'Survived'])
plt.xlabel('Survival')
plt.ylabel('Age')
plt.title('Survival by Age')
plt.tight_layout()
plt.show()


# In[ ]:


df = titanic_mongodb_df.groupBy('embarked').count().orderBy('embarked')
df.show()


# ### Pie Chart

# In[ ]:


# People boarding Titanic from different location
df = titanic_mongodb_df.groupBy('embarked').count().orderBy('embarked').collect()


# In[ ]:


# prepare data
count = [row['count'] for row in df]

# plot
labels=['Unknown', 'Cherbourg', 'Queenstown', 'Southampton']
plt.pie(count, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
plt.title('Percentage of passangers based on pickup location')
plt.show()
# Additional passengers were picked up at Cherbourg and Queenstown."


# Congratulations on finishing this activity. Now, think about how does data visualization help and improve your understanding of the data.
# - It helps to comprehend the data easily
# - It helps to identify relationships and patterns
# - It helps to check for emerging trends in the data
# - It helps to create a story from the data and communicate to stakeholders
