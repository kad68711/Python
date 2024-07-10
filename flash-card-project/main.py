from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"


def is_known():
   data.remove(word)
   new_data=pandas.DataFrame(data)
   new_data.to_csv("new_file.csv",index=0)

   change()
    


    


def change():
   global word
   word=random.choice(data)
   canvas.itemconfig(back,image=white_card_image)
   canvas.itemconfig(card_title,text="French",fill="black")
   canvas.itemconfig(card_word,text=word["French"],fill="black")
   right_button.config(state=DISABLED)
   wrong_button.config(state=DISABLED)

   window.after(3000,board,word)
  

def board(word):
   
   canvas.itemconfig(back,image=green_card_image)
   canvas.itemconfig(card_title,text="English",fill="white")
   canvas.itemconfig(card_word,text=word["English"],fill="white")
   
   right_button.config(state=NORMAL)
   wrong_button.config(state=NORMAL)

   
  


try:
   data=pandas.read_csv("new_file.csv")
   print(data)
   data=data.to_dict(orient="records")
   print(data)
except:
    data=pandas.read_csv("data/french_words.csv")
    data=data.to_dict(orient="records")



window=Tk()
window.config(bg=BACKGROUND_COLOR,padx=50,pady=50)

white_card_image=PhotoImage(file="images/card_front.png")
green_card_image=PhotoImage(file="images/card_back.png")

canvas=Canvas(width=800,height=526,bg=BACKGROUND_COLOR,highlightthickness=0)
back=canvas.create_image(400,263,image=white_card_image)
canvas.grid(column=1,row=0,columnspan=2)
card_title=canvas.create_text(400,150,text="",font=("Arial",40,"bold"))
card_word=canvas.create_text(400,300,text="",font=("Arial",32,"bold"))



wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0,command=change)
wrong_button.grid(column=1,row=1)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0,command=is_known)
right_button.grid(column=2,row=1)

change()

window.mainloop()