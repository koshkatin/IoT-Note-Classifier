import socket
import os

SERVER_IP = '0.0.0.0'
PORT = 5005
BASE_DIR = 'real_data_v2'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((SERVER_IP, PORT))
sock.listen(1)

print(f"[Server] Listening on {SERVER_IP}:{PORT}...")

while True:
    conn, addr = sock.accept()
    print(f"[Server] Connection from {addr}")

    # First read the filename (sent with a newline)
    filename_bytes = b''
    while not filename_bytes.endswith(b'\n'):
        chunk = conn.recv(1)
        if not chunk:
            break
        filename_bytes += chunk

    filename = filename_bytes.decode().strip()
    note_name = filename.split('.')[0]

    # Create note folder if it doesn't exist
    note_folder = os.path.join(BASE_DIR, note_name)
    os.makedirs(note_folder, exist_ok=True)

    # Determine next file index for the note
    existing_files = sorted([
        f for f in os.listdir(note_folder)
        if f.startswith(note_name + "_") and f.endswith('.wav')
    ])
    index = len(existing_files) + 1
    unique_filename = f"{note_name}_{index:02d}.wav"
    save_path = os.path.join(note_folder, unique_filename)

    print(f"[Server] Saving to {save_path}...")
    with open(save_path, 'wb') as f:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            f.write(data)

    conn.close()
    print(f"[Server] ✅ Saved {save_path}\n")