import tkinter as tk
from tkinter import messagebox
import pygame  # For sound playback
import cv2
import threading
from PIL import Image, ImageTk
import time  # For adding delays
import os  # For creating directories and saving images

# Initialize pygame mixer for sound playback
pygame.mixer.init()

# Preload sound
click_sound = pygame.mixer.Sound('click.wav')
alert_sound = pygame.mixer.Sound('alert.wav')

# Variable to track when the sound was last played
last_played_time = 0  # Initialize the variable outside the thread
start_time = time.time()  # Record the start time for displaying elapsed time

# Create a directory to save captured faces
save_directory = "captured_faces"
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# Variable to track if the face has been captured
face_captured = False

def play_click_sound():
    # Play the click sound
    click_sound.play()

def play_face_detected_sound():
    # Play the alert sound
    alert_sound.play()

def save_captured_face(frame, face):
    global face_captured  # Access the global variable to track face capture
    
    # Capture and save the face only if it hasn't been captured already
    if not face_captured:
        # Get timestamp for unique filename
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        (x, y, w, h) = face
        face_image = frame[y:y+h, x:x+w]
        
        # Save the face image with a unique name
        filename = f"{save_directory}/face_{timestamp}.jpg"
        cv2.imwrite(filename, face_image)
        print(f"Captured face saved as {filename}")

        # Mark face as captured
        face_captured = True

def start_face_detection():
    global last_played_time  # Use the global variable for tracking the time

    # Start face detection in a separate thread to avoid delay
    def face_detection_thread():
        global last_played_time, face_captured  # Declare to use the global variable inside the thread

        # Load Haar Cascade for face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
        # Set a lower resolution for faster processing
        cam.set(3, 640)  # Set width to 640
        cam.set(4, 480)  # Set height to 480

        while cam.isOpened():
            ret, frame = cam.read()
            if not ret:
                break

            # Convert frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces in the grayscale image
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # Draw rectangles around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Capture and save the face only once when detected
                save_captured_face(frame, (x, y, w, h))

            # Display the number of faces detected
            num_faces = len(faces)
            cv2.putText(frame, f"Faces Detected: {num_faces}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

            # Display the time elapsed since the start of the program
            elapsed_time = time.time() - start_time
            elapsed_time_str = f"Time: {int(elapsed_time)}s"
            cv2.putText(frame, elapsed_time_str, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

            # Show the frame with detected faces and additional information
            cv2.imshow('Face Detection', frame)

            # Check if faces are detected and the sound hasn't been played recently
            if len(faces) > 0 and (time.time() - last_played_time) > 1.0:  # 1 second delay
                play_face_detected_sound()  # Play sound
                last_played_time = time.time()  # Update the last played time

            # Play the sound every 5 seconds regardless of face detection
            if (time.time() - last_played_time) > 5.0:  # Sound plays every 5 seconds
                play_face_detected_sound()  # Play sound
                last_played_time = time.time()  # Update the last played time

            if cv2.waitKey(10) == ord('q'):
                break

        cam.release()
        cv2.destroyAllWindows()

    # Start face detection in a new thread
    detection_thread = threading.Thread(target=face_detection_thread)
    detection_thread.start()

def on_enter_click():
    # Play a click sound
    play_click_sound()
    
    # Welcome message and start face detection
    messagebox.showinfo("Welcome", "Starting Face Detection!")
    root.destroy()  # Close the tkinter window
    start_face_detection()

# Create the main tkinter window
root = tk.Tk()
root.title("Face Detection")
root.geometry("800x500")

# Add background image
try:
    bg_img_path = r"C:\Users\ANANDA KRISHNAN.M\Desktop\Face detection using Python for Surveillance\background.jpg"
    bg_img = Image.open(bg_img_path)  # Open the image using PIL
    bg_img = bg_img.resize((800, 500), Image.Resampling.LANCZOS)  # Resize to fit the window
    bg_img = ImageTk.PhotoImage(bg_img)  # Convert to Tkinter compatible format
    bg_label = tk.Label(root, image=bg_img)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except Exception as e:
    print(f"Error loading background image: {e}")
    root.configure(bg="#2E4053")  # Set fallback color

# Add labels with text, centered and display one after another
welcome_label = tk.Label(
    root,
    text="Welcome to Face Detection",
    font=("Verdana", 20, "bold"),
    fg="white",
    bg="#2E4053",
)

description_label = tk.Label(
    root,
    font=("Verdana", 12),
    fg="#F7DC6F",
    bg="#2E4053",
)

exit_label = tk.Label(
    root,
    text="Press 'Q' to exit",
    font=("Verdana", 12),
    fg="#F7DC6F",
    bg="#2E4053",
)

# Center the text using pack and display one after another
def display_welcome_text():
    welcome_label.pack(pady=10, anchor='center')
    root.after(2000, display_description_text)  # Wait 2 seconds before showing the next text

def display_description_text():
    description_label.config(text="Click 'Enter' to start detecting faces.")
    description_label.pack(pady=10, anchor='center')
    root.after(2000, display_exit_text)  # Wait 2 seconds before showing the next text

def display_exit_text():
    exit_label.pack(pady=10, anchor='center')
    root.after(2000, display_enter_button)  # Wait 2 seconds before showing the button

def display_enter_button():
    enter_button.pack(pady=20, anchor='center')  # Center the button in the middle

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
    height=1,
    relief="raised",
    bd=5
)

enter_button.bind("<Enter>", on_button_hover)  # Change color on hover
enter_button.bind("<Leave>", on_button_leave)  # Revert color when hover ends

# Start displaying text and buttons
root.after(1000, display_welcome_text)  # Wait 1 second before starting the sequence

# Run the tkinter main loop
root.mainloop()
