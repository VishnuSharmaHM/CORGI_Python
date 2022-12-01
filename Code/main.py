import json,Quality_loss_1 as Q
from Tree import Tree_Generate as TG, H3_Tree_User as HTU
from Matrix import Sub_Tree_Obfuscation_Matrix as SOM,RPB
import Config as C
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="geoapiExercises")

def main():

    Prune_Index=json.loads(C.config.get("Precision_reduction", "Prune_Index"))
    Epsilon_c=json.loads(C.config.get("Obfuscation", "Epsilon"))
    Delta_c=int(C.config['RPB']['Delta'])
    root_value = HTU.Hex_Value_Address()
    root = TG.generate_location_tree_hex(root_value)
    # Sub_tree = root.children[0]
    Sub_tree=root
    print(len(Sub_tree.leaves))
    Z, CPR_prior_prob = SOM.Sub_Tree_Obfuscation(Sub_tree=Sub_tree, EPSILON=Epsilon_c[0])
    # print(Z)
    # out=[]
    # for node in Sub_tree.leaves:
    #     print(node.x1,",",node.y1)
    # print(out)
    # Z_RPB = RPB.RPB_Main(Z, Sub_tree, Delta=Delta_c, Epsilon=Epsilon_c[0], CPR=CPR_prior_prob)
    # for index in range(len(Epsilon_c)):
    #     Z,CPR_prior_prob=SOM.Sub_Tree_Obfuscation(Sub_tree=Sub_tree,EPSILON=Epsilon_c[index])
    #     Z_RPB = RPB.RPB_Main(Z, Sub_tree, Delta=Delta_c, Epsilon=Epsilon_c[index], CPR=CPR_prior_prob)
    #     Z=Z_RPB
    #     Q.Quality_loss(Z=Z, Tree=Sub_tree,index=index)


if __name__ == '__main__':
    main()

    # np.savetxt("../Dataset/Z.csv", Z, delimiter=",")
    # Q.Quality_loss(Z,Sub_tree)
    # for pre, _, node in RenderTree(Sub_tree):
    #     treestr = u"%s%s" % (pre, node.Hex_val)
    #     print(treestr.ljust(8),',', node.x1,',', node.y1)
    # Z_RPB = RPB.RPB_Main(Z, Sub_tree, Delta=Delta_c)
    # print(Z)
    # Q.Quality_loss(Z,Sub_tree)
    # print("Number of row before Pruning - ", len(Z))
    # np.savetxt("../Dataset/Z.csv", Z, delimiter=",")
    # print("Number of row after Pruning - ", len(Z_MP))
    # Z_MP= MPR.Matrix_Prune(Z,Prune_Index)
    # Z_PR=PR.Precision_Reduction(Sub_tree,CPR_prior_prob,Z_MP)
    # print("Z after Precision reduction\n",Z_PR)
    #Hex_value=[]
    # for temp in Sub_tree.leaves:
    #     Hex_value.append(h3.geo_to_h3(temp.x1,temp.y1,8))
    # print(Hex_value.index(h3.geo_to_h3(37.79479206,-122.3930705,8)))