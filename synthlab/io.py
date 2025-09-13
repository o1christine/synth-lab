# synthlab/io.py
from __future__ import annotations
import os, wave
import numpy as np

def ensure_dir(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)

def write_wav(path: str, audio: np.ndarray, sr: int = 48000) -> None:
    """
    Write mono float32/float64 in [-1, 1] to 16-bit PCM WAV.
    """
    ensure_dir(path)
    x = np.clip(audio, -1.0, 1.0)
    y = (x * 32767.0).astype(np.int16)
    with wave.open(path, "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)   # 16-bit
        f.setframerate(sr)
        f.writeframes(y.tobytes())

def try_play(audio: np.ndarray, sr: int = 48000) -> None:
    """
    Best-effort real-time playback using sounddevice if available.
    Safe no-op if it's not installed.
    """
    try:
        import sounddevice as sd
        sd.play(audio.astype(np.float32), sr)
        sd.wait()
    except Exception as e:
        print(f"[playback skipped] {e}")
