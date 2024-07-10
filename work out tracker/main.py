import requests
from datetime import datetime
import dotenv
import os

dotenv.load_dotenv()
APP_ID=os.getenv("APP_ID")
APP_KEY=os.getenv("APP_KEY")


url="https://trackapi.nutritionix.com/v2/natural/exercise"

inp=input("nani o shita:  ")
json_data={
 "query":inp,
 "gender":"female",
 "weight_kg":72.5,
 "height_cm":167.64,
 "age":30
}
headers={

    "x-app-id":APP_ID,
    "x-app-key":APP_KEY
}

response=requests.post(url=url,json=json_data,headers=headers)
data=response.json()


now=datetime.now()
today=now.strftime("%d/%m/%Y")
time=now.strftime("%H:%M:%S")

for i in data['exercises']:
    exercise=i["name"]
    duration=i["duration_min"]
    calories=i["nf_calories"]

    sheety_url="https://api.sheety.co/8ea870d4d3c3064866e12f288d97201b/myWorkouts/workouts"
    sheety_data={
        "workout":{
        "date":today,
        "time":time,
        "exercise":exercise,
        "duration":duration,
        "calories":calories
        }
    }

    sheety_token=os.getenv("sheety_token")

    sheety_header={
        "Content-Type" : "application/json",
        "Authorization": sheety_token
    }

    
   

    sheety_response=requests.post(url=sheety_url,json=sheety_data,headers=sheety_header)
    print(sheety_response.text)




