from tkinter import *
from tkinter import messagebox
import json


# ---------------------------- seacrh ------------------------------- #
def search():
    try:
        with open("file.json", "r") as f:
            data=json.load(f)
            
            if web_entry.get() in data:
                messagebox.showinfo(message=f"{data[web_entry.get()]['email']} \n{data[web_entry.get()]['password']}")
            else:
                messagebox.showinfo(message="no info")

    except FileNotFoundError:
        messagebox.showinfo(message="empty data")
    except:
        messagebox.showinfo(message="input data first")

    



# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    if len(web_entry.get()) == 0 or len(email_entry.get()) == 0 or len(pass_entry.get()) == 0:
        messagebox.showinfo(message="emptyyyy")
    else:
        ii_ka = messagebox.askokcancel(
            title="check", message=f"iie desu ka sore\n {web_entry.get()} \n {email_entry.get()} \n{pass_entry.get()}")
        if ii_ka:
            web=web_entry.get()
            email=email_entry.get()
            passkey=pass_entry.get()
            new_data={web :{"email":email,"password":passkey}}
            try:
                with open("file.json", "r") as f:
                    data=json.load(f)
                    data.update(new_data)
            except:
                with open("file.json", "w") as f:
                    json.dump(new_data,f)
            else:

                with open("file.json","w") as f:
                    json.dump(data,f,indent=4)

            web_entry.delete(0, END)
            email_entry.delete(0, END)
            pass_entry.delete(0, END)
            messagebox.showinfo(message="saved")
        
        

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password_Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

label = Label(text="Website:")
label.grid(column=0, row=1)
label = Label(text="Email/Username:")
label.grid(column=0, row=2)
label = Label(text="Password:")
label.grid(column=0, row=3)


web_entry = Entry(width=40)
web_entry.grid(column=1, row=1, columnspan=2, pady=5, sticky="W")
email_entry = Entry(width=35)
email_entry.grid(column=1, row=2, columnspan=2, pady=5, sticky="EW")
pass_entry = Entry(width=21)
pass_entry.grid(column=1, row=3, pady=5, sticky="EW")


button = Button(text="Search" , command=search)
button.grid(column=2, row=1)
button = Button(text="Generate Password")
button.grid(column=2, row=3)
button = Button(text="ADD", width=36, command=save)
button.grid(column=1, row=4, columnspan=2)


window.mainloop()
