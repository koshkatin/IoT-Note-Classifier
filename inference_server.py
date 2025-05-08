import socket
import os
import subprocess

SERVER_IP = '0.0.0.0'
PORT = 5005
INFER_DIR = 'inference'
os.makedirs(INFER_DIR, exist_ok=True)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((SERVER_IP, PORT))
sock.listen(1)

print(f"[Inference Server] Listening on {SERVER_IP}:{PORT}...")

while True:
    conn, addr = sock.accept()
    print(f"[Inference Server] Connection from {addr}")

    # Read the filename
    filename_bytes = b''
    while not filename_bytes.endswith(b'\n'):
        chunk = conn.recv(1)
        if not chunk:
            break
        filename_bytes += chunk

    filename = filename_bytes.decode().strip()
    save_path = os.path.join(INFER_DIR, "received_note.wav")

    print(f"[Inference Server] Saving to {save_path}...")
    with open(save_path, 'wb') as f:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            f.write(data)

    conn.close()
    print(f"[Inference Server] ✅ Saved {save_path}")

    print("[Inference Server] Running classifier...")
    try:
        result = subprocess.run([
            "python3", "classify.py", save_path
        ], capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"[Classifier ERROR] {e.stderr}")
    except Exception as ex:
        print(f"[Inference Server ERROR] {ex}")