import tkinter as tk
import socket
import threading
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64
import mysql.connector
from mysql.connector import Error

KEY_SIZE = 32  # 256 бит
BLOCK_SIZE = 16  # 128 бит

def generate_key_iv():
    key = os.urandom(KEY_SIZE)
    iv = os.urandom(BLOCK_SIZE)
    return key, iv

def encrypt_message(message, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    pad_length = BLOCK_SIZE - len(message) % BLOCK_SIZE
    message_padded = message.encode('utf-8') + bytes([pad_length] * pad_length)
    encrypted_message = encryptor.update(message_padded) + encryptor.finalize()
    return encrypted_message

def decrypt_message(encrypted_message, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(encrypted_message) + decryptor.finalize()
    pad_length = decrypted_message[-1]
    return decrypted_message[:-pad_length].decode('utf-8')

def save_message_to_db(encrypted_message, key, iv):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='base',
            user='root',
            password='Karen1234'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("INSERT INTO messages (message, encryption_key, encryption_iv) VALUES (%s, %s, %s)",
                           (base64.b64encode(encrypted_message).decode('utf-8'),
                            base64.b64encode(key).decode('utf-8'),
                            base64.b64encode(iv).decode('utf-8')))
            connection.commit()
            cursor.close()
    except Error as e:
        print(f"Error while saving to database: {e}")
    finally:
        if connection.is_connected():
            connection.close()

def log_encrypted_message(encrypted_message, key, iv):
    with open('logs.txt', 'a') as log_file:
        log_file.write(f"Encrypted Message: {base64.b64encode(encrypted_message).decode('utf-8')}\n")
        log_file.write(f"Key: {base64.b64encode(key).decode('utf-8')}\n")
        log_file.write(f"IV: {base64.b64encode(iv).decode('utf-8')}\n\n")

def handle_client(client_socket, chat_text_widget):
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                chat_text_widget.config(state=tk.NORMAL)
                chat_text_widget.insert(tk.END, f"Client: {message}\n")
                chat_text_widget.config(state=tk.DISABLED)

                key, iv = generate_key_iv()

                encrypted_message = encrypt_message(message, key, iv)

                save_message_to_db(encrypted_message, key, iv)
                log_encrypted_message(encrypted_message, key, iv)

            else:
                break
    except Exception as e:
        print(f"Error while handling client: {e}")
    finally:
        client_socket.close()

def start_server(ip, port, chat_text_widget):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(5)

    update_chat_text(chat_text_widget, "Server started. Waiting for connections...\n")

    while True:
        try:
            client_socket, addr = server.accept()
            update_chat_text(chat_text_widget, f"Connected to {addr}\n")
            threading.Thread(target=handle_client, args=(client_socket, chat_text_widget), daemon=True).start()

            while True:
                message = input("Enter message to send to client: ")
                if message:
                    send_message_to_client(message, client_socket, chat_text_widget)

        except Exception as e:
            print(f"Error while accepting connection: {e}")
            break

def send_message_to_client(message, client_socket, chat_text_widget):
    if message and client_socket:
        try:
            client_socket.send(message.encode('utf-8'))
            update_chat_text(chat_text_widget, f"You (Server): {message}\n")
        except Exception as e:
            update_chat_text(chat_text_widget, f"Error sending message: {e}\n")

def update_chat_text(chat_text_widget, text):
    chat_text_widget.config(state=tk.NORMAL)
    chat_text_widget.insert(tk.END, text)
    chat_text_widget.config(state=tk.DISABLED)

def server_interface():
    server_window = tk.Tk()
    server_window.resizable(False, False)
    server_window.title("Server Chat")
    server_window.config(bg="#2e3b4e")

    left_frame = tk.Frame(server_window, bg="#2e3b4e")
    left_frame.pack(side=tk.LEFT, padx=20, pady=20)

    tk.Label(left_frame, text="IP Address:", fg="#ffffff", bg="#2e3b4e", font=("Helvetica", 12)).pack(pady=5)
    ip_entry = tk.Entry(left_frame, width=30, font=("Helvetica", 12))
    ip_entry.insert(0, '127.0.0.1')  # Стандартный IP
    ip_entry.pack(pady=5)

    tk.Label(left_frame, text="Port:", fg="#ffffff", bg="#2e3b4e", font=("Helvetica", 12)).pack(pady=5)
    port_entry = tk.Entry(left_frame, width=30, font=("Helvetica", 12))
    port_entry.insert(0, '65432')  # Стандартный порт
    port_entry.pack(pady=5)

    chat_text = tk.Text(server_window, state=tk.DISABLED, width=50, height=15, bg="#1e2a35", fg="#ffffff",
                        font=("Helvetica", 12))
    chat_text.pack(pady=10)

    def start():
        ip = ip_entry.get()
        port = int(port_entry.get())

        threading.Thread(target=start_server, args=(ip, port, chat_text), daemon=True).start()

        update_chat_text(chat_text, "Server started. Waiting for connections...\n")

    start_button = tk.Button(left_frame, text="Start Server", command=start, width=20, bg="#4e5b70", fg="#ffffff",
                             font=("Helvetica", 12, "bold"))
    start_button.pack(pady=10)

    server_window.mainloop()

if __name__ == "__main__":
    server_interface()
