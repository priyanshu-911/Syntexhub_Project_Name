import socket
import threading
from crypto_utils import encrypt, decrypt

HOST = '127.0.0.1'
PORT = 5000

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break

            message = decrypt(data)
            print(f"\n[RECEIVED]: {message}")

        except:
            break


def send_messages(sock):
    while True:
        message = input()
        encrypted_msg = encrypt(message)
        sock.send(encrypted_msg)


def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    threading.Thread(
        target=receive_messages,
        args=(client,),
        daemon=True
    ).start()

    send_messages(client)


if __name__ == "__main__":
    start_client()