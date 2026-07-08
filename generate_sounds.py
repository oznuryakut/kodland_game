"""Generates all placeholder sound effects and background music.

Everything is synthesised from scratch with plain sine/square waves so
the project has no dependency on external audio files.
Run once with: python3 generate_sounds.py
"""
import numpy as np
import wave
import os

SOUND_DIR = "sounds"
MUSIC_DIR = "music"
os.makedirs(SOUND_DIR, exist_ok=True)
os.makedirs(MUSIC_DIR, exist_ok=True)

RATE = 22050


def to_wav(samples, path):
    samples = np.clip(samples, -1, 1)
    data = (samples * 32767).astype(np.int16)
    with wave.open(path, "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(RATE)
        f.writeframes(data.tobytes())


def tone(freq, duration, wave_type="sine", fade=True):
    t = np.linspace(0, duration, int(RATE * duration), endpoint=False)
    if wave_type == "sine":
        s = np.sin(2 * np.pi * freq * t)
    elif wave_type == "square":
        s = np.sign(np.sin(2 * np.pi * freq * t))
    else:
        s = np.sin(2 * np.pi * freq * t)
    if fade:
        fade_len = max(1, int(RATE * 0.01))
        env = np.ones_like(s)
        env[:fade_len] = np.linspace(0, 1, fade_len)
        env[-fade_len:] = np.linspace(1, 0, fade_len)
        s *= env
    return s


def make_jump():
    t = np.linspace(0, 0.18, int(RATE * 0.18), endpoint=False)
    freq = np.linspace(300, 700, t.size)
    s = np.sin(2 * np.pi * freq * t / RATE * RATE) * 0.5
    s *= np.linspace(1, 0.2, t.size)
    to_wav(s, os.path.join(SOUND_DIR, "jump.wav"))


def make_coin():
    a = tone(880, 0.08, "square") * 0.4
    b = tone(1318, 0.12, "square") * 0.4
    s = np.concatenate([a, b])
    to_wav(s, os.path.join(SOUND_DIR, "coin.wav"))


def make_hit():
    t = np.linspace(0, 0.25, int(RATE * 0.25), endpoint=False)
    noise = (np.random.rand(t.size) * 2 - 1)
    freq = np.linspace(220, 80, t.size)
    tone_part = np.sin(2 * np.pi * freq * t)
    s = (noise * 0.5 + tone_part * 0.5) * np.linspace(1, 0, t.size) * 0.6
    to_wav(s, os.path.join(SOUND_DIR, "hit.wav"))


def make_click():
    s = tone(500, 0.05, "square") * 0.3
    to_wav(s, os.path.join(SOUND_DIR, "click.wav"))


def make_win():
    notes = [523, 659, 784, 1046]
    s = np.concatenate([tone(f, 0.15, "square") * 0.4 for f in notes])
    to_wav(s, os.path.join(SOUND_DIR, "win.wav"))


def make_music():
    # Simple looping four-note melody used as background music.
    melody = [392, 440, 494, 440, 392, 349, 392, 440]
    parts = [tone(f, 0.3, "sine") * 0.25 for f in melody]
    s = np.concatenate(parts)
    to_wav(s, os.path.join(MUSIC_DIR, "theme.wav"))


make_jump()
make_coin()
make_hit()
make_click()
make_win()
make_music()
print("Sounds generated.")
