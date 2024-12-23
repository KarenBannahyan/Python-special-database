import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import ctypes
import sys

def run_as_admin(script_path):
    if ctypes.windll.shell32.IsUserAnAdmin():
        subprocess.run([sys.executable, script_path])
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, script_path, None, 1)
def start_chat():
    subprocess.Popen(['python', 'chat.py'])

def start_decode():
    subprocess.Popen(['python', 'Decrypt.py'])

def start_screen_sharing():
    run_as_admin("screen.py")
def start_ftp():
    subprocess.Popen(['python', 'FTPserver.py'])

root = tk.Tk()
root.resizable(False, False)
root.title("Server Application")
root.geometry("400x300")
root.config(bg="#2e3b4e")

style = {
    'bg': '#4e5b70',
    'fg': '#ffffff',
    'font': ('Helvetica', 12, 'bold'),
    'activebackground': '#627b8d',
    'width': 20
}

frame = tk.Frame(root, bg="#2e3b4e")

frame.pack(pady=40)

button_chat = tk.Button(frame, text="Start Chat", command=start_chat, **style)
button_chat.grid(row=0, column=0, padx=10, pady=10)

button_screen_sharing = tk.Button(frame, text="Start Screen Sharing", command=start_screen_sharing, **style)
button_screen_sharing.grid(row=1, column=0, padx=10, pady=10)

button_ftp = tk.Button(frame, text="Start FTP", command=start_ftp, **style)
button_ftp.grid(row=2, column=0, padx=10, pady=10)

button_exit = tk.Button(frame, text="Decode", command=start_decode, **style)
button_exit.grid(row=3, column=0, padx=10, pady=10)

label = tk.Label(root, text="Server Control Panel", font=('Helvetica', 16, 'bold'), fg='#ffffff', bg='#2e3b4e')
label.pack(pady=10)

root.mainloop()
