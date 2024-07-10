from turtle import Turtle,Screen
import pandas

# screen=Screen()
# turtle=Turtle()
# image="blank_states_img.gif"
# screen.addshape(image)
# turtle.shape(image)
# writer=Turtle()
# writer.hideturtle()
# writer.penup()


    

data=pandas.read_csv("50_states.csv")
states=data.state
guessed=[]



zz=data[data.state=="Ohio"]
# print(zz.iloc[0])
print(type(zz))
print(type(zz.x))
print(zz.x.item())
# print(zz.x.to_list())
# print(zz.x.iloc[0])
# print(zz.iloc[0])
# print(zz.x.iloc[0])

# game_on=True

# while game_on:
    
#     answer=screen.textinput("Guess","Nyuroku o shite kudasai").lower().replace(" ","")
    
#     if answer=="quit":
#         game_on=False
    
    
#     else:
#         for state in states:
#             if answer==state.lower().replace(" ",""):
                
#                 zz=data[data.state==state]
#                 # zz.x[zz.index[0]],zz.y[zz.index[0]]
#                 print(int(zz.x))
#                 writer.goto(int(zz.x),int(zz.y))
#                 writer.write(state)
#                 guessed+=state

#     for state in states:
#         for i in range(len(guessed)):
#             if guessed[i]==state:
#                 game_on=False
    
    
        

    
    
        




# screen.exitonclick()

