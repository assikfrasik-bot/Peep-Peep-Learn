"""Loud or Quiet? — drum, mouse, lion; a sound meter shows how loud. Twist: shh, the baby is sleeping... ACHOO!"""
import sys; sys.path.insert(0, '/home/claude/kit')
from common import *
import numpy as np
from kit import SR, tt, lp, hp, att

F = '/home/claude/ep29'
OX, OY = 500, 1020
ROUNDS = [dict(k='drum', loud=True, a="Loud!", y="Boom, boom, boom!", lvl=0.85),
          dict(k='mouse', loud=False, a="Quiet!", y="Shh... tiny mouse.", lvl=0.18),
          dict(k='lion', loud=True, a="Loud!", y="Roar!", lvl=0.97)]


def sneeze(d=0.6):
    t = tt(d); n = np.random.default_rng(3).standard_normal(len(t))
    s = hp(n, 900) * np.exp(-t / 0.18) * att(t, 0.01)
    return (s / np.abs(s).max()).astype(np.float32)

def squeak():
    t = tt(0.12); f = 2600 + 900 * np.sin(np.pi * t / 0.12)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / 0.12)).astype(np.float32)


def build():
    s = Script(F); t = 0.1
    t = s.say(t, 'hook', "Loud or quiet? Listen!") + 0.05
    t = s.say(t, 'ready', "I'm ready!", 1.0, True) + 0.15
    for i, r in enumerate(ROUNDS):
        s.mark(f's{i}', t if i else 0.05); t += 0.5 if i else 0.15
        s.mark(f'snd{i}', t)
        if r['k'] == 'lion': t = s.say(t, 'roar', "Roooaaar!", 0.8, False, 'am_puck') + 0.3
        else: t += 1.5
        t = s.say(t, f'q{i}', "Is it loud or quiet?") + 0.05
        s.mark(f'c{i}', t); t += 3.0; s.mark(f'r{i}', t)
        t = s.say(t + 0.4, f'a{i}', r['a']) + 0.05
        t = s.say(t, f'y{i}', r['y'], 1.0, True) + 0.3
        s.mark(f'x{i}', t); t += 0.5
    s.mark('tw', t); t += 0.5
    t = s.say(t, 'shh', "Shh... the baby is sleeping.", 0.85) + 0.1
    t = s.say(t, 'shh2', "Shhh...", 0.9, True) + 0.2
    t = s.say(t, 'ahh', "Ah... ah...", 0.85, True) + 0.1
    s.mark('achoo', t); t = s.say(t, 'achoo', "Achoo!", 1.1, True) + 0.5
    t = s.say(t, 'bless', "Bless you! Hee hee!", 1.0, True) + 0.25
    s.mark('again', t); t = s.say(t, 'again', "Again?", 1.0, True) + 0.25
    s.mark('loop', t); t += 0.9
    tl = s.save(t); m = tl['marks']; mx = Mix(tl['dur'])
    mx.music_loop(0, tl['dur'], 110, [([60, 64, 67], 36), ([65, 69, 72], 41), ([67, 71, 74], 43), ([60, 64, 67], 36)],
                  [[72, None, 72, 79, None, 79, 81, None], [79, None, 77, None, 76, None, None, None]], 'bouncy', 0.7)
    for i, r in enumerate(ROUNDS):
        mx.add('sfx', m[f's{i}'], pop(300, 900, 0.12), 0.3)
        sn = m[f'snd{i}']
        if r['k'] == 'drum':
            for k, g in enumerate((0.9, 0.9, 1.0, 1.0)): mx.add('sfx', sn + k * 0.32, kick(), g); mx.add('sfx', sn + k * 0.32, snap(), 0.25)
        if r['k'] == 'mouse':
            for k in range(3): mx.add('sfx', sn + 0.2 + k * 0.35, squeak(), 0.06)
        if r['k'] == 'lion': mx.add('sfx', sn, rumble(1.3), 0.35)
        countdown_ticks(mx, m[f'c{i}'])
        mx.add('sfx', m[f'r{i}'], pop(300, 900, 0.12), 0.35); mx.add('sfx', m[f'r{i}'] + 0.1, ding(), 0.2)
        mx.add('sfx', m[f'x{i}'], flick(), 0.2)
    mx.add('sfx', m['tw'], pop(300, 700, 0.12), 0.15)
    mx.add('sfx', m['achoo'] + 0.05, sneeze(), 0.5); mx.add('sfx', m['achoo'] + 0.1, boing(), 0.25)
    mx.add('sfx', m['achoo'] + 0.5, slide_whistle(1200, 400, 0.6), 0.12)
    mx.add('sfx', m['again'] + 0.2, jingle(), 0.22)
    mx.voices(F, tl['events'])
    mx.write(F + '/audio.wav', quiet=[(m[f'c{i}'], m[f'r{i}']) for i in range(3)] + [(m['tw'], m['achoo'])]); return tl


TL = json.load(open(F + '/timeline.json')) if os.path.exists(F + '/timeline.json') else None


def drum(cr, t, hit=0.0):
    for sx in (-1, 1):
        a = sx * (0.6 - 0.5 * hit)
        cr.save(); cr.translate(sx * 120, -330); cr.rotate(a)
        cr.move_to(0, 0); cr.line_to(0, 200); stroke_dev(cr, OUT, 24); cr.move_to(0, 0); cr.line_to(0, 200); stroke_dev(cr, hexc('#E8B07A'), 14)
        cr.arc(0, 205, 22, 0, 2 * math.pi); fs(cr, hexc('#FFFFFF')); cr.restore()
    cr.move_to(-210, -170); cr.line_to(-210, 60); cr.curve_to(-210, 120, 210, 120, 210, 60); cr.line_to(210, -170); cr.close_path(); fs(cr, hexc('#FF4D4D'))
    cr.save(); cr.move_to(-210, -170); cr.line_to(-210, 60); cr.curve_to(-210, 120, 210, 120, 210, 60); cr.line_to(210, -170); cr.close_path(); cr.clip()
    cr.move_to(-210, -120)
    for k in range(9): cr.line_to(-210 + (k + 0.5) * 52, -20 if k % 2 == 0 else -120)
    stroke_dev(cr, hexc('#FFC93C'), 12)
    cr.restore()
    ellipse(cr, 0, -170, 210, 55 + 6 * hit); fs(cr, hexc('#FFF6E0'))
    for sx in (-1, 1): cr.arc(sx * 60, -10, 12, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill()
    cr.arc(0, 15, 22, 0.15 * math.pi, 0.85 * math.pi); stroke_dev(cr, OUT, 6)

def mouse(cr, t, talk=0.0):
    G = hexc('#B8B5C9'); P = hexc('#FFB3C8')
    cr.move_to(110, 30); cr.curve_to(220, 20, 230, -80, 180, -110); stroke_dev(cr, OUT, 14); cr.move_to(110, 30); cr.curve_to(220, 20, 230, -80, 180, -110); stroke_dev(cr, P, 7)
    ellipse(cr, 20, -40, 120, 90); fs(cr, G)
    for sx in (-1, 1):
        cr.arc(sx * 85 - 30, -190, 62, 0, 2 * math.pi); fs(cr, G); cr.arc(sx * 85 - 30, -190, 38, 0, 2 * math.pi); cr.set_source_rgb(*P); cr.fill()
    cr.arc(-30, -110, 95, 0, 2 * math.pi); fs(cr, G)
    for sx in (-1, 1): cr.arc(-30 + sx * 35, -125, 12, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill(); cr.arc(-30 + sx * 35 - 4, -130, 4, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()
    ellipse(cr, -30, -85, 16, 12); cr.set_source_rgb(*hexc('#FF7FA8')); cr.fill()
    for sx in (-1, 1):
        for dy in (-8, 8): cr.move_to(-30 + sx * 30, -82 + dy); cr.line_to(-30 + sx * 95, -88 + dy * 2.2); stroke_dev(cr, OUT, 3)
    if talk > 0.1: ellipse(cr, -30, -62, 10, 6 + 8 * talk); cr.set_source_rgb(*hexc('#7A2B3A')); cr.fill()
    for sx in (-1, 1): ellipse(cr, -30 + sx * 62, -95, 15, 9); cr.set_source_rgba(1, 0.45, 0.55, 0.5); cr.fill()

def lion(cr, t, talk=0.0):
    M = hexc('#E8862E'); Y = hexc('#FFC24D')
    n = 14
    for k in range(n):
        a = k * 2 * math.pi / n + 0.05 * math.sin(t * 6) * talk
        cr.arc(185 * math.cos(a), -150 + 185 * math.sin(a), 70, 0, 2 * math.pi); cr.new_sub_path()
    stroke_dev(cr, OUT, 12)
    for k in range(n):
        a = k * 2 * math.pi / n + 0.05 * math.sin(t * 6) * talk
        cr.arc(185 * math.cos(a), -150 + 185 * math.sin(a), 70, 0, 2 * math.pi); cr.new_sub_path()
    cr.set_source_rgb(*M); cr.fill()
    for sx in (-1, 1): cr.arc(sx * 110, -265, 38, 0, 2 * math.pi); fs(cr, Y); cr.arc(sx * 110, -265, 20, 0, 2 * math.pi); cr.set_source_rgb(*hexc('#E8A04D')); cr.fill()
    cr.arc(0, -150, 165, 0, 2 * math.pi); fs(cr, Y)
    for sx in (-1, 1): cr.arc(sx * 60, -185, 15, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill(); cr.arc(sx * 60 - 5, -190, 5, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()
    ellipse(cr, 0, -95, 70, 50); cr.set_source_rgb(*hexc('#FFE4A8')); cr.fill()
    cr.move_to(-25, -130); cr.line_to(25, -130); cr.line_to(0, -105); cr.close_path(); fs(cr, hexc('#7A4A28'), 5)
    if talk > 0.1:
        ellipse(cr, 0, -60, 45, 10 + 40 * talk); fs(cr, hexc('#7A2B3A'), 6)
        for sx in (-1, 1): cr.move_to(sx * 30, -60 - 30 * talk); cr.line_to(sx * 20, -40 - 30 * talk); cr.line_to(sx * 10, -60 - 30 * talk); cr.close_path(); cr.set_source_rgb(1, 1, 1); cr.fill()
    else:
        cr.arc(0, -90, 30, 0.2 * math.pi, 0.8 * math.pi); stroke_dev(cr, OUT, 6)
    for sx in (-1, 1): ellipse(cr, sx * 105, -120, 22, 13); cr.set_source_rgba(1, 0.45, 0.55, 0.5); cr.fill()

OBJ = dict(drum=drum, mouse=mouse, lion=lion)


def meter(cr, lvl, t, flash=0.0):
    x, y0, y1, w = 960, 1320, 640, 90
    n = 10
    rrect(cr, x - w / 2 - 14, y1 - 30, w + 28, y0 - y1 + 60, 30); fs(cr, (1, 1, 1))
    seg = (y0 - y1) / n
    for k in range(n):
        on = lvl * n > k
        col = mixc(hexc('#3ECF5E'), hexc('#FFC93C'), clamp(k / 5)) if k < 5 else mixc(hexc('#FFC93C'), hexc('#FF3B3B'), clamp((k - 5) / 4))
        rrect(cr, x - w / 2, y0 - (k + 1) * seg + 6, w, seg - 12, 10)
        if on: cr.set_source_rgb(*col)
        else: cr.set_source_rgb(*mixc(col, (1, 1, 1), 0.75))
        cr.fill()
    # speaker icon
    cr.save(); cr.translate(x, y0 + 100)
    cr.move_to(-40, -18); cr.line_to(-20, -18); cr.line_to(5, -40); cr.line_to(5, 40); cr.line_to(-20, 18); cr.line_to(-40, 18); cr.close_path(); fs(cr, hexc('#3A3550'), 5)
    for k in range(3):
        if lvl * 3 > k: cr.arc(10, 0, 20 + k * 16, -0.8, 0.8); stroke_dev(cr, hexc('#3A3550'), 6)
    cr.restore()
    if flash > 0: rrect(cr, x - w / 2 - 14, y1 - 30, w + 28, y0 - y1 + 60, 30); stroke_dev(cr, hexc('#FF3B3B'), 14, flash)

def button(cr, x, y, label, col, s, glow_a=0.0, dim=0.0):
    if s <= 0.01: return
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    if glow_a > 0: glow(cr, 0, 0, 230, hexc(col), glow_a)
    rrect(cr, -175, -70, 350, 140, 70); fs(cr, mixc(hexc(col), (0.85, 0.85, 0.88), dim))
    rrect(cr, -150, -58, 300, 40, 20); cr.set_source_rgba(1, 1, 1, 0.25); cr.fill()
    cr.restore()
    big_word(cr, label, x, y + 4, 72 * s, (1, 1, 1), 1.0)

def stage_bg(cr, t, shake=0.0):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *hexc('#FFE1F0')); g.add_color_stop_rgb(1, *hexc('#E1EEFF'))
    cr.set_source(g); cr.paint()
    for k in range(7):
        cr.arc(80 + k * 160, 420 + 30 * math.sin(k), 26, 0, 2 * math.pi); cr.set_source_rgba(1, 1, 1, 0.6); cr.fill()
    ellipse(cr, OX, 1090, 360, 70); fs(cr, hexc('#C9A0FF'))
    ellipse(cr, OX, 1075, 330, 55); cr.set_source_rgb(*hexc('#DCC2FF')); cr.fill()
    cr.rectangle(0, 1560, W, H - 1560); cr.set_source_rgb(*hexc('#9FD6A8')); cr.fill()
    cr.move_to(0, 1560); cr.line_to(W, 1560); stroke_dev(cr, OUT, 6)


def frame(cr, t):
    m = TL['marks']
    te = 0.0 if t >= m['loop'] else t
    ach = m['achoo']
    shake = 18 * burst(ach, ach + 0.8, te) * math.sin(te * 70)
    cr.save(); cr.translate(shake, 0.6 * shake)
    stage_bg(cr, t)
    twist = te >= m['tw']
    ri = 0
    for i in range(3):
        if te >= m[f's{i}']: ri = i
    lvl = 0.0; flash = 0.0
    if not twist:
        r = ROUNDS[ri]; s0 = m[f's{ri}']; sn = m[f'snd{ri}']; rv = m[f'r{ri}']; x0 = m[f'x{ri}']
        pin = ease_out_back(clamp((te - s0) / 0.45), 1.6) * (1 - smooth(x0, x0 + 0.4, te))
        act = 0.0
        if r['k'] == 'drum':
            for k in range(4): act = max(act, burst(sn + k * 0.32, sn + k * 0.32 + 0.25, te))
        elif r['k'] == 'mouse':
            for k in range(3): act = max(act, burst(sn + 0.2 + k * 0.35, sn + 0.45 + k * 0.35, te))
        else:
            for ev in TL['events']:
                if ev['name'] == 'roar' and ev['t'] <= te < ev['t'] + ev['dur']: act = 0.7 + 0.3 * math.sin(te * 20)
        if sn <= te < sn + 1.6: lvl = r['lvl'] * (0.75 + 0.25 * act) * smooth(sn, sn + 0.15, te)
        if te >= rv: lvl = r['lvl'] * (1 - smooth(x0, x0 + 0.3, te))
        sq = 1 + 0.08 * act if r['loud'] else 1
        sc = {'drum': 1.0, 'mouse': 0.85, 'lion': 0.95}[r['k']] * pin
        if sc > 0.01:
            cr.save(); cr.translate(OX, OY + 40); cr.scale(sc * sq, sc * (2 - sq)); OBJ[r['k']](cr, te, act); cr.restore()
        if r['loud'] and act > 0.2:
            for side in (-1, 1):
                for k in range(3):
                    cr.arc(OX + side * 260, OY - 150, 50 + k * 45 + 25 * act, -0.5 if side > 0 else math.pi - 0.5, 0.5 if side > 0 else math.pi + 0.5)
                    stroke_dev(cr, OUT, 9, act)
        if r['k'] == 'mouse' and act > 0.2:
            big_word(cr, "squeak", OX + 230, OY - 280, 46, hexc('#9AA7B8'), 1.0, 0.1)
        # answer buttons
        bs = pin
        rv_ok = te >= rv
        gl_l = 0.8 * burst(rv, rv + 0.6, te) if r['loud'] else 0
        gl_q = 0.8 * burst(rv, rv + 0.6, te) if not r['loud'] else 0
        pl = 1 + 0.12 * burst(rv, rv + 0.5, te) if r['loud'] else 1
        pq = 1 + 0.12 * burst(rv, rv + 0.5, te) if not r['loud'] else 1
        button(cr, 300, 1440, "LOUD", '#FF4D4D', bs * pl, gl_l, 0.6 if (rv_ok and not r['loud']) else 0)
        button(cr, 720, 1440, "QUIET", '#2EA7FF', bs * pq, gl_q, 0.6 if (rv_ok and r['loud']) else 0)
    else:
        tw = m['tw']
        pin = ease_out_back(clamp((te - tw) / 0.45), 1.6)
        # nest + sleeping baby
        cr.save(); cr.translate(OX, OY + 60); cr.scale(pin, pin)
        ellipse(cr, 0, 20, 230, 70); fs(cr, hexc('#C9965A'))
        st = base_st(); st['happy'] = 1
        if te >= ach - 1.1 and te < ach: st['happy'] = 0; st['beak'] = 0.4 + 0.3 * math.sin(te * 8)
        if ach <= te < ach + 0.6: st['happy'] = 0; st['beak'] = 1.0; st['wing'] = [1.0, 1.0]
        if te >= ach + 0.6: st['happy'] = 1; st['beak'] = 0
        hop_ = 160 * math.sin(math.pi * clamp((te - ach) / 0.6)) if te >= ach else 0
        chick(cr, 0, 10 - hop_, 0, 0.95, st, te, (0, 0.1), acc='nightcap')
        for k in range(8): cr.move_to(-210 + k * 55, 0); cr.line_to(-180 + k * 55, 50); stroke_dev(cr, hexc('#9B6B43'), 6)
        cr.restore()
        if te < ach:
            for k in range(3):
                u = ((te - tw) * 0.6 + k / 3) % 1
                big_word(cr, "z", OX + 170 + 80 * u, OY - 300 - 200 * u, 50 + 40 * u, hexc('#7A8BFF'), 1.0, 0.2, 1 - u)
        lvl = 0.1 * pin if te < ach else (1.0 if te < ach + 1.2 else 0.15 + 0.85 * (1 - smooth(ach + 1.2, ach + 2.0, te)))
        flash = burst(ach, ach + 1.2, te)
    meter(cr, lvl, te, flash)
    # chickpea
    st = chick_talk(base_st(), te, TL); h = 0; sx = sy = 1; look = (0.7, -0.6)
    for i, r in enumerate(ROUNDS):
        sn = m[f'snd{i}']
        if r['loud'] and sn <= te < sn + 1.5: st['wing'] = [1.0, 1.0]; st['mood'] = 0.0; sx = 1 + 0.02 * math.sin(te * 40)
        if m[f'r{i}'] + 0.4 <= te < m[f'r{i}'] + 1.3:
            h, sx, sy, air = hop_seq(te, m[f'r{i}'] + 0.4, 2, 0.45, 50); st.update(happy=1, wing=[0.3 + 0.8 * air] * 2)
    if twist and te < ach:
        st['wing'] = [0.0, 1.0]
    rot = 0.0; cx = 170
    if ach <= te < ach + 1.4:
        u = clamp((te - ach) / 0.5); cx = 170 - 60 * math.sin(math.pi * u); rot = -0.4 * math.sin(math.pi * clamp((te - ach) / 1.0))
        st['mood'] = 0.0; st['wing'] = [1.0, 1.0]
    shadow_at(cr, cx, 1823, 100)
    chick(cr, cx, 1820, h, 0.72, st, te, look, sx, sy, acc='bow', rot=rot)
    cr.restore()
    for i, r in enumerate(ROUNDS):
        count_bubble(cr, m[f'c{i}'], te, "Say it!", y=470)
        word_pop(cr, r['a'].upper().rstrip('!') + '!', 540, 480, 150 if r['loud'] else 110, '#FF4D4D' if r['loud'] else '#2EA7FF', m[f'r{i}'] + 0.4, m[f'x{i}'] + 0.2, te)
    word_pop(cr, "ACHOO!", 520, 1440, 190, '#FF5FA2', ach, m['again'] + 0.3, te, 0.12)
    word_pop(cr, "Shh...", 540, 480, 110, '#7A8BFF', m['tw'] + 0.5, ach - 0.1, te)
    draw_text(cr, "Loud or Quiet?", 250, 120, t, -1)
    loop_fade(cr, TL, t)

if __name__ == '__main__': episode_main(build, F)
