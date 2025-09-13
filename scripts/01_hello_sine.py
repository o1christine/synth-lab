# scripts/01_hello_sine.py
import numpy as np
from synthlab.io import write_wav, try_play

SR   = 48000
DUR  = 1.0
FREQ = 440.0

t = np.arange(int(SR * DUR), dtype=np.float64) / SR
x = np.sin(2*np.pi*FREQ*t)

# 5 ms fade-in/out to remove clicks
def fade(x: np.ndarray, ms: float = 5.0, sr: int = SR) -> np.ndarray:
    n = int(sr * ms / 1000.0)
    if n <= 0 or n*2 >= x.size:
        return x
    env = np.ones_like(x)
    ramp = np.linspace(0.0, 1.0, n)
    env[:n] *= ramp
    env[-n:] *= ramp[::-1]
    return x * env

y = fade(x, 5.0, SR) * 0.2  # keep headroom
write_wav("out/01_hello_sine.wav", y, SR)
try_play(y, SR)
print("Wrote out/01_hello_sine.wav")
