import sys, math, json, random, os
sys.path.insert(0, '/home/claude/kit')
from kit import *
import cairo
from anim import (hexc, lerp, clamp, ease_io, ease_out_back, smooth, mixc, ellipse, fs, stroke_dev, draw_body, shell_part,
                  star, draw_text, hop, burst, OUT, W, H)
from anim2 import obj_carrot, big_word, glow
from anim3 import rrect, clean_text, star5

F = '/home/claude/ep3'
SM = 560  # snowman x
HEAD = (560, 905); MID = (560, 1135); BOT = (560, 1420)

def build():
    s = Script(F); t = 0.15
    t = s.say(t, 'hook', "Oh no! Our snowman is missing something!") + 0.2
    rounds = [('q1', "What's missing?", 'a1', "Eyes and a smile! Now he can see!"),
              ('q2', "What else is missing?", 'a2', "A carrot nose!"),
              ('q3', "And what's missing now?", 'a3', "Arms! Wave hello!")]
    for i, (qn, q, an, a) in enumerate(rounds):
        t = s.say(t, qn, q) + 0.1
        s.mark(f'c{i}', t); t += 3.0; s.mark(f'r{i}', t)
        t = s.say(t + 0.05, an, a) + 0.35
    s.mark('cold', t)
    t = s.say(t, 'brr', "Brrr! I'm so cold!", 0.95, False, 'am_puck') + 0.15
    t = s.say(t, 'give', "Here, take my scarf!", 1.0, True) + 0.1
    s.mark('scarf', t); t += 0.9
    t = s.say(t, 'thanks', "Thank you, Chickpea!", 1.0, False, 'am_puck') + 0.1
    t = s.say(t, 'ah', "Ah... ah...", 0.9, False, 'am_puck')
    s.mark('achoo', t)
    t = s.say(t, 'achoo', "ACHOO!", 1.0, False, 'am_puck') + 0.6
    t = s.say(t, 'oops', "Oops! Where did the nose go?") + 0.2
    t = s.say(t, 'laugh', "Hee hee! I'm a snowman too!", 1.0, True) + 0.3
    s.mark('again', t)
    t = s.say(t, 'again', "Again?", 1.0, True) + 0.2
    s.mark('loop', t); t += 1.3
    tl = s.save(t); m = tl['marks']; mx = Mix(tl['dur'])
    mx.music_loop(0, tl['dur'], 100, [([60, 64, 67], 36), ([57, 60, 64], 45), ([65, 69, 72], 41), ([67, 71, 74], 43)],
                  [[84, None, 83, None, 79, None, 76, None], [81, None, 79, None, 76, None, None, None]], 'soft', 1.1)
    for j in range(int(tl['dur'] / 0.6)): mx.add('mus', j * 0.6 + 0.3, bell(mtof([96, 100, 103, 100][j % 4]), 0.6), 0.025)
    for i in range(3):
        for j in range(3): mx.add('sfx', m[f'c{i}'] + j, tick(1100 if j < 2 else 1500), 0.35)
        mx.add('sfx', m[f'r{i}'], pop(400, 1000, 0.12), 0.4); mx.add('sfx', m[f'r{i}'] + 0.05, ding(), 0.22); mx.add('sfx', m[f'r{i}'] + 0.15, chirp(), 0.18)
    mx.add('sfx', m['cold'], drumroll(0.8) * 0.5, 0.2)
    mx.add('sfx', m['scarf'], whoosh(0.7), 0.3); mx.add('sfx', m['scarf'] + 0.7, tada(76), 0.15)
    mx.add('sfx', m['achoo'] + 0.05, whoosh(0.5), 0.4); mx.add('sfx', m['achoo'] + 0.1, slide_whistle(1200, 500, 0.6), 0.2)
    mx.add('sfx', m['achoo'] + 0.75, boing(), 0.3)
    mx.add('sfx', m['again'] + 0.1, jingle(), 0.25)
    mx.voices(F, tl['events'])
    mx.write(F + '/audio.wav', quiet=[(m[f'c{i}'], m[f'r{i}']) for i in range(3)]); return tl

TL = json.load(open(F + '/timeline.json')) if os.path.exists(F + '/timeline.json') else None
rr = random.Random(12)
SNOW = [(rr.uniform(0, 1080), rr.uniform(0, 1920), rr.uniform(3, 9), rr.uniform(40, 110), rr.uniform(0, 6)) for _ in range(120)]
PINES = [(80, 1300, 1.0), (230, 1260, 0.7), (900, 1280, 0.85), (1010, 1320, 1.1), (360, 1240, 0.5), (760, 1240, 0.55)]

def pine(cr, x, y, s):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.rectangle(-14, -20, 28, 40); fs(cr, hexc('#7A4A2A'), 5)
    for k, (w, h, yy) in enumerate(((120, 120, -10), (95, 110, -90), (70, 100, -165))):
        cr.move_to(-w, yy); cr.line_to(0, yy - h); cr.line_to(w, yy); cr.close_path(); fs(cr, hexc('#2E8B57'), 6)
        cr.move_to(-w * 0.55, yy - h * 0.45); cr.line_to(0, yy - h); cr.line_to(w * 0.55, yy - h * 0.45)
        cr.curve_to(w * 0.3, yy - h * 0.35, -w * 0.3, yy - h * 0.35, -w * 0.55, yy - h * 0.45); cr.close_path(); cr.set_source_rgb(1, 1, 1); cr.fill()
    cr.restore()

def scenery(cr, t):
    g = cairo.LinearGradient(0, 0, 0, 1400); g.add_color_stop_rgb(0, *hexc('#7CC6F5')); g.add_color_stop_rgb(1, *hexc('#E6F6FF'))
    cr.set_source(g); cr.paint()
    for k, (yb, amp, col) in enumerate(((1180, 60, '#DCEFFB'), (1300, 40, '#EEF8FF'))):
        cr.move_to(0, H)
        for x in range(0, W + 21, 20): cr.line_to(x, yb - amp * math.sin(math.pi * x / 1080 * (1.3 + k * 0.6) + k))
        cr.line_to(W, H); cr.close_path(); cr.set_source_rgb(*hexc(col)); cr.fill()
    for x, y, s in PINES: pine(cr, x, y, s)
    cr.move_to(0, H)
    for x in range(0, W + 21, 20): cr.line_to(x, 1500 + 18 * math.sin(x / 200))
    cr.line_to(W, H); cr.close_path()
    hg = cairo.LinearGradient(0, 1500, 0, H); hg.add_color_stop_rgb(0, 1, 1, 1); hg.add_color_stop_rgb(1, *hexc('#CFE6F7'))
    cr.set_source(hg); cr.fill()

def snowflakes(cr, t, front):
    for i, (x0, y0, r, sp, ph) in enumerate(SNOW):
        if (i % 3 == 0) != front: continue
        y = (y0 + t * sp) % 1980 - 40; x = x0 + 25 * math.sin(t * 0.8 + ph)
        cr.arc(x, y, r * (1.4 if front else 1), 0, 2 * math.pi); cr.set_source_rgba(1, 1, 1, 0.85); cr.fill()

def ball(cr, x, y, r):
    cr.arc(x, y, r, 0, 2 * math.pi)
    g = cairo.RadialGradient(x - r * 0.35, y - r * 0.4, r * 0.1, x, y, r * 1.05)
    g.add_color_stop_rgb(0, 1, 1, 1); g.add_color_stop_rgb(0.7, *hexc('#F2F8FF')); g.add_color_stop_rgb(1, *hexc('#C7DDF2'))
    cr.set_source(g); cr.fill_preserve(); stroke_dev(cr, OUT, 7)

def snowman(cr, t, m):
    e_eyes = ease_out_back((t - m['r0']) / 0.4) if t >= m['r0'] else 0
    e_nose = ease_out_back((t - m['r1']) / 0.4) if t >= m['r1'] else 0
    e_arms = ease_out_back((t - m['r2']) / 0.4) if t >= m['r2'] else 0
    shiver = (4 * math.sin(t * 50)) if m['cold'] <= t < m['scarf'] + 0.5 else 0
    jerk = 0
    if m['achoo'] <= t < m['achoo'] + 0.5: jerk = 40 * burst(m['achoo'], m['achoo'] + 0.5, t)
    cr.save(); cr.translate(shiver, 0)
    # arms (behind body)
    if e_arms > 0.01:
        for s in (-1, 1):
            wave = 0.25 * math.sin(t * 6) if (s == 1 and t < m['cold']) else 0
            cr.save(); cr.translate(SM + s * 120, MID[1] - 30); cr.rotate(s * (-0.5 + wave)); cr.scale(s * e_arms, e_arms)
            cr.move_to(0, 0); cr.line_to(170, -40); stroke_dev(cr, OUT, 20); cr.move_to(0, 0); cr.line_to(170, -40); stroke_dev(cr, hexc('#7A4A2A'), 11)
            for bx, by, ex, ey in ((120, -28, 160, -80), (140, -33, 190, -10)):
                cr.move_to(bx, by); cr.line_to(ex, ey); stroke_dev(cr, OUT, 14); cr.move_to(bx, by); cr.line_to(ex, ey); stroke_dev(cr, hexc('#7A4A2A'), 7)
            cr.restore()
    ball(cr, *BOT, 190); ball(cr, *MID, 140)
    for y in (1080, 1140, 1200): cr.arc(SM, y, 13, 0, 2 * math.pi); cr.set_source_rgb(*hexc('#2B2B3A')); cr.fill()
    hx, hy = HEAD[0], HEAD[1] - jerk * 0.3
    cr.save(); cr.translate(hx, hy); cr.rotate(-jerk * 0.004)
    ball(cr, 0, 0, 105)
    if e_eyes > 0.01:
        blink = (t % 3.7) < 0.12
        for s in (-1, 1):
            if blink: cr.move_to(s * 36 - 12, -20); cr.line_to(s * 36 + 12, -20); stroke_dev(cr, hexc('#2B2B3A'), 6)
            else:
                cr.arc(s * 36, -20, 14 * e_eyes, 0, 2 * math.pi); cr.set_source_rgb(*hexc('#2B2B3A')); cr.fill()
                cr.arc(s * 36 - 4, -25, 4 * e_eyes, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()
        cold = m['cold'] <= t < m['scarf'] + 0.3
        for k in range(5):
            a = math.pi * (0.25 + 0.125 * k); r = 52
            yy = 10 + r * math.sin(a) * (-0.6 if cold else 1)
            cr.arc(r * math.cos(a), yy + (40 if cold else 0), 6 * e_eyes, 0, 2 * math.pi); cr.set_source_rgb(*hexc('#2B2B3A')); cr.fill()
        for s in (-1, 1): ellipse(cr, s * 66, 20, 15, 9); cr.set_source_rgba(1, 0.5, 0.6, 0.45 * e_eyes); cr.fill()
    nose_on = e_nose > 0.01 and t < m['achoo'] + 0.05
    if nose_on:
        cr.save(); cr.translate(6, 8); cr.rotate(-1.5); cr.scale(0.28 * e_nose, 0.28 * e_nose); obj_carrot(cr, 1); cr.restore()
    cr.restore()
    # scarf on snowman
    if t >= m['scarf'] + 0.7:
        scarf(cr, SM, MID[1] - 125, 1.25, t)
    cr.restore()

def scarf(cr, x, y, s, t, tail=True):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    rrect(cr, -95, -20, 190, 40, 18); fs(cr, hexc('#FF4D4D'), 5)
    for k in range(-80, 90, 32): cr.rectangle(k, -20, 12, 40); cr.set_source_rgba(1, 1, 1, 0.6); cr.fill()
    if tail:
        cr.save(); cr.translate(50, 10); cr.rotate(0.25 + 0.08 * math.sin(t * 3))
        rrect(cr, -18, 0, 36, 95, 12); fs(cr, hexc('#FF4D4D'), 5)
        for k in (20, 52): cr.rectangle(-18, k, 36, 10); cr.set_source_rgba(1, 1, 1, 0.6); cr.fill()
        cr.restore()
    cr.restore()

def chick(cr, x, by, h, sc, st, t, look, has_scarf, nose):
    cr.save(); cr.translate(x, by - h); cr.scale(sc, sc)
    draw_body(cr, 0, -215, 1.0, st, t, look)
    for s in (-1, 1):
        cr.arc(s * 118, -230, 30, 0, 2 * math.pi); fs(cr, hexc('#FF7EB6'), 5)
    cr.move_to(-118, -260); cr.curve_to(-100, -380, 100, -380, 118, -260); stroke_dev(cr, hexc('#A15CFF'), 14)
    shell_part(cr, top=False)
    if has_scarf: scarf(cr, 0, -150, 1.15, t)
    if nose:
        cr.save(); cr.translate(40, -205); cr.rotate(-1.4); cr.scale(0.28, 0.28); obj_carrot(cr, 1); cr.restore()
    cr.restore()

def ring_hint(cr, x, y, r, t, a):
    if a <= 0.01: return
    cr.push_group()
    cr.save(); cr.set_dash([22, 16], t * 40); cr.arc(x, y, r, 0, 2 * math.pi); stroke_dev(cr, hexc('#FF9A1F'), 8); cr.restore()
    big_word(cr, "?", x + r * 0.8, y - r * 0.8 + 10 * math.sin(t * 6), 120, hexc('#FFD93B'), 1.0, 0.15 * math.sin(t * 4))
    cr.pop_group_to_source(); cr.paint_with_alpha(a)

def count_bubble(cr, t0, t):
    u = (t - t0) / 3.0
    if not (0 <= u < 1): return
    n = 3 - min(2, int(u * 3)); ph = (u * 3) % 1; s = 1 + 0.25 * max(0, 1 - ph * 5)
    a = smooth(t0, t0 + 0.2, t) * (1 - smooth(t0 + 2.8, t0 + 3.0, t))
    cr.push_group()
    rrect(cr, 300, 515, 480, 150, 75); fs(cr, (1, 1, 1), 7, hexc('#3B2A6B'))
    cr.arc(390, 590, 52 * s, 0, 2 * math.pi); fs(cr, hexc('#FFD93B'), 6, hexc('#3B2A6B'))
    clean_text(cr, str(n), 390, 586, 70 * s, hexc('#FF4D4D'), 3)
    clean_text(cr, "Say it!", 590, 590, 66, hexc('#3B2A6B'), 0.1, (1, 1, 1))
    cr.pop_group_to_source(); cr.paint_with_alpha(a)

def frame(cr, t):
    m = TL['marks']
    scenery(cr, t); snowflakes(cr, t, False)
    snowman(cr, t, m)
    hints = [(HEAD[0], HEAD[1] - 5, 85), (HEAD[0] + 10, HEAD[1] + 10, 55), (SM, MID[1] - 20, 230)]
    for i, (x, y, r) in enumerate(hints):
        q0 = m['hook'] if False else None
    starts = [TL['events'][1]['t'] if len(TL['events']) > 1 else 0]
    qs = [e['t'] for e in TL['events'] if e['name'] in ('q1', 'q2', 'q3')]
    for i, (x, y, r) in enumerate(hints):
        a = smooth(qs[i], qs[i] + 0.3, t) * (1 - smooth(m[f'r{i}'], m[f'r{i}'] + 0.2, t))
        ring_hint(cr, x, y, r, t, a)
        if m[f'r{i}'] <= t < m[f'r{i}'] + 0.8:
            u = (t - m[f'r{i}']) / 0.8
            for k in range(8):
                ang = k * math.pi / 4; d = r * 0.6 + 140 * u
                star(cr, x + d * math.cos(ang), y + d * math.sin(ang), 26 * (1 - u)); cr.set_source_rgb(1, 0.95, 0.5); cr.fill()
    for i in range(3): count_bubble(cr, m[f'c{i}'], t)
    labs = [('Eyes!', '#2EA7FF'), ('Carrot nose!', '#FF9A1F'), ('Arms!', '#8B5A2B')]
    for i, (lab, col) in enumerate(labs):
        r = m[f'r{i}']; nxt = qs[i + 1] if i < 2 else m['cold']
        if r <= t < nxt + 0.3:
            big_word(cr, lab, 540, 590, 120, hexc(col), ease_out_back((t - r) / 0.4), 0.03 * math.sin(t * 3), 1 - smooth(nxt, nxt + 0.3, t))
    if m['achoo'] <= t < m['achoo'] + 1.4:
        big_word(cr, "ACHOO!", 640, 600, 150, hexc('#2EA7FF'), ease_out_back((t - m['achoo']) / 0.3), -0.1, 1 - smooth(m['achoo'] + 1.1, m['achoo'] + 1.4, t))
        u = t - m['achoo']
        for k in range(14):
            ang = -2.6 + k * 0.1; d = 80 + 700 * u
            cr.arc(HEAD[0] + d * math.cos(ang), HEAD[1] + d * math.sin(ang) * 0.5 + 300 * u * u, 10, 0, 2 * math.pi)
            cr.set_source_rgba(1, 1, 1, max(0, 1 - u)); cr.fill()
    # chick
    cx, cby, csc = 210, 1600, 0.7
    st = dict(wing=[0.0, 0.0], beak=0.0, happy=0, mood=0.0); hh = 0
    look = (0.8, -0.5)
    for e in TL['events']:
        if e['chick'] and e['t'] <= t < e['t'] + e['dur']: st['beak'] = 0.5 * abs(math.sin(t * 14)); st['happy'] = 1
    for i in range(3):
        r = m[f'r{i}'] + 0.05
        if r <= t < r + 0.9:
            kk = int((t - r) / 0.45); _, hh, sx, sy, _, air = hop(t, r + 0.45 * kk, 0.45, 70, 0, 0)
            st.update(happy=1, wing=[0.4 + 0.8 * air] * 2, beak=0.6 * air)
    if m['cold'] <= t < m['scarf']: st.update(mood=0.6); look = (1, -0.6)
    has_scarf = t < m['scarf'] + 0.05
    nose = t >= m['achoo'] + 0.75 and t < m['loop']
    if m['achoo'] + 0.75 <= t < m['again']: st.update(happy=1)
    ellipse(cr, cx, cby + 2, 78, 13); cr.set_source_rgba(0.3, 0.45, 0.6, 0.25); cr.fill()
    chick(cr, cx, cby, hh, csc, st, t, look, has_scarf, nose)
    # flying scarf
    if m['scarf'] <= t < m['scarf'] + 0.7:
        u = ease_io((t - m['scarf']) / 0.7)
        x = lerp(cx, SM, u); y = lerp(cby - 0.7 * 150, MID[1] - 125, u) - 220 * math.sin(math.pi * u)
        cr.save(); cr.translate(x, y); cr.rotate(u * 6.28); scarf(cr, 0, 0, lerp(0.8, 1.25, u), t); cr.restore()
    # flying nose
    if m['achoo'] + 0.05 <= t < m['achoo'] + 0.75:
        u = (t - m['achoo'] - 0.05) / 0.7
        x = lerp(HEAD[0] + 10, cx + 28, u); y = lerp(HEAD[1] + 10, cby - 0.7 * 205, u) - 380 * math.sin(math.pi * u)
        cr.save(); cr.translate(x, y); cr.rotate(u * 9); cr.scale(0.28, 0.28); obj_carrot(cr, 1); cr.restore()
    snowflakes(cr, t, True)
    draw_text(cr, "Build a Snowman!", 250, 120, t, -1)

if __name__ == '__main__':
    if sys.argv[1] == 'build': tl = build(); print(tl['dur'], tl['marks'])
