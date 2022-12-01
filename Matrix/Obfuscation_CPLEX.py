import math
from docplex.mp.model import Model
import numpy as np
from h3 import h3
def obf_matrix(x_coord, y_coord, CPR_prior_prob, target_index, NR_LOC, EPSILON,RPB):
    m = Model(name='TACO')
    R = range(NR_LOC)
    x = m.continuous_var_matrix(R,R,lb=0.001,ub=1, name="X")

    for i in R:
        m.add_constraint(m.sum(x[i,j] for j in R)==1,ctname='ct1')
    for k in R:
        for i in R:
            for j in R:

                distance=Distance_Calculation(x_coord[i],x_coord[j],y_coord[i],y_coord[j])
                if distance<=0.9535865317951092*math.sqrt(3):
                    distance=0.9535865317951092
                    m.add_constraint((x[i,k]- math.exp(distance*(EPSILON-RPB[i][j])) * x[j,k]) <= 0)

    out=0
    for i in R:
        temp = 0
        for j in R:
            for k in target_index:
                temp+=x[i, j] * abs(Distance_Calculation(x_coord[i], x_coord[k], y_coord[i], y_coord[k]) -
                                    Distance_Calculation(x_coord[j], x_coord[k], y_coord[j], y_coord[k]))
        out+=temp*CPR_prior_prob[i]
    m.minimize(out)

    # m.minimize(m.sum(m.sum(x[i,j]*abs(Distance_Calculation(x_coord[i],x_coord[k],y_coord[i],y_coord[k])-
    #                                   Distance_Calculation(x_coord[j],x_coord[k],y_coord[j],y_coord[k]))
    #                        for k in target_index for j in R)*CPR_prior_prob[i] for i in R))
    # m.parameters.lpmethod = 2
    m.solve()
    # m.export_as_lp(basename="foo", path="../Dataset/foo.lp")
    Z=np.zeros([NR_LOC,NR_LOC])

    for i in R:
        for j in R:
            Z[i][j]=x[i,j].solution_value
    return Z

def Distance_Calculation(X1,X2,Y1,Y2):
    # distance= math.sqrt(math.pow((X1 - X2), 2) + math.pow((Y1 -Y2), 2))

    point1=(X1,Y1)
    point2=(X2,Y2)
    distance=h3.point_dist(point1, point2, unit='km')
    return distance