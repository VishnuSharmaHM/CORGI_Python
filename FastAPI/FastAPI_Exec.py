from Tree import Tree_Generate as TG, H3_Tree_User as HTU
from Matrix import Sub_Tree_Obfuscation_Matrix as SOM
from Code import Config as C
from geopy.geocoders import Nominatim
from Matrix import Precision_Reduction_Hex as PR
import json
geolocator = Nominatim(user_agent="geoapiExercises")

def Fast_API(item):
    Latitude = str(item.Real_location[0])
    Longitude = str(item.Real_location[1])
    location = geolocator.reverse(Latitude + "," + Longitude)
    C.config['Obfuscation']['address'] = str(location)
    hex_parent = int(C.config['Obfuscation']['hex_parent'])
    C.config['Obfuscation']['hex_leaf'] = str(hex_parent + item.Privacy_level)
    C.config['Obfuscation']['target_index'] = json.dumps(item.Target_location)
    with open(C.file, 'w') as configfile:
        C.config.write(configfile)
    Epsilon_c = int(C.config['Obfuscation']['Epsilon'])
    root_value = HTU.Hex_Value_Address()
    root = TG.generate_location_tree_hex(root_value)
    Sub_tree = root.children[0]
    Z, CPR_prior_prob = SOM.Sub_Tree_Obfuscation(Sub_tree=Sub_tree, EPSILON=Epsilon_c)

    if(item.Precision_level==1):
        Z = PR.Precision_Reduction(Sub_tree, CPR_prior_prob, Z)

    weight=[0 for i in range(49)]
    latitude=[0 for i in range(49)]
    longitude=[0 for i in range(49)]
    for i in range(len(Sub_tree.leaves)):
        latitude[i]=Sub_tree.leaves[i].x1
        longitude[i]=Sub_tree.leaves[i].y1
    Z_Row = Z[0].copy()
    for index in range(len(Z_Row)):
        if Z_Row[index]==0:
            weight[index]=2
        elif 0<Z_Row[index]<=0.5:
            weight[index]=3
        elif 0.5<Z_Row[index]<=0.75:
            weight[index]=4
        else:
            weight[index]=5
    real_location_coorinates=[float(Latitude),float(Longitude)]
    return [real_location_coorinates,latitude,longitude,weight]