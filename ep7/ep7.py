import sys, math, json, random, os
sys.path.insert(0, '/home/claude/kit')
from kit import *
import cairo
from anim import (hexc, lerp, clamp, ease_io, ease_out_back, smooth, mixc, ellipse, fs, stroke_dev, draw_body, shell_part,
                  star, draw_text, hop, burst, draw_snail, draw_egg, tree, OUT, W, H)
from anim2 import big_word, glow
from anim3 import rrect, clean_text, star5

F = '/home/claude/ep7'
L, R = 290, 790
ROUNDS = [dict(kind='balloon', q="Which balloon is BIG?", a="This one! This balloon is big!", ans=1, word='BIG'),
          dict(kind='snail', q="Which snail is little?", a="This one! This snail is little!", ans=1, word='little'),
          dict(kind='tree', q="Which tree is TALL?", a="This one! This tree is tall!", ans=0, word='TALL'),
          dict(kind='egg', q="Which egg is BIG?", a="This one! The big egg!", ans=0, word='BIG')]

def build():
    s = Script(F); t = 0.1
    t = s.say(t, 'hook', "Big or little? Point to it!") + 0.15
    for i, r in enumerate(ROUNDS):
        s.mark(f's{i}', t - 0.15 if i else 0.0)
        t = s.say(t + (0.3 if i else 0), f'q{i}', r['q']) + 0.1
        s.mark(f'c{i}', t); t += 3.0; s.mark(f'r{i}', t)
        t = s.say(t + 0.05, f'a{i}', r['a']) + 0.4
    s.mark('hatch', t); t += 1.6
    t = s.say(t, 'hi', "Hi there!", 1.1, True, 'am_puck') + 0.1
    t = s.say(t, 'tw', "A big egg... and a tiny snail! Silly!") + 0.1
    t = s.say(t, 'laugh', "Hee hee!", 1.0, True) + 0.2
    s.mark('again', t); t = s.say(t, 'again', "Again?", 1.0, True) + 0.2
    s.mark('loop', t); t += 1.2
    tl = s.save(t); m = tl['marks']; mx = Mix(tl['dur'])
    mx.music_loop(0, tl['dur'], 116, [([60, 64, 67], 36), ([62, 65, 69], 38), ([67, 71, 74], 43), ([60, 64, 67], 36)],
                  [[72, None, 79, None, 72, None, 79, None], [74, None, 77, None, 79, None, None, None]], 'bouncy', 0.85)
    for i in range(4):
        if i: mx.add('sfx', m[f's{i}'], whoosh(0.5), 0.3)
        for j in range(3): mx.add('sfx', m[f'c{i}'] + j, tick(1100 if j < 2 else 1500), 0.33)
        big = ROUNDS[i]['word'] in ('BIG', 'TALL')
        mx.add('sfx', m[f'r{i}'], slide_whistle(400, 1300, 0.45) if big else slide_whistle(1300, 900, 0.3), 0.25)
        mx.add('sfx', m[f'r{i}'] + 0.3, ding(), 0.2)
    for k in range(3): mx.add('sfx', m['hatch'] + k * 0.35, bp(rng.standard_normal(int(0.1 * SR)), 1500, 7000) * np.exp(-tt(0.1) / 0.03), 0.4)
    mx.add('sfx', m['hatch'] + 1.1, pop(300, 900, 0.14), 0.45); mx.add('sfx', m['hatch'] + 1.2, tada(72), 0.18)
    mx.add('sfx', m['again'] + 0.2, jingle(), 0.22)
    mx.voices(F, tl['events'])
    mx.write(F + '/audio.wav', quiet=[(m[f'c{i}'], m[f'r{i}']) for i in range(4)]); return tl

TL = json.load(open(F + '/timeline.json')) if os.path.exists(F + '/timeline.json') else None

def balloon(cr, x, y, sc, col, t):
    cr.save(); cr.translate(x, y + 8 * math.sin(t * 2 + x)); cr.scale(sc, sc)
    cr.move_to(0, 95); cr.curve_to(-20, 160, 20, 230, -5, 330); stroke_dev(cr, OUT, 4)
    ellipse(cr, 0, 0, 80, 98); fs(cr, hexc(col), 7)
    cr.move_to(-10, 95); cr.line_to(10, 95); cr.line_to(0, 112); cr.close_path(); fs(cr, hexc(col), 5)
    ellipse(cr, -28, -36, 16, 28); cr.set_source_rgba(1, 1, 1, 0.5); cr.fill()
    cr.restore()

def item(cr, kind, side, t, m):
    x = L if side == 0 else R; base = 1330
    if kind == 'balloon':
        balloon(cr, x, 900, 0.75 if side == 0 else 1.9, '#FF4D4D' if side == 0 else '#2EA7FF', t)
    elif kind == 'snail':
        sc = 3.0 if side == 0 else 1.1
        cr.save(); cr.translate(x + 60 * (side == 0), base); cr.scale(sc, sc); draw_snail(cr, 0, 0, t); cr.restore()
    elif kind == 'tree':
        cr.save(); cr.translate(x, base + 10)
        if side == 0: cr.scale(1.0, 2.1)
        else: cr.scale(1.0, 0.9)
        tree(cr, 0, 0, 1.0, '#4CB944'); cr.restore()
    elif kind == 'egg':
        sc = 1.55 if side == 0 else 0.6
        h0 = m['hatch']
        if t < h0 or side == 1:
            wob = 0.08 * math.sin(t * 25) * burst(h0 - 0.1, h0 + 1.1, t) if side == 0 else 0
            cr.save(); cr.translate(x, base); cr.rotate(wob); cr.scale(sc, sc); draw_egg(cr, clamp((t - h0) / 1.0) if side == 0 else 0); cr.restore()
        else:
            u = t - h0
            if u < 1.1:
                cr.save(); cr.translate(x, base); cr.rotate(0.08 * math.sin(t * 25)); cr.scale(sc, sc); draw_egg(cr, clamp(u / 1.0)); cr.restore()
            else:
                v = u - 1.1
                cr.save(); cr.translate(x, base); cr.scale(sc, sc); shell_part(cr, top=False); cr.restore()
                if v < 1.0:
                    cr.save(); cr.translate(x + 300 * v, base - 300 * sc - 500 * v + 600 * v * v); cr.rotate(5 * v); cr.scale(sc, sc)
                    cr.translate(0, 165); shell_part(cr, top=True); cr.restore()
                e = ease_out_back(v / 0.5)
                cr.save(); cr.translate(x - 10, base - 230 * sc + 20); cr.scale(e * 0.9, e * 0.9); draw_snail(cr, 0, 0, t); cr.restore()

def scene(cr, t):
    for side, col, col2 in ((0, '#FFD0E2', '#FFB3CF'), (1, '#CDE9FF', '#A9D8FF')):
        x0 = 0 if side == 0 else 540
        g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *hexc(col)); g.add_color_stop_rgb(1, *hexc(col2))
        cr.rectangle(x0, 0, 540, H); cr.set_source(g); cr.fill()
        for k in range(8):
            yy = (k * 260 + t * 30) % 2100 - 100; xx = x0 + 60 + (k * 137) % 420
            star5(cr, xx, yy, 14); cr.set_source_rgba(1, 1, 1, 0.5); cr.fill()
    cr.move_to(540, 380); cr.line_to(540, 1350)
    cr.save(); cr.set_dash([24, 18]); stroke_dev(cr, (1, 1, 1), 8, 0.9); cr.restore()
    rrect(cr, 60, 1330, 960, 50, 25); fs(cr, hexc('#7AD36A'), 6)

def count_bubble(cr, t0, t):
    u = (t - t0) / 3.0
    if not (0 <= u < 1): return
    n = 3 - min(2, int(u * 3)); ph = (u * 3) % 1; s = 1 + 0.25 * max(0, 1 - ph * 5)
    a = smooth(t0, t0 + 0.2, t) * (1 - smooth(t0 + 2.8, t0 + 3.0, t))
    cr.push_group()
    rrect(cr, 280, 1385, 520, 140, 70); fs(cr, (1, 1, 1), 7, hexc('#3B2A6B'))
    cr.arc(365, 1455, 50 * s, 0, 2 * math.pi); fs(cr, hexc('#FFD93B'), 6, hexc('#3B2A6B'))
    clean_text(cr, str(n), 365, 1451, 68 * s, hexc('#FF4D4D'), 3)
    clean_text(cr, "Point to it!", 590, 1455, 58, hexc('#3B2A6B'), 0.1, (1, 1, 1))
    cr.pop_group_to_source(); cr.paint_with_alpha(a)

def chick(cr, x, by, h, sc, st, t, look, sx=1, sy=1):
    cr.save(); cr.translate(x, by - h); cr.scale(sc * sx, sc * sy)
    draw_body(cr, 0, -215, 1.0, st, t, look); shell_part(cr, top=False); cr.restore()

def frame(cr, t):
    m = TL['marks']
    scene(cr, t)
    ri = 0
    for i in range(1, 4):
        if t >= m[f's{i}']: ri = i
    r = ROUNDS[ri]
    # transition: slide out old, slide in new
    sw = 0
    if ri > 0 and t < m[f's{ri}'] + 0.5: sw = 1 - ease_io((t - m[f's{ri}']) / 0.5)
    hl = smooth(m[f'r{ri}'], m[f'r{ri}'] + 0.3, t)
    for side in (0, 1):
        is_ans = side == r['ans']
        grow = 1 + (0.06 * hl + 0.06 * burst(m[f'r{ri}'], m[f'r{ri}'] + 0.4, t) if is_ans else 0)
        dim = 0 if is_ans else 0.5 * hl
        if r['kind'] == 'egg' and t >= m['hatch']: dim = 0; grow = 1
        cx = L if side == 0 else R
        HC = dict(balloon=(900, 240, 1.35), snail=(1270, 120, 0.8), tree=(1000, 240, 1.35), egg=(1080, 240, 1.2))[r['kind']]
        if is_ans and hl > 0 and not (r['kind'] == 'egg' and t >= m['hatch']): glow(cr, cx, HC[0], HC[1] * 1.5, (1, 1, 0.7), 0.6 * hl)
        cr.push_group()
        cr.translate(0, sw * 1600); cr.translate(cx, 1330); cr.scale(grow, grow); cr.translate(-cx, -1330)
        item(cr, r['kind'], side, t, m)
        cr.pop_group_to_source(); cr.paint_with_alpha(1 - dim)
        if is_ans and hl > 0 and not (r['kind'] == 'egg' and t >= m['hatch']):
            pr = smooth(m[f'r{ri}'] + 0.1, m[f'r{ri}'] + 0.5, t)
            cr.save(); cr.translate(cx, HC[0]); cr.scale(1, HC[2]); cr.arc(0, 0, HC[1], -2.2, -2.2 + 2.15 * math.pi * pr); cr.restore()
            stroke_dev(cr, hexc('#FF3B3B'), 12)
    # word
    rr0 = m[f'r{ri}']; nxt = m[f's{ri + 1}'] if ri < 3 else m['hatch']
    if rr0 <= t < nxt + 0.2:
        word = r['word']; big = word in ('BIG', 'TALL')
        e = ease_out_back((t - rr0) / 0.45); a = 1 - smooth(nxt - 0.1, nxt + 0.2, t)
        cx = L if r['ans'] == 0 else R
        if big: big_word(cr, word, cx, 470, 200, hexc('#FF4D4D'), e, 0.04 * math.sin(t * 3), a)
        else: big_word(cr, word, cx, 520, 80, hexc('#2EA7FF'), e, 0.04 * math.sin(t * 3), a)
    if m['hatch'] + 1.4 <= t < m['again'] + 0.3:
        a = 1 - smooth(m['again'], m['again'] + 0.3, t)
        big_word(cr, "Silly!", 540, 500, 150, hexc('#A15CFF'), ease_out_back((t - m['hatch'] - 1.4) / 0.4), 0.05 * math.sin(t * 3), a)
    count_bubble(cr, m[f'c{ri}'], t)
    # chick in the middle pointing
    st = dict(wing=[0.0, 0.0], beak=0.0, happy=0, mood=0.0); hh = 0; sxx = syy = 1
    look = (0.0, -0.4)
    for e in TL['events']:
        if e['chick'] and e['t'] <= t < e['t'] + e['dur']: st['beak'] = 0.5 * abs(math.sin(t * 14)); st['happy'] = 1
    if m[f'c{ri}'] <= t < m[f'r{ri}']: look = (math.sin(t * 2.2), -0.3)
    if rr0 <= t < nxt:
        side = r['ans']; st['wing'] = [1.3, 0.0] if side == 0 else [0.0, 1.3]; look = (-0.9 if side == 0 else 0.9, -0.3)
        if t < rr0 + 0.9:
            kk = int((t - rr0) / 0.45); _, hh, sxx, syy, _, air = hop(t, rr0 + 0.45 * kk, 0.45, 50, 0, 0); st['happy'] = 1
    if m['hatch'] + 1.4 <= t < m['again']: st.update(happy=1, beak=0.5 * abs(math.sin(t * 10)), wing=[0.8, 0.8])
    chick(cr, 540, 1780, hh, 0.6, st, t, look, sxx, syy)
    draw_text(cr, "Big or Little?", 250, 130, t, -1)

if __name__ == '__main__':
    if sys.argv[1] == 'build': tl = build(); print(tl['dur'], tl['marks'])
