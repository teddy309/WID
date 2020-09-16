from matplotlib import pyplot as plt
import numpy as np
import math

height=[163,177,179,168,174,176,162,172,155,157,179,155,178,165,179,163,168,170,161,167,165,183,172,175,160,189,167,170,163,160,178,177,175,171,163,169,165,181,175,170,181,177,172,168,160,175,173,158,158,158,175,160]

heightHIGH=[]
heightLOW=[]

def sortHeight(h):
    if h>170:
        heightHIGH.append(h)
    else:
        heightLOW.append(h)
def mean2(S):
    mean=0
    for i in range(0,len(S)):
        mean=mean+S[i]**2
    mean=mean/len(S)
    return mean

for i in range(0,len(height)):
    sortHeight(height[i])

meanH=sum(heightHIGH)/len(heightHIGH)
meanL=sum(heightLOW)/len(heightLOW)

varH=mean2(heightHIGH)-meanH**2
varL=mean2(heightLOW)-meanL**2
sdH=varH**0.5
sdL=varL**0.5

print("tall group(mean: {0}, variance: {1}, standard deviation: {2})".format(meanH,varH,sdH))
print("small group(mean: {0}, variance: {1}, standard deviation: {2})".format(meanL,varL,sdL))

plotData=[heightHIGH,heightLOW]
plt.boxplot(plotData)
plt.xlabel('group(1:group over 170cm,2:group smaller than 170cm)')
plt.ylabel('height')
plt.show()

