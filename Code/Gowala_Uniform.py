import math
import pandas as pd
from h3 import h3
import matplotlib.pyplot as plt
from collections import defaultdict
from geopy.geocoders import Nominatim
import Config as C

# geolocator = Nominatim(user_agent="my_user_agent")
# addr = C.config['Obfuscation']['Address']
# loc = geolocator.geocode(addr)
# print(loc)
# lat=loc.latitude
# long=loc.longitude
# print(long,lat)
# df = pd.read_csv('../Dataset/Gowalla_Orginal.csv')
# # lat=40.758574860727016
# # long=-73.98557643726936
# range_lat = (3/ 6378) * (180 / math.pi)
# range_long = (3/ 6378) * (180 / math.pi) / math.cos(lat* math.pi/180)
# out=[]
# count=0
# for Index,Row in df.iterrows():
#     if lat-range_lat<Row['Latitude']<lat+range_lat and long-range_long<Row['Longitude']<long+range_long:
#         count+=1
#         out.append([int(Row['User_ID']),Row['Latitude'],Row['Longitude']])
# print("Number of entries in CSV - ",count)
# df1 = pd.DataFrame(out, index =None,columns =['User_ID', 'Latitude', 'Longitude'])
# df1.to_csv('../Dataset/Trial.csv',index=False)

df = pd.read_csv('../Dataset/SanFrancisco_Gowalla.csv')

Hex_parent=[]
Hex_Leaf=[]
Parent_resolution=6
Leaf_resolution=Parent_resolution+2

for Index, Row in df.iterrows():
    temp = h3.geo_to_h3(Row.Latitude, Row.Longitude, Parent_resolution)
    if temp not in Hex_parent:
        Hex_parent.append(temp)

for i in Hex_parent:
    val = h3.h3_to_children(i, res=Leaf_resolution)
    for i in val:
        if i in Hex_Leaf:
            continue
        else:
            Hex_Leaf.append(i)

print("Number of Parent Node - ",len(Hex_parent))
print("Number of Leaf Node - ",len(Hex_Leaf))

Count=[0 for a in range(len(Hex_Leaf))]
for Index, Row in df.iterrows():
    temp = h3.geo_to_h3(Row.Latitude, Row.Longitude, Leaf_resolution)
    if temp in Hex_Leaf:
        Count[Hex_Leaf.index(temp)] += 1
#computer average, drop which are 2 sd above and below.

start=0
end=len(Hex_Leaf)
print("Zero Counts - ",Count[:end].count(0))
print("Average Counts - ",sum(Count[:end])/end)
print(Count[:end])
X_axis=[i+1 for i in range(len(Hex_Leaf))]
plt.plot(X_axis[start:end],Count[start:end])
plt.xlabel("Index")
plt.ylabel("Count")
plt.title(C.config['Obfuscation']['Address'])
plt.show()


# temp1=[]
# for Index,Row in df.iterrows():
#     temp = h3.geo_to_h3(Row.Latitude, Row.Longitude, Parent_resolution+2)
#     if temp in Hex_Leaf[:49]:
#         temp1.append([Row.User_ID,Row.Latitude, Row.Longitude])
# print("Number of entries in CSV - ",len(temp1))
# df1 = pd.DataFrame(temp1, index =None,columns =['User_ID', 'Latitude', 'Longitude'])
# df1.to_csv('../Dataset/Trial.csv',index=False)
