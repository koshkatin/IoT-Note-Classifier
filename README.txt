# 🎶 Real-Time Note Classifier

This project captures audio from a Raspberry Pi via an analog microphone, 
classifies the musical note using a trained machine learning model, 
and displays real-time visual feedback in a browser using p5.js.

---

## 👥 Team Members
- Tina Habibi
- Faith Klein

---

## 🗂️ File Structure Overview

```
EE250-PROJECT/
│
├── graphics/                   # Assets for visual display
│   ├── note.txt                # Text file updated with current note
│   ├── Orbitron-VariableFont_wght.ttf
│   ├── p5.html                 # HTML wrapper for visualization
│   └── sketch.js               # Animated note visual in p5.js
│
├── inference/                 # Received inference WAV files
│   └── received_note.wav
│
├── real_data_v2/              # Recorded dataset for training
│   └── [C3/, C4/, ..., B5/]   # Subfolders per note with WAVs
│
├── visualizations/            # Automatically generated plots
│   ├── fft_spectrogram.png
│   └── mfccs.png
│
├── __pycache__/
├── venv/                      # Python virtual environment
│
├── classify.py                # Classifies single WAV file
├── record_send.py            # Runs on RPi to record and send WAV
├── socket_server.py          # Receives dataset files (RPi -> PC)
├── inference_server.py       # Classifies received WAV (inference)
├── real_model.py             # Trains ML model using real_data_v2/
├── ml_model.py               # Trains model from synthetic data
├── batch_record.py           # Automates multiple-note recordings
├── features.py               # Shared feature extraction functions
├── audio_visualizations.py   # Plots MFCCs and FFT from WAV files
│
├── note_classifier_real_only.pkl
├── note_classifier_mfcc.pkl
├── note_scaler.pkl
│
└── README.txt                # Project overview and setup
```

---

## 🚀 How to Run

### 1. Raspberry Pi (Recording)
On your Raspberry Pi, run:
```bash
python3 record_send.py
```

It will record 2 seconds of audio and send it to your PC.

---

### 2. Socket Server (on PC)
To receive and classify the note:
```bash
python3 inference_server.py
```

---

### 3. Visualization
Serve the visualization via a simple HTTP server:
```bash
python3 -m http.server 8000
```
Then open (http://localhost:8000/graphics/p5.html)

---

## 🔧 Dependencies

Install all dependencies:
```bash
pip install numpy librosa joblib scikit-learn matplotlib
```

Raspberry Pi also needs:
```bash
sudo apt-get install python3-spidev
```

---

## 💡 Acknowledgements
- All Python scripts and HTML/JS visualizations were developed with assistance from **ChatGPT**.
- Font used: [Orbitron](https://fonts.google.com/specimen/Orbitron)

## ChatGPT Promts
Audio Capture & Processing (Raspberry Pi):
	“Write a script to record audio from MCP3008 on the Pi and save as WAV.”
	“Normalize and scale ADC values for audio.”
	“Why does the recording sound too fast or off-pitch?”
	“Send the recording to the PC using sockets.”

Machine Learning:
	“Train a note classifier using synthetic and real data.”
	“Extract features like MFCC, chroma, and spectral contrast.”
	“Why is the model always predicting A4?”
	“Retrain using only real data from recordings.”

Batch Recording:
	“Create a script to batch record 5 samples per note, auto-naming them.”
	“Organize recordings into folders like real_data_v2/C4/.”
	“Restart the batch process and overwrite old recordings.”

Inference & Server:
	“Build a socket server to receive files and run classification.”
	“Save incoming files as received_note.wav for real-time use.”
	“Make a second server script just for batch mode.”

Visualization:
	“Visualize predictions using p5.js with animated, colorful shapes.”
	“Link the visual to read the prediction from note.txt.”

Documentation:
	“Write a final report and README with all instructions.”
	“Generate FFT and MFCC plots to include in the writeup.”
---

## 📁 Notes
- Make sure your Raspberry Pi mic circuit is wired and grounded properly.
- You can retrain the model with `real_model.py` after collecting new samples using `batch_record.py`.
