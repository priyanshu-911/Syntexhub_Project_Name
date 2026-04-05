from flask import Flask, request, send_file
import os
from crypto_utils import verify_hmac

app = Flask(__name__)
UPLOAD_FOLDER = "storage"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

SECRET_KEY = b"supersecretkey123"

@app.route("/upload", methods=["POST"])
def upload():
    file_id = request.form["file_id"]
    chunk_index = request.form["chunk_index"]
    hmac_tag = bytes.fromhex(request.form["hmac"])

    chunk = request.files["file"].read()

    try:
        verify_hmac(chunk, SECRET_KEY, hmac_tag)
    except:
        return "Integrity check failed", 400

    filename = f"{UPLOAD_FOLDER}/{file_id}_{chunk_index}"
    with open(filename, "wb") as f:
        f.write(chunk)

    return "Chunk uploaded"


@app.route("/download/<file_id>", methods=["GET"])
def download(file_id):
    chunks = sorted([f for f in os.listdir(UPLOAD_FOLDER) if f.startswith(file_id)])

    filepath = f"{UPLOAD_FOLDER}/{file_id}_complete"
    with open(filepath, "wb") as outfile:
        for chunk_file in chunks:
            with open(f"{UPLOAD_FOLDER}/{chunk_file}", "rb") as infile:
                outfile.write(infile.read())

    return send_file(filepath, as_attachment=True)


if __name__ == "__main__":
    app.run(ssl_context="adhoc")  # HTTPS enabled