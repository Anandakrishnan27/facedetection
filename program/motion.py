import tkinter as tk
from tkinter import messagebox
from tkinter import font
from PIL import Image, ImageTk  # Import PIL (Pillow) for image handling
import winsound
import cv2

# Play a click sound when the button is pressed
def play_click_sound():
    winsound.PlaySound('click.wav', winsound.SND_FILENAME)

def start_motion_detection():
    # Motion detection function
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while cam.isOpened():
        ret, frame1 = cam.read()
        ret, frame2 = cam.read()
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for c in contours:
            if cv2.contourArea(c) < 5000:
                continue
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # Play sound when motion is detected
            winsound.PlaySound('alert.wav', winsound.SND_FILENAME)

        cv2.imshow('Motion Detection', frame1)
        if cv2.waitKey(10) == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

def on_enter_click():
    # Play a click sound
    play_click_sound()
    
    # Welcome message and start motion detection
    messagebox.showinfo("Welcome", "Starting Motion Detection!")
    root.destroy()  # Close the tkinter window
    start_motion_detection()

# Create the main tkinter window
root = tk.Tk()
root.title("Motion Detection")
root.geometry("600x400")
root.configure(bg="#2E4053")

# Add a background image (using full path)
try:
    bg_img_path = r"C:\Users\ANANDA KRISHNAN.M\Desktop\Face detection using Python for security\background.jpg"
    bg_img = Image.open(bg_img_path)  # Open the image using PIL
    bg_img = bg_img.resize((600, 400), Image.Resampling.LANCZOS)  # Resize to fit the window
    bg_img = ImageTk.PhotoImage(bg_img)  # Convert to Tkinter compatible format
    bg_label = tk.Label(root, image=bg_img)
    bg_label.place(x=0, y=0)
    print(f"Background image loaded successfully from {bg_img_path}.")
except Exception as e:
    print(f"Error loading background image: {e}")

# Add animated welcome label
welcome_label = tk.Label(
    root,
    text="Welcome to Motion Detection",
    font=("Verdana", 20, "bold"),
    fg="white",
    bg="#2E4053",
)
welcome_label.pack(pady=20)

# Add a description label with animated fade-in (using after() method)
def animate_description_label():
    description_label.config(text="Click 'Enter' to start detecting motion\nPress 'Q' to quit the motion detection window.")
    description_label.pack(pady=10)

description_label = tk.Label(
    root,
    font=("Verdana", 12),
    fg="#F7DC6F",
    bg="#2E4053",
)
root.after(1000, animate_description_label)  # Adds delay to animate the text

# Add Enter button with hover effect and styling
def on_button_hover(event):
    enter_button.config(bg="#239B56")

def on_button_leave(event):
    enter_button.config(bg="#28B463")

enter_button = tk.Button(
    root,
    text="Enter",
    font=("Verdana", 16, "bold"),
    bg="#28B463",
    fg="white",
    activebackground="#239B56",
    activeforeground="white",
    command=on_enter_click,
    width=8,
    height=2,
    relief="raised",
    bd=5
)

enter_button.pack(pady=10)
enter_button.bind("<Enter>", on_button_hover)  # Change color on hover
enter_button.bind("<Leave>", on_button_leave)  # Revert color when hover ends

# Run the tkinter main loop
root.mainloop()
