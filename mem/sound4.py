import json, numpy as np, scipy.signal as ss, soundfile as sf, wave

TL = json.load(open('/home/claude/mem/timeline.json'))
SR = 44100; DUR = TL['dur']; N = int(SR * DUR) + SR
rng = np.random.default_rng(13)
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
    t = tt(d); return (np.sin(2*np.pi*f*t)*np.exp(-t/0.5) + 0.35*np.sin(2*np.pi*f*2.76*t)*np.exp(-t/0.12) + 0.12*np.sin(2*np.pi*f*5.4*t)*np.exp(-t/0.05)) * att(t, 0.002)
def pluck(f, d=0.5):
    t = tt(d); return sum((1/k)*np.sin(2*np.pi*f*k*t)*np.exp(-t*(5+k*3)) for k in range(1, 7)) * att(t, 0.003)
def bass(f, d=0.4):
    t = tt(d); return (np.sin(2*np.pi*f*t) + 0.35*np.sin(4*np.pi*f*t)) * np.exp(-t/0.22) * att(t, 0.005) * np.minimum(1, (d-t)/0.04)
def kick():
    t = tt(0.3); f = 45 + 120*np.exp(-t/0.035); return np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t/0.12)
def snap():
    t = tt(0.15); return bp(rng.standard_normal(len(t)), 1200, 5000) * np.exp(-t/0.03)
def shaker():
    t = tt(0.07); return hp(rng.standard_normal(len(t)), 6500) * np.exp(-t/0.02)

# ---- quiz-show music loop
BPM = 124; BEAT = 60 / BPM; BAR = 4 * BEAT
PROG = [([60, 64, 67], 36), ([57, 60, 64], 45), ([62, 65, 69], 38), ([59, 62, 67], 43)]
MEL = [[79, None, 76, 79, 84, None, 79, None], [76, None, 72, 76, 81, None, 76, None],
       [77, None, 74, 77, 81, None, 77, 79], [79, 81, 83, None, 86, None, None, None]]
endm = TL['outro']['start']
b = 0
while b * BAR < endm:
    t0 = b * BAR; notes, bn = PROG[b % 4]
    for i in range(4):
        tb = t0 + i * BEAT
        add(mus, tb, bass(mtof(bn + (12 if i % 2 else 0))), 0.38)
        for m in notes: add(mus, tb + BEAT / 2, pluck(mtof(m)), 0.08)
        add(mus, tb, kick(), 0.38 if i % 2 == 0 else 0.0)
        if i % 2 == 1: add(mus, tb, snap(), 0.16)
        add(mus, tb + BEAT / 2, shaker(), 0.07)
    for i, m in enumerate(MEL[b % 4]):
        if m: add(mus, t0 + i * BEAT / 2, bell(mtof(m)), 0.08)
    b += 1
# outro fanfare + happy loop
o = TL['outro']
for j, m in enumerate([72, 76, 79, 84]): add(mus, o['start'] + 0.4 + j * 0.13, bell(mtof(m), 1.5), 0.2)
for j in range(int((DUR - o['start']) / BEAT)):
    tb = o['start'] + 0.9 + j * BEAT
    notes, bn = [([60, 64, 67], 36), ([65, 69, 72], 41), ([67, 71, 74], 43), ([60, 64, 67], 36)][(j // 4) % 4]
    add(mus, tb, bass(mtof(bn)), 0.35); add(mus, tb, kick(), 0.3 if j % 2 == 0 else 0)
    for m in notes: add(mus, tb + BEAT / 2, pluck(mtof(m)), 0.08)
it = tt(1.2); ir = lp(rng.standard_normal(len(it)), 5000) * np.exp(-it/0.28); ir /= np.sqrt(np.sum(ir**2))
mus = mus + 0.18 * ss.fftconvolve(mus, ir)[:N]

# ---- voice
for e in TL['events']:
    s, sr = sf.read(f"/home/claude/mem/vo/{e['name']}.wav"); add(vox, e['t'], ss.resample_poly(s, 147, 80))
env = lp(np.abs(vox), 6); env = np.clip(env / (np.max(env) + 1e-9) * 3, 0, 1)
duck = 1 - 0.6 * env
# lower music during timers
for r in TL['rounds']:
    i0, i1 = int(r['timer'] * SR), int(r['reveal'] * SR)
    duck[i0:i1] *= 0.55
mus *= duck

# ---- sfx
def flick():
    t = tt(0.09); return bp(rng.standard_normal(len(t)), 1500, 6000) * np.exp(-t/0.02) * att(t, 0.003)
def tick(f):
    t = tt(0.08); return (np.sin(2*np.pi*f*t)*0.7 + bp(rng.standard_normal(len(t)), 2000, 6000)*0.3) * np.exp(-t/0.018)
def pop(f0, f1, d=0.1):
    t = tt(d); f = f0 + (f1 - f0)*(t/d); return np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t/(d/3)) * att(t, 0.002)
def whoosh(d=0.4):
    t = tt(d); return bp(rng.standard_normal(len(t)), 600, 3500) * np.sin(np.pi*t/d)**2
def squeak():
    t = tt(0.35); f = 900 + 700*(t/0.35) + 60*np.sin(2*np.pi*30*t); return np.sin(2*np.pi*np.cumsum(f)/SR) * np.sin(np.pi*t/0.35) * 0.6
def drumroll(d):
    out = np.zeros(int(d*SR)); t = 0.0
    while t < d:
        s = bp(rng.standard_normal(int(0.05*SR)), 150, 2500) * np.exp(-tt(0.05)/0.015)
        i = int(t*SR); out[i:i+len(s)] += s[:len(out)-i] * (0.4 + 0.6 * t / d)
        t += 0.045
    return out
def chirp():
    s = np.zeros(int(0.32*SR))
    for st in (0.0, 0.14):
        t = tt(0.1); f = 2300 + 1300*np.sin(np.pi*t/0.1); seg = np.sin(2*np.pi*np.cumsum(f)/SR) * np.sin(np.pi*t/0.1)**2
        i = int(st*SR); s[i:i+len(seg)] += seg
    return s

for k in range(4): add(sfx, 0.15 + 0.06 * k, pop(300, 700, 0.1), 0.25)
for r in TL['rounds']:
    n = len(r['items'])
    for j in range(n): add(sfx, r['start'] + 0.3 + 0.05 * j, flick(), 0.25)
    for j in range(n): add(sfx, r['mem1'] + 0.04 * j, flick(), 0.25)
    for j in range(n):
        if j != r['target']: add(sfx, r['all_up'] + 0.05 * j, flick(), 0.18)
    add(sfx, r['start'], whoosh(0.4), 0.2); add(sfx, r['start'] + 0.2, pop(400, 1000, 0.12), 0.3)
    for k in range(int(r['mem1'] - r['mem0'])): add(sfx, r['mem0'] + k, tick(900), 0.2)
    if r['i'] == 3:
        add(sfx, r['timer'], drumroll(4.0), 0.3)
    for k in range(4):
        add(sfx, r['timer'] + k, tick(1300), 0.4); add(sfx, r['timer'] + k + 0.5, tick(1000), 0.3)
    for k in range(4): add(sfx, r['reveal'] - 0.75 + k * 0.25 - 0.25 * (k > 2), tick(1600), 0.0)
    add(sfx, r['reveal'], flick(), 0.35)
    add(sfx, r['reveal'] + 0.2, bell(mtof(88), 1.2), 0.25); add(sfx, r['reveal'] + 0.12, bell(mtof(93), 1.2), 0.25)
    add(sfx, r['reveal'], pop(250, 800, 0.12), 0.4)
    add(sfx, r['reveal'] + 0.05, squeak(), 0.18)
    for j, m in enumerate((72, 76, 79)): add(sfx, r['reveal'] + 0.3 + j * 0.08, bell(mtof(m), 0.8), 0.12)
    add(sfx, r['reveal'] + 0.15, chirp(), 0.18)
add(sfx, o['start'], whoosh(0.6), 0.3)
add(sfx, o['start'] + 0.4, pop(300, 1000, 0.14), 0.4)
add(sfx, o['bye'] + 0.1, chirp(), 0.2); add(sfx, o['bye'] + 0.9, chirp(), 0.18)

mix = mus * 0.55 + sfx * 0.75 + vox * 1.15
rt = np.arange(N) / SR
mix *= np.clip((DUR - rt) / 0.8, 0, 1); mix = mix[:int(DUR * SR)]
mix = mix / np.max(np.abs(mix)) * 0.89
pcm = (mix * 32767).astype(np.int16)
with wave.open('/home/claude/mem/audio.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(np.stack([pcm, pcm], 1).tobytes())
print('ok', len(pcm) / SR)
