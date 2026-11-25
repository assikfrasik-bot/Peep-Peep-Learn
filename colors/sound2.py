import json, numpy as np, scipy.signal as ss, soundfile as sf, wave, math

TL = json.load(open('/home/claude/colors/timeline.json'))
SR = 44100; DUR = TL['dur']; N = int(SR * DUR) + SR
rng = np.random.default_rng(9)
mus = np.zeros(N); sfx = np.zeros(N); vox = np.zeros(N)

def mtof(m): return 440 * 2 ** ((m - 69) / 12)
def tt(d): return np.arange(int(d * SR)) / SR
def add(buf, t0, sig, g=1.0):
    i = int(t0 * SR)
    if i >= N or i < 0: return
    j = min(N, i + len(sig)); buf[i:j] += sig[:j - i] * g
def att(t, a=0.004): return np.minimum(1, t / a)
def hp(x, fc): b, a = ss.butter(2, fc / (SR / 2), 'high'); return ss.lfilter(b, a, x)
def lp(x, fc): b, a = ss.butter(2, fc / (SR / 2), 'low'); return ss.lfilter(b, a, x)
def bp(x, lo, hi): b, a = ss.butter(2, [lo / (SR / 2), hi / (SR / 2)], 'band'); return ss.lfilter(b, a, x)

def bell(f, d=1.2):
    t = tt(d)
    return (np.sin(2*np.pi*f*t)*np.exp(-t/0.5) + 0.35*np.sin(2*np.pi*f*2.76*t)*np.exp(-t/0.12)
            + 0.12*np.sin(2*np.pi*f*5.4*t)*np.exp(-t/0.05)) * att(t, 0.002)
def pluck(f, d=0.6):
    t = tt(d); return sum((1/k)*np.sin(2*np.pi*f*k*t)*np.exp(-t*(4+k*3)) for k in range(1, 7)) * att(t, 0.003)
def bass(f, d=0.45):
    t = tt(d); return (np.sin(2*np.pi*f*t) + 0.3*np.sin(4*np.pi*f*t)) * np.exp(-t/0.28) * att(t, 0.006) * np.minimum(1, (d-t)/0.05)
def kick():
    t = tt(0.3); f = 45 + 110*np.exp(-t/0.04); return np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t/0.13)
def shaker():
    t = tt(0.08); return hp(rng.standard_normal(len(t)), 6000) * np.exp(-t/0.025)
def pad(notes, d):
    t = tt(d); s = sum(np.sin(2*np.pi*mtof(m)*t) + 0.5*np.sin(2*np.pi*mtof(m)*1.004*t) for m in notes)
    return s * np.minimum(1, t/0.4) * np.minimum(1, (d-t)/0.5) / len(notes)

# ---- intro: sad pad until title
T0 = TL['title']
add(mus, 0, pad([57, 60, 64], T0 + 0.3), 0.35)
for i, m in enumerate([76, 74, 72, 71]): add(mus, 0.4 + i * 0.35, bell(mtof(m)), 0.12)

# ---- main loop from title to bye
BPM = 116; BEAT = 60 / BPM; BAR = 4 * BEAT
PROG = [([60, 64, 67], 36), ([59, 62, 67], 43), ([57, 60, 64], 45), ([60, 65, 69], 41)]
MEL = [[72, None, 76, None, 79, None, 76, None], [74, None, 79, None, 83, None, 79, None],
       [72, None, 76, None, 81, None, 76, None], [77, None, 72, None, 74, None, None, None]]
endm = TL['outro']['bye'] + 1.6
b = 0
while T0 + b * BAR < endm:
    t0 = T0 + b * BAR; notes, bn = PROG[b % 4]
    for i in range(4):
        tb = t0 + i * BEAT
        if tb > endm: break
        add(mus, tb, bass(mtof(bn + (7 if i % 2 else 0))), 0.4)
        for m in notes: add(mus, tb + BEAT / 2, pluck(mtof(m)), 0.09)
        if i % 2 == 0: add(mus, tb, kick(), 0.4)
        add(mus, tb, shaker(), 0.05); add(mus, tb + BEAT / 2, shaker(), 0.08)
    for i, m in enumerate(MEL[b % 4]):
        if m and t0 + i * BEAT / 2 < endm: add(mus, t0 + i * BEAT / 2, bell(mtof(m)), 0.10)
    b += 1
for m in [60, 64, 67, 72, 76]: add(mus, TL['outro']['bye'] + 1.6, pluck(mtof(m), 1.2), 0.12)
it = tt(1.3); ir = lp(rng.standard_normal(len(it)), 5000) * np.exp(-it/0.3); ir /= np.sqrt(np.sum(ir**2))
mus = mus + 0.2 * ss.fftconvolve(mus, ir)[:N]

# ---- voice
for e in TL['events']:
    s, sr = sf.read(f"/home/claude/colors/vo/{e['name']}.wav")
    s = ss.resample_poly(s, 147, 80)
    add(vox, e['t'], s, 1.0)
env = lp(np.abs(vox), 6)
env = np.clip(env / (np.max(env) + 1e-9) * 3, 0, 1)
mus *= (1 - 0.55 * env)

# ---- sfx
def pop(f0=400, f1=1100, d=0.1):
    t = tt(d); f = f0 + (f1 - f0)*(t/d); return np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t/(d/3)) * att(t, 0.002)
def tick(f):
    t = tt(0.08); return (np.sin(2*np.pi*f*t)*0.7 + bp(rng.standard_normal(len(t)), 2000, 6000)*0.3) * np.exp(-t/0.018)
def splash():
    t = tt(0.45); return bp(rng.standard_normal(len(t)), 300, 3000) * np.exp(-t/0.12) * att(t, 0.005)
def whoosh_up(d=0.6):
    t = tt(d); n = rng.standard_normal(len(t)); s = np.zeros_like(n)
    seg = len(t) // 6
    for k in range(6): s[k*seg:(k+1)*seg] = bp(n[k*seg:(k+1)*seg], 400 + 400*k, 1200 + 900*k)
    return s * np.sin(np.pi * t / d) ** 2
def chirp():
    s = np.zeros(int(0.32*SR))
    for st in (0.0, 0.14):
        t = tt(0.1); f = 2300 + 1300*np.sin(np.pi*t/0.1)
        seg = np.sin(2*np.pi*np.cumsum(f)/SR) * np.sin(np.pi*t/0.1)**2
        i = int(st*SR); s[i:i+len(seg)] += seg
    return s

add(sfx, 0.3, pad([52, 55], 1.0), 0.15)
for r in TL['rounds']:
    i = r['i']
    add(sfx, r['appear'] + 0.02, pop(350, 900, 0.12), 0.45)
    for k in range(3): add(sfx, r['wait'] + 0.7 * k, tick(1300 if k % 2 == 0 else 1000), 0.45)
    for m in (84, 88, 91): add(sfx, r['reveal'], bell(mtof(m), 1.4), 0.2)
    add(sfx, r['reveal'], splash(), 0.35); add(sfx, r['reveal'], pop(200, 700, 0.12), 0.4)
    add(sfx, r['reveal'] + 0.12, chirp(), 0.2); add(sfx, r['reveal'] + 0.57, chirp(), 0.15)
    add(sfx, r['fly'], whoosh_up(0.6), 0.3)
    base = [72, 74, 76, 79, 81, 84][i]
    for j, m in enumerate((base, base + 4, base + 7, base + 12)): add(sfx, r['fly'] + 0.6 + j * 0.12, bell(mtof(m), 1.0), 0.13)
o = TL['outro']
for j, m in enumerate((72, 76, 79, 84, 88)): add(sfx, o['start'] + j * 0.08, bell(mtof(m), 1.2), 0.15)
add(sfx, o['start'], splash(), 0.3)
for i, t in enumerate(TL['recap']): add(sfx, t, bell(mtof([72, 74, 76, 79, 81, 84][i]), 0.9), 0.15)
add(sfx, o['bye'] + 0.1, chirp(), 0.25); add(sfx, o['bye'] + 0.8, chirp(), 0.2)

mix = mus * 0.55 + sfx * 0.75 + vox * 1.15
rt = np.arange(N) / SR
mix *= np.clip((DUR - rt) / 0.8, 0, 1)
mix = mix[:int(DUR * SR)]
mix = mix / np.max(np.abs(mix)) * 0.89
pcm = (mix * 32767).astype(np.int16)
with wave.open('/home/claude/colors/audio.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(np.stack([pcm, pcm], 1).tobytes())
print('ok', len(pcm) / SR)
