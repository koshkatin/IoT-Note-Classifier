# Script created with guidance from ChatGPT (OpenAI, 2025).
# Portions of the code were co-developed through interactive 
# sessions with ChatGPT to assist in audio processing, visualization, 
# and classification tasks.

import os
import librosa
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import matplotlib.pyplot as plt

# -----------------------------
# Feature extraction function
# -----------------------------
def extract_features(y, sr=16000, n_mfcc=40):
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
    zero_crossing = librosa.feature.zero_crossing_rate(y)
    combined = np.hstack((
        np.mean(mfcc.T, axis=0),
        np.mean(chroma.T, axis=0),
        np.mean(spectral_contrast.T, axis=0),
        np.mean(zero_crossing.T, axis=0)
    ))
    return combined

# -----------------------------
# Load real recordings
# -----------------------------
def extract_real_dataset_features(base_dir='real_data'):
    features = []
    labels = []
    for note in sorted(os.listdir(base_dir)):
        folder = os.path.join(base_dir, note)
        if not os.path.isdir(folder):
            continue
        for fname in os.listdir(folder):
            if fname.endswith('.wav'):
                path = os.path.join(folder, fname)
                y, sr = librosa.load(path, sr=16000)
                feat = extract_features(y)
                features.append(feat)
                labels.append(note)
    return np.array(features), np.array(labels)

# -----------------------------
# Load and prepare generated data
# -----------------------------
note_frequencies = {
    'C3': 130.81, 'D3': 146.83, 'E3': 164.81, 'F3': 174.61,
    'G3': 196.00, 'A3': 220.00, 'B3': 246.94, 'C4': 261.63, 'D4': 293.66,
    'E4': 329.63, 'F4': 349.23, 'G4': 392.00, 'A4': 440.00, 'B4': 493.88,
    'C5': 523.25, 'D5': 587.33, 'E5': 659.25, 'F5': 698.46, 'G5': 783.99,
    'A5': 880.00, 'B5': 987.77, 'C6': 1046.50, 'D6': 1174.66, 'E6': 1318.51,
    'F6': 1396.91, 'G6': 1567.98, 'A6': 1760.00, 'B6': 1975.53,
    'C7': 2093.00, 'D7': 2349.32, 'E7': 2637.02
}

def generate_clean_data(note_frequencies):
    from scipy.signal import sawtooth
    import wave
    def generate_complex_wave(frequency, sample_rate=16000, duration=2):
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        sine_wave = np.sin(2 * np.pi * frequency * t)
        harmonic1 = 0.5 * np.sin(2 * np.pi * 2 * frequency * t)
        harmonic2 = 0.25 * np.sin(2 * np.pi * 3 * frequency * t)
        combined = sine_wave + harmonic1 + harmonic2
        combined = combined / np.max(np.abs(combined))
        return (combined * 32767).astype(np.int16)

    features = []
    labels = []
    for note, freq in note_frequencies.items():
        y = generate_complex_wave(freq).astype(np.float32) / 32767
        feat = extract_features(y)
        features.append(feat)
        labels.append(note)
    return np.array(features), np.array(labels)

# Load both datasets
X_synth, y_synth = generate_clean_data(note_frequencies)
X_real, y_real = extract_real_dataset_features('real_data')

# Merge
X = np.concatenate([X_synth, X_real])
y = np.concatenate([y_synth, y_real])

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Scale
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train
model = SVC(kernel='rbf', C=1, gamma='scale')
model.fit(X_train_scaled, y_train)
print("Accuracy:", model.score(X_test_scaled, y_test))

# Save
joblib.dump(model, 'note_classifier_mixed.pkl')
joblib.dump(scaler, 'note_scaler.pkl')
