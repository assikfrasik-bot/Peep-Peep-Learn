"""Build an episode and make contact sheets at key marks. usage: python3 check.py epNN [build]"""
import sys, json, subprocess, os
sys.path.insert(0, '/home/claude/kit')
import kit
ep = sys.argv[1]; F = f'/home/claude/{ep}'
if len(sys.argv) > 2 and sys.argv[2] == 'build':
    r = subprocess.run(['python3', f'{F}/{ep}.py', 'build'], capture_output=True, text=True, cwd=F)
    print(r.stdout[-1500:], r.stderr[-3000:])
tl = json.load(open(f'{F}/timeline.json')); m = tl['marks']; d = tl['dur']
ts = sorted(set([0.05] + [round(v + off, 2) for k, v in m.items() for off in ((0.5,) if k[0] in 'sc' else (0.35, 1.2))] + [d - 0.3]))
ts = [x for x in ts if 0 <= x < d]
print('dur', d, 'n', len(ts))
for j in range(0, len(ts), 12):
    kit.sheet(F, ep, ts[j:j + 12], out=f'sheet{j // 12}.png', w=240)
print(ts)
