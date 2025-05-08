import librosa
import numpy as np

def extract_features(y, sr=16000, n_mfcc=40):
    """
    Extract features from an audio sample.
    """
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