# Script created with guidance from ChatGPT (OpenAI, 2025).
# Portions of the code were co-developed through interactive 
# sessions with ChatGPT to assist in audio processing, visualization, 
# and classification tasks.

import librosa
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler

# === CONFIG ===
MODEL_PATH = 'note_classifier_real_only.pkl'
SCALER_PATH = 'note_scaler.pkl'
INPUT_WAV = 'inference/received_note.wav'

# === Feature extraction ===
def extract_features(y, sr=16000, n_mfcc=40):
    from scipy.signal import butter, filtfilt

    def bandpass_filter(signal, sr, lowcut=100, highcut=2000, order=5):
        nyq = 0.5 * sr
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        return filtfilt(b, a, signal)

    y_filtered = y  # Or use bandpass_filter(y, sr) if needed
    mfcc = librosa.feature.mfcc(y=y_filtered, sr=sr, n_mfcc=n_mfcc)
    chroma = librosa.feature.chroma_stft(y=y_filtered, sr=sr)
    spectral_contrast = librosa.feature.spectral_contrast(y=y_filtered, sr=sr)
    zero_crossing = librosa.feature.zero_crossing_rate(y_filtered)

    combined = np.hstack((
        np.mean(mfcc.T, axis=0),
        np.mean(chroma.T, axis=0),
        np.mean(spectral_contrast.T, axis=0),
        np.mean(zero_crossing.T, axis=0)
    ))
    return combined

# === Load model and scaler ===
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# === Load and classify the input file ===
print(f"\n[Loading] {INPUT_WAV}")
y, sr = librosa.load(INPUT_WAV, sr=16000)
feature = extract_features(y)
feature_scaled = scaler.transform([feature])
prediction = model.predict(feature_scaled)[0]

print(f"\n🎵 Predicted Note: {prediction}")

with open("visual/note.txt", "w") as f:
    f.write(prediction + "\n")