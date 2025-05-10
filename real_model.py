# Script created with guidance from ChatGPT (OpenAI, 2025).
# Portions of the code were co-developed through interactive 
# sessions with ChatGPT to assist in audio processing, visualization, 
# and classification tasks.

import os
import numpy as np
import librosa
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from collections import Counter

REAL_DATA_DIR = 'real_data_v2'
SAMPLE_RATE = 16000
N_MFCC = 40

# === Feature extraction ===
def extract_features(y, sr=16000):
    # y, _ = librosa.effects.trim(y, top_db=30)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=N_MFCC)
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

features = []
labels = []

print("[Info] Scanning real_data directory...")
for note in sorted(os.listdir(REAL_DATA_DIR)):
    note_dir = os.path.join(REAL_DATA_DIR, note)
    if not os.path.isdir(note_dir):
        continue
    for fname in os.listdir(note_dir):
        if fname.endswith('.wav'):
            path = os.path.join(note_dir, fname)
            try:
                y, sr = librosa.load(path, sr=SAMPLE_RATE)
                feat = extract_features(y, sr)
                features.append(feat)
                labels.append(note)
            except Exception as e:
                print(f"[Warning] Failed to load {path}: {e}")

print(f"[Data] Extracted {len(features)} samples from real data")
print("[Data] Label distribution:", Counter(labels))

X = np.array(features)
y = np.array(labels)

# === Train-test split ===
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# === Scale features ===
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# === Train model ===
model = SVC(kernel='rbf', C=1, gamma='scale', probability=True)
model.fit(X_train_scaled, y_train)
accuracy = model.score(X_test_scaled, y_test)
print(f"[Model] Accuracy on real data: {accuracy * 100:.2f}%")

# === Save artifacts ===
joblib.dump(model, 'note_classifier_real_only.pkl')
joblib.dump(scaler, 'note_scaler.pkl')
print("[Model] Saved to note_classifier_real_only.pkl")