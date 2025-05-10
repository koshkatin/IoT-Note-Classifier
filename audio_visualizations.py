# Script created with guidance from ChatGPT (OpenAI, 2025).
# Portions of the code were co-developed through interactive 
# sessions with ChatGPT to assist in audio processing, visualization, 
# and classification tasks.

import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import scipy.fft
import sys
import os

def plot_all(audio_path):
    y, sr = librosa.load(audio_path, sr=16000)
    duration = len(y) / sr
    t = np.linspace(0, duration, len(y))

    # ==== FFT ====
    fft = np.abs(scipy.fft.fft(y))
    freqs = scipy.fft.fftfreq(len(fft), 1/sr)
    half_n = len(freqs) // 2

    # ==== Spectrogram ====
    S = librosa.stft(y)
    S_db = librosa.amplitude_to_db(np.abs(S), ref=np.max)

    # ==== MFCC ====
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

    # ==== Plotting ====
    fig, axs = plt.subplots(3, 1, figsize=(10, 12))

    # 1. Time Domain
    axs[0].plot(t, y)
    axs[0].set_title("Waveform (Time Domain)")
    axs[0].set_xlabel("Time (s)")
    axs[0].set_ylabel("Amplitude")

    # 2. Frequency Domain
    axs[1].plot(freqs[:half_n], fft[:half_n])
    axs[1].set_title("FFT (Frequency Spectrum)")
    axs[1].set_xlabel("Frequency (Hz)")
    axs[1].set_ylabel("Magnitude")

    # 3. Spectrogram (dB)
    img = librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='log', ax=axs[2])
    axs[2].set_title("Spectrogram (dB, Log-Frequency Scale)")
    fig.colorbar(img, ax=axs[2], format="%+2.0f dB")

    plt.tight_layout()
    plt.savefig("visualizations/fft_spectrogram.png", dpi=300)
    plt.close()

    # ==== MFCC Plot ====
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(mfccs, x_axis='time', sr=sr)
    plt.colorbar()
    plt.title("MFCCs")
    plt.tight_layout()
    plt.savefig("visualizations/mfccs.png", dpi=300)
    plt.close()

    print("✅ Saved FFT/Spectrogram and MFCC plots to 'visualizations/'")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 audio_visualizations.py path/to/audio.wav")
        sys.exit(1)

    os.makedirs("visualizations", exist_ok=True)
    plot_all(sys.argv[1])