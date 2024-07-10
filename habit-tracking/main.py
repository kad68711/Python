import requests
from datetime import datetime

USERNAME = "esrherhsrhsdrsrdgsrg"
TOKEN = "sergsrg@3434"
GRAPH_ID = "graph1"

pixela_endpoint = "https://pixe.la/v1/users"

user_params = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}

# # POST commented because this was used to create a account since the account is now created it has no use
# response = requests.post(url=pixela_endpoint, json=user_params)
# print(response.text)

# graph_endpoint=f"{pixela_endpoint}/{USERNAME}/graphs"

# graph_congif={
#     "id":"graph1",
#     "name":"tp graph",
#     "unit":"km",
#     "type":"float",
#     "color":"momiji"
# }
header={"X-USER-TOKEN":TOKEN}
# response=requests.post(url=graph_endpoint,json=graph_congif,headers=header)
# print(response.text)
now=datetime.now()

pixel_url=f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}"
pixel_param={
    "date":now.strftime("%Y%m%d",d=24),
    "quantity":"30"
}
response=requests.post(url=pixel_url,json=pixel_param,headers=header)
print(response.text)
