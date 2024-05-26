import cv2
from djitellopy import Tello
import time
from pynput import keyboard
import threading
import numpy as np
import zxingcpp  # import zxingcpp for decoding the QR

# Initialize Tello
tello = Tello()
tello.connect()
tello.streamon()

# Define the keyboard control functions
def on_press(key):
    try:
        if key.char == 'w':
            tello.move_forward(30)
        elif key.char == 's':
            tello.move_back(30)
        elif key.char == 'a':
            tello.move_left(30)
        elif key.char == 'd':
            tello.move_right(30)
        elif key.char == 'q':
            tello.rotate_counter_clockwise(30)
        elif key.char == 'e':
            tello.rotate_clockwise(30)
        elif key.char == 'r':
            tello.move_up(30)
        elif key.char == 'f':
            tello.move_down(30)
    except AttributeError:
        if key == keyboard.Key.esc:
            tello.land()
            return False

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Start listening to the keyboard events
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

# Start video processing
cap = tello.get_frame_read()

while True:
    frame = cap.frame
    frame = cv2.resize(frame, (720, 480))
    
    # Detect barcodes using zxingcpp
    results = zxingcpp.read_barcodes(frame)
    for result in results:
        x, y, w, h = result.rect
        barcode_info = result.data.decode('utf-8')
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, barcode_info, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Display the frame
    cv2.imshow('Tello Video Stream', frame)
    
    # Stop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cv2.destroyAllWindows()
tello.streamoff()
tello.end()
