#python3.7
import os

def countNNG(inputFile):
    arr=[]
    while True:
        line=inputFile.readline()
        if not line:
            break
        line=line.split()
        if line[1]=='NNG':
            arr.append(line[0])
    #print(line[0],' ',line[1])
    
    return arr#arr.head(5)

f=open(os.getcwd()+"\\input.txt",'r')
BoW=countNNG(f)
print(BoW)

f=open(os.getcwd()+"\\output.txt",'w')#C:/file_dir/filename
for i in range(len(BoW)):
    line=BoW[i]+'\t'+str(i)+'\n'
    f.write(line)
f.close()






'''
def makeCase(k,i,iIter):
    tmp=[]
    num=iIter
    if 0<num:
        for i in range(iIter):
            tmp.append(i)
    while(True):
        if num<k:
            break
        else:
            num=num+i
            tmp.append(num)
    print(tmp)
    return tmp
        

def count(N,k):
    count=[]
    for i in range(k):
        temp=[]
        case=[]
        while(True): #make every case with i 
            tmp=[]
            iIter=0
            newCase=makeCase(k,i,iIter)
            if len(newCase)>0:
                iIter=iIter+1
                case.append(newCase)
            else:
                break
        count.append(case)
        #print(case)
    return count
#count.append(numOfCase(range(N),i))



print(count(5,3))

while(True):
    N,k=map(int,input('put two int values(N,k): ').split())
    if N>20:
        print('N overcome 20!!')
    else:
        
        print('combination({},{}) is {}'.format(N,k,count(N,k)))
'''
