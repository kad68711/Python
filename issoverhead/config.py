import requests
dict={"lat":43.075970,"lng":-107.290283,"formatted":0}
response=requests.get(url="https://api.sunrise-sunset.org/json",params=dict)

response.raise_for_status()

data=response.json()
print(data)