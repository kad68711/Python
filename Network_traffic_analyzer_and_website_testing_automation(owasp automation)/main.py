import tkinter as tk
from tkinter import scrolledtext,filedialog
from PIL import Image, ImageTk
from zappppp import scan_website
from Network_traffic_analyzer import main

def network_analyzer():
    file_path = filedialog.askopenfilename(title="Choose a file",initialdir="C:\\Users\\kad\\Desktop\\pythonnnnnnnn\\network analyzer and zap automation\\Network_traffic_analyzer-main")
    
    if file_path:
        # Perform actions with the selected file path (e.g., analyze the network)
        # 10 is simply the threshold for port scanning you can change it 
        results=main(file_path,10)
        result_window = tk.Toplevel()
        result_window.title("Analysis Results")
        result_window.geometry("400x300")
        result_text = scrolledtext.ScrolledText(result_window, wrap=tk.WORD, font=("Helvetica", 12))
        result_text.pack(fill="both", expand=True)

        for result in results:
            result_text.insert(tk.END, result)
            result_text.insert(tk.END, "\n\n\n")



    else:
        print("No file selected.")

    

    

def website_analyzer(canvas):
    # Clear the canvas by deleting all widgets
    for widget in canvas.winfo_children():
        widget.destroy()
    
    # Create input window for website URL
    website_input_label = tk.Label(canvas, text="Enter website URL:", font=("Helvetica", 16))
    website_input_label.pack()

    # Create input field
    website_entry = tk.Entry(canvas, font=("Helvetica", 14))
    website_entry.pack(pady=10)  # Add padding below the input field

    # Create submit button
    submit_button = tk.Button(canvas, text="Submit", command=lambda: websiteanalyze_and_result(canvas,website_entry.get()), **button_style)
    submit_button.pack()

    # Center input field and submit button
    canvas.update()
    canvas.move(website_input_label, (canvas.winfo_width() - website_input_label.winfo_width()) / 2, canvas.winfo_height() / 2 - 50)
    canvas.move(website_entry, (canvas.winfo_width() - website_entry.winfo_width()) / 2, canvas.winfo_height() / 2)
    canvas.move(submit_button, (canvas.winfo_width() - submit_button.winfo_width()) / 2, canvas.winfo_height() / 2 + 50)

    # Add your website analyzer function code here
    print("Website Analyzer Function")

def websiteanalyze_and_result(canvas,site):
    # show as waiting
    for widget in canvas.winfo_children():
        widget.destroy()
    
    waiting_label = tk.Label(canvas, text="Please wait, analyzing website...", font=("Helvetica", 16))
    waiting_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Update the main Tkinter event loop to ensure the waiting message is displayed
    root.update()


    # display alerts on to a new window
    alerts_and_recommendations=scan_website(site)
    alerts=alerts_and_recommendations[0]
    reccommendations=alerts_and_recommendations[1]

     # Create a scrolled text widget to display the results
    result_window = tk.Toplevel()
    result_window.title("Analysis Results")
    result_window.geometry("400x300")
    result_text = scrolledtext.ScrolledText(result_window, wrap=tk.WORD, font=("Helvetica", 12))
    result_text.pack(fill="both", expand=True)

    # Insert alerts into the scrolled text widget
    for alert in alerts:
        result_text.insert(tk.END, f"Alert: {alert['alert']}, Risk: {alert['risk']}, URL: {alert['url']}\n")
    
     # Insert "RECOMMENDATIONS" text with bold and thick styling
    result_text.insert(tk.END, "RECOMMENDATIONS\n", ("bold",))
    
    # Assume 'vulnerability_recommendations_dict' is the dictionary containing recommendations for each vulnerability

    for vulnerability, recommendations in reccommendations.items():
        result_text.insert(tk.END, f"Vulnerability: {vulnerability}\n")
        for recommendation in recommendations:
            result_text.insert(tk.END, f"- {recommendation}\n")
        result_text.insert(tk.END, "\n")



  

    # Close the waiting message
    waiting_label.destroy()
     # Recreate buttons
    network_button = tk.Button(canvas, text="Network Analyzer", command=network_analyzer, **button_style)
    website_button = tk.Button(canvas, text="Website Analyzer", command=lambda: website_analyzer(canvas), **button_style)

    # Add buttons to canvas and center them
    network_button_window = canvas.create_window(window_width // 2, window_height // 2 - 50, anchor="center", window=network_button)
    website_button_window = canvas.create_window(window_width // 2, window_height // 2 + 50, anchor="center", window=website_button)


# Create main application window
root = tk.Tk()
root.title("Cybersecurity Application")

# Set the window size
window_width = 800
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width / 2) - (window_width / 2)
y_coordinate = (screen_height / 2) - (window_height / 2)
root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

# Load background image and resize it to fit the window
background_image = Image.open("app_background.png")
background_image = background_image.resize((window_width, window_height))

# Convert the resized image to a Tkinter PhotoImage
background_image = ImageTk.PhotoImage(background_image)

# Create a canvas to put the background image on
canvas = tk.Canvas(root, width=window_width, height=window_height)
canvas.pack(fill="both", expand=True)

# Place the background image on the canvas
canvas.create_image(0, 0, image=background_image, anchor="nw")

# Create style for buttons
button_style = {
    "font": ("Helvetica", 16),
    "bg": "#cfe2f3",  # Light gray button background color
    "fg": "black",    # Black text color
    "activebackground": "#dee2e6",  # Lighter gray when button is clicked
    "activeforeground": "black",     # Black text color when button is clicked
    "borderwidth": 5,                # Border width
    "relief": "raised",              # Simulated raised effect
    "padx": 20,                      # Horizontal padding
    "pady": 10                       # Vertical padding
}

# Create buttons
network_button = tk.Button(canvas, text="Network Analyzer", command=network_analyzer, **button_style)
website_button = tk.Button(canvas, text="Website Analyzer", command=lambda: website_analyzer(canvas), **button_style)

# Add buttons to canvas and center them
network_button_window = canvas.create_window(window_width // 2, window_height // 2 - 50, anchor="center", window=network_button)
website_button_window = canvas.create_window(window_width // 2, window_height // 2 + 50, anchor="center", window=website_button)

# Run the application
root.mainloop()
