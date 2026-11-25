import json, os, numpy as np, soundfile as sf, scipy.signal as ss
from kokoro_onnx import Kokoro
k = Kokoro("/home/claude/tts/kokoro.onnx", "/home/claude/tts/voices.bin")
D = "/home/claude/odd/vo/"; os.makedirs(D, exist_ok=True)
ev = []

def say(name, text, speed=0.95, chick=False):
    s, sr = k.create(text, voice="af_heart", speed=speed, lang="en-us")
    s = np.asarray(s, dtype=np.float32)
    idx = np.where(np.abs(s) > 0.01)[0]; s = s[max(0, idx[0] - 600): idx[-1] + 2400]
    if chick:
        s = ss.resample_poly(s, 10, 13).astype(np.float32)  # same sr -> higher, faster cartoon voice
    sf.write(D + name + ".wav", s, sr)
    return len(s) / sr

def vo(t, name, text, speed=0.95, chick=False):
    d = say(name, text, speed, chick); ev.append(dict(t=round(t, 3), name=name, dur=round(d, 3))); return t + d

ROUNDS = [
    dict(items=['star', 'star', 'heart', 'star'], odd=2, pre=None, q="Which one is different?",
         a=[("a0", "The heart! The others are stars!", False)], label="Not a star!"),
    dict(items=['apple', 'carrot', 'banana', 'grapes'], odd=1, pre="Level two!", q="Which one doesn't belong?",
         a=[("a1", "The carrot! It's a vegetable, not a fruit!", False)], label="A vegetable!"),
    dict(items=['whale', 'fish', 'crab', 'chick'], odd=3, pre="Level three!", q="Who doesn't belong here?",
         a=[("a2c", "Hey! That's me!", True), ("a2", "Chickpea doesn't live in the sea!", False)], label="Not a sea animal!"),
    dict(items=['bfly_swap', 'bfly', 'bfly', 'bfly'], odd=0, pre="Level four! Look closely!", q="Which butterfly is different?",
         a=[("a3", "This one! Its colors are switched!", False)], label="Colors switched!"),
    dict(items=['n4', 'n8', 'n7', 'n2'], odd=2, pre="Level five! Expert level!", q="Which number is the odd one out?",
         a=[("a4", "Seven! It's the only odd number!", False)], label="Odd number!"),
]
TIMER = 4.0
t = 0.5
t = vo(t, "hook", "Find the odd one out! Can you beat all five levels?") + 0.2
rounds = []
for i, r in enumerate(ROUNDS):
    rd = dict(r); rd['i'] = i
    rd['start'] = round(0.6 if i == 0 else t, 3)  # cards flip in
    if r['pre']:
        t = vo(t + 0.35, f"pre{i}", r['pre']) + 0.12
    t = vo(t, f"q{i}", r['q']) + 0.2
    if i == 0:
        ev.append(dict(t=round(t + 0.05, 3), name="sayit", dur=round(say("sayit", "Say it out loud!", 1.0), 3)))
    rd['timer'] = round(t, 3); rd['reveal'] = round(t + TIMER, 3)
    ta = rd['reveal'] + 0.1
    for name, text, ch in r['a']:
        ta = vo(ta, name, text, 0.95, ch) + 0.1
    rd['end'] = round(max(ta + 0.5, rd['reveal'] + 2.3), 3)
    rounds.append(rd); t = rd['end']
outro = dict(start=round(t, 3))
t = vo(t + 0.5, "wow", "Wow! You're a super detective!") + 0.25
outro['bye'] = round(t, 3)
t = vo(t, "bye", "Bye-bye! See you next time!", 1.0, True) + 1.2
TL = dict(rounds=rounds, outro=outro, events=ev, dur=round(t, 2), timer=TIMER)
json.dump(TL, open("/home/claude/odd/timeline.json", "w"), indent=1)
print("dur", TL['dur'])
for r in rounds: print(r['i'], r['start'], r['timer'], r['reveal'], r['end'])
