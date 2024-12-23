import socket
import tkinter as tk
from tkinter import messagebox
from PIL import ImageGrab, Image
import io
import threading


class ScreenShareClient:
    def __init__(self):
        self.client_socket = None
        self.root = tk.Tk()
        self.root.title("Screen Share Client")
        self.root.geometry("400x300")
        self.root.config(bg="#2e3b4e")

        self.frame = tk.Frame(self.root, bg="#2e3b4e")
        self.frame.pack(pady=20)

        self.ip_label = tk.Label(self.frame, text="Server IP:", font=('Helvetica', 12), fg='#ffffff', bg='#2e3b4e')
        self.ip_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.ip_entry = tk.Entry(self.frame, font=('Helvetica', 12))
        self.ip_entry.grid(row=0, column=1, padx=10, pady=5)

        self.port_label = tk.Label(self.frame, text="Server Port:", font=('Helvetica', 12), fg='#ffffff', bg='#2e3b4e')
        self.port_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.port_entry = tk.Entry(self.frame, font=('Helvetica', 12))
        self.port_entry.grid(row=1, column=1, padx=10, pady=5)

        self.connect_button = tk.Button(self.frame, text="Connect", command=self.connect_to_server,
                                        font=('Helvetica', 12, 'bold'), bg="#4e5b70", fg="#ffffff",
                                        activebackground="#627b8d", width=20)
        self.connect_button.grid(row=2, columnspan=2, pady=10)

        self.start_button = tk.Button(self.frame, text="Start Screen Sharing", state=tk.DISABLED,
                                      command=self.start_sharing, font=('Helvetica', 12, 'bold'), bg="#4e5b70",
                                      fg="#ffffff", activebackground="#627b8d", width=20)
        self.start_button.grid(row=3, columnspan=2, pady=10)

        self.status_label = tk.Label(self.root, text="Disconnected", font=('Helvetica', 12), fg='#ff6347', bg='#2e3b4e')
        self.status_label.pack(pady=5)

    def connect_to_server(self):
        ip = self.ip_entry.get()
        port = self.port_entry.get()

        if not ip or not port:
            self.status_label.config(text="IP and Port are required!", fg="#ff6347")
            return

        try:
            port = int(port)

            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((ip, port))
            self.status_label.config(text=f"Connected to {ip}:{port}", fg="#32cd32")
            print(f"Connected to {ip}:{port}")

            self.start_button.config(state=tk.NORMAL)

        except Exception as e:
            self.status_label.config(text=f"Failed to connect: {e}", fg="#ff6347")
            print(f"Failed to connect: {e}")

    def send_screen(self):
        while True:
            screen = ImageGrab.grab()
            byte_arr = io.BytesIO()
            screen.save(byte_arr, format='PNG')
            byte_arr = byte_arr.getvalue()

            self.client_socket.send(len(byte_arr).to_bytes(8, byteorder='big'))

            self.client_socket.send(byte_arr)

            threading.Event().wait(0.05)

    def start_sharing(self):
        threading.Thread(target=self.send_screen, daemon=True).start()
        self.status_label.config(text="Sharing Screen...", fg="#32cd32")

    def run(self):
        self.root.mainloop()


# Запуск клиента
if __name__ == "__main__":
    client = ScreenShareClient()
    client.run()
