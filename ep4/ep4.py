import sys, math, json, random, os
sys.path.insert(0, '/home/claude/kit')
from kit import *
import cairo
from anim import (hexc, lerp, clamp, ease_io, ease_out_back, smooth, mixc, ellipse, fs, stroke_dev, draw_body, shell_part,
                  star, draw_text, hop, burst, draw_sun, draw_cloud, draw_flower, tree, OUT, W, H)
from anim2 import obj_apple, obj_banana, obj_frog, big_word, glow
from anim3 import rrect, clean_text, star5, item_chick

F = '/home/claude/ep4'
TRACK_Y = 1300
CARS = [330, 490, 650, 810, 970]
CAR_COL = ['#FFB3C7', '#B3E0FF', '#FFE59A', '#C8F2B0', '#E2C6FF']
ROUNDS = [dict(items=['apple', 'banana', 'apple', 'banana', 'apple'], read="Apple, banana, apple, banana...", ans="Apple! Apple, banana, apple!", lab='Apple!'),
          dict(items=['bred', 'bred', 'bblue', 'bred', 'bred'], read="Red, red, blue, red...", ans="Red! Red, red, blue!", lab='Red!'),
          dict(items=['chick', 'frog', 'chick', 'frog', 'me'], read="Chickpea, frog, Chickpea, frog...", ans=None, lab='Chickpea!')]

def build():
    s = Script(F); t = 0.1
    for i, r in enumerate(ROUNDS):
        if i > 0:
            s.mark(f'enter{i}', t); t += 1.6
        else:
            s.mark('enter0', -5)
        q = "What comes next?" if i < 2 else "What's next? Look carefully!"
        if i == 0: t = s.say(t, 'q0', q) + 0.15
        s.mark(f'read{i}', t); t = s.say(t, f'read{i}', r['read'], 0.88) + 0.1
        s.mark(f'readend{i}', t)
        if i > 0: t = s.say(t, f'q{i}', q) + 0.1
        else: t = s.say(t, 'sayit', "Say it out loud!", 1.0) + 0.1
        s.mark(f'c{i}', t); t += 3.0; s.mark(f'r{i}', t)
        if r['ans']: t = s.say(t + 0.05, f'a{i}', r['ans']) + 0.25
        else:
            t = s.say(t + 0.7, 'me', "Me! It's me!", 1.0, True) + 0.2
            t = s.say(t, 'a2', "Chickpea comes next! All aboard!") + 0.1
        s.mark(f'leave{i}', t); t += 1.2 if i < 2 else 0.4
    t = s.say(t, 'choo', "Choo choo!", 1.0, True) + 0.6
    s.mark('again', t); t = s.say(t, 'again', "Again?", 1.0, True) + 0.1
    s.mark('loop', t); t += 1.6
    tl = s.save(t); m = tl['marks']; mx = Mix(tl['dur'])
    mx.music_loop(0, tl['dur'], 118, [([60, 64, 67], 36), ([65, 69, 72], 41), ([67, 71, 74], 43), ([60, 64, 67], 36)],
                  [[72, 76, 79, 76, 72, None, 79, None], [74, 77, 81, 77, 74, None, None, None]], 'march', 0.9)
    def whistle(tt0):
        mx.add('sfx', tt0, (pad([79, 83, 86], 0.7) + 0.3 * bp(rng.standard_normal(int(0.7 * SR)), 1500, 4000)[:int(0.7 * SR)]) * 1.5, 0.25)
    def chug(tt0, d):
        k = 0
        while k * 0.22 < d: mx.add('sfx', tt0 + k * 0.22, bp(rng.standard_normal(int(0.1 * SR)), 300, 1500) * np.exp(-tt(0.1) / 0.03), 0.25); k += 1
    for i in range(3):
        if i > 0: whistle(m[f'enter{i}']); chug(m[f'enter{i}'], 1.5)
        for j in range(3): mx.add('sfx', m[f'c{i}'] + j, tick(1100 if j < 2 else 1500), 0.35)
        mx.add('sfx', m[f'r{i}'], pop(400, 1100, 0.12), 0.4); mx.add('sfx', m[f'r{i}'] + 0.05, ding(), 0.22)
        whistle(m[f'leave{i}']); chug(m[f'leave{i}'], 1.2)
        n = 4; rd = m[f'read{i}']; dur = m[f'readend{i}'] - rd
        for k in range(n): mx.add('sfx', rd + dur * (k + 0.3) / n, marimba(mtof(76 + 3 * k)), 0.25)
    mx.add('sfx', m['r2'] + 0.1, slide_whistle(500, 1500, 0.6), 0.25); mx.add('sfx', m['r2'] + 0.65, boing(), 0.3)
    mx.add('sfx', m['again'] + 0.2, jingle(), 0.22)
    mx.voices(F, tl['events'])
    mx.write(F + '/audio.wav', quiet=[(m[f'c{i}'], m[f'r{i}']) for i in range(3)]); return tl

TL = json.load(open(F + '/timeline.json')) if os.path.exists(F + '/timeline.json') else None
rr = random.Random(14)
FLW = [(rr.uniform(30, 1050), rr.uniform(1500, 1880), rr.choice(['#FF5A5F', '#FFFFFF', '#A66CFF', '#FFB400', '#FF7EB6']), rr.uniform(0.8, 1.1)) for _ in range(12)]

def balloon(cr, col):
    cr.move_to(0, 70); cr.curve_to(-20, 120, 20, 160, -5, 220); stroke_dev(cr, OUT, 4)
    ellipse(cr, 0, 0, 80, 98); fs(cr, hexc(col), 7)
    cr.move_to(-10, 95); cr.line_to(10, 95); cr.line_to(0, 112); cr.close_path(); fs(cr, hexc(col), 5)
    ellipse(cr, -28, -36, 16, 28); cr.set_source_rgba(1, 1, 1, 0.5); cr.fill()

def item(cr, name, t):
    if name == 'apple': cr.save(); cr.scale(0.8, 0.8); obj_apple(cr, 1); cr.restore()
    elif name == 'banana': cr.save(); cr.scale(0.85, 0.85); cr.rotate(-0.3); obj_banana(cr, 1); cr.restore()
    elif name == 'bred': cr.save(); cr.translate(0, -60); balloon(cr, '#FF4D4D'); cr.restore()
    elif name == 'bblue': cr.save(); cr.translate(0, -60); balloon(cr, '#2EA7FF'); cr.restore()
    elif name == 'chick': item_chick(cr, t)
    elif name == 'frog': cr.save(); cr.scale(0.85, 0.85); obj_frog(cr, 1); cr.restore()

def scenery(cr, t):
    g = cairo.LinearGradient(0, 0, 0, 1300); g.add_color_stop_rgb(0, *hexc('#55C2FF')); g.add_color_stop_rgb(1, *hexc('#DDF7FF'))
    cr.set_source(g); cr.paint()
    sc = 0.6; cr.save(); cr.translate(150 - 870 * sc, 420 - 270 * sc); cr.scale(sc, sc); draw_sun(cr, t); cr.restore()
    for i, (x, y, s) in enumerate(((600, 430, 0.5), (950, 600, 0.4), (300, 700, 0.35))):
        draw_cloud(cr, (x + t * 15 + 300) % 1500 - 300, y, s, (1, 1, 1), outline=False)
    cr.move_to(0, H)
    for x in range(0, W + 21, 20): cr.line_to(x, 1080 - 70 * math.sin(math.pi * x / 1080 * 1.6 + 0.4))
    cr.line_to(W, H); cr.close_path(); cr.set_source_rgb(*hexc('#A6E58A')); cr.fill()
    cr.rectangle(0, 1180, W, H - 1180)
    hg = cairo.LinearGradient(0, 1180, 0, H); hg.add_color_stop_rgb(0, *hexc('#6CCB52')); hg.add_color_stop_rgb(1, *hexc('#3E9E3A'))
    cr.set_source(hg); cr.fill()
    cr.rectangle(0, TRACK_Y + 8, W, 40); cr.set_source_rgb(*hexc('#B89870')); cr.fill()
    for x in range(-20, W + 40, 60):
        cr.rectangle(x, TRACK_Y + 10, 34, 34); cr.set_source_rgb(*hexc('#7A4A2A')); cr.fill()
    for y in (TRACK_Y + 14, TRACK_Y + 36):
        cr.move_to(0, y); cr.line_to(W, y); stroke_dev(cr, hexc('#6B7280'), 8)
    # platform
    rrect(cr, -40, 1560, 560, 60, 10); fs(cr, hexc('#C9B79C'), 6)
    cr.rectangle(-40, 1620, 560, 300); cr.set_source_rgb(*hexc('#A88F6E')); cr.fill()

def wheel(cr, x, y, r, ang):
    cr.arc(x, y, r, 0, 2 * math.pi); fs(cr, hexc('#3B3F4A'), 5)
    cr.arc(x, y, r * 0.45, 0, 2 * math.pi); cr.set_source_rgb(*hexc('#FFD93B')); cr.fill()
    cr.move_to(x + r * 0.8 * math.cos(ang), y + r * 0.8 * math.sin(ang)); cr.line_to(x - r * 0.8 * math.cos(ang), y - r * 0.8 * math.sin(ang))
    stroke_dev(cr, hexc('#FFD93B'), 5)

def loco(cr, x, t, ang, smoke_on):
    y = TRACK_Y
    rrect(cr, x + 120, y - 230, 120, 190, 14); fs(cr, hexc('#FF4D4D'), 7)
    rrect(cr, x + 140, y - 210, 80, 70, 10); fs(cr, hexc('#BFE6FF'), 5)
    rrect(cr, x + 105, y - 250, 150, 30, 10); fs(cr, hexc('#2EA7FF'), 6)
    rrect(cr, x + 20, y - 150, 130, 110, 40); fs(cr, hexc('#2EA7FF'), 7)
    cr.rectangle(x + 50, y - 215, 34, 70); fs(cr, hexc('#3B3F4A'), 6)
    rrect(cr, x + 40, y - 230, 54, 22, 8); fs(cr, hexc('#3B3F4A'), 6)
    cr.move_to(x + 20, y - 40); cr.line_to(x - 15, y - 5); cr.line_to(x + 40, y - 5); cr.close_path(); fs(cr, hexc('#FFD93B'), 5)
    cr.arc(x + 30, y - 110, 9, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill()
    cr.arc(x + 28, y - 113, 3, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()
    cr.arc(x + 42, y - 85, 14, 0.6 * math.pi, 1.2 * math.pi); stroke_dev(cr, OUT, 4)
    ellipse(cr, x + 48, y - 92, 10, 6); cr.set_source_rgba(1, 0.4, 0.5, 0.5); cr.fill()
    for wx, r in ((x + 70, 34), (x + 190, 40)): wheel(cr, wx, y - 5, r, ang)
    if smoke_on:
        for k in range(5):
            u = (t * 0.9 + k / 5) % 1
            sx_ = x + 67 + 90 * u + 20 * math.sin(k + t); sy_ = y - 240 - 260 * u
            cr.arc(sx_, sy_, 22 + 40 * u, 0, 2 * math.pi); cr.set_source_rgba(1, 1, 1, 0.75 * (1 - u)); cr.fill()

def car(cr, cx, col, t, ang, k):
    y = TRACK_Y
    rrect(cr, cx - 72, y - 120, 144, 85, 12); fs(cr, hexc(col), 7)
    cr.rectangle(cx - 60, y - 100, 120, 10); cr.set_source_rgba(1, 1, 1, 0.5); cr.fill()
    cr.move_to(cx - 80, y - 60); cr.line_to(cx - 88, y - 60); stroke_dev(cr, OUT, 8)
    for wx in (cx - 40, cx + 40): wheel(cr, wx, y - 5, 26, ang + k)

def qbox(cr, cx, open_u, t):
    y = TRACK_Y - 175
    rrect(cr, cx - 60, y - 55, 120, 110, 14); fs(cr, hexc('#A15CFF'), 7)
    cr.save(); cr.translate(cx - 62, y - 55); cr.rotate(-2.2 * open_u)
    rrect(cr, 0, -18, 124, 22, 8); fs(cr, hexc('#C79BFF'), 6); cr.restore()
    if open_u < 0.3: big_word(cr, "?", cx, y + 4 + 4 * math.sin(t * 6), 100, hexc('#FFD93B'), 1.0)

def train(cr, t, dx, r_i, m, items, reveal_u, bounce_idx):
    ang = (t * 6) if True else 0
    moving = dx != 0
    loco(cr, dx + 40, t, -dx * 0.03, True)
    for k, cx in enumerate(CARS):
        car(cr, cx + dx, CAR_COL[k], t, -dx * 0.03, k)
    for k, cx in enumerate(CARS):
        x = cx + dx; y = TRACK_Y - 210
        b = bounce_idx[k] if bounce_idx else 0
        if k < 4:
            cr.save(); cr.translate(x, y - 30 * b); s = 0.42 * (1 + 0.2 * b); cr.scale(s, s); item(cr, items[k], t); cr.restore()
        else:
            if items[4] == 'me':
                qbox(cr, x, reveal_u, t)
            else:
                if reveal_u < 1: qbox(cr, x, reveal_u, t)
                if reveal_u > 0.3:
                    e = ease_out_back((reveal_u - 0.3) / 0.7)
                    cr.save(); cr.translate(x, y - 60 * e); cr.scale(0.42 * e, 0.42 * e); item(cr, items[4] if items[4] != 'me' else 'chick', t); cr.restore()

def count_bubble(cr, t0, t):
    u = (t - t0) / 3.0
    if not (0 <= u < 1): return
    n = 3 - min(2, int(u * 3)); ph = (u * 3) % 1; s = 1 + 0.25 * max(0, 1 - ph * 5)
    a = smooth(t0, t0 + 0.2, t) * (1 - smooth(t0 + 2.8, t0 + 3.0, t))
    cr.push_group()
    rrect(cr, 300, 600, 480, 150, 75); fs(cr, (1, 1, 1), 7, hexc('#3B2A6B'))
    cr.arc(390, 675, 52 * s, 0, 2 * math.pi); fs(cr, hexc('#FFD93B'), 6, hexc('#3B2A6B'))
    clean_text(cr, str(n), 390, 671, 70 * s, hexc('#FF4D4D'), 3)
    clean_text(cr, "Say it!", 590, 675, 66, hexc('#3B2A6B'), 0.1, (1, 1, 1))
    cr.pop_group_to_source(); cr.paint_with_alpha(a)

def chick(cr, x, by, h, sc, st, t, look, sx=1, sy=1, rot=0):
    cr.save(); cr.translate(x, by - h); cr.rotate(rot); cr.scale(sc * sx, sc * sy)
    draw_body(cr, 0, -215, 1.0, st, t, look)
    cr.save(); cr.translate(0, -330); ellipse(cr, 0, 0, 100, 18); fs(cr, hexc('#2EA7FF'), 5)
    cr.move_to(-80, 0); cr.curve_to(-80, -90, 80, -90, 80, 0); cr.close_path(); fs(cr, hexc('#2EA7FF'), 5)
    cr.rectangle(-80, -20, 160, 16); cr.set_source_rgb(*hexc('#FF4D4D')); cr.fill(); cr.restore()
    shell_part(cr, top=False); cr.restore()

def frame(cr, t):
    m = TL['marks']
    scenery(cr, t)
    # which round
    ri = 0
    for i in (1, 2):
        if t >= m[f'enter{i}']: ri = i
    r = ROUNDS[ri]
    dx = 0
    if ri > 0 and t < m[f'enter{ri}'] + 1.5:
        dx = 1150 * (1 - ease_io((t - m[f'enter{ri}']) / 1.5))
    if t >= m[f'leave{ri}']:
        dx = -1350 * (ease_io((t - m[f'leave{ri}']) / (1.2 if ri < 2 else 2.0)))
    if ri == 2 and t >= m['again']:
        dx = 1150 * (1 - ease_io((t - m['again']) / 1.4)); r = ROUNDS[0]
        loop_mode = True
    else: loop_mode = False
    bounce = [0] * 5
    rd = m[f'read{ri}']; re_ = m[f'readend{ri}']
    if not loop_mode and rd <= t < re_ + 0.2:
        n = 4; d = (re_ - rd) / n
        for k in range(4): bounce[k] = burst(rd + d * k, rd + d * k + d * 0.9, t)
    reveal_u = 0 if loop_mode else clamp((t - m[f'r{ri}']) / 0.6)
    if loop_mode: reveal_u = 0
    if r['items'][4] == 'me': reveal_u = clamp((t - m['r2']) / 0.4) if t >= m['r2'] else 0
    train(cr, t, dx, ri, m, r['items'], reveal_u, bounce)
    if not loop_mode:
        count_bubble(cr, m[f'c{ri}'], t)
        if t >= m[f'r{ri}'] + 0.1 and (ri < 2 or t >= m['r2'] + 0.9):
            t0 = m[f'r{ri}'] + (0.1 if ri < 2 else 0.9); t1 = m[f'leave{ri}']
            col = '#FF4D4D' if ri < 2 else '#FF9A1F'
            big_word(cr, r['lab'], 540, 680, 135, hexc(col), ease_out_back((t - t0) / 0.4), 0.03 * math.sin(t * 3), 1 - smooth(t1 - 0.1, t1 + 0.2, t))
    # chick
    st = dict(wing=[0.0, 0.0], beak=0.0, happy=0, mood=0.0); hh = 0; sxx = syy = 1
    cx, cb, csc = 200, 1585, 0.62
    look = (0.9, -0.5)
    for e in TL['events']:
        if e['chick'] and e['t'] <= t < e['t'] + e['dur']: st['beak'] = 0.5 * abs(math.sin(t * 14)); st['happy'] = 1
    for i in range(2):
        rr_ = m[f'r{i}'] + 0.05
        if rr_ <= t < rr_ + 0.9:
            kk = int((t - rr_) / 0.45); _, hh, sxx, syy, _, air = hop(t, rr_ + 0.45 * kk, 0.45, 70, 0, 0)
            st.update(happy=1, wing=[0.4 + 0.8 * air] * 2, beak=0.6 * air)
    in_car = False
    if t >= m['r2'] + 0.2 and t < m['again']:
        u = clamp((t - m['r2'] - 0.2) / 0.7)
        tx, ty = CARS[4] + dx, TRACK_Y - 110
        if u < 1:
            cx = lerp(200, CARS[4], u); cb = lerp(1585, ty, u) - 420 * math.sin(math.pi * u); csc = lerp(0.62, 0.42, u)
        else:
            cx, cb, csc = tx, ty, 0.42; st.update(happy=1, wing=[0.2, 1.1 + 0.4 * math.sin(t * 12)])
        in_car = True
    elif t >= m['again']:
        u = clamp((t - m['again']) / 0.6); cx = lerp(-150, 200, ease_io(u))
    if not in_car:
        ellipse(cr, cx, cb + 2, 70, 12); cr.set_source_rgba(0, 0, 0, 0.2); cr.fill()
    chick(cr, cx, cb, hh, csc, st, t, look, sxx, syy)
    if in_car and t >= m['r2'] + 0.9:
        car(cr, CARS[4] + dx, CAR_COL[4], t, -dx * 0.03, 4)
    for i, (x, y, c, s) in enumerate(FLW):
        if not (x < 540 and y > 1520): draw_flower(cr, x, y, s, hexc(c), t, i)
    draw_text(cr, "What Comes Next?", 250, 122, t, -1)

if __name__ == '__main__':
    if sys.argv[1] == 'build': tl = build(); print(tl['dur'], tl['marks'])
