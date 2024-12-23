import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
import mysql.connector

style = {
    'bg': '#4e5b70',
    'fg': '#ffffff',
    'font': ('Helvetica', 12, 'bold'),
    'activebackground': '#627b8d',
    'width': 20
}

def create_database():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Karen1234',
            database='base'
        )
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_passwords (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
    except mysql.connector.Error as e:
        print(f"Error connecting or creating a database: {e}")
        messagebox.showerror("Error", f"Failed to connect to the database: {e}")


def encrypt_password(password, key):
    cipher = Fernet(key)
    encrypted_password = cipher.encrypt(password.encode())
    return encrypted_password


def save_to_db(name, password, key):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Karen1234',
            database='base'
        )
        cursor = conn.cursor()

        encrypted_password = encrypt_password(password, key)

        cursor.execute('''
            INSERT INTO user_passwords (name, password) VALUES (%s, %s)
        ''', (name, encrypted_password))
        conn.commit()
        conn.close()
        print("The data has been successfully saved in the database.")
    except mysql.connector.Error as e:
        print(f"Error saving data to database: {e}")
        messagebox.showerror("Error", f"Failed to save data to the database: {e}")


def on_submit():
    name = entry_name.get()
    password = entry_password.get()

    if not name or not password:
        messagebox.showwarning("Error", "Please enter your username and password!")
        return

    key = Fernet.generate_key()

    save_to_db(name, password, key)

    label_key.config(text=f"Encryption key: {key.decode()}")
    button_copy.config(state=tk.NORMAL)


def copy_key():
    key = label_key.cget("text").replace("Encryption key: ", "")
    root.clipboard_clear()
    root.clipboard_append(key)
    messagebox.showinfo("Success", "The encryption key has been copied to the clipboard!")


root = tk.Tk()
root.resizable(False, False)
root.title("Data encryption")
root.geometry("400x300")
root.configure(bg='#4e5b70')

label_name = tk.Label(root, text="Username:", bg='#4e5b70', fg='#ffffff', font=('Helvetica', 12))
label_name.pack(pady=5)

entry_name = tk.Entry(root, font=('Helvetica', 12))
entry_name.pack(pady=5)

label_password = tk.Label(root, text="Password:", bg='#4e5b70', fg='#ffffff', font=('Helvetica', 12))
label_password.pack(pady=5)

entry_password = tk.Entry(root, font=('Helvetica', 12), show="*")
entry_password.pack(pady=5)

button_submit = tk.Button(root, text="Send", command=on_submit, **style)
button_submit.pack(pady=20)

label_key = tk.Label(root, text="", bg='#4e5b70', fg='#ffffff', font=('Helvetica', 12))
label_key.pack(pady=10)

button_copy = tk.Button(root, text="Copy Key", command=copy_key, state=tk.DISABLED, **style)
button_copy.pack(pady=10)

create_database()

root.mainloop()
