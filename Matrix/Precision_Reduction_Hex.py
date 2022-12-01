"""
Function will generate Obfuscation matrix higher level node depending on Obfuscation matrix of children node.
"""

from Code import Check_Z
from Code import Config as C
import json,numpy

def Precision_Reduction(Sub_tree, CPR_prior_prob, Z, Precision_level=0):

    Zip_All=[]
    Zip = []
    Zip_Count = []
    lst = []
    Prior=[]
    Tree_Node=[]
    V1=json.loads(C.config.get("Precision_reduction", "Prune_Index"))

    Pruned_Index=[0 for i in range(len(Z)+len(V1))]
    for i in range(len(Z)):
        if i in V1:
            Pruned_Index[i]=-1

    for i in range(len(Sub_tree.leaves)):
        if(Pruned_Index[i]!=-1):
            Zip_All.append(Sub_tree.leaves[i].Hex_val)
            Prior.append(CPR_prior_prob[i])
            Tree_Node.append(Sub_tree.leaves[i])

    for i in range(len(Tree_Node)):
        if Tree_Node[i].parent not in Zip:
            Zip.append(Tree_Node[i].parent)
            Zip_Count.append(i)

    Zip_Count.append(len(Zip_All))
    Z_out = [[0 for i in range(len(Zip))] for i in range(len(Zip))]

    for i in range(len(Zip_Count) - 1):
        lst.append([i for i in range(Zip_Count[i], Zip_Count[i + 1])])

    for Si in range(len(Zip)):
        for Sj in range(len(Zip)):
            Pr_ij = 0
            Pr_Si = 0
            for Su in lst[Si]:
                Pr_j = 0
                for Sv in lst[Sj]:
                    Pr_j += Z[Su][Sv]
                Pr_ij += (Prior[Su] * Pr_j)
            for i in lst[Si]:
                Pr_Si +=Prior[i]

            Z_out[Si][Sj] = Pr_ij / Pr_Si
    Z_out = numpy.asarray(Z_out)
    return Z_out
