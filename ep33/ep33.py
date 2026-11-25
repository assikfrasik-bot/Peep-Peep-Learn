"""Freeze Dance! — dance with Chickpea, then FREEZE when the music stops. Twist: a butterfly lands on his beak... it tickles!"""
import sys; sys.path.insert(0, '/home/claude/kit')
from common import *
import numpy as np
from kit import SR

F = '/home/claude/ep33'
BPM = 126
BEAT = 60 / BPM
ROUNDS = [dict(cue="Flap your wings!", kind='flap'), dict(cue="Hop, hop, hop!", kind='hop'), dict(cue="Wiggle and spin!", kind='spin')]
CX, CY = 540, 1540
SC = 1.55


def build():
    s = Script(F); t = 0.1
    s.mark('d0', 0.05)
    t = s.say(t, 'hook', "Freeze dance! Dance with Chickpea!") + 0.05
    t = s.say(t, 'cue0', ROUNDS[0]['cue'], 1.0, True) + 1.4
    for i in range(3):
        if i:
            t = s.say(t, f'cue{i}', ROUNDS[i]['cue'], 1.0, True) + 1.8
        s.mark(f'fz{i}', t)
        t = s.say(t, f'freeze{i}', "Freeze!", 1.05) + 0.05
        s.mark(f'hold{i}', t); t += 3.0
        s.mark(f'go{i}', t)
        if i < 2:
            t = s.say(t, f'dance{i}', "And... dance!") + 0.1
            s.mark(f'd{i + 1}', t - 0.6)
    t += 0.2
    t = s.say(t, 'good', "Great freezing!") + 0.1
    s.mark('d3', t)
    t = s.say(t, 'one', "One more time! Dance!", 1.0, True) + 1.4
    s.mark('fz3', t)
    t = s.say(t, 'freeze3', "Freeze!", 1.05) + 0.1
    s.mark('bfly', t); t += 1.6
    s.mark('tickle', t)
    t = s.say(t, 'ahh', "Ah... ah... hee hee hee!", 1.0, True) + 0.05
    t = s.say(t, 'tick', "It tickles!", 1.0, True) + 0.1
    t = s.say(t, 'oops', "Oops! Chickpea moved!") + 0.25
    s.mark('again', t); t = s.say(t, 'again', "Again?", 1.0, True) + 0.25
    s.mark('loop', t); t += 0.9
    tl = s.save(t); m = tl['marks']; mx = Mix(tl['dur'])
    mx.music_loop(0, tl['dur'], BPM, [([60, 64, 67], 36), ([57, 60, 64], 45), ([65, 69, 72], 41), ([67, 71, 74], 43)],
                  [[72, 74, 76, None, 79, None, 76, 74], [72, None, 69, 72, None, None, 79, None]], 'bouncy', 0.95)
    # the music really stops during every freeze
    fades = [(m[f'fz{i}'], m[f'go{i}']) for i in range(3)] + [(m['fz3'], m['tickle'] + 0.6)]
    env = np.ones(mx.N, np.float32)
    for a, b in fades:
        ia, ib = int(a * SR), int(b * SR); f = int(0.06 * SR)
        env[ia:ia + f] = np.minimum(env[ia:ia + f], np.linspace(1, 0, f)); env[ia + f:ib] = 0
        env[ib:ib + f] = np.minimum(env[ib:ib + f], np.linspace(0, 1, f))
    mx.mus *= env
    for i in range(4):
        mx.add('sfx', m[f'fz{i}'], slide_whistle(900, 250, 0.35), 0.25)
        mx.add('sfx', m[f'fz{i}'] + 0.05, bell(mtof(96), 0.9), 0.12)
    for i in range(3):
        for k in range(3): mx.add('sfx', m[f'hold{i}'] + k, tick(1600), 0.35)
        mx.add('sfx', m[f'go{i}'], ding(), 0.2)
    mx.add('sfx', m['bfly'] + 0.2, chime_up(), 0.15)
    mx.add('sfx', m['tickle'], boing(), 0.25)
    mx.add('sfx', m['again'] + 0.2, jingle(), 0.22)
    mx.voices(F, tl['events'])
    mx.write(F + '/audio.wav'); return tl


TL = json.load(open(F + '/timeline.json')) if os.path.exists(F + '/timeline.json') else None
TILE_COLS = ['#FF5FA2', '#FFC93C', '#3ECF5E', '#2EA7FF', '#A15CFF', '#FF9A1F']


def party(cr, t, frozen, beat_i):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *hexc('#3B2A7A')); g.add_color_stop_rgb(1, *hexc('#6B3FA0'))
    cr.set_source(g); cr.paint()
    # light beams
    if frozen < 0.5:
        for k in range(5):
            a = math.sin(t * 1.3 + k * 1.7) * 0.5
            x0 = 120 + k * 210
            cr.save(); cr.translate(x0, 300); cr.rotate(a)
            cr.move_to(-15, 0); cr.line_to(15, 0); cr.line_to(140, 1100); cr.line_to(-140, 1100); cr.close_path()
            cr.set_source_rgba(*hexc(TILE_COLS[k % 6]), 0.16); cr.fill(); cr.restore()
    # disco ball
    cr.move_to(540, 300); cr.line_to(540, 360); stroke_dev(cr, (0.8, 0.8, 0.9), 4)
    cr.save(); cr.translate(540, 440); cr.arc(0, 0, 80, 0, 2 * math.pi); cr.clip()
    for i in range(-5, 6):
        for j in range(-5, 6):
            v = 0.6 + 0.4 * math.sin(i * 1.7 + j * 2.3 + (t * 4 if frozen < 0.5 else 0))
            cr.rectangle(i * 16 - 8 + (t * 20 % 16 if frozen < 0.5 else 0), j * 16 - 8, 15, 15); cr.set_source_rgb(v, v, v + 0.05); cr.fill()
    cr.restore(); cr.arc(540, 440, 80, 0, 2 * math.pi); stroke_dev(cr, OUT, 6)
    # dance floor
    y0 = 1100
    for r_ in range(6):
        y = y0 + r_ * 140
        for c in range(-1, 9):
            x = c * 140 + (r_ % 2) * 0
            col = TILE_COLS[(c + r_ + beat_i) % 6]
            lit = 0.55 + 0.45 * ((c * 3 + r_ * 5 + beat_i) % 3 == 0)
            rrect(cr, x + 6, y + 6, 128, 128, 18); cr.set_source_rgb(*mixc(hexc('#2A1E5C'), hexc(col), lit * (1 - 0.6 * frozen))); cr.fill()
    cr.move_to(0, y0); cr.line_to(W, y0); stroke_dev(cr, OUT, 6)

def frost(cr, a, t):
    if a <= 0.01: return
    cr.rectangle(0, 0, W, H); cr.set_source_rgba(0.7, 0.88, 1.0, 0.28 * a); cr.fill()
    for k in range(24):
        x = (k * 211) % W; y = (k * 337 + t * 60) % H
        cr.save(); cr.translate(x, y); cr.rotate(k)
        for j in range(3):
            cr.save(); cr.rotate(j * math.pi / 3); cr.move_to(-16, 0); cr.line_to(16, 0); stroke_dev(cr, (1, 1, 1), 4, a * 0.9); cr.restore()
        cr.restore()
    # icy corners
    for sx in (0, W):
        for k in range(6):
            cr.move_to(sx, 300 + k * 260); cr.line_to(sx + (60 if sx == 0 else -60), 330 + k * 260); cr.line_to(sx, 360 + k * 260); cr.close_path()
            cr.set_source_rgba(0.85, 0.95, 1, 0.8 * a); cr.fill()


def frame(cr, t):
    m = TL['marks']
    te = 0.0 if t >= m['loop'] else t
    # current phase
    frozen_win = [(m[f'fz{i}'], m[f'go{i}']) for i in range(3)] + [(m['fz3'], m['tickle'])]
    frozen = 0.0; fi = -1
    for i, (a, b) in enumerate(frozen_win):
        if a <= te < b: frozen = smooth(a, a + 0.12, te); fi = i
    beat_i = int(te / BEAT) if frozen < 0.5 else int(frozen_win[fi][0] / BEAT)
    party(cr, t, frozen, beat_i)
    # which dance?
    di = 0
    for i in range(4):
        if te >= m[f'd{i}']: di = i
    kind = ROUNDS[di]['kind'] if di < 3 else 'flap'
    tt_ = te if frozen < 0.5 else frozen_win[fi][0]       # freeze the pose time
    ph = (tt_ / BEAT) % 1
    st = base_st(); st['happy'] = 1
    h = 0; sx = sy = 1; rot = 0.0; look = (0, 0)
    if kind == 'flap':
        w = 0.5 + 0.5 * math.sin(tt_ * 2 * math.pi / BEAT * 2)
        st['wing'] = [w, w]; sy = 1 - 0.07 * math.sin(ph * 2 * math.pi) ** 2; sx = 2 - sy
    elif kind == 'hop':
        u = ph; h = 110 * math.sin(math.pi * u); st['wing'] = [0.3 + 0.7 * math.sin(math.pi * u)] * 2
        if u < 0.12: sx, sy = 1.1, 0.9
    else:
        rot = 0.3 * math.sin(tt_ * 2 * math.pi / BEAT); sx = math.cos(tt_ * math.pi / BEAT) * 0.15 + 0.95
        st['wing'] = [0.9, 0.2] if math.sin(tt_ * 2 * math.pi / BEAT) > 0 else [0.2, 0.9]
    if frozen > 0.5:
        st['happy'] = 0; look = (0, 0)
    # twist: butterfly lands on the beak
    bf = None
    if di == 3 and te >= m['bfly']:
        u = clamp((te - m['bfly']) / 1.2)
        tx, ty = CX + 5, CY - SC * 200 - h
        bf = (lerp(900, tx, ease_io(u)) + 60 * math.sin(u * 9) * (1 - u), lerp(600, ty - 25, ease_io(u)) + 40 * math.sin(u * 7) * (1 - u))
        look = (0.05, -0.4)
        if te >= m['tickle'] - 0.6 and te < m['tickle']: sx = 1 + 0.02 * math.sin(te * 50)
    if te >= m['tickle']:
        st.update(happy=1, wing=[0.8 + 0.4 * math.sin(te * 12)] * 2); rot = 0.12 * math.sin(te * 14); h = 30 * abs(math.sin(te * 8))
        if bf:
            u = clamp((te - m['tickle']) / 1.2); bf = (bf[0] + 500 * u, bf[1] - 500 * u)
    shadow_at(cr, CX, CY + 8, 240 * (1 - h / 400))
    chick(cr, CX, CY, h, SC, st, te, look, sx, sy, acc='glasses' if di == 1 else ('bow' if di == 2 else None), rot=rot)
    if bf: draw_bfly(cr, bf[0], bf[1], te if te >= m['tickle'] or te < m['bfly'] + 1.2 else te * 0.15, 0.2, 1.6)
    # music notes while dancing
    if frozen < 0.5 and te < m['tickle']:
        for k in range(4):
            u = ((te * 0.5 + k / 4) % 1)
            x = 160 + k * 260 + 30 * math.sin(te * 2 + k); y = 1050 - u * 450
            cr.save(); cr.translate(x, y); cr.rotate(0.2 * math.sin(te * 3 + k))
            ellipse(cr, 0, 0, 22, 16); cr.set_source_rgba(*hexc(TILE_COLS[k]), 1 - u); cr.fill()
            cr.move_to(18, 0); cr.line_to(18, -60); cr.line_to(40, -48); stroke_dev(cr, hexc(TILE_COLS[k]), 7, 1 - u)
            cr.restore()
    frost(cr, frozen * (0.0 if di == 3 and te >= m['tickle'] else 1.0), t)
    for i in range(3):
        count_bubble(cr, m[f'hold{i}'], te, "Don't move!", y=600, w=520)
    for i in range(4):
        word_pop(cr, "FREEZE!", 540, 800, 170, '#7FD3FF', m[f'fz{i}'], (m[f'go{i}'] if i < 3 else m['tickle']) - 0.1, te, 0.06)
    for i in range(2):
        word_pop(cr, "Dance!", 540, 800, 150, '#FF5FA2', m[f'go{i}'], m[f'go{i}'] + 1.2, te, 0.1)
    word_pop(cr, "Oops!", 540, 800, 160, '#FFC93C', m['tickle'] + 0.8, m['again'] + 0.3, te, 0.1)
    draw_text(cr, "Freeze Dance!", 250, 125, t, -1)
    loop_fade(cr, TL, t)

if __name__ == '__main__': episode_main(build, F)
