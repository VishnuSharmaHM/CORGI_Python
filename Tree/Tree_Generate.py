from Tree import Node_Class as nc
from anytree import search
from h3 import h3
from Code import Config as C
# from Code importlib.reload(Config)
def find_subtree(location_tree, search_node):
    parent_node = search.findall(location_tree, filter_=lambda node: node.Hex_val in search_node)
    return parent_node[0]

def generate_location_tree_hex(root_value):
    Hex_Parent_C = int(C.config['Obfuscation']['Hex_Parent'])
    Hex_Leaf_C=int(C.config['Obfuscation']['Hex_leaf'])
    root = nc.Location('root')
    for i in root_value:
        lst = h3.h3_to_geo(i)
        temp=nc.Location(i,lst[0],lst[1],parent=root)
        val = h3.h3_to_children(i, res=Hex_Parent_C+1)
        val=list(val)
        val.sort()

        for j in val:
            lst=h3.h3_to_geo(j)
            temp1=nc.Location(j,lst[0],lst[1], parent=temp)

            if Hex_Leaf_C-Hex_Parent_C == 2:
                val1 = h3.h3_to_children(j, res=Hex_Parent_C+2)
                val1=list(val1)
                val1.sort()
                for k in val1:
                    lst1 = h3.h3_to_geo(k)
                    nc.Location(k, lst1[0], lst1[1], parent=temp1)
    return root

#TODO: Tree generation should be seperate from matrix generation Code.