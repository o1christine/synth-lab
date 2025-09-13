# scripts/02_adsr_bleep.py
import numpy as np
from synthlab.io import write_wav, try_play
from synthlab.env import ADSR

SR = 48000
DUR = 0.6
F  = 660.0  # a brighter pitch so the envelope shape is obvious

t = np.arange(int(SR*DUR)) / SR
osc = np.sin(2*np.pi*F*t)

adsr = ADSR(attack=0.005, decay=0.090, sustain=0.25, release=0.200)
y = adsr.apply(osc, SR) * 0.4

write_wav("out/02_adsr_bleep.wav", y, SR)
try_play(y, SR)
print("Wrote out/02_adsr_bleep.wav")
