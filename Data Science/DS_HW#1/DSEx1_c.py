from matplotlib import pyplot as plt
import numpy as np
import math
import random

count=[0]*10
for i in range(0,10000): #get 10000 random integers and count a list.
    tmp=random.randint(0,9)
    count[tmp]=count[tmp]+1
print(count)

numbers=list(range(0,10))
plt.pie(count,labels=numbers,autopct='%1.2f%%')
plt.show()
