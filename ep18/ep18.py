"""Shape Sorter! — name the shape, it drops into its hole. Twist: Chickpea squeezes into the circle hole, then peekaboo."""
import sys; sys.path.insert(0, '/home/claude/kit')
from common import *

F = '/home/claude/ep18'
BX0, BX1 = 250, 830          # box front x range
TOPY0, TOPY1, BOTY = 960, 1110, 1480
HOLES = dict(circle=(355, 1035), square=(480, 1035), triangle=(605, 1035), star=(730, 1035))
ROUNDS = [dict(k='circle', q="What shape is this?", a="A circle! Round and round!", c='#FF4D4D'),
          dict(k='square', q="What shape is this one?", a="A square! Four sides!", c='#2EA7FF'),
          dict(k='triangle', q="And this shape?", a="A triangle! Three sides!", c='#3ECF5E'),
          dict(k='star', q="Last one! What shape?", a="A star! Twinkle, twinkle!", c='#FFB400')]
CH_X, CH_B = 950, 1780


def build():
    s = Script(F); t = 0.1
    for i, r in enumerate(ROUNDS):
        s.mark(f's{i}', 0.0 if i == 0 else t)
        t = s.say(t + (0.35 if i else 0), f'q{i}', r['q']) + 0.1
        s.mark(f'c{i}', t); t += 3.0; s.mark(f'r{i}', t)
        t = s.say(t + 0.05, f'a{i}', r['a']) + 0.1
        s.mark(f'd{i}', t); t += 0.9
    s.mark('ask', t)
    t = s.say(t, 'ask', "Can I fit in the circle?", 1.0, True) + 0.1
    s.mark('jump', t); t += 2.2
    s.mark('peek', t)
    t = s.say(t, 'peek', "Peekaboo! Hee hee!", 1.0, True) + 0.25
    s.mark('again', t); t = s.say(t, 'again', "Again?", 1.0, True) + 0.25
    s.mark('loop', t); t += 0.9
    tl = s.save(t); m = tl['marks']; mx = Mix(tl['dur'])
    mx.music_loop(0, tl['dur'], 116, [([60, 64, 67], 36), ([67, 71, 74], 43), ([65, 69, 72], 41), ([60, 64, 67], 36)],
                  [[72, None, 76, None, 79, 76, 72, None], [74, None, 77, None, 76, None, None, None]], 'bouncy', 0.8)
    for i in range(4):
        mx.add('sfx', m[f's{i}'] + (0.0 if i == 0 else 0.05), pop(300, 800, 0.12), 0.3)
        countdown_ticks(mx, m[f'c{i}'])
        mx.add('sfx', m[f'r{i}'], ding(), 0.2)
        mx.add('sfx', m[f'd{i}'], whoosh(0.5), 0.2); mx.add('sfx', m[f'd{i}'] + 0.55, pop(700, 150, 0.22), 0.5)
        mx.add('sfx', m[f'd{i}'] + 0.6, kick(), 0.3)
    mx.add('sfx', m['jump'], boing(), 0.3); mx.add('sfx', m['jump'] + 1.0, slide_whistle(1400, 300, 0.7), 0.25)
    mx.add('sfx', m['jump'] + 1.7, pop(700, 150, 0.22), 0.45)
    for k in range(4): mx.add('sfx', m['jump'] + 1.8 + k * 0.1, kick(), 0.15)
    mx.add('sfx', m['peek'], pop(300, 1200, 0.15), 0.4); mx.add('sfx', m['peek'] + 0.1, tada(72), 0.2)
    mx.add('sfx', m['again'] + 0.2, jingle(), 0.22)
    mx.voices(F, tl['events'])
    mx.write(F + '/audio.wav', quiet=[(m[f'c{i}'], m[f'r{i}']) for i in range(4)]); return tl


TL = json.load(open(F + '/timeline.json')) if os.path.exists(F + '/timeline.json') else None


# ---------------- shapes ----------------
def shape_path(cr, k, s):
    if k == 'circle': cr.arc(0, 0, 100 * s, 0, 2 * math.pi)
    elif k == 'square': rrect(cr, -92 * s, -92 * s, 184 * s, 184 * s, 22 * s)
    elif k == 'triangle':
        cr.move_to(0, -110 * s); cr.line_to(110 * s, 80 * s); cr.line_to(-110 * s, 80 * s); cr.close_path()
    elif k == 'star':
        cr.move_to(0, -112 * s)
        for j in range(1, 10):
            a = j * math.pi / 5; r = 112 * s if j % 2 == 0 else 50 * s
            cr.line_to(r * math.sin(a), -r * math.cos(a))
        cr.close_path()

def block(cr, k, x, y, sc, rot, t, col, happy=False):
    if sc <= 0.01: return
    cr.save(); cr.translate(x, y); cr.rotate(rot); cr.scale(sc, sc)
    cr.save(); cr.translate(14, 16); shape_path(cr, k, 1.0); cr.set_source_rgba(0, 0, 0, 0.15); cr.fill(); cr.restore()
    shape_path(cr, k, 1.0); fs(cr, hexc(col), 7)
    shape_path(cr, k, 0.8); stroke_dev(cr, (1, 1, 1), 5, 0.35)
    ellipse(cr, -35, -40 if k != 'triangle' else -10, 18, 28); cr.set_source_rgba(1, 1, 1, 0.45); cr.fill()
    if happy:
        for sx in (-1, 1): cr.arc(sx * 30, 8, 11, math.pi * 1.1, math.pi * 1.9); stroke_dev(cr, OUT, 5)
        cr.arc(0, 26, 14, 0.15 * math.pi, 0.85 * math.pi); stroke_dev(cr, OUT, 5)
    else:
        face(cr, 0, 12 if k != 'triangle' else 25, 0.85)
    cr.restore()


# ---------------- room & box ----------------
def room(cr, t):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *hexc('#FFE9F2')); g.add_color_stop_rgb(1, *hexc('#FFF5E6'))
    cr.set_source(g); cr.paint()
    for y in range(340, 1560, 110):
        for x in range(0 if (y // 110) % 2 else 55, W, 110):
            star5(cr, x, y, 10); cr.set_source_rgba(1, 1, 1, 0.7); cr.fill()
    # shelf with toys
    rrect(cr, 40, 640, 300, 26, 10); fs(cr, hexc('#C88A55'))
    cr.arc(110, 590, 45, 0, 2 * math.pi); fs(cr, hexc('#FF9A1F'))
    rrect(cr, 190, 545, 90, 90, 14); fs(cr, hexc('#A15CFF'))
    rrect(cr, 760, 700, 280, 26, 10); fs(cr, hexc('#C88A55'))
    cr.move_to(830, 700); cr.line_to(880, 610); cr.line_to(930, 700); cr.close_path(); fs(cr, hexc('#3ECF8E'))
    cr.arc(985, 655, 40, 0, 2 * math.pi); fs(cr, hexc('#2EA7FF'))
    cr.rectangle(0, 1560, W, H - 1560); cr.set_source_rgb(*hexc('#B98AE0')); cr.fill()
    cr.move_to(0, 1560); cr.line_to(W, 1560); stroke_dev(cr, OUT, 6)
    for x in range(-100, W + 100, 120):
        cr.move_to(x, 1560); cr.line_to(x - 140, H); stroke_dev(cr, hexc('#A877D4'), 4, 0.6)

def box_back(cr):
    # top face (lid)
    cr.move_to(BX0, TOPY1); cr.line_to(BX0 + 90, TOPY0); cr.line_to(BX1 + 90, TOPY0); cr.line_to(BX1, TOPY1); cr.close_path()
    fs(cr, hexc('#FFD86B'))
    # side face
    cr.move_to(BX1, TOPY1); cr.line_to(BX1 + 90, TOPY0); cr.line_to(BX1 + 90, BOTY - 150); cr.line_to(BX1, BOTY); cr.close_path()
    fs(cr, hexc('#E8A93A'))

def hole(cr, k, glow_a=0.0):
    x, y = HOLES[k]
    cr.save(); cr.translate(x, y); cr.scale(1, 0.5)
    if glow_a > 0:
        cr.save(); cr.scale(1, 2); glow(cr, 0, 0, 120, (1, 1, 0.6), glow_a); cr.restore()
    shape_path(cr, k, 0.5); cr.set_source_rgb(*hexc('#5A3A1E')); cr.fill_preserve(); stroke_dev(cr, OUT, 5)
    cr.restore()

def box_front(cr, shake=0.0):
    cr.save(); cr.translate(shake, 0)
    rrect(cr, BX0, TOPY1, BX1 - BX0, BOTY - TOPY1, 18); fs(cr, hexc('#FFC93C'))
    rrect(cr, BX0 + 26, TOPY1 + 26, BX1 - BX0 - 52, BOTY - TOPY1 - 52, 12); stroke_dev(cr, (1, 1, 1), 6, 0.6)
    for k, (x, c) in enumerate(((330, '#FF4D4D'), (450, '#2EA7FF'), (570, '#3ECF5E'), (700, '#A15CFF'))):
        star5(cr, x + 20, 1300 + 30 * math.sin(k), 26); cr.set_source_rgb(*hexc(c)); cr.fill()
    face(cr, 540, 1390, 1.1)
    cr.restore()


def prop_cap(cr, t):
    cr.save(); cr.translate(0, -332)
    cr.move_to(-90, 10); cr.curve_to(-90, -80, 90, -80, 90, 10); cr.close_path()
    p = cr.copy_path(); fs(cr, hexc('#2EA7FF'))
    cr.save(); cr.append_path(p); cr.clip()
    for k, c in enumerate(['#FF4D4D', '#FFD93B', '#3ECF5E']):
        cr.move_to(-90 + k * 60, 10); cr.line_to(-60 + k * 60, -80); cr.line_to(-30 + k * 60, -80); cr.line_to(-60 + k * 60, 10); cr.close_path()
        cr.set_source_rgb(*hexc(c)); cr.fill()
    cr.restore(); cr.append_path(p); stroke_dev(cr, OUT, 6)
    cr.move_to(0, -62); cr.line_to(0, -92); stroke_dev(cr, OUT, 6)
    sp = math.cos(t * 18)
    ellipse(cr, 0, -96, 75 * abs(sp) + 8, 12); fs(cr, hexc('#FF5FA2'), 5)
    cr.arc(0, -96, 9, 0, 2 * math.pi); fs(cr, hexc('#FFD93B'), 4)
    cr.restore()


def frame(cr, t):
    m = TL['marks']
    te = 0.0 if t >= m['loop'] else t
    room(cr, t)
    box_back(cr)
    for i, r in enumerate(ROUNDS):
        d = m[f'd{i}']
        ga = burst(d + 0.5, d + 1.1, te) * 0.9 if te >= d + 0.5 else 0
        hole(cr, r['k'], ga)
    # twist: chick squeezes into the circle hole
    jt = m['jump']; pk = m['peek']
    st = chick_talk(base_st(), te, TL); look = (-0.8, -0.3); h = 0; sx = sy = 1
    chick_drawn = False
    hx, hy = HOLES['circle']
    if jt <= te < jt + 1.7:
        u = te - jt
        if u < 0.8:
            p = u / 0.8
            x = lerp(CH_X, hx, ease_io(p)); b = lerp(CH_B, hy + 10, p) - 380 * math.sin(math.pi * p)
            st.update(happy=1, wing=[1.2, 1.2])
            chick(cr, x, b, 0, 0.62, st, te, (-0.5, 0.5), acc=None, extra=prop_cap)
        else:
            p = clamp((u - 0.8) / 0.9)
            wig = 0.12 * math.sin(te * 30) * (1 - p)
            cr.save(); cr.translate(hx, hy); cr.scale(1, 0.5); shape_path(cr, 'circle', 0.5); cr.restore()
            cr.save()
            cr.rectangle(0, 0, W, hy + 2); cr.clip()
            chick(cr, hx, hy + 10 + 260 * ease_io(p), 0, 0.62, st, te, (0, 0.3), sx=1 - 0.25 * math.sin(math.pi * p), sy=1 + 0.15 * math.sin(math.pi * p), rot=wig, extra=prop_cap)
            cr.restore()
        chick_drawn = True
    if te >= pk:
        e = ease_out_back((te - pk) / 0.5)
        cr.save(); cr.rectangle(0, 0, W, hy + 2); cr.clip()
        st2 = chick_talk(base_st(), te, TL); st2['happy'] = 1; st2['wing'] = [0.8 + 0.4 * math.sin(te * 8), 0.8 + 0.4 * math.sin(te * 8 + 1)]
        cr.save(); cr.translate(hx, hy + 250 - 255 * e); cr.scale(0.62, 0.62); draw_body(cr, 0, -215, 1.0, st2, te, (0, 0.2)); prop_cap(cr, te); cr.restore()
        cr.restore()
        chick_drawn = True
    shake = 0
    if jt + 1.7 <= te < jt + 2.2: shake = 10 * math.sin(te * 50)
    box_front(cr, shake)
    # blocks
    for i, r in enumerate(ROUNDS):
        s0 = m[f's{i}']; r0 = m[f'r{i}']; d = m[f'd{i}']
        if te < s0 - 0.01 and i: continue
        if te >= d + 0.7: continue
        app = ease_out_back((te - s0) / 0.5) if i else 1.0
        x, y, sc, rot = 540, 690 + 18 * math.sin(te * 2.2), 1.15 * app, 0.08 * math.sin(te * 1.8)
        if te >= d:
            u = te - d
            hxx, hyy = HOLES[r['k']]
            if u < 0.45:
                p = ease_io(u / 0.45); x = lerp(540, hxx, p); y = lerp(690, hyy - 120, p) - 80 * math.sin(math.pi * p); sc = lerp(1.15, 0.5, p); rot = 0
                block(cr, r['k'], x, y, sc, rot, te, r['c'], True)
            else:
                p = clamp((u - 0.45) / 0.25)
                cr.save(); cr.rectangle(0, 0, W, hyy); cr.clip()
                block(cr, r['k'], hxx, hyy - 50 + 140 * p, 0.5, 0, te, r['c'], True); cr.restore()
            continue
        happy = te >= r0
        if happy: sc *= 1 + 0.08 * burst(r0, r0 + 0.4, te)
        block(cr, r['k'], x, y, sc, rot, te, r['c'], happy)
    # chick on the right
    if not chick_drawn and te < jt:
        for i in range(4):
            if m[f'c{i}'] <= te < m[f'r{i}']: look = (-0.9, -0.9)
            if m[f'r{i}'] <= te < m[f'r{i}'] + 0.9:
                h, sx, sy, air = hop_seq(te, m[f'r{i}'], 2, 0.45, 55); st.update(happy=1, wing=[0.3 + 0.8 * air] * 2)
            if m[f'd{i}'] <= te < m[f'd{i}'] + 0.8: look = (-0.9, 0.2)
        shadow_at(cr, CH_X, CH_B + 3, 95)
        chick(cr, CH_X, CH_B, h, 0.72, st, te, look, sx, sy, extra=prop_cap)
    elif not chick_drawn and te >= jt + 1.7 and te < pk:
        pass
    for i, r in enumerate(ROUNDS):
        count_bubble(cr, m[f'c{i}'], te, y=420)
        word_pop(cr, r['k'].upper() + '!', 540, 470, 150, r['c'], m[f'r{i}'], m[f'd{i}'] + 0.4, te)
    word_pop(cr, "Peekaboo!", 540, 470, 150, '#FF5FA2', pk + 0.2, m['again'] + 0.3, te)
    draw_text(cr, "Shape Sorter!", 250, 135, t, -1)
    loop_fade(cr, TL, t)

if __name__ == '__main__': episode_main(build, F)
