"""
Helper Function for Obfuscation_Matrix.py (send input parameters).
"""
import numpy as np
from Matrix import Obfuscation_CPLEX as OM
from Code import Config as C
import json

def Sub_Tree_Obfuscation(Sub_tree,EPSILON,CPR_prior_prob=0,RPB=0):
    x_coord=[]
    y_coord=[]
    for i in Sub_tree.leaves:
        x_coord.append(i.x1)
        y_coord.append(i.y1)

    if(isinstance(RPB, int)):
        RPB = np.zeros([len(Sub_tree.leaves), len(Sub_tree.leaves)])

    if (isinstance(CPR_prior_prob, int)):
        if len(Sub_tree.leaves)==49:
            # CPR_prior_prob = [1 / len(Sub_tree.leaves) for i in range(len(Sub_tree.leaves))]
            CPR_prior_prob=[0.01692357443138946, 0.011462038733786066, 0.020588552333728576, 0.004455463332255398, 0.04060220617297258,
             0.0016528331716431318, 0.018540476447127304, 0.0037368402141496893, 0.002048075886601272,
             0.056950882109877476, 0.001221659300779706, 0.01699543674320003, 0.012216593007797061,
             0.0010420035212532787, 0.05680715748625633, 0.038625992598181884, 0.008946857820416083,
             0.06539470374761956, 0.007581473896015235, 0.022564765908519278, 0.04599187955876541, 0.004383601020444828,
             0.05648377708310876, 0.011102727174733212, 0.01872013222665373, 0.03891344184542417, 0.0016887643275484171,
             0.06499946103266142, 0.013078940749523912, 0.006611332686572527, 0.0030182170960439797,
             0.005748984944845676, 0.0403147569257303, 0.009952930185764076, 0.02482842873055226, 0.028062232762027954,
             0.0011138658330638496, 0.009270238223563652, 0.007401818116488807, 0.028313750853364954,
             0.006755057310193669, 0.057849161007509614, 0.0033775286550968343, 0.016240882469189033,
             0.0015809708598325607, 0.05339369767525421, 0.004778843735402968, 0.026696848837627105,
             0.0009701412094427077]

        else:
            CPR_prior_prob = [1 / len(Sub_tree.leaves) for i in range(len(Sub_tree.leaves))]

    NR_LOC = len(Sub_tree.leaves)
    target_index = json.loads(C.config.get("Obfuscation","target_index"))
    Z = OM.obf_matrix(x_coord, y_coord, CPR_prior_prob, target_index, NR_LOC, EPSILON,RPB)
    return Z,CPR_prior_prob
