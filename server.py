import socket
import threading
from crypto_utils import encrypt, decrypt

HOST = '0.0.0.0'
PORT = 5000

clients = []

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except:
                clients.remove(client)

def handle_client(client_socket, addr):
    print(f"[CONNECTED] {addr}")

    while True:
        try:
            data = client_socket.recv(1024)

            if not data:
                break

            message = decrypt(data)
            print(f"[{addr}] {message}")

            encrypted_msg = encrypt(message)
            broadcast(encrypted_msg, client_socket)

        except:
            break

    print(f"[DISCONNECTED] {addr}")
    clients.remove(client_socket)
    client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"[SERVER STARTED] {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)

        thread = threading.Thread(
            target=handle_client,
            args=(client_socket, addr)
        )
        thread.start()


if __name__ == "__main__":
    start_server()