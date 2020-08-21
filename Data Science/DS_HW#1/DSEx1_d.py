from matplotlib import pyplot as plt
import numpy as np
import math
import random

np.set_printoptions(suppress=True)
np.set_printoptions(precision=2)

n=int(input("Put an integer n: "))

M=np.random.random((n,n))
print("--Matrix M------------------")
print(M)
RevM=np.linalg.inv(M)
print("--Reverse matrix M^-1-------")
print(RevM)
print("--Product of M&M^-1---------")
print(np.abs(M@RevM))
print("--Program End---------------")
finish=input()
