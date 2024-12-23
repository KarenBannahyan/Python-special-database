import socket
import threading
import tkinter as tk
from PIL import Image, ImageTk
import io

class ScreenShareServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.client_socket = None
        self.client_address = None

        self.root = tk.Tk()
        self.root.title("Screen Share Server")
        self.canvas = tk.Canvas(self.root, width=1000, height=1000)
        self.canvas.pack()

        self.current_image = None

    def handle_client(self, client_socket):
        while True:
            try:
                size_data = client_socket.recv(8)
                if not size_data:
                    break

                size = int.from_bytes(size_data, byteorder='big')
                image_data = b""
                while len(image_data) < size:
                    image_data += client_socket.recv(size - len(image_data))

                image = Image.open(io.BytesIO(image_data))
                self.current_image = ImageTk.PhotoImage(image)

                self.root.after(0, self.update_canvas)

            except Exception as e:
                print(f"Error: {e}")
                break

        client_socket.close()

    def update_canvas(self):
        if self.current_image:
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.current_image)
            self.root.update_idletasks()
            self.root.update()

    def start_server(self):
        print(f"Server started on {self.host}:{self.port}")
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Client connected from {client_address}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def run(self):
        server_thread = threading.Thread(target=self.start_server)
        server_thread.daemon = True
        server_thread.start()
        self.root.mainloop()

if __name__ == "__main__":
    server = ScreenShareServer('192.168.0.105', 12345)
    server.run()
