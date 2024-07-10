import tkinter 

THEME_COLOR = "#375362"

class QuizInterface:

    def __init__(self,quiz) -> None:
        self.score=0
        self.quiz=quiz
        
        self.window=tkinter.Tk()
        self.window.title("QUIZLLER")
        self.window.config(bg=THEME_COLOR,padx=50,pady=50)

        self.label=tkinter.Label(text="score: 0",fg="white",bg=THEME_COLOR)
        self.label.grid(column=1,row=0)

        self.canvas=tkinter.Canvas(width=300,height=250)
        self.question_text=self.canvas.create_text(150,125,text="a",font=("Arial",20,"italic"),width=280)
        self.canvas.grid(column=0,row=1,columnspan=2,pady=50)


        true_image=tkinter.PhotoImage(file="images/true.png")
        self.true_button=tkinter.Button(image=true_image,command=self.check_if_true)
        self.true_button.grid(column=0,row=2,padx=50,pady=50)


        false_image=tkinter.PhotoImage(file="images/false.png")
        self.false_button=tkinter.Button(image=false_image,command=self.check_if_false)
        self.false_button.grid(column=1,row=2,padx=50,pady=50)

        self.get_next_question()

        self.window.mainloop()


    def get_next_question(self):
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():
            
            q_text=self.quiz.next_question()  
            self.canvas.itemconfig(self.question_text,text=q_text)
        else:
            self.canvas.itemconfig(self.question_text,text="game over")
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")

    def check_if_true(self):
        self.asnwer= self.quiz.check_answer("True",self.label)
        self.color_change(self.asnwer)


    def check_if_false(self):
        self.asnwer=self.quiz.check_answer("False",self.label)
        self.color_change(self.asnwer)

    def color_change(self,ans):
        if ans==True:
            self.canvas.config(bg="green")
            self.score+=1
        else:
            self.canvas.config(bg="red")

        self.label.config(text=f"Score:{self.score}")
        
        self.window.after(1000,self.get_next_question)


    







        


