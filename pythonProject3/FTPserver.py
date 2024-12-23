import socket
import os
import tkinter as tk
from tkinter import messagebox

def get_server_ip():
    return socket.gethostbyname(socket.gethostname())

def get_new_photo_filename():
    photo_dir = "received_photos"
    if not os.path.exists(photo_dir):
        os.makedirs(photo_dir)

    existing_photos = [f for f in os.listdir(photo_dir) if f.lower().startswith("received_photo") and f.lower().endswith(".jpg")]
    new_photo_number = len(existing_photos) + 1
    return os.path.join(photo_dir, f"received_photo{new_photo_number}.jpg")

def start_server():
    port = int(entry_port.get())
    server_ip = get_server_ip()
    label_ip.config(text=f"IPv4 address of server : {server_ip}")

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((server_ip, port))
        server_socket.listen(1)
        print("Server is on, waiting for connections...")
        listbox_log.insert(tk.END, "Server is on, waiting for connections...")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Client connected: {client_address}")
            listbox_log.insert(tk.END, f"Client connected: {client_address}")

            photo_data = b""
            while True:
                chunk = client_socket.recv(1024)
                if not chunk:
                    break
                photo_data += chunk

            photo_name = get_new_photo_filename()
            with open(photo_name, 'wb') as file:
                file.write(photo_data)

            print(f"Photo saved as {photo_name}")
            listbox_log.insert(tk.END, f"Photo saved as{photo_name}")
            client_socket.close()

    except Exception as e:
        listbox_log.insert(tk.END, f"Error: {str(e)}")
        messagebox.showerror("Error", f"Server error: {e}")

import threading
def start_server_thread():
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

root = tk.Tk()
root.resizable(False, False)
root.title("Server for saving photos")
root.geometry("600x500")
root.config(bg="#f7f7f7")

style = {
    'bg': '#4e5b70',
    'fg': '#ffffff',
    'font': ('Helvetica', 12, 'bold'),
    'activebackground': '#627b8d',
    'width': 20
}

frame_input = tk.Frame(root, bg="#f7f7f7")
frame_input.pack(pady=20)

label_port = tk.Label(frame_input, text="Port:", bg="#f7f7f7", font=('Helvetica', 12))
label_port.grid(row=0, column=0, padx=10, sticky="e")
entry_port = tk.Entry(frame_input, font=('Helvetica', 12), width=25, bd=2)
entry_port.grid(row=0, column=1, padx=10)

button_start = tk.Button(root, text="Run server", command=start_server_thread, **style)
button_start.pack(pady=20)

label_ip = tk.Label(root, text="IPv4 address of server: Undefined", bg="#f7f7f7", font=('Helvetica', 12))
label_ip.pack(pady=10)

frame_log = tk.Frame(root, bg="#f7f7f7")
frame_log.pack(pady=20)

listbox_log = tk.Listbox(frame_log, height=10, width=50, font=('Helvetica', 12), bd=2, selectmode=tk.SINGLE)
listbox_log.pack(side=tk.LEFT, fill=tk.BOTH)
scrollbar_log = tk.Scrollbar(frame_log)
scrollbar_log.pack(side=tk.RIGHT, fill=tk.Y)

listbox_log.config(yscrollcommand=scrollbar_log.set)
scrollbar_log.config(command=listbox_log.yview)

root.mainloop()
