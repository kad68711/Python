from flask import Flask
import random

number=random.randint(0,9)




app=Flask(__name__)

@app.route('/')
def count():
    return "<h1>Guess a number between 0 and 9</h1>"\
           "<img src='https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWhqOG9zMmc1Z3B3aHJzbHVsOXQ3bDlwOHZmMmRteGFsZXYweHcyOSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7aCSPqXE5C6T8tBC/giphy.gif' >"

@app.route('/<int:n>')
def atetemite(n):
    if n>number:
        return "<h1 style='color:purple'>UE!! mochoto atetemite</h1>"\
           "<img src='https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExeDZiM2J6MXk5NmJybzluaGM4ZDRucGtjZ2dsbXlna2NhMTBvdTB1cyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o6ZtaO9BZHcOjmErm/giphy.gif' >"
    elif n<number:
        return "<h1 style='color:red'>SHITA!! mochoto atetemite</h1>"\
           "<img src='https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExdDUwbXA2OTZnaGRneXVldGRkdTd2aDBiZXh3YzRxc2gycmVheDA3MSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jD4DwBtqPXRXa/giphy.gif' >"
        
    else:
        return "<h1 style='color:green'>MITSUKATA</h1>"\
           "<img src='https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExcjI1dnZtMHZycnIzdHM1aWxobXpkNHM4OHIxZnFzMmhtM3lqejdjYyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/4T7e4DmcrP9du/giphy.gif' >"

        

app.run(debug=True)