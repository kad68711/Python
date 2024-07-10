# import requests

# param={
# "appid":"69f04e4613056b159c2761a9d9e664d2",
# "lat":45.541553,
# "lon":10.211802,
# "exclude":"current,minutely,daily"
# }

# response=requests.get(url="https://api.openweathermap.org/data/2.5/onecall",params=param)

# response.raise_for_status()

# data=response.json()

# hourly_data=[]

# for i in range(12):
#    hourly_data.append(data["hourly"][i]["weather"][0]["id"])

# rain=False
# for data in hourly_data:
#    if data<700:
#       rain=True

# if rain:
#    print("ame desu khasa o motekimasu")


import os

print(os.getenv("a"))