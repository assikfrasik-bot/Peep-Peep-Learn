"""Render an episode and verify the output length matches the timeline. usage: python3 make.py epNN outname"""
import sys, json, subprocess
sys.path.insert(0, '/home/claude/kit')
import kit
ep, name = sys.argv[1], sys.argv[2]
F = f'/home/claude/{ep}'
d = json.load(open(f'{F}/timeline.json'))['dur']
kit.render(F, ep, d, 'out.mp4')
got = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'{F}/out.mp4'], capture_output=True, text=True).stdout)
assert abs(got - d) < 0.1, f'LENGTH MISMATCH {got} vs {d}'
subprocess.run(['cp', f'{F}/out.mp4', f'/home/claude/out_eps/{name}.mp4'], check=True)
print('OK', name, got)
