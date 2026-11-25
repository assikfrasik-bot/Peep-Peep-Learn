import sys, math, json, random, os
sys.path.insert(0, '/home/claude/kit')
from kit import *
import cairo
from anim import (hexc, lerp, clamp, ease_io, ease_out_back, smooth, mixc, ellipse, fs, stroke_dev, draw_body, shell_part,
                  star, draw_text, hop, burst, draw_snail, OUT, W, H)
from anim2 import obj_frog, big_word, glow
from anim3 import bfly_c, rrect, clean_text, star5

F = '/home/claude/ep1'
SCR = (200, 620, 680, 680)  # screen x,y,w,h

def build():
    s = Script(F); t = 0.15
    t = s.say(t, 'hook', "Who's that shadow?") + 0.1
    t = s.say(t, 'say', "Say it out loud!") + 0.1
    s.mark('c1', t); t += 3.5; s.mark('r1', t)
    t = s.say(t + 0.1, 'a1', "A butterfly! Flutter, flutter!") + 0.4
    s.mark('s2', t)
    t = s.say(t + 0.4, 'q2', "Who's this? It goes hop, hop, hop!") + 0.1
    s.mark('c2', t); t += 3.5; s.mark('r2', t)
    t = s.say(t + 0.1, 'a2', "A frog! Ribbit, ribbit!") + 0.4
    s.mark('s3', t)
    t = s.say(t + 0.6, 'q3', "Uh-oh... who's THAT?", 0.85) + 0.1
    s.mark('c3', t); t += 3.5; s.mark('r3', t)
    t = s.say(t + 0.2, 'a3', "It's just a tiny snail! Hello, snail!") + 0.15
    t = s.say(t, 'laugh', "Hee hee! Silly snail!", 1.0, True) + 0.3
    s.mark('again', t)
    t = s.say(t, 'again', "Again?", 1.0, True) + 0.2
    s.mark('loop', t); t += 1.4
    tl = s.save(t)
    m = tl['marks']; mx = Mix(tl['dur'])
    mx.music_loop(0, m['s3'], 104, [([60, 64, 67], 36), ([57, 60, 64], 45), ([65, 69, 72], 41), ([67, 71, 74], 43)],
                  [[72, None, 76, None, 79, None, None, None], [76, None, 72, None, 69, None, None, None]], 'soft', 1.0)
    mx.music_loop(m['s3'], m['r3'], 80, [([57, 60, 63], 45), ([56, 60, 63], 44)], None, 'soft', 0.9)
    mx.music_loop(m['r3'], tl['dur'], 112, [([60, 64, 67], 36), ([65, 69, 72], 41), ([67, 71, 74], 43), ([60, 64, 67], 36)],
                  [[79, None, 76, 79, 84, None, None, None]], 'bouncy', 0.9)
    for k in ('c1', 'c2', 'c3'):
        for j in range(3): mx.add('sfx', m[k] + j * 1.1 + 0.2, tick(1100 if j < 2 else 1500), 0.35)
    for k in ('r1', 'r2'):
        mx.add('sfx', m[k], whoosh(0.4), 0.3); mx.add('sfx', m[k] + 0.1, ding(), 0.25); mx.add('sfx', m[k] + 0.2, chirp(), 0.2)
    for j in range(3): mx.add('sfx', m['s2'] + 0.5 + j * 0.45, boing(), 0.2)
    mx.add('sfx', m['s3'] + 0.3, rumble(1.6), 0.25)
    mx.add('sfx', m['r3'], slide_whistle(400, 1400, 0.5), 0.25); mx.add('sfx', m['r3'] + 0.45, pop(500, 1200, 0.1), 0.4)
    mx.add('sfx', m['r3'] + 0.5, tada(72), 0.25)
    mx.add('sfx', m['again'], chirp(), 0.25); mx.add('sfx', m['loop'] - 0.2, whoosh(0.5), 0.2)
    mx.voices(F, tl['events'])
    mx.write(F + '/audio.wav', quiet=[(m['c1'], m['r1']), (m['c2'], m['r2']), (m['c3'], m['r3'])])
    return tl

TL = json.load(open(F + '/timeline.json')) if os.path.exists(F + '/timeline.json') else None
rr = random.Random(4)
STARS = [(rr.uniform(0, 1080), rr.uniform(60, 560), rr.uniform(4, 10), rr.uniform(0, 6)) for _ in range(60)]
BULB_C = ['#FF5A5F', '#FFD93B', '#3ECF5E', '#2EA7FF', '#FF7EB6', '#A66CFF']

def bg(cr, t, light):
    g = cairo.LinearGradient(0, 0, 0, 1500)
    g.add_color_stop_rgb(0, *hexc('#15123F')); g.add_color_stop_rgb(1, *hexc('#3E2F86'))
    cr.set_source(g); cr.paint()
    for x, y, r, ph in STARS:
        k = 0.5 + 0.5 * math.sin(t * 2 + ph); star(cr, x, y, r * (0.6 + 0.4 * k)); cr.set_source_rgba(1, 1, 0.85, 0.4 + 0.5 * k); cr.fill()
    glow(cr, 930, 390, 130, (1, 1, 0.85), 0.25)
    cr.arc(930, 390, 52, 0, 2 * math.pi); cr.set_source_rgb(*hexc('#FFF4C2')); cr.fill()
    cr.arc(952, 378, 48, 0, 2 * math.pi); cr.set_source_rgb(*hexc('#1E1950')); cr.fill()
    # string lights
    for row, (y0, sag) in enumerate(((470, 70), (520, 50))):
        pts = [(x, y0 + sag * math.sin(math.pi * x / 1080) + 4 * math.sin(t * 1.5 + row)) for x in range(-20, 1101, 20)]
        cr.move_to(*pts[0])
        for p in pts[1:]: cr.line_to(*p)
        stroke_dev(cr, hexc('#2A2050'), 4)
        for j, x in enumerate(range(40, 1080, 90)):
            xx = x + 45 * row; y = y0 + sag * math.sin(math.pi * xx / 1080) + 4 * math.sin(t * 1.5 + row) + 14
            c = hexc(BULB_C[(j + row) % 6]); on = 0.6 + 0.4 * math.sin(t * 3 + j * 1.3 + row)
            glow(cr, xx, y, 40, c, 0.45 * on); ellipse(cr, xx, y, 10, 14); cr.set_source_rgb(*mixc(c, (1, 1, 1), 0.3 * on)); cr.fill()
    # ground
    cr.move_to(0, H)
    for x in range(0, W + 21, 20): cr.line_to(x, 1480 + 30 * math.sin(x / 300))
    cr.line_to(W, H); cr.close_path(); cr.set_source_rgb(*hexc('#1F4A3A')); cr.fill()
    glow(cr, 540, 1500, 600, (1, 0.85, 0.5), 0.18 * light)

def theater(cr, t, light):
    x, y, w, h = SCR
    for lx in (230, 850):
        cr.rectangle(lx - 16, y + h, 32, 240); fs(cr, hexc('#7A4A2A'))
    rrect(cr, x - 50, y - 60, w + 100, h + 110, 24); fs(cr, hexc('#9B6236'), 8)
    rrect(cr, x - 30, y - 40, w + 60, h + 70, 16); cr.set_source_rgb(*hexc('#7A4A2A')); cr.fill()
    g = cairo.RadialGradient(540, 980, 40, 540, 960, 520)
    g.add_color_stop_rgb(0, *mixc(hexc('#FFF6D6'), (1, 1, 1), 0.3 * light)); g.add_color_stop_rgb(1, *hexc('#F2B95A'))
    cr.rectangle(x, y, w, h); cr.set_source(g); cr.fill()

def curtains(cr):
    x, y, w, h = SCR
    for side in (-1, 1):
        cr.save()
        if side == 1: cr.translate(1080, 0); cr.scale(-1, 1)
        cr.move_to(x - 4, y - 4); cr.line_to(x + 150, y - 4); cr.curve_to(x + 90, y + 80, x + 40, y + 160, x - 4, y + 230); cr.close_path()
        cg = cairo.LinearGradient(x, 0, x + 150, 0)
        for j in range(5): cg.add_color_stop_rgb(j / 4, *(hexc('#D6203C') if j % 2 == 0 else hexc('#9C1029')))
        cr.set_source(cg); cr.fill_preserve(); stroke_dev(cr, hexc('#5C0716'), 4)
        cr.restore()
    cr.move_to(x - 30, y - 40); cr.line_to(x + w + 30, y - 40); cr.line_to(x + w + 30, y + 10)
    for j in range(8, -1, -1):
        xx = x - 30 + j * (w + 60) / 9; cr.curve_to(xx + 50, y + 50, xx + 20, y + 50, xx, y + 10)
    cr.close_path(); cr.set_source_rgb(*hexc('#C8183A')); cr.fill_preserve(); stroke_dev(cr, hexc('#FFC93B'), 5)

def shadow_of(cr, draw_fn, a=0.92):
    x, y, w, h = SCR
    cr.save(); cr.rectangle(x, y, w, h); cr.clip()
    cr.push_group(); draw_fn(cr); pat = cr.pop_group()
    cr.set_source_rgba(0.24, 0.1, 0.22, a); cr.mask(pat)
    cr.restore()

def chick(cr, x, by, h, sc, st, t, look, sx=1, sy=1):
    cr.save(); cr.translate(x, by - h); cr.scale(sc * sx, sc * sy)
    draw_body(cr, 0, -215, 1.0, st, t, look)
    cr.save(); cr.translate(10, -320); cr.rotate(0.25)
    cr.move_to(-90, 10); cr.curve_to(-60, -60, 40, -120, 120, -60 + 8 * math.sin(t * 3)); cr.curve_to(60, -40, 80, 0, 90, 10); cr.close_path()
    fs(cr, hexc('#5B7CFA'))
    for k in range(4): star5(cr, -40 + k * 35, -20 - k * 15, 9); cr.set_source_rgb(1, 1, 0.8); cr.fill()
    cr.arc(122, -58 + 8 * math.sin(t * 3), 22, 0, 2 * math.pi); fs(cr, (1, 1, 1), 5)
    ellipse(cr, 0, 12, 98, 18); fs(cr, (1, 1, 1), 5)
    cr.restore()
    shell_part(cr, top=False); cr.restore()

def bubble_count(cr, t0, t, label="Say it!"):
    u = (t - t0) / 3.5
    if not (0 <= u < 1): return
    n = 3 - min(2, int(u * 3)); ph = (u * 3) % 1; s = 1 + 0.25 * max(0, 1 - ph * 5)
    a = smooth(t0, t0 + 0.2, t) * (1 - smooth(t0 + 3.3, t0 + 3.5, t))
    cr.push_group()
    cr.arc(640, 1440, 62 * s, 0, 2 * math.pi); fs(cr, (1, 1, 1), 7, hexc('#3B2A6B'))
    clean_text(cr, str(n), 640, 1436, 80 * s, hexc('#FF4D4D'), 3)
    clean_text(cr, label, 820, 1440, 60, (1, 1, 1), 9)
    cr.pop_group_to_source(); cr.paint_with_alpha(a)

def frame(cr, t):
    m = TL['marks']; dur = TL['dur']
    light = burst(m['r1'] - 0.05, m['r1'] + 0.6, t) + burst(m['r2'] - 0.05, m['r2'] + 0.6, t) + burst(m['r3'] - 0.05, m['r3'] + 0.6, t)
    flick_ = 1.0
    if m['s3'] <= t < m['c3'] + 0.5: flick_ = 0.75 + 0.25 * (math.sin(t * 23) > -0.3)
    bg(cr, t, light); theater(cr, t, light * flick_)
    if flick_ < 1: cr.rectangle(*SCR); cr.set_source_rgba(0.1, 0.05, 0.15, 1 - flick_); cr.fill()
    sx0, sy0 = 540, 960
    # --- shadows
    if t < m['r1'] + 0.15 or t >= m['loop'] - 0.6:
        a = 1 - smooth(m['r1'], m['r1'] + 0.15, t) if t < m['loop'] - 0.6 else smooth(m['loop'] - 0.6, m['loop'], t)
        bx = sx0 + 110 * math.sin(t * 1.1); by = sy0 - 30 + 60 * math.sin(t * 1.9)
        shadow_of(cr, lambda c: (c.save(), c.translate(bx, by), c.scale(1.35, 1.35), c.rotate(0.15 * math.sin(t * 2)), bfly_c(c, t + 0.22, '#000000', '#000000'), c.restore()), 0.92 * a)
    if m['s2'] <= t < m['r2'] + 0.15:
        a = smooth(m['s2'], m['s2'] + 0.2, t) * (1 - smooth(m['r2'], m['r2'] + 0.15, t))
        u = t - m['s2'] - 0.5
        if u < 1.35:
            k = int(max(0, u) / 0.45); x0 = 860 - k * 110; _, hh, sx, sy, _, _ = hop(max(0, u), k * 0.45, 0.45, 120, 0, 0) if u > 0 else (0, 0, 1, 1, 0, 0)
            fx = lerp(x0, x0 - 110, clamp((max(0, u) - k * 0.45) / 0.45)) if u > 0 else 900
        else:
            fx = 530; hh = 18 * abs(math.sin(t * 3)); sx = sy = 1
        shadow_of(cr, lambda c: (c.save(), c.translate(fx, 1120 - hh), c.scale(1.6 * sx, 1.6 * sy), obj_frog(c, 1), c.restore()), 0.92 * a)
    if m['s3'] + 0.4 <= t < m['r3'] + 0.2:
        a = smooth(m['s3'] + 0.4, m['s3'] + 1.2, t) * (1 - smooth(m['r3'], m['r3'] + 0.2, t))
        g = lerp(1.6, 4.3, ease_io((t - m['s3'] - 0.4) / 1.6))
        wob = 0.04 * math.sin(t * 5)
        def mon(c):
            c.save(); c.translate(560, 1080); c.rotate(wob); c.scale(g, g); draw_snail(c, 0, 40, t); c.restore()
        shadow_of(cr, mon, 0.95 * a)
        if a > 0.5:
            for ex in (-76, -48):
                glow(cr, 560 + ex * g * 1.0, 1080 + (40 - 70) * g, 26, (1, 0.95, 0.6), 0.9 * a)
    curtains(cr)
    # --- reveals (colored characters)
    if m['r1'] <= t < m['s2'] + 0.6:
        u = t - m['r1']; e = ease_io(u / 0.9)
        x = lerp(820, 860, e) + 30 * math.sin(t * 2); y = lerp(1000, 520, e) + 25 * math.sin(t * 3)
        a = 1 - smooth(m['s2'] + 0.2, m['s2'] + 0.6, t)
        if a > 0:
            cr.push_group(); cr.translate(x, y); cr.scale(0.7, 0.7); bfly_c(cr, t, '#FF7EB6', '#B57BFF'); cr.pop_group_to_source(); cr.paint_with_alpha(a)
    if m['r2'] <= t < m['s3'] + 0.5:
        u = t - m['r2']; kk = min(2, int(u / 0.45))
        _, hh, sx, sy, _, _ = hop(u, kk * 0.45, 0.45, 110, 0, 0) if u < 1.35 else (0, 0, 1, 1, 0, 0)
        fx = lerp(760, 930, clamp(u / 1.35)); a = 1 - smooth(m['s3'], m['s3'] + 0.5, t)
        cr.push_group(); cr.translate(fx, 1420 - hh); cr.scale(0.55 * sx, 0.55 * sy); obj_frog(cr, 1); cr.pop_group_to_source(); cr.paint_with_alpha(a)
    if t >= m['r3']:
        u = t - m['r3']; e = ease_out_back(u / 0.6); a = 1 - smooth(m['loop'] - 0.4, m['loop'], t)
        sx_ = 560; sy_ = lerp(1330, 1290, e)
        cr.push_group()
        cr.move_to(sx_ - 40, sy_ - 20); cr.line_to(sx_ - 240, sy_ - 420); cr.line_to(sx_ + 60, sy_ - 440); cr.close_path()
        cr.set_source_rgba(1, 1, 0.8, 0.25); cr.fill()
        cr.save(); cr.translate(sx_, sy_); cr.scale(e * 1.45, e * 1.45); draw_snail(cr, 0, 0, t)
        cr.save(); cr.translate(-80, -30); cr.rotate(-0.9); rrect(cr, -12, -40, 24, 50, 6); fs(cr, hexc('#2EA7FF'), 4); cr.restore()
        cr.restore()
        cr.pop_group_to_source(); cr.paint_with_alpha(a)
    # --- labels & countdown
    for k, lab, col in (('r1', 'Butterfly!', '#FF7EB6'), ('r2', 'Frog!', '#3ECF5E'), ('r3', 'A tiny snail!', '#FF9A1F')):
        r = m[k]; nxt = {'r1': m['s2'], 'r2': m['s3'], 'r3': m['again']}[k]
        if r + 0.15 <= t < nxt + 0.3:
            big_word(cr, lab, 610, 1600, 115, hexc(col), ease_out_back((t - r - 0.15) / 0.4), 0.03 * math.sin(t * 3), 1 - smooth(nxt, nxt + 0.3, t))
    for k in ('c1', 'c2', 'c3'): bubble_count(cr, m[k], t)
    # --- chick
    st = dict(wing=[0.0, 0.0], beak=0.0, happy=0, mood=0.0); hh = 0; sx = sy = 1
    look = (0.8, -0.6)
    for e in TL['events']:
        if e['chick'] and e['t'] <= t < e['t'] + e['dur']: st['beak'] = 0.5 * abs(math.sin(t * 14)); st['happy'] = 1
    if m['s3'] + 0.4 <= t < m['r3']:
        st.update(wing=[1.1, 1.1], beak=0.9, mood=0.6); look = (0.6, -0.8)
    for k in ('r1', 'r2', 'r3'):
        r = m[k] + 0.1
        if r <= t < r + 0.9:
            kk = int((t - r) / 0.45); _, hh, sx, sy, _, air = hop(t, r + 0.45 * kk, 0.45, 70, 0, 0)
            st.update(happy=1, wing=[0.4 + 0.8 * air] * 2, beak=0.6 * air, mood=0)
    if m['again'] <= t < m['loop']: st.update(wing=[0.2, 1.2 + 0.3 * math.sin(t * 10)], happy=0); look = (0.2, 0.3)
    ellipse(cr, 150, 1652, 80, 14); cr.set_source_rgba(0, 0, 0, 0.3); cr.fill()
    chick(cr, 150, 1650, hh, 0.72, st, t, look, sx, sy)
    vg = cairo.RadialGradient(540, 960, 700, 540, 960, 1300)
    vg.add_color_stop_rgba(0, 0, 0, 0, 0); vg.add_color_stop_rgba(1, 0, 0, 0.1, 0.3); cr.set_source(vg); cr.paint()
    draw_text(cr, "Who's That Shadow?", 250, 118, t, -1)

if __name__ == '__main__':
    if sys.argv[1] == 'build': tl = build(); print(tl['dur'], tl['marks'])
