import socket
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def list_photos():
    photo_list = [f for f in os.listdir('.') if f.lower().endswith(('.jpg', '.jpeg'))]
    return photo_list

def send_photo():
    server_ip = entry_ip.get()
    server_port = int(entry_port.get())

    if not server_ip or not server_port:
        messagebox.showerror("Error", "Please, enter valid IP and Port.")
        return

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (server_ip, server_port)
        client_socket.connect(server_address)
    except Exception as e:
        messagebox.showerror("Error during connection", f"Cant connect to server: {e}")
        return

    if not photo_name:
        messagebox.showerror("Error", "Choose photo for send.")
        client_socket.close()
        return

    try:
        with open(photo_name, 'rb') as file:
            photo_data = file.read()

        client_socket.sendall(photo_data)
        messagebox.showinfo("Success", f"Photo '{photo_name}' successfully seneded to server.")
    except FileNotFoundError:
        messagebox.showerror("Error", f"File '{photo_name}' not found.")
    finally:
        client_socket.close()

def show_photos():
    photos = list_photos()
    if photos:
        photos_list.delete(0, tk.END)
        for p in photos:
            photos_list.insert(tk.END, p)
    else:
        messagebox.showinfo("Information", "Photo has not found.")

def choose_photo():
    global photo_name
    photo_name = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg")])
    if photo_name:
        label_photo.config(text=f"Chosen photo: {os.path.basename(photo_name)}")
    else:
        label_photo.config(text="Photo dont chosen.")

root = tk.Tk()
root.resizable(False, False)
root.title("Photo sender")
root.geometry("500x500")
root.config(bg="#f0f0f0")

style = {
    'bg': '#4e5b70',
    'fg': '#ffffff',
    'font': ('Helvetica', 12, 'bold'),
    'activebackground': '#627b8d',
    'width': 20
}

frame_input = tk.Frame(root, bg="#f0f0f0")
frame_input.pack(pady=20)

label_ip = tk.Label(frame_input, text="Ip address:", bg="#f0f0f0", font=('Helvetica', 12))
label_ip.grid(row=0, column=0, padx=5, sticky="e")
entry_ip = tk.Entry(frame_input, font=('Helvetica', 12), width=25, bd=2)
entry_ip.grid(row=0, column=1, padx=5)

label_port = tk.Label(frame_input, text="Port:", bg="#f0f0f0", font=('Helvetica', 12))
label_port.grid(row=1, column=0, padx=5, sticky="e")
entry_port = tk.Entry(frame_input, font=('Helvetica', 12), width=25, bd=2)
entry_port.grid(row=1, column=1, padx=5)

frame_buttons = tk.Frame(root, bg="#f0f0f0")
frame_buttons.pack(pady=20)

button_choose = tk.Button(frame_buttons, text="Choose photo", command=choose_photo, **style)
button_choose.grid(row=0, column=0, padx=10)

button_send = tk.Button(frame_buttons, text="Send photo", command=send_photo, **style)
button_send.grid(row=0, column=1, padx=10)

label_photo = tk.Label(root, text="Photo dont chosen.", bg="#f0f0f0", font=('Helvetica', 12))
label_photo.pack(pady=10)

button_show = tk.Button(root, text="Display available photos", command=show_photos, **style)
button_show.pack(pady=10)

photos_list = tk.Listbox(root, font=('Helvetica', 12), height=6, width=40, selectmode=tk.SINGLE)
photos_list.pack(pady=10)

photo_name = ""

root.mainloop()
