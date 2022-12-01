import csv
from Code import Config as C
import json
from Matrix import Obfuscation_CPLEX as OM
import random
import numpy as np
from decimal import *

def Quality_loss(Z, Tree,index):
    target_index = json.loads(C.config.get("Obfuscation", "target_index"))
    Epsilon=json.loads(C.config.get("Obfuscation", "epsilon"))
    Real_coordinates_index= 17

    X1, Y1 = [Tree.leaves[Real_coordinates_index].x1, Tree.leaves[Real_coordinates_index].y1]
    output=[]
    Z_Row = Z[Real_coordinates_index][:]
    cum_sum = [0 for a in range(len(Z_Row))]
    sum_val = 0

    for j in range(len(Z_Row)):
        sum_val += Z_Row[j]
        cum_sum[j] = sum_val

    for i in target_index:
        X2, Y2 = [Tree.leaves[i].x1,Tree.leaves[i].y1]
        Real_target_distance=OM.Distance_Calculation(X1,X2,Y1,Y2)
        for k in range(100):
            temp = [Epsilon[index], Real_target_distance, i]
            rand_Val = random.uniform(0, 1)
            Num = closest(cum_sum, rand_Val)
            Fake_Index = np.argwhere(cum_sum == Num)
            Fake_Index = int(Fake_Index[0][0])
            temp.append(Fake_Index)
            X3,Y3=[Tree.leaves[Fake_Index].x1,Tree.leaves[Fake_Index].y1]
            distance=OM.Distance_Calculation(X2,X3,Y2,Y3)
            quality_loss=abs(distance-Real_target_distance)
            relative_quality_loss=quality_loss/Real_target_distance
            temp.append(quality_loss)
            temp.append(relative_quality_loss)
            output.append(temp)


    Column=['EPSILON','RD(km)','Target','Fake','QL','RQL']

    if index != 0:
        prev = float(Epsilon[index-1])
        with open('../Dataset/Quality_Loss_'+str(float(prev))+'.csv', 'r') as read_obj, \
                open('../Dataset/Quality_Loss_' + str(float(Epsilon[index])) + '.csv', 'w', newline='') as write_obj:
            csv_reader = csv.reader(read_obj)
            csv_writer = csv.writer(write_obj)
            count=0
            for row in csv_reader:
                if count==0:
                    for value in Column:
                        row.append(value)
                    count+=1
                else:
                    for value in output[count-1]:
                        row.append(value)
                    count+=1
                csv_writer.writerow(row)

    elif index==0:
        with open("../Dataset/Quality_Loss_"+str(float(Epsilon[0]))+".csv", 'w+',newline='') as f:
                write = csv.writer(f)
                write.writerow(Column)
                write.writerows(output)

    # print("Epsilon == "+str(Epsilon[index])+" data is transferred to the csv")
def closest(lst, Num):
    return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - Num))]