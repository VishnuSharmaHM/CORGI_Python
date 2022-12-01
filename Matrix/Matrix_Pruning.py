"""
Function will prune the Obfuscation Matrix based on the user preference value. It will return new Obfuscation Matrix.
V1 - list has either 0 or -1 value. -1 for nodes to be pruned
V0 - list has all the leaf node
"""

import numpy as np
from Code import Check_Z
from Code import Config as C

def Matrix_Prune(Z,S):
    if len(S)==0:
        return Z
    V1=[0 for i in range(len(Z))]
    count=0
    for i in range(len(Z)):
        if i in S:
            V1[i]=-1
            count+=1
    Z_out =np.zeros((len(V1)-count,len(V1)-count))
    count_i=0

    for i in range(len(V1)):
        count_j = 0
        if(V1[i]==-1):
            continue
        for j in range(len(V1)):
            if(V1[j]==-1):
                continue
            nf=0
            for k in range(len(V1)):
                if(V1[k]==-1):
                    nf+=Z[i][k]
            if nf==1:
                print("Exception is raised because of nf==1 ")
                exit()
            else:
                Z_out[count_i][count_j] = Z[i][j] / (1 - nf)
            count_j+=1
        count_i+=1
    return Z_out