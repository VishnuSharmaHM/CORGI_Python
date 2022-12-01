import json
from h3 import h3
import numpy as np
import random
from Matrix import Matrix_Pruning as MP
from Code import Config as C
import math
# TODO:If Precision level >0 call Precision reduction

def Average_Distance(Z,Sub_tree,df_test,Delta,CPR_prior_prob,Precision_level=0):
    Hex_val=[]
    Target_Hex=[]
    User_target_real=[]
    User_target_fake=[]

    target_index = json.loads(C.config.get("Obfuscation","target_index"))
    Fake_index_iteration=int(C.config['User_Distance']['Fake_index_iteration'])

    for i in range(len(Sub_tree.leaves)):
        Hex_val.append(Sub_tree.leaves[i].Hex_val)
        if i in target_index:
            Target_Hex.append(Sub_tree.leaves[i].Hex_val)

    for i in df_test.User_ID.unique():
        df1=df_test[df_test.User_ID==i]
        Average_real=0
        count=0

        for Index, Row in df1.iterrows():
            Target_real_distance = 0
            temp = h3.geo_to_h3(Row.Latitude, Row.Longitude, 7)

            if temp in Hex_val:
                count+=1
                Real_Index=Hex_val.index(temp)

                for i in range(len(target_index)):
                    Target_real_distance+=Euclidean_distance(temp, Target_Hex[i])
                Target_real_distance=Target_real_distance/len(target_index)

                Z_MP = Z.copy()
                count=1
                S=[]
                Hex_val_MP=[]
                if Delta!=0:
                    while(True):
                        rand_index = int(random.randint(0, len(Z)))
                        if count>Delta:
                            break
                        if rand_index==Real_Index or rand_index in target_index:
                            continue
                        if rand_index in S:
                            continue
                        else:
                            S.append(rand_index)
                            count+=1
                    Z_MP,V1=MP.Matrix_Prune(Z_MP,S)

                for i in range(len(Hex_val)):
                    if i in S:
                        pass
                    else:
                        Hex_val_MP.append(Hex_val[i])
                if temp not in Hex_val_MP:
                    continue

                Real_Index = Hex_val_MP.index(temp)
                Z_Row=Z_MP[Real_Index]
                cum_sum = [0 for a in range(len(Z_Row))]
                sum_val = 0

                for i in range(len(Z_Row)):
                    sum_val += Z_Row[i]
                    cum_sum[i] = sum_val

                Fake_Mean = []
                for i in range(Fake_index_iteration):

                    rand_Val = random.uniform(0,1)
                    Num=closest(cum_sum,rand_Val)
                    Fake_Index=np.argwhere(cum_sum==Num)
                    Fake_Index=int(Fake_Index[0][0])

                    if Num>=rand_Val:
                        pass
                    else:
                        Fake_Index+=1
                        if cum_sum[Fake_Index]== cum_sum[Fake_Index-1]:#TODO:Not required
                            Fake_Index-=1

                    for i in range(len(target_index)):
                        Fake_Index_Hex=Hex_val_MP[Fake_Index]
                        Fake_Mean.append(Euclidean_distance(Target_Hex[i], Fake_Index_Hex))

                Average_real+=Target_real_distance
            Fake_Mean.sort()
            Average_fake=sum(Fake_Mean[2:-2])/(len(target_index)*Fake_index_iteration-4)

        User_target_real.append(Average_real/count)
        User_target_fake.append(Average_fake/(count))

        Average_distance_difference=[]
        for i in range(len(User_target_real)):
            Average_distance_difference.append(abs(User_target_fake[i]-User_target_real[i]))

    print("Average distance between Fake and Target location of different Users  - ", User_target_fake)
    print("Average distance between Real and Target location of different Users  - ", User_target_real)
    print("Average difference in distance ",Average_distance_difference)

def closest(lst, Num):
    return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - Num))]

def Euclidean_distance(Hex1, Hex2):
    X1, Y1 = h3.h3_to_geo(Hex1)
    X2, Y2 = h3.h3_to_geo(Hex2)
    distance = math.sqrt(math.pow((X1 - X2), 2) + math.pow((Y1 - Y2), 2))
    return distance