import sys, math, json, random, os
sys.path.insert(0, '/home/claude/kit')
from kit import *
import cairo
from anim import (hexc, lerp, clamp, ease_io, ease_out_back, smooth, mixc, ellipse, fs, stroke_dev, draw_body, shell_part,
                  star, draw_text, hop, burst, OUT, W, H)
from anim2 import obj_frog, big_word, glow
from anim3 import rrect, clean_text, star5, bfly_c

F = '/home/claude/ep5'
MOVES = ['jump', 'spin', 'wiggle']
LAB = ['JUMP!', 'SPIN!', 'WIGGLE!']

def build():
    s = Script(F); t = 0.1
    s.mark('d0', 0.0)
    t = s.say(t, 'hook', "Let's dance! When the music stops... freeze!") + 0.3
    s.say(t, 'm0', "Jump, jump, jump!")
    t += 3.2; s.mark('f0', t)
    t = s.say(t + 0.05, 'fz0', "FREEZE!", 1.0) + 1.6
    t = s.say(t, 'g0', "Great freezing!") + 0.2
    s.mark('d1', t)
    s.say(t + 0.1, 'm1', "Now spin around!")
    t += 4.0; s.mark('f1', t)
    t = s.say(t + 0.05, 'fz1', "FREEZE!", 1.0) + 1.6
    t = s.say(t, 'g1', "Wow! Like statues!") + 0.2
    s.mark('d2', t)
    s.say(t + 0.1, 'm2', "Wiggle, wiggle, wiggle!")
    t += 4.0; s.mark('f2', t)
    t = s.say(t + 0.05, 'fz2', "FREEZE!", 1.0) + 1.0
    s.mark('fall', t)
    t = s.say(t + 0.2, 'oops', "Whoa! Oops! I can't stop wiggling!", 1.05, False, 'am_puck') + 0.15
    t = s.say(t, 'laugh', "Hee hee hee!", 1.0, True) + 0.25
    s.mark('again', t)
    t = s.say(t, 'again', "Again?", 1.0, True)
    s.mark('d3', t + 0.15); t += 2.0
    tl = s.save(t); m = tl['marks']; mx = Mix(tl['dur'])
    prog = [([60, 64, 67], 36), ([57, 60, 64], 45), ([65, 69, 72], 41), ([67, 71, 74], 43)]
    mel = [[72, 74, 76, 79, 76, 74, 72, None], [76, 79, 81, 79, 76, None, 72, None], [77, 76, 74, 72, 74, None, None, None], [79, 81, 83, 84, None, 79, None, None]]
    for a, b in (('d0', 'f0'), ('d1', 'f1'), ('d2', 'f2'), ('d3', None)):
        mx.music_loop(m[a], m[b] if b else tl['dur'], 128, prog, mel, 'bouncy', 1.25)
    for k in ('f0', 'f1', 'f2'):
        mx.mus[int(m[k] * SR):int(m[k] * SR) + int(0.02 * SR)] *= np.linspace(1, 0, int(0.02 * SR))
        i0 = int(m[k] * SR); i1 = int((m[{'f0': 'd1', 'f1': 'd2', 'f2': 'd3'}[k]]) * SR); mx.mus[i0 + int(0.02 * SR):i1] = 0
        sc = bp(rng.standard_normal(int(0.25 * SR)), 300, 3000) * np.linspace(1, 0, int(0.25 * SR)); mx.add('sfx', m[k], sc, 0.35)
        mx.add('sfx', m[k] + 0.05, bell(mtof(96), 1.5) + bell(mtof(100), 1.5), 0.15)
    mx.add('sfx', m['fall'] + 0.3, slide_whistle(1200, 300, 0.7), 0.25); mx.add('sfx', m['fall'] + 1.0, boing(), 0.35)
    mx.voices(F, tl['events'])
    mx.write(F + '/audio.wav'); return tl

TL = json.load(open(F + '/timeline.json')) if os.path.exists(F + '/timeline.json') else None
TILE_C = ['#FF5FA2', '#FFD93B', '#3ECF8E', '#2EA7FF', '#A15CFF', '#FF9A1F']
BEAT = 60 / 128

def state(t):
    """returns (phase, move_index, ct) where ct is the animation time (frozen during freeze)"""
    m = TL['marks']
    segs = [('d0', 'f0', 0), ('d1', 'f1', 1), ('d2', 'f2', 2)]
    for a, b, i in segs:
        if m[a] <= t < m[b]: return 'dance', i, t
        nxt = m[segs[i + 1][0]] if i < 2 else m['d3']
        if m[b] <= t < nxt: return 'freeze', i, m[b]
    return 'dance', 0, t

def room(cr, t, on):
    g = cairo.LinearGradient(0, 0, 0, 1250); g.add_color_stop_rgb(0, *hexc('#2A1260')); g.add_color_stop_rgb(1, *hexc('#7A3FD0'))
    cr.set_source(g); cr.paint()
    for i in range(40):
        x = (i * 263) % 1080; y = 100 + (i * 157) % 1100
        k = 0.5 + 0.5 * math.sin(t * 3 + i); star(cr, x, y, 6 + 4 * k); cr.set_source_rgba(1, 1, 1, 0.25 + 0.35 * k * on); cr.fill()
    # light beams
    if on > 0:
        for k in range(6):
            a = math.pi / 2 + 0.6 * math.sin(t * 1.3 + k * 1.1)
            cr.move_to(540, 520); cr.line_to(540 + 1800 * math.cos(a - 0.06), 520 + 1800 * math.sin(a - 0.06))
            cr.line_to(540 + 1800 * math.cos(a + 0.06), 520 + 1800 * math.sin(a + 0.06)); cr.close_path()
            cr.set_source_rgba(*hexc(TILE_C[k]), 0.12 * on); cr.fill()
    # floor
    beat = int(t / BEAT)
    for row in range(7):
        y0 = 1250 + row ** 1.35 * 55; y1 = 1250 + (row + 1) ** 1.35 * 55
        for col in range(-4, 12):
            xa0 = 540 + (col * 160 - 540) * (0.6 + row * 0.12); xa1 = 540 + ((col + 1) * 160 - 540) * (0.6 + row * 0.12)
            xb0 = 540 + (col * 160 - 540) * (0.6 + (row + 1) * 0.12); xb1 = 540 + ((col + 1) * 160 - 540) * (0.6 + (row + 1) * 0.12)
            c = hexc(TILE_C[(row + col + beat) % 6]); lit = on * (1 if (row * 3 + col + beat) % 4 == 0 else 0.35)
            cr.move_to(xa0, y0); cr.line_to(xa1, y0); cr.line_to(xb1, y1); cr.line_to(xb0, y1); cr.close_path()
            cr.set_source_rgb(*mixc(hexc('#3A2370'), c, 0.25 + 0.6 * lit)); cr.fill_preserve(); stroke_dev(cr, hexc('#1E0F45'), 3)
    # disco ball
    cr.move_to(540, 0); cr.line_to(540, 430); stroke_dev(cr, hexc('#C9C9D6'), 4)
    glow(cr, 540, 520, 200, (1, 1, 1), 0.25 * on)
    cr.arc(540, 520, 90, 0, 2 * math.pi); fs(cr, hexc('#B8C1D9'), 6)
    cr.save(); cr.arc(540, 520, 88, 0, 2 * math.pi); cr.clip()
    for i in range(-5, 6):
        for j in range(-5, 6):
            x = 540 + i * 18 + (t * 30 % 18); y = 520 + j * 18
            k = 0.5 + 0.5 * math.sin(i * 1.7 + j * 2.3 + t * 4)
            cr.rectangle(x - 7, y - 7, 14, 14); cr.set_source_rgb(*mixc(hexc('#8E9AB8'), (1, 1, 1), k * (0.4 + 0.6 * on))); cr.fill()
    cr.restore()
    # balloons
    for x, y, c in ((120, 700, '#FF5FA2'), (190, 780, '#FFD93B'), (930, 720, '#2EA7FF'), (1000, 800, '#3ECF8E')):
        yy = y + 10 * math.sin(t * 2 + x)
        cr.move_to(x, yy + 80); cr.curve_to(x - 20, yy + 140, x + 20, yy + 200, x, yy + 300); stroke_dev(cr, (1, 1, 1), 3, 0.6)
        ellipse(cr, x, yy, 60, 74); fs(cr, hexc(c), 6); ellipse(cr, x - 20, yy - 25, 12, 20); cr.set_source_rgba(1, 1, 1, 0.5); cr.fill()

def dance_pose(move, ct, phase_off):
    b = (ct / BEAT + phase_off)
    if move == 'jump':
        u = b % 1; h = 110 * 4 * u * (1 - u); sq = 1 - 0.15 * math.sin(math.pi * u) if u > 0.85 or u < 0.15 else 1
        return dict(h=h, sx=1 / sq, sy=sq, rot=0, flip=1, wing=0.4 + 0.8 * math.sin(math.pi * u))
    if move == 'spin':
        a = b * math.pi / 2
        return dict(h=20 * abs(math.sin(b * math.pi)), sx=1, sy=1, rot=0.15 * math.sin(b * math.pi), flip=math.cos(a), wing=1.0)
    return dict(h=10 * abs(math.sin(b * math.pi * 2)), sx=1 + 0.06 * math.sin(b * math.pi * 4), sy=1 - 0.06 * math.sin(b * math.pi * 4),
                rot=0.3 * math.sin(b * math.pi * 2), flip=1, wing=0.6 + 0.5 * math.sin(b * math.pi * 4))

def chick(cr, x, by, sc, pose, st, t, look):
    cr.save(); cr.translate(x, by - pose['h']); cr.rotate(pose['rot'])
    f = pose['flip']; cr.scale(sc * pose['sx'] * (f if abs(f) > 0.05 else 0.05), sc * pose['sy'])
    draw_body(cr, 0, -215, 1.0, st, t, look)
    cr.save(); cr.translate(-20, -335); cr.rotate(-0.3)
    cr.move_to(-60, 10); cr.line_to(0, -120); cr.line_to(60, 10); cr.close_path(); fs(cr, hexc('#FF5FA2'), 5)
    for k in range(3): star5(cr, -25 + k * 25, -20 - k * 25, 10); cr.set_source_rgb(1, 1, 0.7); cr.fill()
    cr.arc(0, -125, 16, 0, 2 * math.pi); fs(cr, hexc('#FFD93B'), 4)
    cr.restore()
    shell_part(cr, top=False); cr.restore()

def frame(cr, t):
    m = TL['marks']
    phase, mi, ct = state(t)
    frozen = phase == 'freeze'
    on = 0.0 if frozen else 1.0
    room(cr, ct if frozen else t, on)
    move = MOVES[mi] if t < m['d3'] else 'jump'
    # frog
    fp = dance_pose(move, ct, 0.5)
    fall = 0
    fx, fby = 790, 1500
    if mi == 2 and t >= m['f2'] + 0.9:
        u = t - m['f2'] - 0.9
        if t < m['fall'] + 1.0:
            fp = dance_pose('wiggle', t, 0.5); fp['rot'] = fp['rot'] * min(1, u)
        else:
            fall = ease_out_back(clamp((t - m['fall'] - 1.0) / 0.4))
        if t >= m['fall'] + 1.0:
            fp = dict(h=0, sx=1, sy=1, rot=lerp(0, 1.45, fall), flip=1, wing=0)
    if t >= m['again']:
        fall = 1 - smooth(m['again'], m['again'] + 0.5, t); fp = dict(h=0, sx=1, sy=1, rot=1.45 * fall, flip=1, wing=0)
        if t >= m['d3']: fp = dance_pose('jump', t, 0.5)
    ellipse(cr, fx, fby + 4, 95, 16); cr.set_source_rgba(0, 0, 0, 0.3); cr.fill()
    cr.save(); cr.translate(fx, fby - fp['h']); cr.rotate(fp['rot']); f = fp['flip']
    cr.scale(0.62 * fp['sx'] * (f if abs(f) > 0.05 else 0.05), 0.62 * fp['sy']); cr.translate(0, -150); obj_frog(cr, 1); cr.restore()
    # chick
    cp = dance_pose(move, ct, 0.0)
    st = dict(wing=[cp['wing']] * 2, beak=0.0, happy=0 if frozen else 1, mood=0.0)
    if frozen: st['beak'] = 0.0
    for e in TL['events']:
        if e['chick'] and e['t'] <= t < e['t'] + e['dur']: st['beak'] = 0.5 * abs(math.sin(t * 14)); st['happy'] = 1
    if mi == 2 and m['fall'] + 1.0 <= t < m['d3']: st.update(happy=1, beak=0.5 * abs(math.sin(t * 10)))
    cx, cby = 310, 1520
    ellipse(cr, cx, cby + 4, 95, 16); cr.set_source_rgba(0, 0, 0, 0.3); cr.fill()
    chick(cr, cx, cby, 0.78, cp, st, ct, (0.3, 0.2))
    # butterfly
    bt = ct
    bx = 540 + 260 * math.sin(bt * 1.4); by = 920 + 90 * math.sin(bt * 2.8)
    cr.save(); cr.translate(bx, by); cr.rotate(0.2 * math.sin(bt * 3)); cr.scale(0.55, 0.55); bfly_c(cr, bt, '#FF7EB6', '#B57BFF'); cr.restore()
    # freeze overlay
    if frozen:
        fk = smooth(state(t)[2], state(t)[2] + 0.15, t)
        cr.set_source_rgba(0.55, 0.85, 1.0, 0.28 * fk); cr.paint()
        for k in range(18):
            x = (k * 197 + 80) % 1080; y = 300 + (k * 331) % 1500
            star(cr, x, y, 16 + 8 * math.sin(t * 5 + k)); cr.set_source_rgba(1, 1, 1, 0.7 * fk); cr.fill()
        for k, (x0, y0) in enumerate(((60, 300), (1020, 300), (60, 1800), (1020, 1800))):
            cr.save(); cr.translate(x0, y0)
            for j in range(6):
                cr.rotate(math.pi / 3); cr.move_to(0, 0); cr.line_to(0, 70); stroke_dev(cr, (1, 1, 1), 8, 0.8 * fk)
            cr.restore()
        fz = m[f'f{mi}']
        if mi < 2 or t < m['fall'] + 0.2:
            big_word(cr, "FREEZE!", 540, 800, 170, hexc('#7FD6FF'), ease_out_back((t - fz) / 0.3), 0.04 * math.sin(t * 2))
    else:
        t0 = m[f'd{mi}'] if t < m['d3'] else m['d3']
        lab = LAB[mi] if t < m['d3'] else 'DANCE!'
        if t >= m['d0'] + 2.2 or mi > 0:
            big_word(cr, lab, 540, 800, 140, hexc(TILE_C[(int(t / BEAT)) % 6]), 1 + 0.08 * abs(math.sin(t * math.pi / BEAT)), 0.06 * math.sin(t * math.pi / BEAT))
    if mi == 2 and t >= m['fall'] + 1.0 and t < m['again']:
        big_word(cr, "Oops!", 790, 1160, 110, hexc('#3ECF8E'), ease_out_back((t - m['fall'] - 1.0) / 0.3), -0.1)
    if t < 2.2:
        big_word(cr, "Dance with me!", 540, 800, 110, hexc('#FFD93B'), ease_out_back(t / 0.4), 0.04 * math.sin(t * 4))
    draw_text(cr, "Freeze Dance!", 250, 130, t, -1)

if __name__ == '__main__':
    if sys.argv[1] == 'build': tl = build(); print(tl['dur'], tl['marks'])
