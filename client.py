import requests
import os
from crypto_utils import encrypt, generate_hmac, derive_key

SERVER_URL = "https://127.0.0.1:5000"
CHUNK_SIZE = 1024 * 1024  # 1MB

password = b"mypassword"
salt = b"salt123"
key = derive_key(password, salt)

def upload_file(filepath):
    file_id = os.path.basename(filepath)

    with open(filepath, "rb") as f:
        data = f.read()

    encrypted = encrypt(data, key)

    for i in range(0, len(encrypted), CHUNK_SIZE):
        chunk = encrypted[i:i+CHUNK_SIZE]
        tag = generate_hmac(chunk, key)

        files = {"file": chunk}
        data_form = {
            "file_id": file_id,
            "chunk_index": i // CHUNK_SIZE,
            "hmac": tag.hex()
        }

        r = requests.post(
            SERVER_URL + "/upload",
            files=files,
            data=data_form,
            verify=False
        )

        print(f"Uploaded chunk {i // CHUNK_SIZE}")


def download_file(file_id):
    r = requests.get(SERVER_URL + f"/download/{file_id}", verify=False)

    encrypted_data = r.content

    from crypto_utils import decrypt
    decrypted = decrypt(encrypted_data, key)

    with open("downloaded_" + file_id, "wb") as f:
        f.write(decrypted)

    print("Downloaded and decrypted file")


if __name__ == "__main__":
    upload_file("test.txt")
    download_file("test.txt")