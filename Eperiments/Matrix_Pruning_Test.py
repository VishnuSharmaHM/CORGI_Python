import numpy as np
import pandas as pd
from Tree import Tree_Generate as TG, H3_Tree_User as HTU
from Matrix import Matrix_Pruning as MP
import json
from Code import Config as C,Check_Z as CZ

Z=np.zeros(([49,49]))
df = pd.read_csv('../Dataset/Z_RPB.csv')
Prune_Index=json.loads(C.config.get("Precision_reduction", "Prune_Index"))
for Index,Row in df.iterrows():
    for i in range(len(Row)):
        Z[Index][i]=Row[i]

root_value = HTU.Hex_Value_Address()
root = TG.generate_location_tree_hex(root_value)
Sub_tree = root.children[0]

Prune_Index=json.loads(C.config.get("Precision_reduction", "Prune_Index"))
Epsilon_c=int(C.config['Obfuscation']['Epsilon'])
CPR_prior_prob=[1 / (len(Sub_tree.leaves)) for i in range(len(Sub_tree.leaves)-len(Prune_Index))]

x_coord = []
y_coord = []
for i in range(len(Sub_tree.leaves)) :
    if i not in Prune_Index:
        x_coord.append(Sub_tree.leaves[i].x1)
        y_coord.append(Sub_tree.leaves[i].y1)

Z_MP=MP.Matrix_Prune(Z,Prune_Index)
CZ.isValid_Z(Z_MP,Epsilon_c,CPR_prior_prob,x_coord,y_coord)