"""Which Is Heavier? — a seesaw scale: feather vs rock, elephant vs mouse, big balloon vs little apple. Twist: elephant lands, Chickpea goes flying!"""
import sys; sys.path.insert(0, '/home/claude/kit')
from common import *
sys.path.insert(0, '/home/claude/ep23'); sys.path.insert(0, '/home/claude/ep29'); sys.path.insert(0, '/home/claude/ep12')
from ep23 import elephant
from ep29 import mouse
from ep12 import obj_rock
from anim2 import obj_apple

F = '/home/claude/ep30'
PX, PY = 540, 1290          # pivot
ARM = 345
MAXA = 0.32
ROUNDS = [dict(L='feather', R='rock', heavy='R', q="The feather or the rock?", a="The rock is heavier!", y="Thud!", word='Rock!', col='#8792A0'),
          dict(L='elephant', R='mouse', heavy='L', q="The elephant or the mouse?", a="The elephant!", y="Big and heavy!", word='Elephant!', col='#7A8BCC'),
          dict(L='balloon', R='apple', heavy='R', q="The big balloon or the little apple?", a="The little apple! Balloons are light!", y="Whoa!", word='Apple!', col='#FF4D4D')]


def build():
    s = Script(F); t = 0.1
    t = s.say(t, 'hook', "Which is heavier? Let's weigh it!") + 0.05
    t = s.say(t, 'hmm', "Hmm!", 1.0, True) + 0.15
    for i, r in enumerate(ROUNDS):
        s.mark(f's{i}', t if i else 0.05); t += 0.7 if i else 0.1
        t = s.say(t, f'q{i}', r['q']) + 0.05
        s.mark(f'c{i}', t); t += 3.0; s.mark(f'r{i}', t)
        t = s.say(t + 0.6, f'a{i}', r['a']) + 0.05
        t = s.say(t, f'y{i}', r['y'], 1.0, True) + 0.3
        s.mark(f'x{i}', t); t += 0.5
    s.mark('tw', t); t += 0.3
    t = s.say(t, 'now', "Now Chickpea hops on!") + 0.1
    s.mark('look', t)
    t = s.say(t, 'uhoh', "Uh oh... who's coming?") + 0.1
    s.mark('land', t + 0.5); t += 0.75
    t = s.say(t, 'whee', "Wheeeee!", 1.0, True) + 0.6
    s.mark('down', t)
    t = s.say(t + 0.4, 'again0', "Hee hee! That was fun!", 1.0, True) + 0.25
    s.mark('again', t); t = s.say(t, 'again', "Again?", 1.0, True) + 0.25
    s.mark('loop', t); t += 0.9
    tl = s.save(t); m = tl['marks']; mx = Mix(tl['dur'])
    mx.music_loop(0, tl['dur'], 112, [([60, 64, 67], 36), ([62, 65, 69], 38), ([67, 71, 74], 43), ([60, 64, 67], 36)],
                  [[72, None, 76, None, 74, None, 77, None], [76, None, 74, None, 72, None, None, None]], 'bouncy', 0.72)
    for i in range(3):
        mx.add('sfx', m[f's{i}'] + 0.3, pop(300, 900, 0.12), 0.25); mx.add('sfx', m[f's{i}'] + 0.5, pop(300, 1000, 0.12), 0.25)
        countdown_ticks(mx, m[f'c{i}'])
        mx.add('sfx', m[f'r{i}'] + 0.05, snap(), 0.3); mx.add('sfx', m[f'r{i}'] + 0.35, kick(), 0.5)
        mx.add('sfx', m[f'r{i}'] + 0.55, ding(), 0.2)
        mx.add('sfx', m[f'x{i}'], flick(), 0.2)
    mx.add('sfx', m['tw'] + 0.3, boing(), 0.25); mx.add('sfx', m['tw'] + 0.7, kick(), 0.3)
    mx.add('sfx', m['land'] - 0.8, slide_whistle(1500, 300, 0.8), 0.15)
    mx.add('sfx', m['land'], kick(), 0.8); mx.add('sfx', m['land'], rumble(0.6), 0.3)
    mx.add('sfx', m['land'] + 0.05, slide_whistle(300, 1600, 0.9), 0.18)
    mx.add('sfx', m['down'] - 0.6, slide_whistle(1500, 400, 0.6), 0.12); mx.add('sfx', m['down'], boing(), 0.3)
    mx.add('sfx', m['down'] + 0.2, tada(72), 0.15)
    mx.add('sfx', m['again'] + 0.2, jingle(), 0.22)
    mx.voices(F, tl['events'])
    mx.write(F + '/audio.wav', quiet=[(m[f'c{i}'], m[f'r{i}']) for i in range(3)]); return tl


TL = json.load(open(F + '/timeline.json')) if os.path.exists(F + '/timeline.json') else None


def feather(cr, t):
    cr.save(); cr.translate(0, -40); cr.rotate(-0.5 + 0.08 * math.sin(t * 3))
    cr.move_to(0, 120); cr.curve_to(10, 40, 30, -60, 60, -150)
    cr.curve_to(110, -100, 80, 40, 10, 90); cr.close_path(); fs(cr, hexc('#9FD8FF'))
    cr.move_to(0, 120); cr.curve_to(-60, 30, -30, -90, 60, -150); cr.close_path(); fs(cr, hexc('#C7E9FF'))
    cr.move_to(0, 130); cr.curve_to(10, 40, 30, -60, 60, -150); stroke_dev(cr, OUT, 6)
    for k in range(4):
        y = 40 - k * 45; x = 12 + k * 12
        cr.move_to(x, y); cr.line_to(x + 40, y - 30); stroke_dev(cr, (1, 1, 1), 4, 0.8)
    cr.restore()

def balloon(cr, t):
    sway = 0.06 * math.sin(t * 1.8)
    cr.save(); cr.rotate(sway)
    cr.move_to(0, 0); cr.curve_to(-30, -80, 30, -160, 0, -240); stroke_dev(cr, OUT, 4)
    ellipse(cr, 0, -390, 135, 160); fs(cr, hexc('#FF5FA2'))
    cr.move_to(-14, -228); cr.line_to(14, -228); cr.line_to(0, -246); cr.close_path(); fs(cr, hexc('#FF5FA2'), 4)
    ellipse(cr, -55, -450, 25, 45); cr.set_source_rgba(1, 1, 1, 0.5); cr.fill()
    for sx in (-1, 1): cr.arc(sx * 40, -390, 12, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill()
    cr.arc(0, -365, 22, 0.15 * math.pi, 0.85 * math.pi); stroke_dev(cr, OUT, 6)
    cr.restore()

# drawer, scale, y offset so the object's bottom sits at 0
OBJ = dict(feather=(feather, 1.3, -95), rock=(obj_rock, 1.2, -96), elephant=(elephant, 0.62, 0), mouse=(mouse, 0.75, -50),
           balloon=(balloon, 1.0, 0), apple=(lambda cr, t: obj_apple(cr, 1), 0.8, -100))


def end_pt(side, ang):
    sx = -1 if side == 'L' else 1
    return PX + sx * ARM * math.cos(ang), PY - 40 + sx * ARM * math.sin(ang)

def draw_obj(cr, k, x, y, t, s=1.0, rot=0.0):
    if s <= 0.01: return
    fn, sc, yo = OBJ[k]
    cr.save(); cr.translate(x, y); cr.rotate(rot); cr.scale(sc * s, sc * s); cr.translate(0, yo); fn(cr, t); cr.restore()

def seesaw(cr, ang, lock=0.0):
    # fulcrum
    cr.move_to(PX, PY - 40); cr.line_to(PX - 110, PY + 150); cr.line_to(PX + 110, PY + 150); cr.close_path(); fs(cr, hexc('#FF9A1F'))
    cr.arc(PX, PY - 40, 22, 0, 2 * math.pi); fs(cr, hexc('#FFC93C'), 6)
    if lock > 0.01:
        for sx in (-1, 1):
            cr.save(); cr.translate(PX + sx * 250, PY + 80 - 120 * lock + 120); rrect(cr, -18, -120 * lock, 36, 120 * lock, 10); fs(cr, hexc('#C9965A')); cr.restore()
    cr.save(); cr.translate(PX, PY - 40); cr.rotate(ang)
    rrect(cr, -ARM - 70, -18, 2 * ARM + 140, 36, 18); fs(cr, hexc('#9B6B43'))
    for x in range(-ARM - 40, ARM + 60, 70): cr.move_to(x, -10); cr.line_to(x + 30, -10); stroke_dev(cr, hexc('#C9965A'), 5)
    for sx in (-1, 1):
        ellipse(cr, sx * ARM, -22, 110, 18); fs(cr, hexc('#C9D2DD'))
    cr.restore()
    cr.arc(PX, PY - 40, 14, 0, 2 * math.pi); fs(cr, hexc('#FFFFFF'), 5)


def scene(cr, t):
    sky(cr, '#86D3FF', '#E8F8FF', 1400)
    clouds(cr, t, ((760, 430, 0.45), (220, 560, 0.38), (900, 760, 0.3)))
    small_sun(cr, t, 150, 430, 0.55)
    hills(cr, 1330, '#A6E58A', 50); ground(cr, 1430)
    for x in (80, 1000): bush(cr, x, 1450, 1.0)


def frame(cr, t):
    m = TL['marks']
    te = 0.0 if t >= m['loop'] else t
    scene(cr, t)
    twist = te >= m['tw']
    ri = 0
    for i in range(3):
        if te >= m[f's{i}']: ri = i
    if not twist:
        r = ROUNDS[ri]; s0 = m[f's{ri}']; rv = m[f'r{ri}']; x0 = m[f'x{ri}']
        sgn = 1 if r['heavy'] == 'R' else -1
        u = clamp((te - rv - 0.05) / 0.45)
        ang = sgn * MAXA * (u * u) if u < 1 else sgn * MAXA * (1 - 0.15 * math.exp(-(te - rv - 0.5) * 5) * math.sin((te - rv - 0.5) * 18))
        ang *= (1 - smooth(x0, x0 + 0.4, te))
        lock = 1 - smooth(rv - 0.05, rv + 0.1, te)
        seesaw(cr, ang, lock if te > s0 else 1)
        for side in ('L', 'R'):
            k = r[side]
            drop = clamp((te - s0 - (0.15 if side == 'L' else 0.35)) / 0.35)
            ex, ey = end_pt(side, ang)
            y = ey - 900 * (1 - drop) ** 2 - 20
            poof = smooth(x0, x0 + 0.35, te)
            draw_obj(cr, k, ex, y, te, (1 - poof) * (1 if drop > 0 else 0), ang)
            if (side == r['heavy']) and te >= rv + 0.6:
                word_pop(cr, "HEAVY", ex, ey + 140, 64, '#FF4D4D', rv + 0.6, x0, te)
            if (side != r['heavy']) and te >= rv + 0.6:
                word_pop(cr, "LIGHT", ex, ey - 330 if k == 'balloon' else ey - 250, 64, '#2EA7FF', rv + 0.6, x0, te)
    else:
        tw = m['tw']; land = m['land']
        # chickpea hops onto the left end; elephant falls on the right
        if te < land: ang = -MAXA * smooth(tw + 0.5, tw + 0.9, te)
        else:
            u = clamp((te - land) / 0.2)
            ang = lerp(-MAXA, MAXA, u) if u < 1 else MAXA * (1 - 0.12 * math.exp(-(te - land - 0.2) * 5) * math.sin((te - land) * 18))
        seesaw(cr, ang, 0)
        ex, ey = end_pt('R', ang)
        fall = clamp((te - (land - 0.8)) / 0.8)
        if te >= land - 0.8:
            y = ey - 1500 * (1 - fall ** 2) - 20
            sq = 1 + 0.15 * burst(land, land + 0.4, te)
            cr.save(); cr.translate(ex, y); cr.rotate(ang); cr.scale(0.62 * sq, 0.62 * (2 - sq)); elephant(cr, te); cr.restore()
        if land <= te < land + 0.8:
            for k in range(6):
                u = (te - land) / 0.8; a = math.pi + k * math.pi / 5
                cr.arc(ex + math.cos(a) * 200 * u, ey + 30 + math.sin(a) * 60 * u, 30 * (1 - u) + 5, 0, 2 * math.pi); cr.set_source_rgba(0.9, 0.85, 0.75, 1 - u); cr.fill()
    # chickpea
    st = chick_talk(base_st(), te, TL); h = 0; sx = sy = 1; look = (0.0, -0.8); rot = 0
    if not twist:
        for i in range(3):
            if m[f'c{i}'] <= te < m[f'r{i}']: look = (0.8 * math.sin(te * 2), -0.8)
            if m[f'r{i}'] + 0.6 <= te < m[f'r{i}'] + 1.5:
                h, sx, sy, air = hop_seq(te, m[f'r{i}'] + 0.6, 2, 0.45, 55); st.update(happy=1, wing=[0.3 + 0.8 * air] * 2)
        shadow_at(cr, 540, 1833, 100)
        chick(cr, 540, 1830, h, 0.72, st, te, look, sx, sy, acc='beret')
    else:
        tw = m['tw']; land = m['land']; down = m['down']
        lx, ly = end_pt('L', ang)
        if te < tw + 0.6:
            u = clamp((te - tw) / 0.6)
            x = lerp(540, lx, u); y = lerp(1830, ly - 15, u) - 300 * math.sin(math.pi * u)
        elif te < land:
            x, y = lx, ly - 15
            if m['look'] <= te: look = (0.9, -0.9); st['mood'] = 0.0 if te > land - 1.0 else st['mood']
        else:
            u = clamp((te - land) / (down - land))
            x = lx + 30 * math.sin(math.pi * u)
            ytop = -650
            y = ly - 15 + (ytop - (ly - 15)) * math.sin(math.pi * u)
            rot = 2 * math.pi * u * 2 if u < 1 else 0
            st.update(happy=1, wing=[1.0, 1.0])
            if te >= down:
                x, y = lx, ly - 15
                st.update(happy=1, wing=[0.6 + 0.4 * math.sin(te * 9)] * 2); rot = 0
                sx = 1 + 0.15 * burst(down, down + 0.35, te); sy = 2 - sx
        chick(cr, x, y, 0, 0.62, st, te, look, sx, sy, acc='beret', rot=rot)
        if land <= te < down:
            u = (te - land) / (down - land)
            for k in range(5):
                cr.arc(x - 20 + 10 * k, y + 60 + k * 30, 10, 0, 2 * math.pi); cr.set_source_rgba(1, 1, 1, 0.5); cr.fill()
        if te >= down: sparkles(cr, x, y - 150, down, te, 8, 120, 220)
    for i, r in enumerate(ROUNDS):
        count_bubble(cr, m[f'c{i}'], te, "Say it!", y=470)
        word_pop(cr, r['word'], 540, 480, 130, r['col'], m[f'r{i}'] + 0.6, m[f'x{i}'] + 0.2, te)
    word_pop(cr, "Wheee!", 540, 1560, 140, '#FF9A1F', m['land'] + 0.1, m['down'], te, 0.1)
    draw_text(cr, "Which Is Heavier?", 250, 115, t, -1)
    loop_fade(cr, TL, t)

if __name__ == '__main__': episode_main(build, F)
