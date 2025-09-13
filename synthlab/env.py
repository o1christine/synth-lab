# synthlab/env.py
from __future__ import annotations
import numpy as np
from dataclasses import dataclass

@dataclass
class ADSR:
    attack: float   # seconds
    decay: float    # seconds
    sustain: float  # 0..1
    release: float  # seconds

    def apply(self, x: np.ndarray, sr: int) -> np.ndarray:
        n = x.size
        a = int(self.attack  * sr)
        d = int(self.decay   * sr)
        r = int(self.release * sr)
        # sustain portion is "whatever remains" of the note
        s = max(0, n - (a + d + r))

        env = np.zeros(n, dtype=x.dtype)
        idx = 0
        # attack
        if a > 0:
            env[idx:idx+a] = np.linspace(0.0, 1.0, a, endpoint=False)
            idx += a
        # decay
        if d > 0:
            env[idx:idx+d] = np.linspace(1.0, self.sustain, d, endpoint=False)
            idx += d
        # sustain
        if s > 0:
            env[idx:idx+s] = self.sustain
            idx += s
        # release
        if r > 0:
            start = env[idx-1] if idx > 0 else 0.0
            env[idx:idx+r] = np.linspace(start, 0.0, r, endpoint=False)
            idx += r
        # if we undershot/overshot, slice
        return x[:idx] * env[:idx]
