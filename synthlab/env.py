# synthlab/env.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple
from .backend import xp  # numpy or mlx.core

@dataclass
class ADSR:
    attack:  float  # seconds
    decay:   float  # seconds
    sustain: float  # 0..1
    release: float  # seconds

    def _segment_lengths(self, n_total: int, sr: int) -> Tuple[int,int,int,int]:
        a = int(round(self.attack  * sr))
        d = int(round(self.decay   * sr))
        r = int(round(self.release * sr))
        s = max(0, n_total - (a + d + r))
        # If the note is very short, we clamp in order: sustain -> decay -> attack.
        if s == 0 and a + d + r > n_total:
            # shrink in reverse priority (release is non-negotiable to end gracefully)
            over = (a + d + r) - n_total
            # steal from decay first
            steal = min(d, over); d -= steal; over -= steal
            # then attack
            steal = min(a, over); a -= steal; over -= steal
            # if still over, reduce release minimally (last resort)
            if over > 0:
                r = max(0, r - over)
        s = max(0, n_total - (a + d + r))
        return a, d, s, r

    def render(self, n_total: int, sr: int) -> "xp.ndarray":
        """Vectorized envelope of length n_total."""
        a, d, s, r = self._segment_lengths(n_total, sr)
        env = xp.zeros(n_total, dtype=xp.float32)
        idx = 0

        # Attack: 0 -> 1
        if a > 0:
            env[idx:idx+a] = xp.linspace(0.0, 1.0, a, endpoint=False)
            idx += a

        # Decay: 1 -> sustain
        if d > 0:
            env[idx:idx+d] = xp.linspace(1.0, self.sustain, d, endpoint=False)
            idx += d

        # Sustain: sustain -> sustain
        if s > 0:
            env[idx:idx+s] = self.sustain
            idx += s

        # Release: current -> 0
        if r > 0:
            start = float(env[idx-1]) if idx > 0 else 0.0
            env[idx:idx+r] = xp.linspace(start, 0.0, r, endpoint=False)
            idx += r

        # Guard: if we undershot due to rounding, pad last sample; if overshot, slice
        if idx < n_total:
            env[idx:] = 0.0
        elif idx > n_total:
            env = env[:n_total]
        return env

    def apply(self, x: "xp.ndarray", sr: int) -> "xp.ndarray":
        env = self.render(x.shape[0], sr)
        return x * env
