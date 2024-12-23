import tkinter as tk
from tkinter import simpledialog, messagebox
from cryptography.fernet import Fernet
import pyperclip  # buffer
import mysql.connector


def generate_key():
    return Fernet.generate_key()


def encrypt_password(password, key):
    f = Fernet(key)
    encrypted = f.encrypt(password.encode())
    return encrypted


def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    decrypted = f.decrypt(encrypted_password).decode()
    return decrypted


def add_password_to_db(encrypted_password):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Karen1234",
            database="base"
        )
        cursor = conn.cursor()

        cursor.execute("INSERT INTO server_passwords (password) VALUES (%s)", (encrypted_password,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Password successfully added to the database!")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error when adding a password to the database: {err}")


def custom_input_window(title, prompt, default_value=""):
    input_window = tk.Toplevel()
    input_window.title(title)
    input_window.geometry("350x200")
    input_window.config(bg='#4e5b70')

    label = tk.Label(input_window, text=prompt, font=("Helvetica", 14, 'bold'), fg='#ffffff', bg='#4e5b70')
    label.pack(pady=20)

    entry = tk.Entry(input_window, font=("Helvetica", 12), width=30)
    entry.insert(0, default_value)
    entry.pack(pady=10)

    result = None

    def on_submit():
        nonlocal result
        result = entry.get()
        input_window.destroy()

    submit_button = tk.Button(input_window, text="OK", command=on_submit, font=("Helvetica", 12), bg='#627b8d', fg='#ffffff', width=10)
    submit_button.pack(pady=10)

    input_window.wait_window()

    return result


def custom_info_window(title, message):
    info_window = tk.Toplevel()
    info_window.title(title)
    info_window.geometry("350x200")
    info_window.config(bg='#4e5b70')

    label = tk.Label(info_window, text=message, font=("Helvetica", 12), fg='#ffffff', bg='#4e5b70')
    label.pack(pady=20)

    close_button = tk.Button(info_window, text="Close", command=info_window.destroy, font=("Helvetica", 12), bg='#627b8d', fg='#ffffff', width=10)
    close_button.pack(pady=10)

    info_window.wait_window()


# Интерфейс
def on_encrypt_button_click():
    password = custom_input_window("Encrypting", "Enter password for encrypting:")
    if password:
        key = generate_key()
        encrypted_password = encrypt_password(password, key)

        add_password_to_db(encrypted_password.decode())

        message = f"Encrypted password: {encrypted_password.decode()}\n\nKey: {key.decode()}"
        custom_info_window("Encrypted password", message)
        return key, encrypted_password
    else:
        messagebox.showerror("Error", "You didn't enter your password!")


def on_decrypt_button_click():
    key_str = custom_input_window("Key", "Enter key for decrypting:")
    encrypted_password_str = custom_input_window("Encrypted password", "Enter encrypted password:")

    try:
        key = key_str.encode()
        encrypted_password = encrypted_password_str.encode()

        decrypted_password = decrypt_password(encrypted_password, key)
        custom_info_window("Decrypted password", f"Decrypted password: {decrypted_password}")
    except Exception as e:
        messagebox.showerror("Error", f"Error during decrypting: {str(e)}")


def copy_key_to_clipboard(key):
    pyperclip.copy(key.decode())
    custom_info_window("Key has been copied", "The key has been successfully copied to the clipboard!")


style = {
    'bg': '#4e5b70',
    'fg': '#ffffff',
    'font': ('Helvetica', 12, 'bold'),
    'activebackground': '#627b8d',
    'width': 20,
    'height': 2
}

def main_window():
    root = tk.Tk()
    root.resizable(False, False)
    root.title("Password encrypting and decrypting")
    root.geometry("450x350")
    root.config(bg='#4e5b70')

    header_label = tk.Label(root, text="Password encrypting and decrypting", font=("Helvetica", 16, 'bold'), bg='#4e5b70', fg='#ffffff')
    header_label.pack(pady=20)

    encrypt_button = tk.Button(root, text="Encrypt", command=lambda: on_encrypt_button_click(), **style)
    encrypt_button.pack(pady=15)

    decrypt_button = tk.Button(root, text="Decrypt", command=on_decrypt_button_click, **style)
    decrypt_button.pack(pady=15)

    def on_copy_key_button_click():
        key, _ = on_encrypt_button_click()
        copy_key_to_clipboard(key)

    copy_key_button = tk.Button(root, text="Encrypt and copy key", command=on_copy_key_button_click, **style)
    copy_key_button.pack(pady=15)

    root.mainloop()


if __name__ == "__main__":
    main_window()
