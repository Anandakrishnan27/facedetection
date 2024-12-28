import cv2
import winsound
import time

# Initialize webcam and variables
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
motion_detected = False
sensitivity_threshold = 5000  # Minimum contour area for motion
paused = False

print("Press 'q' to quit, 'r' to reset sensitivity, 'p' to pause/resume.")

# Frame processing loop
while cam.isOpened():
    ret, frame1 = cam.read()
    if not ret:
        print("Failed to grab frame. Exiting...")
        break
    
    if not paused:
        # Use previous frame to compare
        ret, frame2 = cam.read()
        if not ret:
            print("Failed to grab second frame. Exiting...")
            break

        # Frame processing for motion detection
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False
        for c in contours:
            if cv2.contourArea(c) < sensitivity_threshold:
                continue
            motion_detected = True
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame1, f"Motion Detected! Area: {cv2.contourArea(c):.0f}", 
                        (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            # Play sound alert
            winsound.PlaySound('alert.wav', winsound.SND_ASYNC)

        # Add status to frame
        status = "Motion Detected" if motion_detected else "No Motion"
        cv2.putText(frame1, f"Status: {status}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.6, (255, 255, 255), 1)

    # Display the frame
    cv2.imshow('Interactive Motion Detector', frame1)

    # Handle keyboard input
    key = cv2.waitKey(10)
    if key == ord('q'):  # Quit
        print("Exiting program...")
        break
    elif key == ord('r'):  # Reset sensitivity
        sensitivity_threshold = 5000
        print("Sensitivity reset to 5000.")
    elif key == ord('p'):  # Pause/Resume
        paused = not paused
        print("Paused." if paused else "Resumed.")

# Clean up resources
cam.release()
cv2.destroyAllWindows()
