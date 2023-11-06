
import numpy as np
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import json
import uvicorn
from fastapi.responses import FileResponse


result1=pd.read_csv("data.csv")
app = FastAPI()
lst=['Business','Economy', 'First']
lst1=['05-12', '23-05', '18-23', '12-18']
lst2=['United Airlines','JetBlue Airways','Delta Air Lines','Southwest Airlines']

with open('flights.json', 'r') as file:
    mp4 = json.load(file)

with open('flights_data.json', 'r') as file:
    mp = json.load(file)

class InputData(BaseModel):
    input1: int
    input2: str

@app.get("/")
async def root():
    return FileResponse("index.html")

@app.post("/process_inputs/")
def process_inputs(data: InputData):
    print(data)
    user=data.input1
    destination=data.input2
    lst3=[]
    # result1 = data1[~data1.index.duplicated()]

    sum1 = sum(result1.loc[user - 1,key] for key in lst)
    sum2 = sum(result1.loc[user - 1,key] for key in lst1)
    sum3 = sum(result1.loc[user - 1,key] for key in lst2)

    for key in lst:
        lst3.append(result1.loc[user - 1,key]/ sum1)
        # print(result1.loc[user - 1,key])

    for key in lst1:
        lst3.append(result1.loc[user - 1,key] / sum2)

    for key in lst2:
        x=result1.loc[user - 1,key]/ sum3
        lst3.append(x*2)

    # print(result.loc[user - 1,"meals"])
    lst3.append(result1.loc[user - 1,"meals"])
    df1 = pd.DataFrame([lst3],columns=['Business','Economy', 'First','05-12', '23-05', '18-23', '12-18','United Airlines','JetBlue Airways','Delta Air Lines','Southwest Airlines','meals'])

    flight_rec={} 
    for i in mp4[destination]:
        df1.loc[1]=0
        j=i.split(":")[2]
        df1.loc[1,j]=2
        z=mp[i]
        df1.loc[1,z[2]]=1
        if(mp[i][3]=="1"):
            df1.loc[1,"meals"]=1
        
        departure_time_temp=mp[i][0]
        if 5 <= departure_time_temp < 12:
            departure_time="05-12"
        elif 12 <= departure_time_temp< 18:
            departure_time= "12-18"
        elif 18 <=departure_time_temp< 23:
            departure_time= "18-23"
        else:
            departure_time= "23-05"

        df1.loc[1,departure_time]=1
        
        

        euclidean_distance = np.linalg.norm(df1.loc[0] - df1.loc[1])

        flight_rec[i]=euclidean_distance
        

    sorted_flights = sorted(flight_rec.items(), key=lambda x: x[1])
    # print(str(sorted_flights[2][0])+str(sorted_flights[2][1]))
    
    i=1
    c=0
    output1=[]
    while c==0:
        if sorted_flights[0][1]!=sorted_flights[i][1] or sorted_flights[0][0].split(":")[2]!=sorted_flights[i][0].split(":")[2]:
                # output1 = "This is output 1"
                # output2 = 42
                c=1
                
                
                output1.append(str(sorted_flights[0][0].split(":")[0]) + ":" +str(sorted_flights[0][0].split(":")[2]) + ":" +":".join(str(i) for i in mp[sorted_flights[0][0]]))
                output1.append(str(sorted_flights[i][0].split(":")[0]) + ":" +str(sorted_flights[i][0].split(":")[2]) + ":" +":".join(str(i) for i in mp[sorted_flights[i][0]]))
        i+=1

    output2=[result1.loc[user - 1][0:15],result1.loc[user - 1][222:230]]
    output3=[sorted_flights[0][0],sorted_flights[1][0]]

    

    return output1
   


