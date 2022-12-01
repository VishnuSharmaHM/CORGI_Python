import pandas as pd
from h3 import h3
import Gowalla_Dataset as GD
import Config as C

df = pd.read_csv('../Dataset/London_Dataset.csv')
User_Count=0
hex_par=[]
print("Original Dataframe Shape - ",df.shape)
df_Train = pd.DataFrame()
User_ID_Index=[]

User_Count_C=int(C.config['Gowalla']['User_Count'])
Hex_Value_C=C.config['Gowalla']['Hex_value']
Hex_Parent_C=int(C.config['Obfuscation']['Hex_Parent'])
Test_sample_count_C=int(C.config['Gowalla']['Test_sample_count'])
Hex_Cont_C=int(C.config['Gowalla']['Hex_Count'])

for i in df.User_ID.unique():
    df1=df[df.User_ID==i]
    Hex_Count=0
    if User_Count>User_Count_C:
        break

    for Index,Row in df1.iterrows():
        temp=h3.geo_to_h3(Row.Latitude, Row.Longitude, Hex_Parent_C)
        if temp ==Hex_Value_C:
            Hex_Count+=1
    if Hex_Count>Hex_Cont_C:
        Test_Count=0
        User_Count+=1
        for Index, Row in df1.iterrows():
            temp = h3.geo_to_h3(Row.Latitude, Row.Longitude, Hex_Parent_C)
            if(Test_Count>Test_sample_count_C):
                break
            if temp == Hex_Value_C:
                Test_Count+=1
                hex_par.append([int(Row.User_ID), Row.Latitude, Row.Longitude])
                df1=df1.drop([Index])
                if Row.User_ID not in User_ID_Index:
                    User_ID_Index.append(int(Row.User_ID))
        df_Train=pd.concat([df_Train, df1], axis=0)

for i in df.User_ID.unique():
    if i in User_ID_Index:
        pass
    else:
        df1=df1=df[df.User_ID==i]
        df_Train = pd.concat([df_Train, df1], axis=0)

df_Train=df_Train.sort_values(by='User_ID')
df_Test = pd.DataFrame(hex_par,columns=['User_ID','Latitude','Longitude'])
print("Train Dataframe Shape - ",df_Train.shape)
print("Test Dataframe Shape - ",df_Test.shape)
# df_Train.to_csv('../Dataset/London_Train.csv',index=False)
# df_Test.to_csv('../Dataset/London_Test.csv',index=False)
GD.Gowalla_Dataset(df_Train,df_Test)
