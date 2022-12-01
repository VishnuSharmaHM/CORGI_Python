import Config as C
import matplotlib.pyplot as plt
from statistics import stdev,median,mean,variance
import random
# Count=[94, 471, 2440, 0, 1122, 628, 206, 0, 1486, 340, 8, 691, 1509, 188, 413, 743, 124, 309, 350, 0, 57, 184, 211, 29,
#        1083, 3437, 2691, 146, 452, 6, 1075, 319, 364, 17, 1280, 516, 104, 1130, 573, 277, 133, 788, 258, 1610, 473, 84,
#        781, 521, 7934]
Count=[471, 319, 573, 124, 1130, 0, 516, 104, 57, 2691, 8, 473, 340, 0, 2440, 1075, 249, 7934, 211, 628, 1280, 122, 3437, 309,
 521, 1083, 29, 1610, 364, 184, 84, 160, 1122, 277, 691, 781, 0, 258, 206, 788, 188, 1509, 94, 452, 17, 1486, 133, 743, 6]

Average=mean(Count)
# print(Average)
# print(Average)
# print(stdev(Count))
#TODO: Improve how low and very high values are transformed.
for i in range(len(Count)):
    if Count[i]<50:
        Count[i]=random.randint(25,50)
    elif Count[i]>1500:
        Count[i] = random.randint(1500, 2000)
Sum1=sum(Count)
for index in range(len(Count)):
    Count[index]=Count[index]/Sum1
print(Count)
X_axis=[i+1 for i in range(len(Count))]
plt.plot(X_axis,Count)
plt.xlabel("Index")
plt.ylabel("Count")
plt.title("CPR")
plt.show()