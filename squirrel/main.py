import pandas

data=pandas.read_csv("2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv")

fur_data=data["Primary Fur Color"]
gray=0
cinnamon=0
black=0

for i in fur_data:
    if i=="Gray":
        gray+=1
    
    elif i=="Cinnamon":
        cinnamon+=1

    elif i=="Black":
        black+=1

dict={"Fur Color":["Gray","Cinnamon","Black"],"Count":[gray,cinnamon,black]}


dataframe=pandas.DataFrame(dict)

dataframe.to_csv("new_file")


