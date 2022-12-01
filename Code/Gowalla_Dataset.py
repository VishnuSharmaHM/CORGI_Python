import pandas as pd
from anytree import RenderTree
from h3 import h3
from Tree import Tree_Generate as TG
from Matrix import Sub_Tree_Obfuscation_Matrix as SOM, RPB, Matrix_Pruning as MP, Precision_Reduction_Hex as PR
import User_Distance as UD
import Config as C

def Gowalla_Dataset(df_train,df_test):
    Hex_val=[]

    Hex_Parent_C=int(C.config['Obfuscation']['Hex_Parent'])
    Hex_leaf_C=int(C.config['Obfuscation']['Hex_leaf'])
    Zero_count_C=float(C.config['Gowalla']['Zero_count'])
    Epsilon=float(C.config['Obfuscation']['Epsilon'])
    Uniform_Prior_C=int(C.config['Obfuscation']['Uniform_Prior'])
    Delta_C=int(C.config['RPB']['Delta'])

    for Index,Row in df_train.iterrows():
        temp=h3.geo_to_h3(Row.Latitude, Row.Longitude,Hex_Parent_C)
        if temp not in Hex_val:
            Hex_val.append(temp)

    print("Unique Hex_Value of latitude and Longitude value - ",len(Hex_val))
    root=TG.generate_location_tree_hex(Hex_val,Hex_Parent_C)
    print("Total Number of leaf node of Tree - ",len(root.leaves))

    hex_ch=[]
    Sub_tree=root.children[0]
    Count=[0 for x in range(len(Sub_tree.leaves))]

    for i in Sub_tree.leaves:
            hex_ch.append(i.Hex_val)

    for Index,Row in df_train.iterrows():
        temp = h3.geo_to_h3(Row.Latitude, Row.Longitude,Hex_leaf_C )
        if temp in hex_ch:
            Count[hex_ch.index(temp)]+=1

    for i in range(len(Count)):
        if Count[i]==0:
            Count[i] =Zero_count_C

    print("Number of leaf in sub tree",len(Sub_tree.leaves))
    sum_count=sum(Count)
    CPR_prior_prob=[]

    for i in range(len(Sub_tree.leaves)):
        if Count[i]/sum_count==0:
            print("Node with Count == 0 is not properly deleted ")
        else:
            CPR_prior_prob.append(Count[i]/sum_count)

    Z,CPR=SOM.Sub_Tree_Obfuscation(Sub_tree,EPSILON=Epsilon,CPR_prior_prob=Uniform_Prior_C)
    print("Number of row before Pruning - ", len(Z))
    Z= RPB.RPB_Main(Z, Sub_tree, Delta_C, CPR=Uniform_Prior_C)
    # UD.Average_Distance(Z, Sub_tree, df_test, Delta_C, CPR_prior_prob=CPR_prior_prob)

if __name__=="__main__":
    df_train = pd.read_csv('../Dataset/London_Train.csv')
    df_test = pd.read_csv('../Dataset/London_Test.csv')
    Gowalla_Dataset(df_train,df_test)