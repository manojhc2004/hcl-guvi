import librosa
import numpy as np


def detect_voice(file_path):

    y, sr = librosa.load(file_path, sr=16000, duration=5)

    pitch = librosa.yin(y, fmin=50, fmax=300)
    pitch_var = np.var(pitch)

    zcr = np.mean(librosa.feature.zero_crossing_rate(y=y))
    spectral = np.mean(librosa.feature.spectral_flatness(y=y))
    rms = librosa.feature.rms(y=y)
    energy_var = np.var(rms)



    score_value = pitch_var + zcr + spectral + (energy_var * 2)


    confidence = float(min(max(score_value / 10, 0.60), 0.98))

    if score_value < 7:
        return "AI_GENERATED", confidence, "Synthetic speech patterns detected"

    return "HUMAN", confidence, "Natural human voice characteristics detected"
