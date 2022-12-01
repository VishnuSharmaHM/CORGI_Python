"""
Function to check whether Sum of entries in each row of obfuscation matrix add up to 1
and also to check Column constraint is satisfied
"""

import math
def Row_Check(Z):
    flag=1
    for i in range(len(Z)):
        temp=0
        for j in range(len(Z)):
            temp+=Z[i][j]
        var=round(temp,2)
        if(var==1):
            pass
        else:
            flag=0
            #print("Sum of Row "+ str(i)+ " is not 1")
    if(flag):
        print("Row Check Passed")
        pass
    else:
        print("Row Check Failed")

def Column_Check(Z,EPSILON,CPR_prior_prob,x_coord,y_coord):
    flag=1
    count=0
    for k in range(len(Z)):
        for i in range(len(Z)):
            for j in range(len(Z)):
                if (i == j):
                    pass
                else:
                    if (Z[j][k] != 0):
                        LHS = Z[i][k] / Z[j][k]
                        distance = math.sqrt(math.pow((x_coord[i] - x_coord[j]), 2) +
                                             math.pow((y_coord[i] - y_coord[j]), 2))
                        RHS = math.exp(EPSILON * distance) * (CPR_prior_prob[i] / CPR_prior_prob[j])
                        if (round(LHS) <= round(RHS)):
                            pass
                        else:
                            flag=0
                            count+=1
                            # print("Column Check Failed at " +"Column = "+str(k)+" Row = "+str(i)+", "+str(j))

    if(flag):
        print("Column Check Passed")
    else:
        print("Column Check Failed")
        print('Count of violations - ',count)

def isValid_Z(Z,EPSILON,CPR_prior_prob,x_coord,y_coord):
    Row_Check(Z)
    Column_Check(Z,EPSILON,CPR_prior_prob,x_coord,y_coord)