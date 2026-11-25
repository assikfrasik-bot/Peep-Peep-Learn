"""Sink or Float? — pond cross-section, Chickpea in a sailor cap fishes objects into the water."""
import sys; sys.path.insert(0, '/home/claude/kit')
from common import *

F = '/home/claude/ep12'
SURF, BOT = 1090, 1730
X0, TIPY, HANGY = 650, 575, 830
S = 0.78
CH_X, CH_B = 160, 1000
ROUNDS = [dict(k='duck', q="A rubber duck! Will it sink, or float?", a="It floats!", fl=True),
          dict(k='rock', q="A big rock! Sink, or float?", a="It sinks! Down, down, down!", fl=False),
          dict(k='apple', q="An apple! Sink, or float?", a="It floats! Apples float!", fl=True),
          dict(k='key', q="A shiny key! Sink, or float?", a="It sinks!", fl=False)]
HALF = dict(duck=120, rock=95, apple=150, key=75)
FLOAT_DY = dict(duck=-30, apple=5)
PARK = dict(duck=(890, 0), rock=(450, 0), apple=(440, 0), key=(840, 0))


def build():
    s = Script(F); t = 0.1
    t = s.say(t, 'hook', "Sink or float? Let's find out!") + 0.2
    for i, r in enumerate(ROUNDS):
        s.mark(f's{i}', 0.0 if i == 0 else t)
        if i: t += 0.7
        t = s.say(t, f'q{i}', r['q']) + 0.1
        s.mark(f'c{i}', t); t += 3.0; s.mark(f'r{i}', t)
        t += 0.75 if r['fl'] else 0.6
        s.mark(f'a{i}', t)
        t = s.say(t, f'a{i}', r['a']) + 0.35
    s.mark('ask', t)
    t = s.say(t, 'ask', "Can I float too?", 1.0, True) + 0.15
    s.mark('jump', t); t += 1.1
    t = s.say(t, 'boat', "Look! Chickpea floats like a little boat!") + 0.1
    t = s.say(t, 'laugh', "Hee hee!", 1.0, True) + 0.25
    s.mark('again', t); t = s.say(t, 'again', "Again?", 1.0, True) + 0.25
    s.mark('loop', t); t += 0.9
    tl = s.save(t); m = tl['marks']; mx = Mix(tl['dur'])
    mx.music_loop(0, tl['dur'], 112, [([60, 64, 67], 36), ([67, 71, 74], 43), ([57, 60, 64], 45), ([65, 69, 72], 41)],
                  [[72, None, 76, None, 79, None, 76, None], [74, None, 71, None, 67, None, None, None]], 'bouncy', 0.8)
    for i, r in enumerate(ROUNDS):
        if i: mx.add('sfx', m[f's{i}'], slide_whistle(1200, 700, 0.5), 0.12)
        countdown_ticks(mx, m[f'c{i}'])
        mx.add('sfx', m[f'r{i}'], whoosh(0.4), 0.3)
        mx.add('sfx', m[f'r{i}'] + 0.42, splash_snd(), 0.5)
        if r['fl']: mx.add('sfx', m[f'r{i}'] + 0.7, boing(), 0.18)
        else:
            mx.add('sfx', m[f'r{i}'] + 0.6, bubbles_snd(7, 1.3), 0.3)
            mx.add('sfx', m[f'r{i}'] + 0.6, slide_whistle(900, 280, 0.9), 0.1)
        mx.add('sfx', m[f'a{i}'], ding(), 0.18)
    mx.add('sfx', m['jump'], boing(), 0.3); mx.add('sfx', m['jump'] + 0.8, splash_snd(0.8), 0.6)
    mx.add('sfx', m['jump'] + 1.1, tada(72), 0.18)
    mx.add('sfx', m['again'] + 0.2, jingle(), 0.22)
    mx.voices(F, tl['events'])
    mx.write(F + '/audio.wav', quiet=[(m[f'c{i}'], m[f'r{i}']) for i in range(4)]); return tl


TL = json.load(open(F + '/timeline.json')) if os.path.exists(F + '/timeline.json') else None
rr = random.Random(12)
WEEDS = [(rr.uniform(20, 1060), rr.uniform(90, 200), rr.uniform(0, 6.28), rr.choice(['#2FAE5B', '#44C46D', '#249A55'])) for _ in range(9)]
PEBBLES = [(rr.uniform(0, 1080), rr.uniform(BOT + 20, 1900), rr.uniform(10, 26), rr.choice(['#E8C98F', '#D9B373', '#F2DAA8', '#C9A465'])) for _ in range(40)]
FISHES = [(0.45, 1380, 0.22, 1), (0.3, 1560, 0.18, -1)]


# ---------------- objects ----------------
def obj_duck(cr, t):
    yc = hexc('#FFDE3B')
    cr.move_to(-120, 10); cr.line_to(-175, -55); cr.line_to(-95, -25); cr.close_path(); fs(cr, yc)
    ellipse(cr, 0, 35, 140, 85); fs(cr, yc)
    cr.save(); cr.translate(-15, 30); cr.rotate(-0.2); ellipse(cr, 0, 0, 62, 34); fs(cr, hexc('#FFC61F')); cr.restore()
    cr.arc(60, -65, 64, 0, 2 * math.pi); fs(cr, yc)
    ellipse(cr, 135, -52, 42, 17); fs(cr, hexc('#FF8A1F'), 5)
    cr.move_to(98, -52); cr.line_to(172, -52); stroke_dev(cr, hexc('#D9661A'), 3)
    cr.arc(78, -82, 12, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill()
    cr.arc(74, -86, 4.5, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()
    ellipse(cr, 92, -40, 14, 9); cr.set_source_rgba(1, 0.45, 0.5, 0.5); cr.fill()
    ellipse(cr, 30, -100, 18, 10); cr.set_source_rgba(1, 1, 1, 0.55); cr.fill()
    ellipse(cr, -60, 5, 30, 12); cr.set_source_rgba(1, 1, 1, 0.4); cr.fill()

def obj_rock(cr, t):
    cr.move_to(-140, 30); cr.curve_to(-150, -60, -60, -100, 10, -92); cr.curve_to(100, -90, 150, -40, 140, 30)
    cr.curve_to(135, 85, 60, 98, 0, 96); cr.curve_to(-80, 96, -135, 85, -140, 30); cr.close_path()
    fs(cr, hexc('#A3ADB8'))
    for x, y, r in ((-80, -40, 14), (70, 50, 10), (95, -30, 8), (-40, 60, 9)):
        cr.arc(x, y, r, 0, 2 * math.pi); cr.set_source_rgb(*hexc('#8792A0')); cr.fill()
    ellipse(cr, -60, -60, 30, 12); cr.set_source_rgba(1, 1, 1, 0.4); cr.fill()
    for sx in (-1, 1):
        cr.arc(sx * 34, 2, 13, 0.15 * math.pi, 0.85 * math.pi); stroke_dev(cr, OUT, 5)
        ellipse(cr, sx * 60, 22, 14, 9); cr.set_source_rgba(1, 0.45, 0.55, 0.45); cr.fill()
    cr.arc(0, 26, 12, 0.15 * math.pi, 0.85 * math.pi); stroke_dev(cr, OUT, 5)

def obj_key(cr, t):
    gc = hexc('#FFC93C')
    cr.rectangle(-20, -18, 175, 36); fs(cr, gc)
    for x0 in (95, 128):
        cr.rectangle(x0, 14, 20, 40); fs(cr, gc)
    cr.rectangle(-20, -14, 175, 28); cr.set_source_rgb(*gc); cr.fill()
    cr.arc(-75, 0, 75, 0, 2 * math.pi); fs(cr, gc)
    cr.arc(-75, -38, 16, 0, 2 * math.pi); fs(cr, hexc('#7FD0FF'), 5)
    ellipse(cr, -110, -30, 12, 22); cr.set_source_rgba(1, 1, 1, 0.55); cr.fill()
    cr.rectangle(10, -10, 120, 6); cr.set_source_rgba(1, 1, 1, 0.45); cr.fill()
    face(cr, -75, 18, 0.62)

OBJS = dict(duck=obj_duck, rock=obj_rock, apple=lambda c, t: obj_apple(c, 1), key=obj_key)


def obj_state(i, t, m):
    """returns (x, y, rot, visible, phase) for round i object"""
    r = ROUNDS[i]; k = r['k']; si = m[f's{i}']; ri = m[f'r{i}']
    if t < si: return None
    if t < ri:
        e = ease_out_back((t - si) / 0.7) if i else 1.0
        y = lerp(TIPY - 80, HANGY, e) + 8 * math.sin(t * 2.4)
        return X0, y, 0.08 * math.sin(t * 2.1), 'hang'
    u = t - ri
    fall = 0.45
    if u < fall:
        p = u / fall; y = lerp(HANGY, SURF, p * p); return X0, y, 0.25 * p, 'fall'
    v = u - fall
    if r['fl']:
        yfl = SURF + FLOAT_DY[k] * S / 0.55
        dip = 70 * math.exp(-v * 3.2) * math.cos(v * 9)
        px, _ = PARK[k]
        dr = smooth(1.6, 3.0, v)
        x = lerp(X0, px, dr)
        return x, yfl + dip + 6 * math.sin(t * 2.5 + i), 0.08 * math.sin(t * 2.0 + i), 'float'
    ybot = BOT - HALF[k] * S + 6
    p = clamp(v / 1.7)
    y = lerp(SURF + 20, ybot, 1 - (1 - p) ** 2)
    px, _ = PARK[k]
    x = lerp(X0 + 25 * math.sin(v * 4) * (1 - p), px, smooth(2.0, 3.0, v))
    return x, y, 0.2 * math.sin(v * 3) * (1 - p) + (0.12 if k == 'rock' else -0.25) * p, 'sink'


# ---------------- scenery ----------------
def wave_y(x, t): return SURF + 7 * math.sin(x / 70 + t * 2.2) + 4 * math.sin(x / 31 - t * 3.1)

def background(cr, t):
    sky(cr, '#57C1FF', '#E6F8FF', SURF)
    small_sun(cr, t, 930, 380, 0.55)
    clouds(cr, t, ((520, 330, 0.45), (180, 600, 0.35), (900, 680, 0.3)))
    hills(cr, 1040, '#9FE07E', 45)
    for x, s in ((520, 0.55), (980, 0.62)): tree(cr, x, 1065, s, '#4CB944')
    bush(cr, 760, 1075, 0.5)
    # underwater back
    g = cairo.LinearGradient(0, SURF, 0, H); g.add_color_stop_rgb(0, *hexc('#6FD0FF')); g.add_color_stop_rgb(1, *hexc('#2F8FE0'))
    cr.rectangle(0, SURF - 20, W, H - SURF + 20); cr.set_source(g); cr.fill()
    for k in range(5):
        x = 140 + k * 220 + 30 * math.sin(t * 0.7 + k)
        cr.move_to(x - 40, SURF); cr.line_to(x + 40, SURF); cr.line_to(x + 120, BOT); cr.line_to(x - 10, BOT); cr.close_path()
        cr.set_source_rgba(1, 1, 1, 0.07); cr.fill()
    for x, h, ph, c in WEEDS:
        cr.move_to(x, BOT + 10)
        for j in range(1, 7):
            yy = BOT + 10 - h * j / 6; xx = x + 18 * math.sin(t * 1.6 + ph + j * 0.6) * j / 6
            cr.line_to(xx, yy)
        stroke_dev(cr, OUT, 22);
        cr.move_to(x, BOT + 10)
        for j in range(1, 7):
            yy = BOT + 10 - h * j / 6; xx = x + 18 * math.sin(t * 1.6 + ph + j * 0.6) * j / 6
            cr.line_to(xx, yy)
        stroke_dev(cr, hexc(c), 12)
    for sp, y, sc, d in FISHES:
        x = ((t * 120 * sp * d) % 1500) - 200 if d > 0 else 1300 - ((t * 120 * sp) % 1500)
        cr.save(); cr.translate(x, y + 15 * math.sin(t * 2 + y)); cr.scale(-sc * d, sc); item_fish(cr, t); cr.restore()
    # sand
    cr.move_to(0, H)
    for x in range(0, W + 21, 20): cr.line_to(x, BOT + 10 * math.sin(x / 120))
    cr.line_to(W, H); cr.close_path(); cr.set_source_rgb(*hexc('#F3D79B')); cr.fill_preserve(); stroke_dev(cr, OUT, 6)
    for x, y, r, c in PEBBLES:
        ellipse(cr, x, y, r, r * 0.7); cr.set_source_rgb(*hexc(c)); cr.fill()

def water_front(cr, t):
    cr.move_to(0, BOT + 10 * math.sin(0))
    for x in range(0, W + 11, 10): cr.line_to(x, wave_y(x, t))
    for x in range(W, -21, -20): cr.line_to(x, BOT + 10 * math.sin(x / 120))
    cr.close_path()
    g = cairo.LinearGradient(0, SURF, 0, BOT); g.add_color_stop_rgba(0, 0.35, 0.75, 1, 0.42); g.add_color_stop_rgba(1, 0.1, 0.45, 0.9, 0.35)
    cr.set_source(g); cr.fill()
    cr.move_to(0, wave_y(0, t))
    for x in range(0, W + 11, 10): cr.line_to(x, wave_y(x, t))
    stroke_dev(cr, (1, 1, 1), 8, 0.9)
    for k in range(6):
        x = (k * 190 + t * 40) % 1180 - 50
        cr.move_to(x, wave_y(x, t) + 22); cr.line_to(x + 60, wave_y(x + 60, t) + 22); stroke_dev(cr, (1, 1, 1), 5, 0.5)

def dock(cr, posts_only=False):
    if posts_only:
        for x in (50, 250):
            cr.rectangle(x - 18, CH_B + 20, 36, BOT - CH_B); fs(cr, hexc('#9B6B43'))
        return
    rrect(cr, -30, CH_B, 330, 46, 12); fs(cr, hexc('#C88A55'))
    for x in (60, 140, 220): cr.move_to(x, CH_B + 4); cr.line_to(x, CH_B + 42); stroke_dev(cr, hexc('#9B6B43'), 4)


def splash(cr, x0, t0, t, big=1.0):
    u = t - t0
    if u < 0 or u > 1.0: return
    for k in range(12):
        ang = math.pi * (0.15 + 0.7 * k / 11); v = (380 + 120 * (k % 3)) * big
        x = x0 + math.cos(ang) * v * u * (1 if k % 2 else -1) * 0.9
        y = SURF - math.sin(ang) * v * u * 1.6 + 1100 * u * u
        if y < SURF + 10:
            cr.arc(x, y, 14 * big * (1 - u * 0.5), 0, 2 * math.pi); fs(cr, hexc('#BFEAFF'), 4)
    for j in range(2):
        rr_ = (60 + 260 * u) * big * (1 + 0.5 * j); a = (1 - u) * 0.8
        ellipse(cr, x0, SURF + 8, rr_, rr_ * 0.16); stroke_dev(cr, (1, 1, 1), 6, a)

def bubbles(cr, x, y, t0, t):
    u = t - t0
    if u < 0 or u > 2.2: return
    for k in range(7):
        ph = (u * 0.9 + k / 7) % 1
        if u + k * 0.05 > 2.2: continue
        bx = x + 30 * math.sin(k * 2.1 + u * 3); by = y - ph * (y - SURF)
        if by > SURF + 10:
            cr.arc(bx, by, 9 + 5 * (k % 3), 0, 2 * math.pi); stroke_dev(cr, (1, 1, 1), 4, 0.8)


# ---------------- frame ----------------
def draw_obj(cr, k, x, y, rot):
    cr.save(); cr.translate(x, y); cr.rotate(rot); cr.scale(S, S); OBJS[k](cr, 0); cr.restore()

def mast(cr, t):
    cr.move_to(150, -30); cr.line_to(150, -330); stroke_dev(cr, OUT, 10)
    cr.move_to(150, -330); cr.line_to(150, -30); stroke_dev(cr, hexc('#9B6B43'), 5)
    cr.move_to(156, -325); cr.curve_to(220, -300 + 8 * math.sin(t * 5), 240, -280, 270, -270 + 10 * math.sin(t * 5)); cr.line_to(156, -215); cr.close_path()
    fs(cr, hexc('#FF4D4D'), 5)

def frame(cr, t):
    m = TL['marks']
    if t >= m['loop']: t_eff = 0.0
    else: t_eff = t
    background(cr, t)
    dock(cr, posts_only=True)
    states = []
    for i in range(4):
        stt = obj_state(i, t_eff, m)
        if stt: states.append((i, stt))
    # underwater / falling objects first, floating & hanging later
    for i, (x, y, rot, ph) in states:
        if ph in ('sink',): draw_obj(cr, ROUNDS[i]['k'], x, y, rot)
        if ph == 'sink': bubbles(cr, x, y, m[f'r{i}'] + 0.45, t_eff)
    for i, (x, y, rot, ph) in states:
        if ph in ('float', 'fall'): draw_obj(cr, ROUNDS[i]['k'], x, y, rot)
    # chick in the water (twist)
    jt = m['jump']
    in_water = jt + 0.85 <= t_eff
    st = chick_talk(base_st(), t_eff, TL)
    look = (0.9, -0.2)
    if in_water:
        bob = 8 * math.sin(t * 2.5)
        cx = X0 + 15; cb = SURF + 62 + bob
        st.update(happy=1, wing=[0.9 + 0.3 * math.sin(t * 6), 0.9 + 0.3 * math.sin(t * 6 + 1)])
        chick_talk(st, t_eff, TL)
        chick(cr, cx, cb, 0, 0.72, st, t, (0.0, -0.2), acc='sailor', rot=0.05 * math.sin(t * 2), extra=mast)
    water_front(cr, t)
    for i, (x, y, rot, ph) in states:
        if ph == 'float' and t_eff - m[f'r{i}'] < 1.6: splash(cr, X0, m[f'r{i}'] + 0.45, t_eff)
    if jt + 0.8 <= t_eff < jt + 1.8: splash(cr, X0 + 15, jt + 0.8, t_eff, 1.3)
    for i, (x, y, rot, ph) in states:
        if ph == 'sink' and t_eff - m[f'r{i}'] < 1.4: splash(cr, X0, m[f'r{i}'] + 0.45, t_eff, 0.8)
    dock(cr)
    # rod + line + hanging object
    cur = None
    for i, (x, y, rot, ph) in states:
        if ph == 'hang': cur = (i, x, y, rot)
    rod_on = not (jt <= t_eff)
    if rod_on:
        hx, hy = CH_X + 82, CH_B - 128
        cr.move_to(hx, hy); cr.line_to(X0, TIPY); stroke_dev(cr, OUT, 14); cr.move_to(hx, hy); cr.line_to(X0, TIPY); stroke_dev(cr, hexc('#9B6B43'), 7)
        cr.arc(hx + 25, hy - 20, 16, 0, 2 * math.pi); fs(cr, hexc('#C9CED6'), 5)
        if cur:
            i, x, y, rot = cur
            top = y - HALF[ROUNDS[i]['k']] * S + 4
            cr.move_to(X0, TIPY); cr.line_to(x, top); stroke_dev(cr, OUT, 3)
            cr.arc(x, top - 6, 9, 0, 2 * math.pi); fs(cr, hexc('#C9CED6'), 4)
            draw_obj(cr, ROUNDS[i]['k'], x, y, rot)
        else:
            cr.move_to(X0, TIPY); cr.line_to(X0, TIPY + 90); stroke_dev(cr, OUT, 3)
    # chick on dock
    if not in_water:
        h = 0; sx = sy = 1; rot = 0; cx = CH_X; cb = CH_B
        for i in range(4):
            ri = m[f'r{i}']
            if ri - 0.1 <= t_eff < ri + 0.6: look = (0.9, 0.9)
            if m[f'a{i}'] <= t_eff < m[f'a{i}'] + 0.9:
                h, sx, sy, air = hop_seq(t_eff, m[f'a{i}'], 2, 0.45, 50); st.update(happy=1, wing=[0.4 + 0.8 * air, 0.0])
            if m[f'c{i}'] <= t_eff < ri: look = (0.9 + 0.1 * math.sin(t * 3), -0.1)
        if t_eff < jt: st['wing'][1] = max(st['wing'][1], 0.9)
        if jt <= t_eff < jt + 0.85:
            u = (t_eff - jt) / 0.85
            cx = lerp(CH_X, X0 + 15, ease_io(u)); cb = lerp(CH_B, SURF + 62, u) - 300 * math.sin(math.pi * u)
            rot = 0.5 * math.sin(math.pi * u); st.update(happy=1, wing=[1.3, 1.3]); look = (0.5, 0.6)
        else:
            shadow_at(cr, cx, CH_B + 2, 95)
        chick(cr, cx, cb, h, 0.72, st, t, look, sx, sy, acc='sailor', rot=rot)
    # words
    for i, r in enumerate(ROUNDS):
        a0 = m[f'a{i}']; t1 = m[f's{i + 1}'] if i < 3 else m['ask']
        word = 'FLOATS!' if r['fl'] else 'SINKS!'
        word_pop(cr, word, 540, 680, 160, '#2EA7FF' if r['fl'] else '#A15CFF', a0 - 0.2, t1 - 0.1, t_eff)
        count_bubble(cr, m[f'c{i}'], t_eff)
    word_pop(cr, "Wheee!", 540, 680, 160, '#FF9A1F', jt + 1.0, m['again'], t_eff)
    draw_text(cr, "Sink or Float?", 250, 135, t, -1)
    loop_fade(cr, TL, t)

if __name__ == '__main__': episode_main(build, F)
