import os
import time
import subprocess

NOTES = [
    "C3", "D3", "E3", "F3", "G3", "A3", "B3",
    "C4", "D4", "E4", "F4", "G4", "A4", "B4",
    "C5", "D5", "E5", "F5", "G5", "A5", "B5"
]

RECORDINGS_PER_NOTE = 5
PAUSE_BETWEEN = 0.5

for note in NOTES:
    print(f"\n🎵 Starting recordings for note: {note}")
    for i in range(RECORDINGS_PER_NOTE):
        print(f"  Recording sample {i+1}/{RECORDINGS_PER_NOTE} for {note}...")
        result = subprocess.run(["python3", "record_send.py", note])
        if result.returncode != 0:
            print(f"  ⚠️ Recording failed for {note} sample {i+1}")
        time.sleep(PAUSE_BETWEEN)
    print(f"✅ Finished {RECORDINGS_PER_NOTE} recordings for {note}")
    input("Press ENTER to continue to the next note...")