import socket
import threading
import cv2
import numpy as np

# Tello IP and port
TELLO_IP = "192.168.10.1"
TELLO_PORT = 
TELLO_ADDRESS = (TELLO_IP, TELLO_PORT)

# Local IP and port for receiving video
LOCAL_IP = "0.0.0.0"
LOCAL_PORT = 11111

# Create a UDP socket for sending commands to Tello
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LOCAL_IP, LOCAL_PORT))


def send_command(command):
    """
    Send a command to Tello.
    """
    sock.sendto(command.encode("utf-8"), TELLO_ADDRESS)
    print(f"Sent command: {command}")


def receive_video():
    """
    Receive video from Tello.
    """
    cap = cv2.VideoCapture(f"udp://{LOCAL_IP}:{LOCAL_PORT}")

    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imshow("Tello Live Feed", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


def main():
    # Send command to Tello to start video stream
    send_command("command")
    send_command("streamon")

    # Start receiving video
    video_thread = threading.Thread(target=receive_video)
    video_thread.start()


if __name__ == "__main__":
    main()