# Synth Lab — Procedural Audio in Python (UV‑powered)

A tiny, builder‑friendly lab for learning audio synthesis from scratch. You’ll generate real sounds (WAVs) in seconds, understand the DSP under the hood, and grow the system step‑by‑step—oscillators → envelopes → filters → modulation → space.

---

## Why this exists

* **Fast feedback loops.** Every lesson is a runnable script that writes a short WAV to `out/` and (optionally) plays it.
* **Incremental artifacts.** You’ll keep a gallery of tiny sounds as you learn.
* **Simple, composable DSP.** Oscillator → Envelope → Effects → Mix → Output.
* **Reproducible tooling.** Uses [`uv`](https://docs.astral.sh/uv) for project init, dependency management, and execution.

> ⚠️ Listen at safe levels. Some experiments (clipping, aliasing) can get harsh. Start with low volume.

---

## Quickstart

### 1) Create or enter the project

```bash
# if starting fresh
uv init synth-lab
cd synth-lab
```

### 2) Add dependencies

```bash
uv add numpy sounddevice      # sounddevice is optional; it enables live playback
# optional GPU/ML backend on Apple Silicon (macOS 13.5+)
uv add mlx
```

### 3) Project layout

```
synth-lab/
  pyproject.toml
  out/                      # rendered WAVs land here
  scripts/                  # runnable lessons (L1, L2, ...)
    01_hello_sine.py
    02_adsr_bleep.py
    03_waveforms.py
    04_sequencer.py
    05_noise_and_hits.py
    06_filters.py
    07_modulation.py
    08_delay_reverb.py
    __init__.py
  synthlab/                 # reusable DSP + IO
    __init__.py
    backend.py              # NumPy (default) or MLX (optional)
    io.py                   # write_wav(), try_play()
    env.py                  # ADSR envelope
    osc.py                  # oscillators (added in later lessons)
    dsp.py                  # filters + helpers (later)
    music.py                # note→freq, tiny sequencer (later)
```

> If you see `ModuleNotFoundError: synthlab`, run lessons **as modules** (below) or set `PYTHONPATH=.`.

### 4) Run lesson 1

```bash
# recommended (ensures project root is on sys.path)
uv run -m scripts.01_hello_sine

# or (direct execution; add project root to import path)
PYTHONPATH=. uv run scripts/01_hello_sine.py        # macOS/Linux
$env:PYTHONPATH='.'; uv run scripts/01_hello_sine.py  # Windo
```

