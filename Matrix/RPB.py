import itertools
import numpy as np
from Matrix import Sub_Tree_Obfuscation_Matrix as SOM, Obfuscation_CPLEX as OM
from Code import Config as C
import math
import matplotlib.pyplot as plt

def RPB_Main(Z,Tree,Delta,Epsilon,CPR=0):
    NR_LOC=len(Tree.leaves)
    RPB=np.zeros([NR_LOC,NR_LOC])
    RPB_Iteration_C=int(C.config['RPB']['Iteration'])
    Convergence_value=[]
    for i in range(RPB_Iteration_C):
        RPB=RPB_Calculator(Z,Tree,Delta,RPB,Epsilon)
        try:
            Z_RPB, CPR = SOM.Sub_Tree_Obfuscation(Tree,CPR_prior_prob=CPR,RPB=RPB,EPSILON=Epsilon)
            difference=np.absolute(Z-Z_RPB)
            Z=Z_RPB
            # print(np.mean(difference))
        except:
            print("Error in RPB for Epsilon = ",Epsilon," and Iteration = ",i)
            return Z
    # Convergence_value.append(np.mean(difference))

    # X_axis=[i+1 for i in range(len(Convergence_value))]
    # plt.plot(X_axis,Convergence_value)
    # plt.xlabel("Iteration")
    # plt.ylabel("Convergence Value")
    # plt.title('Robust Obfuscation Matrix')
    # plt.show()
    # print("Convergence Value -", Convergence_value)
    return Z

def RPB_Calculator(Z,Tree,Delta,RPB,Epsilon):
    NR_LOC=len(Tree.leaves)
    for i in range(NR_LOC):
        for j in range(NR_LOC):
            Z_Row = Z[i].copy()
            Z_Row[i]=-1
            Z_Row = np.sort(Z_Row)[::-1]
            topk_sum=np.sum(Z_Row[:Delta])
            # print("Topk before",topk_sum)
            if topk_sum>0.9:
                topk_sum=0.8
            # print("Topk after", topk_sum)
            X1=Tree.leaves[i].x1
            X2 = Tree.leaves[j].x1
            Y1 = Tree.leaves[i].y1
            Y2 = Tree.leaves[j].y1
            distance = OM.Distance_Calculation(X1, X2, Y1, Y2)
            # print("Distance",distance)
            Maximum=(1-(topk_sum/math.exp(Epsilon*distance)))/(1-topk_sum)
            RPB[i][j]=min(Maximum,math.exp(Epsilon*distance))
            # print('Maximum ',Maximum)
    return RPB