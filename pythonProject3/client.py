import tkinter as tk
import socket
import threading

def receive_messages(client_socket, chat_text_widget):
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                chat_text_widget.after(0, update_chat_text, chat_text_widget, f"Server: {message}\n")
            else:
                break
    except Exception as e:
        print(f"Error receiving message: {e}")
    finally:
        client_socket.close()

def send_message_to_server(message, client_socket, chat_text_widget):
    if message:
        try:
            client_socket.send(message.encode('utf-8'))
            chat_text_widget.after(0, update_chat_text, chat_text_widget, f"You: {message}\n")
        except Exception as e:
            print(f"Error sending message: {e}")

def connect_to_server(ip, port, chat_text_widget):
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((ip, port))
        update_chat_text(chat_text_widget, f"Connected to {ip}:{port}\n")

        threading.Thread(target=receive_messages, args=(client_socket, chat_text_widget), daemon=True).start()

    except Exception as e:
        update_chat_text(chat_text_widget, f"Connection failed: {e}\n")

def update_chat_text(chat_text_widget, text):
    chat_text_widget.config(state=tk.NORMAL)
    chat_text_widget.insert(tk.END, text)
    chat_text_widget.config(state=tk.DISABLED)

def client_interface():
    global client_socket

    client_window = tk.Tk()
    client_window.resizable(False, False)
    client_window.title("Client Chat")
    client_window.config(bg="#2e3b4e")

    left_frame = tk.Frame(client_window, bg="#2e3b4e")
    left_frame.pack(side=tk.LEFT, padx=20, pady=20)

    tk.Label(left_frame, text="IP Address:", fg="#ffffff", bg="#2e3b4e", font=("Helvetica", 12)).pack(pady=5)
    ip_entry = tk.Entry(left_frame, width=30, font=("Helvetica", 12))
    ip_entry.insert(0, '127.0.0.1')
    ip_entry.pack(pady=5)

    # Поле ввода порта
    tk.Label(left_frame, text="Port:", fg="#ffffff", bg="#2e3b4e", font=("Helvetica", 12)).pack(pady=5)
    port_entry = tk.Entry(left_frame, width=30, font=("Helvetica", 12))
    port_entry.insert(0, '65432')
    port_entry.pack(pady=5)

    chat_text = tk.Text(client_window, state=tk.DISABLED, width=50, height=15, bg="#1e2a35", fg="#ffffff",
                        font=("Helvetica", 12))
    chat_text.pack(pady=10)

    entry_message = tk.Entry(client_window, width=40, font=("Helvetica", 12))
    entry_message.pack(pady=10)

    def send_message():
        message = entry_message.get()
        if client_socket:
            send_message_to_server(message, client_socket, chat_text)
            entry_message.delete(0, tk.END)

    send_button = tk.Button(client_window, text="Send", command=send_message, width=15, bg="#4e5b70", fg="#ffffff",
                            font=("Helvetica", 12, "bold"))
    send_button.pack(pady=5)

    def connect():
        ip = ip_entry.get()
        port = int(port_entry.get())

        connect_to_server(ip, port, chat_text)

    connect_button = tk.Button(left_frame, text="Connect to Server", command=connect, width=20, bg="#4e5b70",
                               fg="#ffffff", font=("Helvetica", 12, "bold"))
    connect_button.pack(pady=10)

    client_window.mainloop()

if __name__ == "__main__":
    client_interface()
