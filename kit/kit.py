"""Shared toolkit for Chickpea episodes: TTS, timeline, audio synth, mixing, rendering."""
import sys, os, json, math, subprocess
sys.path.insert(0, '/home/claude/cartoon'); sys.path.insert(0, '/home/claude/colors')
sys.path.insert(0, '/home/claude/odd'); sys.path.insert(0, '/home/claude/mem')
import numpy as np, scipy.signal as ss, soundfile as sf, wave

SR = 44100
_K = None
def kokoro():
    global _K
    if _K is None:
        from kokoro_onnx import Kokoro
        _K = Kokoro("/home/claude/tts/kokoro.onnx", "/home/claude/tts/voices.bin")
    return _K

class Script:
    def __init__(self, folder):
        self.folder = folder; self.vo = os.path.join(folder, 'vo'); os.makedirs(self.vo, exist_ok=True)
        self.events = []; self.marks = {}
    def say(self, t, name, text, speed=0.92, chick=False, voice="af_heart"):
        s, sr = kokoro().create(text, voice=voice, speed=speed, lang="en-us")
        s = np.asarray(s, dtype=np.float32); idx = np.where(np.abs(s) > 0.01)[0]
        s = s[max(0, idx[0] - 600): idx[-1] + 2400]
        if chick: s = ss.resample_poly(s, 10, 13).astype(np.float32)
        sf.write(os.path.join(self.vo, name + '.wav'), s, sr)
        d = len(s) / sr
        self.events.append(dict(t=round(t, 3), name=name, dur=round(d, 3), chick=chick))
        return t + d
    def mark(self, k, t): self.marks[k] = round(t, 3)
    def save(self, dur, **extra):
        d = dict(events=self.events, marks=self.marks, dur=round(dur, 2)); d.update(extra)
        json.dump(d, open(os.path.join(self.folder, 'timeline.json'), 'w'), indent=1); return d

# ---------------- audio ----------------
rng = np.random.default_rng(7)
def mtof(m): return 440 * 2 ** ((m - 69) / 12)
def tt(d): return np.arange(int(d * SR)) / SR
def att(t, a=0.004): return np.minimum(1, t / a)
def hp(x, fc): b, a = ss.butter(2, fc / (SR / 2), 'high'); return ss.lfilter(b, a, x)
def lp(x, fc): b, a = ss.butter(2, fc / (SR / 2), 'low'); return ss.lfilter(b, a, x)
def bp(x, lo, hi): b, a = ss.butter(2, [lo / (SR / 2), hi / (SR / 2)], 'band'); return ss.lfilter(b, a, x)
def bell(f, d=1.2):
    t = tt(d); return (np.sin(2*np.pi*f*t)*np.exp(-t/0.5) + 0.35*np.sin(2*np.pi*f*2.76*t)*np.exp(-t/0.12) + 0.12*np.sin(2*np.pi*f*5.4*t)*np.exp(-t/0.05)) * att(t, 0.002)
def pluck(f, d=0.5):
    t = tt(d); return sum((1/k)*np.sin(2*np.pi*f*k*t)*np.exp(-t*(5+k*3)) for k in range(1, 7)) * att(t, 0.003)
def marimba(f, d=0.6):
    t = tt(d); return (np.sin(2*np.pi*f*t) + 0.25*np.sin(2*np.pi*4*f*t)*np.exp(-t/0.03)) * np.exp(-t/0.18) * att(t, 0.002)
def bass(f, d=0.4):
    t = tt(d); return (np.sin(2*np.pi*f*t) + 0.35*np.sin(4*np.pi*f*t)) * np.exp(-t/0.22) * att(t, 0.005) * np.minimum(1, (d-t)/0.04)
def kick():
    t = tt(0.3); f = 45 + 120*np.exp(-t/0.035); return np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t/0.12)
def snap():
    t = tt(0.15); return bp(rng.standard_normal(len(t)), 1200, 5000) * np.exp(-t/0.03)
def shaker():
    t = tt(0.07); return hp(rng.standard_normal(len(t)), 6500) * np.exp(-t/0.02)
def pad(notes, d):
    t = tt(d); s = sum(np.sin(2*np.pi*mtof(m)*t) + 0.5*np.sin(2*np.pi*mtof(m)*1.004*t) for m in notes)
    return s * np.minimum(1, t/0.4) * np.minimum(1, np.maximum(0, d-t)/0.5) / len(notes)
def flick():
    t = tt(0.09); return bp(rng.standard_normal(len(t)), 1500, 6000) * np.exp(-t/0.02) * att(t, 0.003)
def tick(f=1200):
    t = tt(0.08); return (np.sin(2*np.pi*f*t)*0.7 + bp(rng.standard_normal(len(t)), 2000, 6000)*0.3) * np.exp(-t/0.018)
def pop(f0=300, f1=900, d=0.12):
    t = tt(d); f = f0 + (f1 - f0)*(t/d); return np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t/(d/3)) * att(t, 0.002)
def whoosh(d=0.4):
    t = tt(d); return bp(rng.standard_normal(len(t)), 600, 3500) * np.sin(np.pi*t/d)**2
def boing():
    t = tt(0.4); f = 220 + 380*(t/0.4) + 45*np.sin(2*np.pi*22*t); ph = 2*np.pi*np.cumsum(f)/SR
    return (np.sin(ph) + 0.3*np.sin(2*ph)) * np.exp(-t/0.16) * att(t, 0.004)
def slide_whistle(f0, f1, d=0.5):
    t = tt(d); f = f0 * (f1/f0) ** (t/d); return np.sin(2*np.pi*np.cumsum(f)/SR) * np.sin(np.pi*t/d) ** 0.5
def chirp():
    s = np.zeros(int(0.32*SR))
    for st in (0.0, 0.14):
        t = tt(0.1); f = 2300 + 1300*np.sin(np.pi*t/0.1); seg = np.sin(2*np.pi*np.cumsum(f)/SR) * np.sin(np.pi*t/0.1)**2
        i = int(st*SR); s[i:i+len(seg)] += seg
    return s
def ding():
    return bell(mtof(88), 1.2) + bell(mtof(93), 1.2) * 0.8
def tada(base=72):
    out = np.zeros(int(1.6*SR))
    for j, m in enumerate((base, base+4, base+7, base+12)):
        s = bell(mtof(m), 1.3); i = int(j*0.09*SR); out[i:i+len(s)] += s
    return out
def drumroll(d):
    out = np.zeros(int(d*SR)); t = 0.0
    while t < d - 0.05:
        s = bp(rng.standard_normal(int(0.05*SR)), 150, 2500) * np.exp(-tt(0.05)/0.015)
        i = int(t*SR); out[i:i+len(s)] += s[:len(out)-i] * (0.4 + 0.6 * t / d); t += 0.045
    return out
def rumble(d=1.2):
    t = tt(d); return lp(rng.standard_normal(len(t)), 160) * np.exp(-t/0.5) * np.minimum(1, t/0.15) * 3
def jingle():
    """2-second Chickpea & Friends sting"""
    out = np.zeros(int(2.2*SR))
    for j, m in enumerate((72, 76, 79, 84, 88)):
        s = bell(mtof(m), 1.2); i = int(j*0.11*SR); out[i:i+len(s)] += s * 0.8
    c = chirp(); i = int(0.6*SR); out[i:i+len(c)] += c * 0.5
    return out

class Mix:
    def __init__(self, dur):
        self.dur = dur; self.N = int(SR * dur) + SR
        self.mus = np.zeros(self.N); self.sfx = np.zeros(self.N); self.vox = np.zeros(self.N)
    def add(self, buf, t0, sig, g=1.0):
        b = getattr(self, buf); i = int(t0 * SR)
        if i >= self.N or i < 0: return
        j = min(self.N, i + len(sig)); b[i:j] += sig[:j - i] * g
    def music_loop(self, t0, t1, bpm, prog, mel=None, style='bouncy', gain=1.0):
        BEAT = 60 / bpm; BAR = 4 * BEAT; b = 0
        while t0 + b * BAR < t1:
            tb0 = t0 + b * BAR; notes, bn = prog[b % len(prog)]
            for i in range(4):
                tb = tb0 + i * BEAT
                if tb >= t1: break
                if style == 'bouncy':
                    self.add('mus', tb, bass(mtof(bn + (12 if i % 2 else 0))), 0.38 * gain)
                    for m in notes: self.add('mus', tb + BEAT / 2, pluck(mtof(m)), 0.08 * gain)
                    if i % 2 == 0: self.add('mus', tb, kick(), 0.36 * gain)
                    else: self.add('mus', tb, snap(), 0.14 * gain)
                    self.add('mus', tb + BEAT / 2, shaker(), 0.06 * gain)
                elif style == 'soft':
                    if i == 0: self.add('mus', tb, pad(notes, BAR + 0.3), 0.22 * gain); self.add('mus', tb, bass(mtof(bn), BAR * 0.9), 0.25 * gain)
                    self.add('mus', tb, marimba(mtof(notes[i % 3] + 12)), 0.10 * gain)
                elif style == 'march':
                    self.add('mus', tb, bass(mtof(bn + (7 if i % 2 else 0))), 0.36 * gain)
                    self.add('mus', tb, kick(), 0.3 * gain)
                    for m in notes: self.add('mus', tb, marimba(mtof(m + 12)), 0.05 * gain)
                    self.add('mus', tb + BEAT / 2, shaker(), 0.05 * gain)
            if mel:
                for i, m in enumerate(mel[b % len(mel)]):
                    if m and tb0 + i * BEAT / 2 < t1: self.add('mus', tb0 + i * BEAT / 2, bell(mtof(m)), 0.08 * gain)
            b += 1
    def voices(self, folder, events):
        for e in events:
            s, sr = sf.read(os.path.join(folder, 'vo', e['name'] + '.wav'))
            self.add('vox', e['t'], ss.resample_poly(s, 147, 80))
    def write(self, path, quiet=()):
        it = tt(1.2); ir = lp(rng.standard_normal(len(it)), 5000) * np.exp(-it/0.28); ir /= np.sqrt(np.sum(ir**2))
        mus = self.mus + 0.18 * ss.fftconvolve(self.mus, ir)[:self.N]
        env = lp(np.abs(self.vox), 6); env = np.clip(env / (np.max(env) + 1e-9) * 3, 0, 1)
        duck = 1 - 0.6 * env
        for a, b in quiet: duck[int(a * SR):int(b * SR)] *= 0.55
        mix = mus * duck * 0.55 + self.sfx * 0.75 + self.vox * 1.15
        rt = np.arange(self.N) / SR
        mix *= np.clip((self.dur - rt) / 0.6, 0, 1); mix = mix[:int(self.dur * SR)]
        mix = mix / np.max(np.abs(mix)) * 0.89
        pcm = (mix * 32767).astype(np.int16)
        with wave.open(path, 'wb') as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(np.stack([pcm, pcm], 1).tobytes())

# ---------------- render ----------------
RUNNER = '/home/claude/kit/runner.py'
def render(folder, module, dur, out_name, fps=30, parts=4):
    nf = math.ceil(dur * fps); q = nf // parts
    ranges = [(k * q, nf if k == parts - 1 else (k + 1) * q) for k in range(parts)]
    def start(k):
        a, b = ranges[k]
        cmd = (f"python3 {RUNNER} {folder} {module} {a} {b} | ffmpeg -y -loglevel error -f rawvideo -pix_fmt bgra "
               f"-s 1080x1920 -r {fps} -i - -c:v libx264 -crf 18 -preset veryfast -pix_fmt yuv420p -r {fps} {folder}/tmp_p{k}.mp4 "
               f"&& mv {folder}/tmp_p{k}.mp4 {folder}/p{k}.mp4")
        return subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
    for g in range(0, parts, 2):
        ps = [start(k) for k in range(g, min(parts, g + 2))]
        for p in ps:
            _, err = p.communicate()
            if p.returncode != 0: raise RuntimeError(err.decode()[-2000:])
    with open(f'{folder}/list.txt', 'w') as f:
        for k in range(parts): f.write(f"file 'p{k}.mp4'\n")
    subprocess.run(f"ffmpeg -y -loglevel error -f concat -safe 0 -i {folder}/list.txt -c copy {folder}/v.mp4", shell=True, check=True)
    subprocess.run(f"ffmpeg -y -loglevel error -i {folder}/v.mp4 -i {folder}/audio.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k "
                   f"-shortest -movflags +faststart {folder}/tmp_final.mp4 && mv {folder}/tmp_final.mp4 {folder}/{out_name}", shell=True, check=True)

def sheet(folder, module, times, out='sheet.png', w=270):
    sys.path.insert(0, folder)
    import importlib, cairo
    from PIL import Image
    m = importlib.import_module(module)
    ims = []
    for t in times:
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080, 1920); cr = cairo.Context(s); m.frame(cr, t); s.flush()
        im = Image.frombuffer('RGBA', (1080, 1920), bytes(s.get_data()), 'raw', 'BGRA', 0, 1).convert('RGB').resize((w, int(w * 1920 / 1080)))
        ims.append(im)
    cols = min(len(ims), 6); rows = (len(ims) + cols - 1) // cols; h = ims[0].height
    c = Image.new('RGB', (w * cols, h * rows))
    for i, im in enumerate(ims): c.paste(im, ((i % cols) * w, (i // cols) * h))
    c.save(os.path.join(folder, out))
