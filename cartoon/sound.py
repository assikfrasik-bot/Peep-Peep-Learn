import numpy as np, scipy.signal as ss, wave, math

SR = 44100; DUR = 26.0; N = int(SR * DUR)
rng = np.random.default_rng(3)
mus = np.zeros(N); sfx = np.zeros(N)

def mtof(m): return 440 * 2 ** ((m - 69) / 12)
def tt(d): return np.arange(int(d * SR)) / SR
def add(buf, t0, sig, g=1.0):
    i = int(t0 * SR)
    if i >= N: return
    j = min(N, i + len(sig)); buf[i:j] += sig[:j - i] * g
def att(t, a=0.004): return np.minimum(1, t / a)

def bell(f, d=1.3):
    t = tt(d)
    s = np.sin(2*np.pi*f*t)*np.exp(-t/0.5) + 0.35*np.sin(2*np.pi*f*2.76*t)*np.exp(-t/0.12) + 0.12*np.sin(2*np.pi*f*5.4*t)*np.exp(-t/0.05)
    return s * att(t, 0.002)
def pluck(f, d=0.7):
    t = tt(d); s = sum((1/k) * np.sin(2*np.pi*f*k*t) * np.exp(-t*(4 + k*3)) for k in range(1, 7))
    return s * att(t, 0.003)
def bass(f, d=0.5):
    t = tt(d); s = (np.sin(2*np.pi*f*t) + 0.3*np.sin(4*np.pi*f*t)) * np.exp(-t/0.3)
    return s * att(t, 0.006) * np.minimum(1, (d - t) / 0.05)
def kick():
    t = tt(0.3); f = 45 + 110*np.exp(-t/0.04); ph = 2*np.pi*np.cumsum(f)/SR
    return np.sin(ph) * np.exp(-t/0.13)
def hp(x, fc): b, a = ss.butter(2, fc/(SR/2), 'high'); return ss.lfilter(b, a, x)
def lp(x, fc): b, a = ss.butter(2, fc/(SR/2), 'low'); return ss.lfilter(b, a, x)
def bp(x, lo, hi): b, a = ss.butter(2, [lo/(SR/2), hi/(SR/2)], 'band'); return ss.lfilter(b, a, x)
def shaker():
    t = tt(0.08); return hp(rng.standard_normal(len(t)), 6000) * np.exp(-t/0.025)
def clap():
    t = tt(0.2); return bp(rng.standard_normal(len(t)), 900, 3000) * (np.exp(-t/0.05) + 0.5*np.exp(-np.maximum(0, t-0.012)/0.02)*(t > 0.012))
def pad(notes, d):
    t = tt(d); s = sum(np.sin(2*np.pi*mtof(m)*t) + 0.5*np.sin(2*np.pi*mtof(m)*1.003*t) for m in notes)
    return s * np.minimum(1, t/0.35) * np.minimum(1, (d - t)/0.4) / len(notes)

CH = {'C': ([60, 64, 67], 36), 'F': ([60, 65, 69], 41), 'G': ([59, 62, 67], 43),
      'Am': ([57, 60, 64], 45), 'Dm': ([57, 62, 65], 38)}
BARS = ['C', 'F', 'G', 'C', 'Am', 'F', 'G', 'Am', 'Dm', 'G', 'C', 'F', 'G']
MEL = [[72,None,None,None,76,None,None,None],[77,None,None,None,81,None,None,None],[79,None,83,None,86,None,None,None],
       [76,79,84,79,76,79,76,72],[76,81,84,81,76,None,72,None],[77,81,84,86,84,81,77,None],[79,83,86,83,79,None,74,None],
       [69,None,72,None,76,None,72,None],[74,None,77,None,81,None,77,None],[79,None,83,None,86,None,None,None],
       [84,None,79,84,88,None,84,None],[81,84,89,84,81,84,86,None],[86,83,79,83,84,None,None,None]]
BEAT = 0.5
for b, name in enumerate(BARS):
    t0 = b * 2.0; notes, bn = CH[name]
    sec = 0 if b < 3 else 1 if b < 7 else 2 if b < 10 else 3
    for i, m in enumerate(MEL[b]):
        if m: add(mus, t0 + i*0.25, bell(mtof(m)), 0.32 if sec != 2 else 0.24)
    if sec == 0:
        for i in range(4): add(mus, t0 + i*BEAT, pluck(mtof(notes[i % 3])), 0.22)
        add(mus, t0, bass(mtof(bn), 1.8), 0.35)
    elif sec == 2:
        add(mus, t0, pad(notes, 2.1), 0.22); add(mus, t0, bass(mtof(bn), 1.9), 0.3)
    else:
        last = (b == 12)
        for i in range(4):
            if last and i >= 2:
                chord, bb = CH['C']
            else:
                chord, bb = notes, bn
            add(mus, t0 + i*BEAT, bass(mtof(bb + (7 if i % 2 else 0)), 0.45), 0.45)
            for m in chord: add(mus, t0 + i*BEAT + 0.25, pluck(mtof(m)), 0.12)
            if sec == 1:
                if i % 2 == 0: add(mus, t0 + i*BEAT, kick(), 0.55)
            else:
                add(mus, t0 + i*BEAT, kick(), 0.5)
                if i % 2 == 1: add(mus, t0 + i*BEAT, clap(), 0.25)
            for k in range(2): add(mus, t0 + i*BEAT + k*0.25, shaker(), 0.12 if k else 0.07)
        if last:
            for m in [60, 64, 67, 72]: add(mus, 25.0, pluck(mtof(m), 1.0), 0.15)

# reverb
it = tt(1.4); ir = lp(rng.standard_normal(len(it)), 5000) * np.exp(-it/0.32); ir /= np.sqrt(np.sum(ir**2))
mus = mus + 0.22 * ss.fftconvolve(mus, ir)[:N]

# ---------- SFX ----------
def tick():
    t = tt(0.06); return (np.sin(2*np.pi*1100*t) * 0.7 + bp(rng.standard_normal(len(t)), 1500, 4000) * 0.4) * np.exp(-t/0.012)
def crack():
    t = tt(0.12); s = bp(rng.standard_normal(len(t)), 1500, 7000) * np.exp(-t/0.03)
    s[int(0.03*SR):] += bp(rng.standard_normal(len(t) - int(0.03*SR)), 2000, 8000) * np.exp(-t[:len(t)-int(0.03*SR)]/0.02)
    return s
def pop(f0=400, f1=1100, d=0.1):
    t = tt(d); f = f0 + (f1 - f0) * (t / d); ph = 2*np.pi*np.cumsum(f)/SR
    return np.sin(ph) * np.exp(-t/(d/3)) * att(t, 0.002)
def boing():
    t = tt(0.4); u = t / 0.4; f = 220 + 380*u + 45*np.sin(2*np.pi*22*t); ph = 2*np.pi*np.cumsum(f)/SR
    return (np.sin(ph) + 0.3*np.sin(2*ph)) * np.exp(-t/0.16) * att(t, 0.004)
def chirp():
    s = np.zeros(int(0.32*SR))
    for k, st in enumerate((0.0, 0.14)):
        t = tt(0.1); f = 2300 + 1300*np.sin(np.pi*t/0.1); ph = 2*np.pi*np.cumsum(f)/SR
        seg = np.sin(ph) * np.sin(np.pi*t/0.1)**2
        i = int(st*SR); s[i:i+len(seg)] += seg
    return s
def whoosh(d=0.6):
    t = tt(d); return bp(rng.standard_normal(len(t)), 500, 2500) * np.sin(np.pi*t/d)**2
def thunder():
    t = tt(1.6); return lp(rng.standard_normal(len(t)), 160) * np.exp(-t/0.5) * np.minimum(1, t/0.15) * 3

# wobble ticks at swing peaks
def burst(a, b, t): return math.sin(math.pi * min(1, max(0, (t - a)/(b - a))))
def wamp(t): return 0.10*burst(1.2, 1.8, t) + 0.14*burst(2.4, 3.0, t) + 0.2*burst(3.3, 4.4, t)
k = 0
while True:
    tp = (math.pi/2 + k*math.pi) / 18; k += 1
    if tp > 4.45: break
    if wamp(tp) > 0.05: add(sfx, tp, tick(), 0.35 + wamp(tp))
for tc in (3.7, 4.05, 4.3): add(sfx, tc, crack(), 0.5)
add(sfx, 4.5, pop(300, 900, 0.14), 0.7); add(sfx, 4.5, whoosh(0.5), 0.25)
add(sfx, 4.85, chirp(), 0.25); add(sfx, 6.3, chirp(), 0.25)
add(sfx, 6.0, whoosh(0.8), 0.15)
for k in range(6): add(sfx, 7.1 + k, boing(), 0.35)
add(sfx, 14.6, thunder(), 0.35)
# rain
rt = np.arange(N) / SR
def ramt(t):
    def sm(a, b, x): x = np.clip((x - a)/(b - a), 0, 1); return x*x*(3 - 2*x)
    return sm(14.8, 15.4, t) * (1 - sm(17.5, 18.3, t))
i0, i1 = int(14.6*SR), int(18.6*SR)
rn = bp(rng.standard_normal(i1 - i0), 1200, 9000) * 0.12
drops = np.zeros(i1 - i0)
for _ in range(220):
    p = rng.integers(0, i1 - i0 - 2000); dt = tt(0.03); drops[p:p+len(dt)] += np.sin(2*np.pi*rng.uniform(1500, 3500)*dt)*np.exp(-dt/0.006)*0.25
sfx[i0:i1] += (rn + drops) * ramt(rt[i0:i1])
add(sfx, 15.6, whoosh(0.8), 0.2); add(sfx, 18.6, whoosh(0.9), 0.15)
for i, m in enumerate([84, 88, 91, 96, 100, 103]): add(sfx, 19.8 + i*0.07, bell(mtof(m), 0.9), 0.18)
for i in range(8): add(sfx, 20.3 + 0.15*i, pop(500 + 60*i, 1300 + 80*i, 0.08), 0.35)
for tc in (21.0, 22.0, 23.0): add(sfx, tc + 0.05, chirp(), 0.18)
add(sfx, 24.3, chirp(), 0.25); add(sfx, 25.0, chirp(), 0.22)
for i, m in enumerate([96, 100, 103, 108]): add(sfx, 24.25 + i*0.06, bell(mtof(m), 0.8), 0.12)

mix = mus * 0.6 + sfx * 0.85
fade = np.clip((DUR - rt) / 0.7, 0, 1); mix *= fade
mix = mix / np.max(np.abs(mix)) * 0.89
pcm = (mix * 32767).astype(np.int16)
st = np.stack([pcm, pcm], 1)
with wave.open('/home/claude/cartoon/audio.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
print('ok', len(pcm)/SR)
