import json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
k = Kokoro("/home/claude/tts/kokoro.onnx", "/home/claude/tts/voices.bin")
VOICE, SPEED = "af_heart", 0.92
D = "/home/claude/colors/vo/"
import os; os.makedirs(D, exist_ok=True)

def say(name, text, speed=SPEED):
    s, sr = k.create(text, voice=VOICE, speed=speed, lang="en-us")
    s = np.asarray(s, dtype=np.float32)
    idx = np.where(np.abs(s) > 0.01)[0]  # trim silence
    s = s[max(0, idx[0] - 600): idx[-1] + 2400]
    sf.write(D + name + ".wav", s, sr)
    return len(s) / sr

ROUNDS = [("red", "apple", "Red! The apple is red!", "What color is the apple?"),
          ("orange", "carrot", "Orange! The carrot is orange!", "What color is the carrot?"),
          ("yellow", "banana", "Yellow! The banana is yellow!", "What color is the banana?"),
          ("green", "frog", "Green! The frog is green!", "What color is the frog?"),
          ("blue", "whale", "Blue! The whale is blue!", "What color is the whale?"),
          ("purple", "grapes", "Purple! The grapes are purple!", "What color are the grapes?")]
ev = []  # (time, kind, data)
def vo(t, name, text, speed=SPEED):
    d = say(name, text, speed); ev.append(dict(t=round(t, 3), kind="vo", name=name, dur=round(d, 3))); return t + d

t = 0.35
t = vo(t, "hook1", "Oh no! The rainbow lost its colors!") + 0.25
title_t = t
t = vo(t, "hook2", "Help Chickpea find them!") + 0.35
rounds = []
for i, (col, obj, ans, q) in enumerate(ROUNDS):
    r = dict(i=i, color=col, obj=obj, appear=round(t, 3))
    tq = t + 0.35
    tq_end = vo(tq, f"q{i}", q)
    r["wait"] = round(tq_end + 0.15, 3)
    r["reveal"] = round(r["wait"] + 2.1, 3)
    ta_end = vo(r["reveal"] + 0.08, f"a{i}", ans)
    r["fly"] = round(r["reveal"] + 0.7, 3)
    r["end"] = round(max(ta_end + 0.45, r["fly"] + 1.5), 3)
    rounds.append(r); t = r["end"]
outro = dict(start=round(t, 3))
t = vo(t + 0.1, "yay", "Yay! The rainbow is back!") + 0.2
recap = []
for i, (col, *_r) in enumerate(ROUNDS):
    recap.append(round(t, 3)); t = vo(t, f"r{i}", col.capitalize() + "!", 1.0) + 0.12
t += 0.25
outro["bye"] = round(t, 3)
t = vo(t, "bye", "Bye-bye! See you next time!") + 1.0
TL = dict(title=round(title_t, 3), rounds=rounds, outro=outro, recap=recap, events=ev, dur=round(t, 2))
json.dump(TL, open("/home/claude/colors/timeline.json", "w"), indent=1)
print("duration", TL["dur"])
for r in rounds: print(r)
