from turtle import Turtle

class SCOREBOARD(Turtle):
    def __init__(self):
        super().__init__()
        self.score=0
        self.highscore=0
        
        self.color("white")
        self.penup()
        self.goto(0,260)
        self.write(f"Score:{self.score}",align="center",font=("Courier",22,"normal"))
        self.hideturtle()
    def increase_score(self):
        self.clear()
        self.score+=1
    def update_scoreboard(self):
        self.clear()
        self.write(f"Score:{self.score}",align="center",font=("Courier",24,"normal"))
        
    
    def reset(self):
        if self.score>self.highscore:
            self.highscore=self.score
        self.score=0
        self.update_scoreboard()
    
    
        



        
     
