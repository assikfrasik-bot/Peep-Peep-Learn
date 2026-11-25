import sys, math, json, random, os
sys.path.insert(0, '/home/claude/kit')
from kit import *
import cairo
from anim import (hexc, lerp, clamp, ease_io, ease_out_back, smooth, mixc, ellipse, fs, stroke_dev, draw_body, shell_part,
                  star, draw_text, hop, burst, draw_sun, draw_cloud, draw_flower, tree, bush, OUT, W, H)
from anim2 import big_word, glow
from anim3 import rrect, clean_text, star5

F = '/home/claude/ep6'

def build():
    s = Script(F); t = 0.1
    s.mark('slip', 0.7)
    t = s.say(t, 'hook', "Oh no! Frog's balloon flew away!") + 0.2
    t = s.say(t, 'q1', "How does Frog feel?") + 0.1
    s.mark('c1', t); t += 3.0; s.mark('r1', t)
    t = s.say(t + 0.05, 'a1', "Sad! Frog feels sad.") + 0.3
    t = s.say(t, 'give', "Don't be sad! You can have my balloon!", 1.0, True) + 0.1
    s.mark('give', t); t += 1.4
    t = s.say(t, 'q2', "How does Frog feel now?") + 0.1
    s.mark('c2', t); t += 3.0; s.mark('r2', t)
    t = s.say(t + 0.05, 'a2', "Happy! Sharing makes friends happy!") + 0.2
    s.mark('lift', t)
    t = s.say(t + 0.9, 'q3', "Whoa! And now?") + 0.1
    s.mark('c3', t); t += 3.0; s.mark('r3', t)
    t = s.say(t + 0.05, 'a3', "Surprised!") + 0.1
    t = s.say(t, 'whee', "Wheee! Wait for me!", 1.0, True) + 0.4
    s.mark('again', t)
    t = s.say(t, 'again', "Again?", 1.0, True) + 0.2
    s.mark('loop', t); t += 1.2
    tl = s.save(t); m = tl['marks']; mx = Mix(tl['dur'])
    mx.music_loop(0, m['r1'] + 1.5, 96, [([57, 60, 64], 45), ([53, 57, 60], 41), ([55, 59, 62], 43), ([57, 60, 64], 45)],
                  [[76, None, 74, None, 72, None, None, None]], 'soft', 1.0)
    mx.music_loop(m['r1'] + 1.5, tl['dur'], 112, [([60, 64, 67], 36), ([65, 69, 72], 41), ([67, 71, 74], 43), ([60, 64, 67], 36)],
                  [[72, None, 76, None, 79, None, 84, None], [81, None, 79, None, 76, None, None, None]], 'bouncy', 0.9)
    mx.add('sfx', m['slip'], slide_whistle(500, 1600, 0.8), 0.25)
    for k in ('c1', 'c2', 'c3'):
        for j in range(3): mx.add('sfx', m[k] + j, tick(1100 if j < 2 else 1500), 0.33)
    mx.add('sfx', m['r1'], bell(mtof(64), 1.5), 0.25); mx.add('sfx', m['r1'] + 0.3, bell(mtof(60), 1.5), 0.2)
    mx.add('sfx', m['give'], whoosh(0.6), 0.3); mx.add('sfx', m['give'] + 0.8, tada(72), 0.18)
    mx.add('sfx', m['r2'], ding(), 0.25); mx.add('sfx', m['r2'] + 0.1, chirp(), 0.2)
    mx.add('sfx', m['lift'], whoosh(1.0), 0.4); mx.add('sfx', m['lift'] + 0.3, slide_whistle(400, 1200, 1.0), 0.2)
    mx.add('sfx', m['r3'], pop(400, 1200, 0.12), 0.4); mx.add('sfx', m['r3'] + 0.05, ding(), 0.2)
    mx.add('sfx', m['again'] + 0.2, jingle(), 0.22)
    mx.voices(F, tl['events'])
    mx.write(F + '/audio.wav', quiet=[(m['c1'], m['r1']), (m['c2'], m['r2']), (m['c3'], m['r3'])]); return tl

TL = json.load(open(F + '/timeline.json')) if os.path.exists(F + '/timeline.json') else None
rr = random.Random(21)
FLW = [(rr.uniform(30, 1050), rr.uniform(1620, 1880), rr.choice(['#FF5A5F', '#FFFFFF', '#A66CFF', '#FFB400', '#FF7EB6']), rr.uniform(0.8, 1.1)) for _ in range(12)]

def scenery(cr, t):
    g = cairo.LinearGradient(0, 0, 0, 1400); g.add_color_stop_rgb(0, *hexc('#4DB8FF')); g.add_color_stop_rgb(1, *hexc('#E0F7FF'))
    cr.set_source(g); cr.paint()
    sc = 0.6; cr.save(); cr.translate(140 - 870 * sc, 420 - 270 * sc); cr.scale(sc, sc); draw_sun(cr, t); cr.restore()
    for i, (x, y, s) in enumerate(((700, 420, 0.5), (250, 650, 0.4), (950, 760, 0.35))):
        draw_cloud(cr, (x + t * 14 + 300) % 1500 - 300, y, s, (1, 1, 1), outline=False)
    cr.move_to(0, H)
    for x in range(0, W + 21, 20): cr.line_to(x, 1200 - 60 * math.sin(math.pi * x / 1080 * 1.4 + 0.2))
    cr.line_to(W, H); cr.close_path(); cr.set_source_rgb(*hexc('#A6E58A')); cr.fill()
    for x, s in ((90, 0.75), (1000, 0.8)): tree(cr, x, 1200 - 60 * math.sin(math.pi * x / 1080 * 1.4 + 0.2) + 40, s, '#4CB944')
    bush(cr, 520, 1190, 0.6)
    cr.move_to(0, H)
    for x in range(0, W + 21, 20): cr.line_to(x, 1430 + 14 * math.sin(x / 180))
    cr.line_to(W, H); cr.close_path()
    hg = cairo.LinearGradient(0, 1430, 0, H); hg.add_color_stop_rgb(0, *hexc('#62C64C')); hg.add_color_stop_rgb(1, *hexc('#3E9E3A'))
    cr.set_source(hg); cr.fill()

def frog(cr, x, y, sc, mood, t, rot=0, legs=0):
    """mood: 'happy' | 'sad' | 'surprised'"""
    gc = hexc('#3ECF5E')
    cr.save(); cr.translate(x, y); cr.rotate(rot); cr.scale(sc, sc)
    for s in (-1, 1):
        cr.save(); cr.translate(s * 85, 140); cr.rotate(s * legs); ellipse(cr, 0, legs * 30, 45, 20); fs(cr, gc); cr.restore()
    for s in (-1, 1): cr.arc(s * 62, -62, 46, 0, 2 * math.pi); fs(cr, gc)
    ellipse(cr, 0, 40, 145, 108); fs(cr, gc)
    for s in (-1, 1):
        cr.arc(s * 62, -62, 46, math.pi * 1.05, math.pi * 1.95); cr.close_path(); cr.set_source_rgb(*gc); cr.fill()
        er = 36 if mood == 'surprised' else 30
        cr.arc(s * 62, -64, er, 0, 2 * math.pi); fs(cr, (1, 1, 1), 5)
        py = -56 if mood == 'sad' else -62
        cr.arc(s * 62 + 2, py, 15 if mood != 'surprised' else 12, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill()
        cr.arc(s * 62 - 3, py - 6, 5, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()
        if mood == 'sad':
            cr.move_to(s * 30, -118); cr.line_to(s * 88, -104); stroke_dev(cr, OUT, 7)
        if mood == 'surprised':
            cr.arc(s * 62, -128, 26, 1.2 * math.pi, 1.8 * math.pi); stroke_dev(cr, OUT, 6)
    ellipse(cr, 0, 85, 85, 48); cr.set_source_rgb(*hexc('#A8F0B4')); cr.fill()
    if mood == 'happy':
        cr.arc(0, 0, 70, 0.22 * math.pi, 0.78 * math.pi); stroke_dev(cr, OUT, 7)
    elif mood == 'sad':
        cr.arc(0, 85, 50, 1.25 * math.pi, 1.75 * math.pi); stroke_dev(cr, OUT, 7)
        ty = -20 + (t * 140) % 90
        cr.move_to(-62, ty - 12); cr.curve_to(-72, ty + 6, -52, ty + 6, -62, ty - 12); cr.close_path()
        ellipse(cr, -62, ty + 4, 9, 12); cr.set_source_rgb(*hexc('#7FD0FF')); cr.fill()
    else:
        ellipse(cr, 0, 50, 26, 32); fs(cr, hexc('#C0392B'), 6)
    for s in (-1, 1):
        ellipse(cr, s * 95, 25, 18, 11); cr.set_source_rgba(1, 0.45, 0.55, 0.55 if mood != 'sad' else 0.2); cr.fill()
    cr.restore()

def balloon_at(cr, bx, by, hx, hy, col, t):
    cr.move_to(hx, hy); cr.curve_to(hx + 20, (hy + by) / 2 + 30, bx - 20, (hy + by) / 2 - 20, bx, by + 95); stroke_dev(cr, OUT, 4)
    cr.save(); cr.translate(bx, by); cr.rotate(0.06 * math.sin(t * 2))
    ellipse(cr, 0, 0, 80, 98); fs(cr, hexc(col), 7)
    cr.move_to(-10, 95); cr.line_to(10, 95); cr.line_to(0, 112); cr.close_path(); fs(cr, hexc(col), 5)
    ellipse(cr, -28, -36, 16, 28); cr.set_source_rgba(1, 1, 1, 0.5); cr.fill()
    cr.restore()

def emo_face(cr, x, y, mood, s):
    if s <= 0.01: return
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.arc(0, 0, 70, 0, 2 * math.pi); fs(cr, hexc('#FFD93B'), 7)
    for sx in (-1, 1):
        cr.arc(sx * 24, -14, 9 if mood != 'surprised' else 11, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill()
    if mood == 'happy': cr.arc(0, 4, 34, 0.2 * math.pi, 0.8 * math.pi); stroke_dev(cr, OUT, 7)
    elif mood == 'sad': cr.arc(0, 50, 30, 1.25 * math.pi, 1.75 * math.pi); stroke_dev(cr, OUT, 7)
    else: ellipse(cr, 0, 28, 14, 18); fs(cr, hexc('#C0392B'), 5)
    cr.restore()

def count_bubble(cr, t0, t):
    u = (t - t0) / 3.0
    if not (0 <= u < 1): return
    n = 3 - min(2, int(u * 3)); ph = (u * 3) % 1; s = 1 + 0.25 * max(0, 1 - ph * 5)
    a = smooth(t0, t0 + 0.2, t) * (1 - smooth(t0 + 2.8, t0 + 3.0, t))
    cr.push_group()
    rrect(cr, 300, 470, 480, 150, 75); fs(cr, (1, 1, 1), 7, hexc('#3B2A6B'))
    cr.arc(390, 545, 52 * s, 0, 2 * math.pi); fs(cr, hexc('#FFD93B'), 6, hexc('#3B2A6B'))
    clean_text(cr, str(n), 390, 541, 70 * s, hexc('#FF4D4D'), 3)
    clean_text(cr, "Say it!", 590, 545, 66, hexc('#3B2A6B'), 0.1, (1, 1, 1))
    cr.pop_group_to_source(); cr.paint_with_alpha(a)

def chick(cr, x, by, h, sc, st, t, look, sx=1, sy=1):
    cr.save(); cr.translate(x, by - h); cr.scale(sc * sx, sc * sy)
    draw_body(cr, 0, -215, 1.0, st, t, look); shell_part(cr, top=False); cr.restore()

def frame(cr, t):
    m = TL['marks']
    scenery(cr, t)
    # mood
    mood = 'happy'
    if m['slip'] + 0.5 <= t < m['give'] + 0.6: mood = 'sad'
    if m['lift'] + 0.3 <= t < m['again']: mood = 'surprised'
    # frog position (lifts off)
    fx, fby = 720, 1470
    lift = 0
    if t >= m['lift']: lift = ease_io(clamp((t - m["lift"]) / 2.5)) * 330 + 20 * math.sin(t * 2)
    if t >= m['again']: lift = lerp(lift, 0, smooth(m['again'], m['again'] + 0.6, t))
    if t >= m['loop']: lift = 0
    fy = fby - 110 - lift
    fsway = 0.06 * math.sin(t * 2.2) if lift > 30 else 0
    if lift < 30:
        ellipse(cr, fx, fby + 4, 100, 16); cr.set_source_rgba(0, 0, 0, 0.22); cr.fill()
    # red balloon: on string until slip, then flies away
    hand_f = (fx - 120, fy + 30)
    if t < m['slip'] or t >= m['loop'] - 0.4:
        a = 1 if t < m['slip'] else smooth(m['loop'] - 0.4, m['loop'], t)
        cr.push_group(); balloon_at(cr, fx - 160, fy - 360 + 10 * math.sin(t * 2), *hand_f, '#FF4D4D', t); cr.pop_group_to_source(); cr.paint_with_alpha(a)
    elif t < m['slip'] + 3:
        u = t - m['slip']
        bx = fx - 160 + 80 * u + 30 * math.sin(u * 3); by = fy - 360 - 420 * u
        balloon_at(cr, bx, by, bx + 10 * math.sin(u * 5), by + 260, '#FF4D4D', t)
    # blue balloon: with chick, then to frog
    cx, cby = 300, 1500
    gu = clamp((t - m['give']) / 1.2) if t >= m['give'] else 0
    if t < m['give']:
        hand = (cx + 70, cby - 160); balloon_at(cr, cx + 140, cby - 560 + 10 * math.sin(t * 2), *hand, '#2EA7FF', t)
    elif t < m['loop'] - 0.3:
        e = ease_io(gu)
        bx = lerp(cx + 140, fx - 140, e); by = lerp(cby - 560, fy - 360, e) - 120 * math.sin(math.pi * e)
        hx, hy = lerp(cx + 70, hand_f[0], e), lerp(cby - 160, hand_f[1], e)
        balloon_at(cr, bx, by + 10 * math.sin(t * 2) - (lift * 0 if True else 0), hx, hy, '#2EA7FF', t)
    frog(cr, fx, fy, 0.72, mood, t, fsway, 0.3 * math.sin(t * 6) if lift > 30 else 0)
    # chick
    st = dict(wing=[0.0, 0.0], beak=0.0, happy=0, mood=0.0); hh = 0; sxx = syy = 1
    look = (0.9, -0.3)
    for e in TL['events']:
        if e['chick'] and e['t'] <= t < e['t'] + e['dur']: st['beak'] = 0.5 * abs(math.sin(t * 14)); st['happy'] = 1
    if m['slip'] + 0.5 <= t < m['give']: st['mood'] = 0.6
    if t < m['give']: st['wing'] = [0.0, 0.9]
    if m['r2'] + 0.05 <= t < m['r2'] + 0.95:
        r = m['r2'] + 0.05; kk = int((t - r) / 0.45); _, hh, sxx, syy, _, air = hop(t, r + 0.45 * kk, 0.45, 70, 0, 0)
        st.update(happy=1, wing=[0.4 + 0.8 * air] * 2, beak=0.6 * air)
    ccx = cx; ccb = cby
    if t >= m['r3'] + 0.6 and t < m['again'] + 0.6:
        u = clamp((t - m['r3'] - 0.6) / 1.2)
        ccx = lerp(cx, fx - 40, ease_io(u)); ccb = lerp(cby, fy + 300, ease_io(u)) - 100 * math.sin(math.pi * u)
        st.update(happy=1, wing=[1.2, 1.2], beak=0.5)
        look = (0.3, -0.9)
    if t >= m['again']:
        u = smooth(m['again'], m['again'] + 0.6, t); ccx = lerp(ccx, cx, u); ccb = lerp(ccb, cby, u)
    if abs(ccb - cby) < 5:
        ellipse(cr, ccx, ccb + 3, 85, 14); cr.set_source_rgba(0, 0, 0, 0.22); cr.fill()
    chick(cr, ccx, ccb, hh, 0.68, st, t, look, sxx, syy)
    for i, (x, y, c, s) in enumerate(FLW): draw_flower(cr, x, y, s, hexc(c), t, i)
    # countdown + labels
    for k in ('c1', 'c2', 'c3'): count_bubble(cr, m[k], t)
    labs = [('r1', 'Sad', 'sad', '#2EA7FF', m['give'] - 0.6), ('r2', 'Happy', 'happy', '#FF9A1F', m['lift'] + 0.6), ('r3', 'Surprised!', 'surprised', '#A15CFF', m['again'])]
    for k, lab, md, col, t1 in labs:
        r = m[k]
        if r <= t < t1 + 0.3:
            e = ease_out_back((t - r) / 0.4); a = 1 - smooth(t1, t1 + 0.3, t)
            cr.push_group(); emo_face(cr, 540, 420, md, e); cr.pop_group_to_source(); cr.paint_with_alpha(a)
            big_word(cr, lab, 540, 590, 130, hexc(col), e, 0.03 * math.sin(t * 3), a)
    # question hint (floating "?" over frog during counts)
    for k in ('c1', 'c2', 'c3'):
        a = smooth(m[k], m[k] + 0.2, t) * (1 - smooth(m[k] + 2.8, m[k] + 3.0, t))
        if a > 0: big_word(cr, "?", fx + 140, fy - 150 + 10 * math.sin(t * 5), 130, hexc('#FFD93B'), a, 0.15 * math.sin(t * 4))
    draw_text(cr, "How Does Frog Feel?", 250, 116, t, -1)

if __name__ == '__main__':
    if sys.argv[1] == 'build': tl = build(); print(tl['dur'], tl['marks'])
