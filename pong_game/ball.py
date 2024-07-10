
from turtle import Turtle

class Ball(Turtle):
    def __init__(self) -> None:
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.x_move=10
        self.y_move=10
    def move(self):
        new_xcor=self.xcor()+self.x_move
        new_ycor=self.ycor()+self.y_move
        self.goto(new_xcor,new_ycor)
    def bounce_y(self):
        self.y_move*=-1
    def bounce_x(self):
        self.x_move*=-1
    def on(self):
        self.goto(0,0)
        self.bounce_y()
        self.bounce_x()
    

