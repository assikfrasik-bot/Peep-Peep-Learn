import sys, math, json, random, os
sys.path.insert(0, '/home/claude/kit')
from kit import *
import cairo
from anim import (hexc, lerp, clamp, ease_io, ease_out_back, smooth, mixc, ellipse, fs, stroke_dev, draw_body, shell_part,
                  star, draw_text, hop, burst, draw_sun, draw_cloud, draw_flower, OUT, W, H)
from anim2 import obj_apple, big_word, glow
from anim3 import rrect, clean_text, star5

F = '/home/claude/ep2'
NUMS = ['One!', 'Two!', 'Three!', 'Four!', 'Five!']
ROW = [330, 470, 610, 750, 890]
TREE_POS = [(400, 640), (640, 580), (520, 760), (300, 800), (760, 760)]

def build():
    s = Script(F); t = 0.15
    t = s.say(t, 'hook', "How many apples will fall? Let's count!") + 0.2
    s.mark('bump', t)
    t += 0.5
    for k in range(5):
        s.mark(f'land{k}', t + 0.45)
        t = s.say(t + 0.5, f'n{k}', NUMS[k], 0.9) + 0.25
    t = s.say(t + 0.2, 'q1', "How many apples?") + 0.1
    s.mark('c1', t); t += 3.0; s.mark('r1', t)
    t = s.say(t + 0.05, 'a1', "Five! Five red apples!") + 0.3
    s.mark('eat', t)
    t = s.say(t + 1.6, 'yum', "Yum yum!", 1.0, True) + 0.2
    t = s.say(t, 'q2', "Uh-oh! How many apples now?") + 0.1
    s.mark('c2', t); t += 3.0; s.mark('r2', t)
    t = s.say(t + 0.05, 'a2', "Four! Five take away one is four!") + 0.3
    s.mark('worm', t)
    t = s.say(t + 0.5, 'hey', "Hey! That was my house!", 1.05, False, 'am_puck') + 0.15
    t = s.say(t, 'oops', "Oops! Sorry, worm!", 1.0, True) + 0.3
    s.mark('again', t)
    t = s.say(t, 'again', "Count again?", 1.0, True) + 0.2
    s.mark('loop', t); t += 1.3
    tl = s.save(t); m = tl['marks']; mx = Mix(tl['dur'])
    mx.music_loop(0, tl['dur'], 112, [([60, 64, 67], 36), ([65, 69, 72], 41), ([67, 71, 74], 43), ([60, 64, 67], 36)],
                  [[72, None, 74, None, 76, None, 79, None], [77, None, 76, None, 74, None, None, None]], 'bouncy', 0.9)
    mx.add('sfx', m['bump'], kick(), 0.6); mx.add('sfx', m['bump'], whoosh(0.5), 0.3)
    for k in range(5):
        mx.add('sfx', m[f'land{k}'] - 0.35, slide_whistle(1400, 600, 0.35), 0.12)
        mx.add('sfx', m[f'land{k}'], pop(200, 500, 0.1), 0.45); mx.add('sfx', m[f'land{k}'], marimba(mtof(72 + [0, 2, 4, 5, 7][k])), 0.3)
    for k in ('c1', 'c2'):
        for j in range(3): mx.add('sfx', m[k] + j, tick(1100 if j < 2 else 1500), 0.35)
    for k in ('r1', 'r2'): mx.add('sfx', m[k], ding(), 0.25); mx.add('sfx', m[k] + 0.1, chirp(), 0.2)
    for j in range(3):
        mx.add('sfx', m['eat'] + 0.4 + j * 0.4, bp(rng.standard_normal(int(0.12 * SR)), 1500, 6000) * np.exp(-tt(0.12) / 0.03), 0.5)
    mx.add('sfx', m['worm'], slide_whistle(300, 900, 0.5), 0.25); mx.add('sfx', m['worm'] + 0.45, pop(), 0.35)
    mx.add('sfx', m['again'] + 0.2, jingle(), 0.25)
    mx.voices(F, tl['events'])
    mx.write(F + '/audio.wav', quiet=[(m['c1'], m['r1']), (m['c2'], m['r2'])]); return tl

TL = json.load(open(F + '/timeline.json')) if os.path.exists(F + '/timeline.json') else None
rr = random.Random(8)
GR = [(x + rr.uniform(-5, 5), rr.uniform(26, 48), rr.uniform(0, 6)) for x in range(-10, 1100, 13)]
def ground_y(x): return 1520 + 16 * math.sin(x / 170)
FLW = [(rr.uniform(30, 1050), rr.uniform(1640, 1880), rr.choice(['#FF5A5F', '#FFFFFF', '#A66CFF', '#FFB400', '#FF7EB6']), rr.uniform(0.8, 1.1)) for _ in range(10)]

def scenery(cr, t):
    g = cairo.LinearGradient(0, 0, 0, 1500); g.add_color_stop_rgb(0, *hexc('#4FC0FF')); g.add_color_stop_rgb(1, *hexc('#D8F6FF'))
    cr.set_source(g); cr.paint()
    sc = 0.7; cr.save(); cr.translate(930 - 870 * sc, 360 - 270 * sc); cr.scale(sc, sc); draw_sun(cr, t); cr.restore()
    for i, (x, y, s) in enumerate(((150, 420, 0.5), (780, 560, 0.4))):
        draw_cloud(cr, (x + t * 12 + 300) % 1500 - 300, y, s, (1, 1, 1), outline=False)
    cr.move_to(0, H)
    for x in range(0, W + 21, 20): cr.line_to(x, 1330 - 50 * math.sin(math.pi * x / 1080 * 1.4 + 0.3))
    cr.line_to(W, H); cr.close_path(); cr.set_source_rgb(*hexc('#A6E58A')); cr.fill()
    cr.move_to(0, H)
    for x in range(0, W + 21, 20): cr.line_to(x, ground_y(x))
    cr.line_to(W, H); cr.close_path()
    hg = cairo.LinearGradient(0, 1500, 0, H); hg.add_color_stop_rgb(0, *hexc('#62C64C')); hg.add_color_stop_rgb(1, *hexc('#3E9E3A'))
    cr.set_source(hg); cr.fill()

def tree(cr, t, shake):
    sx = 14 * shake * math.sin(t * 40)
    cr.move_to(480, 1530); cr.curve_to(500, 1300, 490, 1100, 470 + sx * 0.3, 900); cr.line_to(610 + sx * 0.3, 900)
    cr.curve_to(590, 1100, 580, 1300, 600, 1530); cr.close_path(); fs(cr, hexc('#9B6B43'), 8)
    cr.arc(545, 1250, 28, 0, 2 * math.pi); cr.set_source_rgb(*hexc('#5C3A1F')); cr.fill()
    blobs = [(540, 640, 270), (330, 760, 190), (750, 760, 190), (400, 560, 180), (690, 560, 180), (540, 840, 200)]
    cr.save(); cr.translate(sx, 0)
    for x, y, r in blobs: cr.arc(x, y, r, 0, 2 * math.pi); cr.new_sub_path()
    stroke_dev(cr, OUT, 14)
    for x, y, r in blobs: cr.arc(x, y, r, 0, 2 * math.pi); cr.new_sub_path()
    g = cairo.RadialGradient(480, 520, 50, 540, 700, 480); g.add_color_stop_rgb(0, *hexc('#7BDB5C')); g.add_color_stop_rgb(1, *hexc('#3FAE3C'))
    cr.set_source(g); cr.fill()
    for x, y, r in ((420, 520, 40), (640, 480, 30), (300, 700, 28), (760, 680, 26)):
        cr.arc(x, y, r, 0, 2 * math.pi); cr.set_source_rgba(1, 1, 1, 0.18); cr.fill()
    cr.restore()
    return sx

def apple_core(cr):
    cr.move_to(-40, -60); cr.curve_to(-10, -30, -10, 30, -40, 60); cr.line_to(40, 60); cr.curve_to(10, 30, 10, -30, 40, -60); cr.close_path()
    fs(cr, hexc('#FFF3D6'), 6)
    ellipse(cr, 0, -62, 46, 16); fs(cr, hexc('#FF4D4D'), 6); ellipse(cr, 0, 62, 46, 16); fs(cr, hexc('#FF4D4D'), 6)
    cr.move_to(0, -76); cr.line_to(5, -100); stroke_dev(cr, hexc('#8B5A2B'), 8)
    for y in (-14, 14): ellipse(cr, 0, y, 5, 8); cr.set_source_rgb(*hexc('#5C3A1F')); cr.fill()

def worm(cr, x, y, e, t):
    if e <= 0.01: return
    cr.save(); cr.translate(x, y); cr.scale(e, e)
    for k in range(4, 0, -1):
        cr.arc(8 * math.sin(t * 6 + k), -k * 26, 22, 0, 2 * math.pi); fs(cr, hexc('#FF9EBB'), 5)
    hx = 8 * math.sin(t * 6 + 5); cr.arc(hx, -130, 30, 0, 2 * math.pi); fs(cr, hexc('#FF9EBB'), 5)
    for s in (-1, 1):
        cr.arc(hx + s * 12, -136, 9, 0, 2 * math.pi); fs(cr, (1, 1, 1), 3); cr.arc(hx + s * 12, -134, 4, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill()
    cr.move_to(hx - 10, -116); cr.line_to(hx + 10, -116); stroke_dev(cr, OUT, 4)
    cr.move_to(hx - 22, -150); cr.line_to(hx - 6, -158); stroke_dev(cr, OUT, 4); cr.move_to(hx + 22, -150); cr.line_to(hx + 6, -158); stroke_dev(cr, OUT, 4)
    cr.restore()

def chick(cr, x, by, h, sc, st, t, look, sx=1, sy=1, rot=0):
    cr.save(); cr.translate(x, by - h); cr.rotate(rot); cr.scale(sc * sx, sc * sy)
    draw_body(cr, 0, -215, 1.0, st, t, look); shell_part(cr, top=False); cr.restore()

def count_bubble(cr, t0, t, label="Count!"):
    u = (t - t0) / 3.0
    if not (0 <= u < 1): return
    n = 3 - min(2, int(u * 3)); ph = (u * 3) % 1; s = 1 + 0.25 * max(0, 1 - ph * 5)
    a = smooth(t0, t0 + 0.2, t) * (1 - smooth(t0 + 2.8, t0 + 3.0, t))
    cr.push_group()
    rrect(cr, 300, 1105, 480, 150, 75); fs(cr, (1, 1, 1), 7, hexc('#3B2A6B'))
    cr.arc(390, 1180, 52 * s, 0, 2 * math.pi); fs(cr, hexc('#FFD93B'), 6, hexc('#3B2A6B'))
    clean_text(cr, str(n), 390, 1176, 70 * s, hexc('#FF4D4D'), 3)
    clean_text(cr, "Say it!", 590, 1180, 66, hexc('#3B2A6B'), 0.1, (1, 1, 1))
    cr.pop_group_to_source(); cr.paint_with_alpha(a)

def frame(cr, t):
    m = TL['marks']
    scenery(cr, t)
    shake = burst(m['bump'], m['bump'] + 0.6, t) + 0.6 * sum(burst(m[f'land{k}'] - 0.6, m[f'land{k}'] - 0.3, t) for k in range(5))
    regrow = smooth(m['again'], m['again'] + 0.6, t)
    sx = tree(cr, t, min(1, shake))
    # apples on tree
    for k, (ax, ay) in enumerate(TREE_POS):
        tl0 = m[f'land{k}'] - 0.5
        if t < tl0 or regrow > 0:
            s = 1 if t < tl0 else ease_out_back(regrow)
            if s > 0.01:
                cr.save(); cr.translate(ax + sx, ay + 4 * math.sin(t * 2 + k)); cr.rotate(0.1 * math.sin(t * 2 + k)); cr.scale(0.32 * s, 0.32 * s); obj_apple(cr, 1); cr.restore()
    # falling / landed apples
    eaten = m['eat'] + 0.4
    for k in range(5):
        tl0 = m[f'land{k}'] - 0.5; tl1 = m[f'land{k}']
        if t < tl0 or regrow >= 1: continue
        ax, ay = TREE_POS[k]; gx = ROW[k]; gy = ground_y(gx) + 30
        if t < tl1:
            u = (t - tl0) / 0.5; x = lerp(ax, gx, u); y = lerp(ay, gy - 50, u * u); rot = u * 2; sq = 1
        else:
            u = t - tl1; x = gx; y = gy - 50 - 60 * abs(math.sin(min(u, 0.5) * math.pi * 2)) * max(0, 1 - u * 2); rot = 0.08 * math.sin(t * 2 + k); sq = 1
        a = 1 - regrow
        glow_k = 0
        if m['r1'] <= t < m['eat']:
            glow_k = burst(m['r1'] + 0.15 * k, m['r1'] + 0.15 * k + 0.4, t)
        if glow_k > 0: glow(cr, x, y, 110, (1, 1, 0.6), 0.7 * glow_k)
        cr.push_group(); cr.translate(x, y); cr.rotate(rot)
        if k == 0 and t >= eaten:
            bites = min(3, int((t - eaten) / 0.4) + 1)
            if bites < 3:
                cr.scale(0.36 * (1 - 0.18 * bites), 0.36); obj_apple(cr, 1)
            else:
                cr.scale(0.75, 0.75); apple_core(cr)
        else:
            cr.scale(0.36 * (1 + 0.15 * glow_k), 0.36 * (1 + 0.15 * glow_k)); obj_apple(cr, 1)
        cr.pop_group_to_source(); cr.paint_with_alpha(a)
        if t >= tl1 and t < m['eat'] and regrow == 0:
            ns = ease_out_back((t - tl1) / 0.35)
            if ns > 0.01:
                cr.save(); cr.translate(gx, gy - 160); cr.scale(ns, ns)
                cr.arc(0, 0, 42, 0, 2 * math.pi); fs(cr, (1, 1, 1), 6, hexc('#3B2A6B'))
                clean_text(cr, str(k + 1), 0, -3, 60, hexc('#FF4D4D'), 3); cr.restore()
    # numbers in big during counting
    for k in range(5):
        a0 = m[f'land{k}']; a1 = m[f'land{k + 1}'] if k < 4 else a0 + 1.0
        if a0 <= t < a1:
            big_word(cr, str(k + 1), 540, 1080, 260, hexc(['#FF4D4D', '#FF9A1F', '#3ECF5E', '#2EA7FF', '#A15CFF'][k]),
                     ease_out_back((t - a0) / 0.3), 0, 1 - smooth(a1 - 0.2, a1, t))
    # worm
    if t >= m['worm']:
        e = ease_out_back((t - m['worm']) / 0.5) * (1 - smooth(m['again'], m['again'] + 0.4, t))
        worm(cr, ROW[0], ground_y(ROW[0]) - 30, e * 0.9, t)
    # labels
    for k, lab in (('r1', 'Five apples!'), ('r2', '5 - 1 = 4')):
        r = m[k]; nxt = m['eat'] if k == 'r1' else m['worm'] + 0.8
        if r <= t < nxt + 0.3:
            big_word(cr, lab, 540, 1080, 130, hexc('#FF4D4D') if k == 'r1' else hexc('#2EA7FF'),
                     ease_out_back((t - r) / 0.4), 0.03 * math.sin(t * 3), 1 - smooth(nxt, nxt + 0.3, t))
    count_bubble(cr, m['c1'], t); count_bubble(cr, m['c2'], t)
    # chick
    st = dict(wing=[0.0, 0.0], beak=0.0, happy=0, mood=0.0); hh = 0; sxx = syy = 1; rot = 0
    cx = 150; look = (0.5, -0.8)
    for e in TL['events']:
        if e['chick'] and e['t'] <= t < e['t'] + e['dur']: st['beak'] = 0.5 * abs(math.sin(t * 14)); st['happy'] = 1
    if m['bump'] - 0.5 <= t < m['bump'] + 0.4:
        u = (t - m['bump'] + 0.5) / 0.9; cx = 150 + 260 * math.sin(math.pi * u); rot = 0.25 * math.sin(math.pi * u)
    if m['land0'] - 0.5 <= t < m['r1']:
        k = min(4, max(0, int((t - m['land0'] + 0.5) / max(0.1, (m['land4'] - m['land0']) / 4))))
        look = (0.6 if k < 3 else 0.9, 0.3)
    for k in range(5):
        a0 = m[f'land{k}']
        if a0 <= t < a0 + 0.4: st.update(wing=[0.8, 0.8], beak=0.5)
    if m['eat'] - 0.3 <= t < m['eat'] + 1.6:
        u = clamp((t - m['eat'] + 0.3) / 0.6); cx = lerp(150, ROW[0] - 135, ease_io(u)); look = (1, 0.6)
        if t >= m['eat'] + 0.4: st.update(beak=0.7 * abs(math.sin(t * 16)), happy=1)
    elif m['eat'] + 1.6 <= t < m['again']:
        cx = ROW[0] - 135; look = (1, 0.2)
    elif t >= m['again']:
        u = clamp((t - m['again']) / 0.6); cx = lerp(ROW[0] - 135, 150, ease_io(u))
    if m['worm'] + 0.4 <= t < m['again']: st.update(mood=0.7, wing=[1.0, 1.0]); look = (1, -0.3)
    for k in ('r1', 'r2'):
        r = m[k] + 0.05
        if r <= t < r + 0.9:
            kk = int((t - r) / 0.45); _, hh, sxx, syy, _, air = hop(t, r + 0.45 * kk, 0.45, 70, 0, 0)
            st.update(happy=1, wing=[0.4 + 0.8 * air] * 2, beak=0.6 * air)
    by = ground_y(cx) + 40
    ellipse(cr, cx, by + 2, 80, 14); cr.set_source_rgba(0.1, 0.25, 0.05, 0.25); cr.fill()
    chick(cr, cx, by, hh, 0.66, st, t, look, sxx, syy, rot)
    for i, (x, y, c, s) in enumerate(FLW): draw_flower(cr, x, y, s, hexc(c), t, i)
    draw_text(cr, "Count the Apples!", 250, 118, t, -1)

if __name__ == '__main__':
    if sys.argv[1] == 'build': tl = build(); print(tl['dur'], tl['marks'])
