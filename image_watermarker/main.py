# # #####  image and text resizing can be added should be added to make it better also better desiging of the gui can be done
# # instead of doing the draggble sizing which is much better by the way you can simply ask the user for the size 
# or the color also maybe and much more else  ############
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageGrab, ImageDraw, ImageFont

textwatermarkused=False

def fileupload():
    filepath = filedialog.askopenfilename()
    openimage(filepath)


def openimage(filepath):
    # this function is for textbased watermark as well opening the backgound main image
    global photo
    global canvas
    global text_object
    global original_imageheight
    global original_imagewidth
    global original_image
    
    image = Image.open(filepath)
    original_image = image
    original_imagewidth = image.width
    original_imageheight = image.height
    image = image.resize((800, 600))

    # Convert the image to Tkinter format
    photo = ImageTk.PhotoImage(image)

    # Create a Tkinter Canvas

    canvas = Canvas(window, width=image.width, height=image.height)
    canvas.grid(row=0, column=4, rowspan=2)

    canvas.create_image(0, 0, anchor=NW, image=photo)

    # Create a text object on the canvas
    text_object = canvas.create_text(
        100, 100, text="", fill="black", font=("Arial", 24))

    # Bind mouse events to the canvas
    canvas.drag_data = {"x": 0, "y": 0}
    canvas.tag_bind(text_object, "<ButtonPress-1>", on_drag_start)
    canvas.tag_bind(text_object, "<B1-Motion>", on_drag_motion)


def saveimage():

    photo = ImageTk.PhotoImage(original_image)

    

    # Get the scale factor to map canvas coordinates to original image coordinates
    scale_factor_width = original_image.width / canvas.winfo_width()
    scale_factor_height = original_image.height / canvas.winfo_height()
    
    if textwatermarkused==True:
        # Get coordinates of the text object relative to the canvas
        text_coords = canvas.coords(text_object)
        # Convert canvas coordinates to original image coordinates
        text_coords = (text_coords[0] * scale_factor_width,
                    text_coords[1] * scale_factor_height)

        # Get the text of the text object
        text = canvas.itemcget(text_object, "text")

        # Create a drawing object
        draw = ImageDraw.Draw(original_image)

        # Load a font
        font = ImageFont.truetype("arial.ttf", 24)

        # Draw text on image
        draw.text(text_coords, text, fill="white", font=font)

        
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[
                                                ("PNG files", "*.png"), ("All files", "*.*")])
        original_image.save(filename)
    else:
        watermarkimage_coords = canvas.coords(image_object)

        watermarkimage_coords = (int(watermarkimage_coords[0] * scale_factor_width),
                   int(watermarkimage_coords[1] * scale_factor_height))
    

        original_image.paste(watermark_image, watermarkimage_coords)

        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[
                                                ("PNG files", "*.png"), ("All files", "*.*")])
        original_image.save(filename)
    


def on_drag_start(event):
    # Save the initial position of the mouse
    canvas.drag_data["x"] = event.x
    canvas.drag_data["y"] = event.y


def on_drag_motion(event,callername=""):
    # Calculate the distance moved by the mouse
    delta_x = event.x - canvas.drag_data["x"]
    delta_y = event.y - canvas.drag_data["y"]

    # Move the text object by the calculated distance


    if callername=="insert_image":
        canvas.move(image_object, delta_x, delta_y)
    else:
        canvas.move(text_object, delta_x, delta_y)

    # Update the initial position of the mouse
    canvas.drag_data["x"] = event.x
    canvas.drag_data["y"] = event.y


def addwatermark():
    global textwatermarkused
    textwatermarkused=True
    canvas.itemconfig(text_object, text=entry.get())


def insertimage():
    global photoaswatermark
    global image_object
    global watermark_image
    filepath = filedialog.askopenfilename()
    watermark_image = Image.open(filepath)
    original_image = watermark_image
    
    watermark_image = watermark_image.resize((100, 100))

    # Convert the image to Tkinter format
    photoaswatermark = ImageTk.PhotoImage(watermark_image)

    # Create a text object on the canvas
    image_object = canvas.create_image(0, 0, anchor=NW, image=photoaswatermark)

    # Bind mouse events to the canvas
    canvas.drag_data = {"x": 0, "y": 0}
    canvas.tag_bind(image_object, "<ButtonPress-1>",  on_drag_start)
    canvas.tag_bind(image_object, "<B1-Motion>", lambda event, callername="insert_image": on_drag_motion(event, callername))


window = Tk()

button = Button(text="upload image", command=fileupload)
button.grid(row=0, column=0)


entry = Entry()
entry.insert(END, string='add watermark text')
entry.grid(row=0, column=1)
button2 = Button(text="add text to image", command=addwatermark)
button2.grid(row=0, column=2)

button3 = Button(text="insert_image_as_watermark", command=insertimage)
button3.grid(row=1, column=1)

button4 = Button(text="save_image", command=saveimage)
button4.grid(row=2, column=1)


window.mainloop()
