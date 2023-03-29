"""
create data frame from dta generate by ABAQUS models 
"""
import pandas as pd
import numpy as np

fname ='M.txt'
r = np.genfromtxt(fname,delimiter=',',dtype=None, names=True);
data=np.zeros((len(r),len(r[0])+1))

for i in range(len(r)):
    for j in range(len(r[i])):
        data[i,j]=float(r[i][j]);

df = pd.DataFrame(data=data, columns=list(range(data.shape[1])))

fname1 ='output.txt'
r1 = np.genfromtxt(fname1,delimiter=',',dtype=None, names=True);
output=np.zeros(len(r1))

for i in range(len(r1)):
    output[i]=float(r1[i][0])
    

x=df
y=output 



    
    
    
    