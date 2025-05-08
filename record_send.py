import spidev
import socket
import wave
import time
import struct
import os
import sys

# ===== SETTINGS =====
DURATION_SEC = 2
SAMPLE_RATE = 16000
SAMPLE_CHANNEL = 0  # MCP3008 CH0

# ===== DEFAULT NOTE NAME =====
NOTE_NAME = sys.argv[1] if len(sys.argv) > 1 else "recorded_note"
FILENAME = NOTE_NAME + ".wav"

# ===== SPI SETUP =====
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

# ===== NETWORK SETUP =====
SERVER_IP = '172.20.10.12'
SERVER_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ===== RECORD FUNCTION =====
def read_adc(channel):
    assert 0 <= channel <= 7
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    value = ((adc[1] & 3) << 8) + adc[2]
    return value

def save_to_wav(filename, samples, sample_rate):
    samples = [int(max(-32768, min(32767, sample))) for sample in samples]
    packed = struct.pack('<' + 'h' * len(samples), *samples)
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(packed)

try:
    print(f"[Client] Recording {NOTE_NAME} for {DURATION_SEC} seconds...")
    raw = []
    start_time = time.time()
    while time.time() - start_time < DURATION_SEC:
        val = read_adc(SAMPLE_CHANNEL)
        raw.append(val)
        if len(raw) % 1000 == 0:
            print(f"Sample {len(raw)}: Raw ADC = {val}")

    mean = sum(raw) / len(raw)
    samples = [int(max(-32768, min(32767, ((x - mean) / 512.0) * 10000))) for x in raw]

    save_to_wav(FILENAME, samples, SAMPLE_RATE)
    print(f"[Client] Saved to {FILENAME}")

    sock.connect((SERVER_IP, SERVER_PORT))
    sock.sendall((FILENAME + '\n').encode())
    with open(FILENAME, 'rb') as f:
        sock.sendfile(f)
    sock.close()
    print("[Client] File sent")

    os.remove(FILENAME)

except Exception as e:
    print(f"[Client] Error: {e}")

finally:
    spi.close()
    sock.close()