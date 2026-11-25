import json, os, numpy as np, soundfile as sf, scipy.signal as ss
from kokoro_onnx import Kokoro
k = Kokoro("/home/claude/tts/kokoro.onnx", "/home/claude/tts/voices.bin")
D = "/home/claude/mem/vo/"; os.makedirs(D, exist_ok=True)
ev = []
def say(name, text, speed=0.95, chick=False):
    s, sr = k.create(text, voice="af_heart", speed=speed, lang="en-us")
    s = np.asarray(s, dtype=np.float32); idx = np.where(np.abs(s) > 0.01)[0]; s = s[max(0, idx[0] - 600): idx[-1] + 2400]
    if chick: s = ss.resample_poly(s, 10, 13).astype(np.float32)
    sf.write(D + name + ".wav", s, sr); return len(s) / sr
def vo(t, name, text, speed=0.95, chick=False):
    d = say(name, text, speed, chick); ev.append(dict(t=round(t, 3), name=name, dur=round(d, 3))); return t + d

ROUNDS = [
    dict(grid=(2, 2), items=['apple', 'fish', 'star', 'frog'], kind='where', target=1, mem=3.5,
         pre="Remember the pictures!", q="Where's the fish?", a="Top right! Here's the fish!", label="Top right!"),
    dict(grid=(3, 2), items=['banana', 'heart', 'whale', 'crab', 'grapes', 'butterfly'], kind='where', target=4, mem=4.5,
         pre="Level two! Six cards!", q="Where are the grapes?", a="Bottom middle! There they are!", label="Bottom middle!"),
    dict(grid=(3, 2), items=['frog', 'star', 'fish', 'carrot', 'heart', 'apple'], kind='under', target=3, mem=4.5,
         pre="Level three! Something new!", q="What's under this card?", a="The carrot! Did you remember?", label="The carrot!"),
    dict(grid=(3, 3), items=['star', 'whale', 'apple', 'crab', 'heart', 'banana', 'butterfly', 'frog', 'grapes'], kind='where', target=6, mem=6.0,
         pre="Expert level! Nine cards!", q="Where's the butterfly?", a="Bottom left! You're a memory master!", label="Bottom left!"),
]
TIMER = 4.0
t = 0.4
t = vo(t, "hook", "Memory challenge! Can you remember them all?") + 0.15
out = []
for i, r in enumerate(ROUNDS):
    rd = dict(r); rd['i'] = i
    rd['start'] = round(t, 3)
    tv = vo(t + 0.15, f"pre{i}", r['pre'])
    rd['mem0'] = round(t + 0.65, 3)
    rd['mem1'] = round(max(rd['mem0'] + r['mem'], tv + 0.3), 3)
    tq = vo(rd['mem1'] + 0.5, f"q{i}", r['q'])
    rd['timer'] = round(tq + 0.15, 3); rd['reveal'] = round(rd['timer'] + TIMER, 3)
    ta = vo(rd['reveal'] + 0.1, f"a{i}", r['a'])
    rd['all_up'] = round(rd['reveal'] + 1.1, 3)
    rd['end'] = round(max(ta + 0.4, rd['reveal'] + 2.6), 3)
    out.append(rd); t = rd['end']
outro = dict(start=round(t, 3))
t = vo(t + 0.5, "wow", "Amazing! Your memory is super strong!") + 0.2
outro['bye'] = round(t, 3)
t = vo(t, "bye", "Bye-bye! See you next time!", 1.0, True) + 1.1
TL = dict(rounds=out, outro=outro, events=ev, dur=round(t, 2), timer=TIMER)
json.dump(TL, open("/home/claude/mem/timeline.json", "w"), indent=1)
print("dur", TL['dur'])
for r in out: print(r['i'], r['start'], r['mem0'], r['mem1'], r['timer'], r['reveal'], r['end'])
