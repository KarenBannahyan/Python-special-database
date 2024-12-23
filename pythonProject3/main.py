import tkinter as tk
from tkinter import messagebox
import mysql.connector
from cryptography.fernet import Fernet
import subprocess  # For server.py and client.py


def generate_key():
    return Fernet.generate_key()


def encrypt_password(password, key):
    f = Fernet(key)
    encrypted = f.encrypt(password.encode())
    return encrypted


def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    try:
        decrypted = f.decrypt(encrypted_password).decode()
        return decrypted
    except Exception as e:
        return None


def get_encrypted_passwords_from_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Karen1234",
            database="base"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM Server_Passwords")
        result = cursor.fetchall()
        conn.close()
        return [row[0] for row in result]
    except mysql.connector.Error as err:
        print(f"Error connecting: {err}")
        return []


def get_encrypted_password_from_db(username):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Karen1234",
            database="base"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM user_passwords WHERE name = %s", (username,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        else:
            return None
    except mysql.connector.Error as err:
        print(f"Error connectiong: {err}")
        return None


def start_server():
    try:
        subprocess.Popen(['python', 'server.py'])  # Запуск server.py
        messagebox.showinfo("Run", "Server successfully has ran!")
    except Exception as e:
        messagebox.showerror("Error", f"Cant run server: {e}")


def start_client():
    try:
        subprocess.Popen(['python', 'Main-Client.py'])  # Запуск client.py
        messagebox.showinfo("Launching", "Client successfully launched!")
    except Exception as e:
        messagebox.showerror("Error", f"Cant launch client: {e}")


style = {
    'bg': '#4e5b70',
    'fg': '#ffffff',
    'font': ('Helvetica', 12, 'bold'),
    'activebackground': '#627b8d',
    'width': 20
}


def custom_input_server_window(title, prompt):
    input_window = tk.Toplevel()
    input_window.title(title)
    input_window.geometry("400x200")
    input_window.config(bg='#4e5b70')

    label = tk.Label(input_window, text=prompt, font=('Helvetica', 12, 'bold'), bg='#4e5b70', fg='#ffffff')
    label.pack(pady=10)

    entry = tk.Entry(input_window, font=('Helvetica', 12), bg='#f5f5f5', fg='#333333', width=30)
    entry.pack(pady=10)

    def on_ok():
        key = entry.get()
        input_window.destroy()
        check_server_key(key)

    ok_button = tk.Button(input_window, text="OK", command=on_ok, **style)
    ok_button.pack(pady=10)

    input_window.mainloop()


def custom_input_client_window(title, prompt):
    input_window = tk.Toplevel()
    input_window.title(title)
    input_window.geometry("400x250")
    input_window.config(bg='#4e5b70')

    label = tk.Label(input_window, text=prompt, font=('Helvetica', 12, 'bold'), bg='#4e5b70', fg='#ffffff')
    label.pack(pady=10)

    name_label = tk.Label(input_window, text="Username:", font=('Helvetica', 12), bg='#4e5b70', fg='#ffffff')
    name_label.pack(pady=5)

    name_entry = tk.Entry(input_window, font=('Helvetica', 12), bg='#f5f5f5', fg='#333333', width=30)
    name_entry.pack(pady=10)

    key_label = tk.Label(input_window, text="Enter key:", font=('Helvetica', 12), bg='#4e5b70', fg='#ffffff')
    key_label.pack(pady=5)

    key_entry = tk.Entry(input_window, font=('Helvetica', 12), bg='#f5f5f5', fg='#333333', width=30)
    key_entry.pack(pady=10)

    def on_ok():
        username = name_entry.get()
        key_str = key_entry.get()
        input_window.destroy()
        if username and key_str:
            check_client_key(username, key_str)
        else:
            messagebox.showerror("Error", "Not all shields are full!")

    ok_button = tk.Button(input_window, text="OK", command=on_ok, **style)
    ok_button.pack(pady=10)

    input_window.mainloop()


def check_server_key(key_str):
    if not key_str:
        messagebox.showerror("Error", "Key not entered!")
        return

    try:
        key = key_str.encode()
        encrypted_passwords_db = get_encrypted_passwords_from_db()

        if encrypted_passwords_db:

            for encrypted_password_db in encrypted_passwords_db:
                decrypted_password = decrypt_password(encrypted_password_db.encode(), key)

                if decrypted_password:
                    messagebox.showinfo("Success", "Key is right")
                    start_server()
                    return

            messagebox.showerror("Error", "Invalid key")
        else:
            messagebox.showerror("Error", "Invalid password!")

    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")


def check_client_key(username, key_str):
    if not key_str:
        messagebox.showerror("Error", "Key not found!")
        return

    try:
        key = key_str.encode()
        encrypted_password_db = get_encrypted_password_from_db(username)

        if encrypted_password_db:
            decrypted_password = decrypt_password(encrypted_password_db.encode(), key)
            if decrypted_password:
                messagebox.showinfo("Success", "Key is right")
                start_client()
            else:
                messagebox.showerror("Error", "Invalid key!")
        else:
            messagebox.showerror("Eror", f"Username '{username}' not found!")

    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")


def on_server_button_click():
    custom_input_server_window("Key for server", "Enter key for decrypting:")


def on_client_button_click():
    custom_input_client_window("Key Verification", "Enter username and key:")


root = tk.Tk()
root.resizable(False, False)
root.title("Programm with server and client")
root.geometry("400x250")
root.config(bg='#4e5b70')

server_button = tk.Button(root, text="Server", command=on_server_button_click, **style)
client_button = tk.Button(root, text="Client", command=on_client_button_click, **style)

# Выравнивание по горизонтали с помощью pack()
server_button.place(relx=0.5, rely=0.3, anchor="center")  # Центрируем кнопку "Server"
client_button.place(relx=0.5, rely=0.6, anchor="center") # К

root.mainloop()
