import tkinter as tk
from tkinter import messagebox
import mysql.connector
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
from mysql.connector import Error

BLOCK_SIZE = 16  # 128 бит

def decrypt_message(encrypted_message, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(encrypted_message) + decryptor.finalize()
    pad_length = decrypted_message[-1]
    return decrypted_message[:-pad_length].decode('utf-8')

def get_message_from_db(message_id):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='base',
            user='root',
            password='Karen1234'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT message, encryption_key, encryption_iv FROM messages WHERE id = %s", (message_id,))
            result = cursor.fetchone()
            cursor.close()

            if result:
                encrypted_message = base64.b64decode(result[0])
                key = base64.b64decode(result[1])
                iv = base64.b64decode(result[2])
                return encrypted_message, key, iv
            else:
                return None, None, None

    except Error as e:
        print(f"Error while retrieving from database: {e}")
        return None, None, None

    finally:
        if connection.is_connected():
            connection.close()

def decrypt_from_db():
    try:
        message_id = int(message_id_entry.get())
        encrypted_message, key, iv = get_message_from_db(message_id)

        if encrypted_message and key and iv:
            decrypted_message = decrypt_message(encrypted_message, key, iv)
            result_label.config(text=f"Decrypted Message: {decrypted_message}")
        else:
            messagebox.showerror("Error", "No message found with this ID or invalid data.")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid message ID.")

def decryption_interface():
    window = tk.Tk()
    window.resizable(False, True)
    window.title("Message Decryption")
    window.geometry("400x300")  # Размер окна
    window.config(bg="#2e3b4e")

    main_frame = tk.Frame(window, bg="#2e3b4e", padx=20, pady=20)
    main_frame.pack(padx=20, pady=20)

    title_label = tk.Label(main_frame, text="Message Decryption", font=("Helvetica", 16, "bold"), fg="#ffffff", bg="#2e3b4e")
    title_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

    message_id_label = tk.Label(main_frame, text="Enter Message ID:", font=("Helvetica", 12), fg="#ffffff", bg="#2e3b4e")
    message_id_label.grid(row=1, column=0, pady=5, sticky="w")
    global message_id_entry
    message_id_entry = tk.Entry(main_frame, font=("Helvetica", 12), width=30)
    message_id_entry.grid(row=1, column=1, pady=5)

    decrypt_button = tk.Button(main_frame, text="Decrypt Message", command=decrypt_from_db, font=("Helvetica", 12), bg="#4e5b70", fg="#ffffff", relief="flat")
    decrypt_button.grid(row=2, column=0, columnspan=2, pady=15)

    separator = tk.Label(main_frame, text="", bg="#2e3b4e")
    separator.grid(row=3, column=0, columnspan=2, pady=10)

    global result_label

    result_label = tk.Label(main_frame, text="Decrypted Message will appear here.", font=("Helvetica", 12), fg="#e1e1e1", bg="#2e3b4e")
    result_label.place(x=10, y=15)
    result_label.grid(row=4, column=0, columnspan=2, pady=5, sticky="w")
    window.mainloop()

if __name__ == "__main__":
    decryption_interface()
