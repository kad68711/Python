from tkinter import *
import math
import time

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 5
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
checkmark_string = ""

# ---------------------------- TIMER RESET ------------------------------- #


def reseto():
    global reps
    global checkmark_string
    reps = 0
    checkmark_string = ""
    check.config(text=checkmark_string)
    start_timer()



# ---------------------------- TIMER MECHANISM ------------------------------- #

def start_timer():
    global reps
    global checkmark_string
    reps += 1
    if reps % 8 == 0:
        checkmark = "✔"
        checkmark_string += checkmark
        check.config(text=checkmark_string)

        timu(LONG_BREAK_MIN*60)
        Heading.config(text="ASOBEEEEEEEEE", fg=RED)

    elif reps % 2 == 0:
        timu(SHORT_BREAK_MIN*60)
        Heading.config(text="ASOBE", fg=PINK)

    else:
        
        timu(120*60)
        
        Heading.config(text="HATARAKE", fg=GREEN)
        import datetime

    def timepass_code():
        start_time = datetime.datetime.now()
        while True:
            current_time = datetime.datetime.now()
            elapsed_time = (current_time - start_time).total_seconds()
            if elapsed_time >= 1:
                break

    if __name__ == "__main__":
        start_time = datetime.datetime.now()
        timepass_code()
        end_time = datetime.datetime.now()
        elapsed_time = (end_time - start_time).total_seconds()
        print(f"Execution time: {elapsed_time} seconds")

        print(reps)
        time.sleep(5)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

def timu(count):
    global reps

    minutes = math.floor(count/60)

    seconds = count % 60

    if seconds < 10:
        seconds = f"0{seconds}"

    if count > 0:
        canvas.itemconfig(timer_text, text=f"{minutes}:{seconds}")
        
        window.after(1, timu, count-1)
        print("after this")
        
    else:
        start_timer()
        print("Sdhsdh")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("POMODORORORORO")
window.config(padx=100, pady=50, bg=YELLOW)

Heading = Label(text="TIMER", fg=GREEN, bg=YELLOW,
                font=(FONT_NAME, 20, "bold"))
Heading.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)

tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(
    100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=2)




button = Button(text="start", command=start_timer)
button.grid(column=0, row=3)

check = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 15, "bold"))
check.grid(column=1, row=3, ipady=10)


button = Button(text="reset", command=reseto)
button.grid(column=2, row=3)



window.mainloop()
