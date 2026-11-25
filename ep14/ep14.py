"""Mix the Colors! — art studio, paint cans pour into a glass bowl. Twist: all colours -> brown splat on Chickpea."""
import sys; sys.path.insert(0, '/home/claude/kit')
from common import *

F = '/home/claude/ep14'
BX, BY, BR = 540, 1130, 250
COLS = dict(red='#FF3B3B', yellow='#FFD21F', blue='#2E7BFF', orange='#FF8A1F', green='#2FC24E', purple='#9B4DFF', brown='#8A5A2E')
ROUNDS = [dict(a='red', b='yellow', r='orange', q="Red and yellow make...?", ans="Orange! Red and yellow make orange!"),
          dict(a='blue', b='yellow', r='green', q="Blue and yellow make...?", ans="Green! Blue and yellow make green!"),
          dict(a='red', b='blue', r='purple', q="Red and blue make...?", ans="Purple! Red and blue make purple!")]
LEV_LO, LEV_HI = BY + BR - 10, BY - 70


def build():
    s = Script(F); t = 0.1
    t = s.say(t, 'hook', "Let's mix colors! Ready?") + 0.15
    for i, r in enumerate(ROUNDS):
        s.mark(f's{i}', 0.0 if i == 0 else t - 0.1)
        s.mark(f'p{i}', t + 0.1)
        t = s.say(t, f'q{i}', r['q']) + 0.25
        s.mark(f'c{i}', t); t += 3.0; s.mark(f'r{i}', t)
        t = s.say(t + 0.5, f'a{i}', r['ans']) + 0.3
        s.mark(f'e{i}', t); t += 0.6
    s.mark('all', t)
    t = s.say(t, 'allc', "Now... ALL the colors!", 1.0, True) + 0.2
    s.mark('mixall', t); t += 1.4
    t = s.say(t, 'brown', "Uh-oh! All the colors make brown!") + 0.1
    s.mark('splat', t - 0.6)
    t = s.say(t + 0.2, 'oops', "Oops! Hee hee!", 1.0, True) + 0.25
    s.mark('again', t); t = s.say(t, 'again', "Again?", 1.0, True) + 0.25
    s.mark('loop', t); t += 0.9
    tl = s.save(t); m = tl['marks']; mx = Mix(tl['dur'])
    mx.music_loop(0, tl['dur'], 108, [([60, 64, 67], 36), ([57, 60, 64], 45), ([65, 69, 72], 41), ([67, 71, 74], 43)],
                  [[76, None, 79, None, 84, None, 79, None], [77, None, 76, None, 74, None, None, None]], 'bouncy', 0.8)
    for i in range(3):
        mx.add('sfx', m[f'p{i}'], whoosh(0.5), 0.2)
        mx.add('sfx', m[f'p{i}'] + 0.4, bp(rng.standard_normal(int(1.4 * SR)), 200, 1800) * np.sin(np.pi * tt(1.4) / 1.4) ** 2, 0.18)
        countdown_ticks(mx, m[f'c{i}'])
        mx.add('sfx', m[f'r{i}'], slide_whistle(300, 1500, 0.8), 0.15); mx.add('sfx', m[f'r{i}'] + 0.8, chime_up(), 0.25)
        mx.add('sfx', m[f'e{i}'], whoosh(0.5), 0.15)
    mx.add('sfx', m['all'] + 0.5, bp(rng.standard_normal(int(1.6 * SR)), 200, 1800) * np.sin(np.pi * tt(1.6) / 1.6) ** 2, 0.25)
    mx.add('sfx', m['mixall'], bubbles_snd(8, 1.4), 0.35)
    mx.add('sfx', m['splat'], splash_snd(0.7), 0.6); mx.add('sfx', m['splat'] + 0.05, slide_whistle(900, 200, 0.6), 0.15)
    mx.add('sfx', m['again'] + 0.2, jingle(), 0.22)
    mx.voices(F, tl['events'])
    mx.write(F + '/audio.wav', quiet=[(m[f'c{i}'], m[f'r{i}']) for i in range(3)]); return tl


TL = json.load(open(F + '/timeline.json')) if os.path.exists(F + '/timeline.json') else None
rr = random.Random(14)
SPLATS = [(rr.uniform(-90, 90), rr.uniform(-330, -90), rr.uniform(14, 30)) for _ in range(9)]
DROPS = [(rr.uniform(-1, 1), rr.uniform(-1.3, -0.6), rr.uniform(14, 26)) for _ in range(18)]


def C(n): return hexc(COLS[n])


# ---------------- studio ----------------
def studio(cr, t):
    g = cairo.LinearGradient(0, 0, 0, 1500); g.add_color_stop_rgb(0, *hexc('#FFF1D6')); g.add_color_stop_rgb(1, *hexc('#FFE2B8'))
    cr.set_source(g); cr.paint()
    for x in range(0, W, 120):
        cr.rectangle(x, 0, 60, 1500); cr.set_source_rgba(1, 1, 1, 0.25); cr.fill()
    # window with sun
    rrect(cr, 740, 360, 280, 300, 30); fs(cr, hexc('#8FD8FF'), 8)
    cr.arc(880, 470, 45, 0, 2 * math.pi); cr.set_source_rgb(*hexc('#FFE14D')); cr.fill()
    cr.move_to(880, 360); cr.line_to(880, 660); cr.move_to(740, 510); cr.line_to(1020, 510); stroke_dev(cr, (1, 1, 1), 12)
    rrect(cr, 740, 360, 280, 300, 30); stroke_dev(cr, OUT, 8)
    # framed paintings on wall
    for x, y, w, h, c in ((70, 380, 200, 160, '#FF7EB6'), (90, 600, 150, 120, '#3ECF8E')):
        rrect(cr, x, y, w, h, 12); fs(cr, hexc('#C88A55'), 7)
        rrect(cr, x + 18, y + 18, w - 36, h - 36, 6); fs(cr, (1, 1, 1), 4)
        cr.arc(x + w / 2, y + h / 2 + 5, min(w, h) / 4, 0, 2 * math.pi); cr.set_source_rgb(*hexc(c)); cr.fill()
    # table
    rrect(cr, -20, 1400, W + 40, 60, 14); fs(cr, hexc('#C88A55'))
    cr.rectangle(0, 1458, W, H - 1458); cr.set_source_rgb(*hexc('#9B6B43')); cr.fill()
    for x in range(0, W, 140): cr.move_to(x, 1470); cr.line_to(x + 60, H); stroke_dev(cr, hexc('#8A5D39'), 4, 0.5)


def can(cr, x, y, col_name, tilt, t, label=True):
    cr.save(); cr.translate(x, y); cr.rotate(tilt)
    cr.rectangle(-70, -80, 140, 160); fs(cr, hexc('#E6EBF2'))
    cr.rectangle(-70, -30, 140, 70); fs(cr, C(col_name), 5)
    ellipse(cr, 0, -80, 70, 18); fs(cr, hexc('#C9D2DD'))
    ellipse(cr, 0, -80, 56, 12); cr.set_source_rgb(*C(col_name)); cr.fill()
    cr.arc(0, -110, 70, math.pi * 1.1, math.pi * 1.9); stroke_dev(cr, OUT, 6)
    face(cr, 0, 0, 0.7)
    cr.restore()


def lip(x, y, tilt, side):
    a = tilt; lx, ly = side * 62, -84
    return x + lx * math.cos(a) - ly * math.sin(a), y + lx * math.sin(a) + ly * math.cos(a)


def stream(cr, x0, y0, x1, y1, col, w=34):
    cr.move_to(x0, y0); cr.curve_to(x0 + (x1 - x0) * 0.4, y0 - 10, x1, y0 + (y1 - y0) * 0.4, x1, y1)
    stroke_dev(cr, OUT, w + 12); cr.move_to(x0, y0); cr.curve_to(x0 + (x1 - x0) * 0.4, y0 - 10, x1, y0 + (y1 - y0) * 0.4, x1, y1)
    stroke_dev(cr, col, w)


def bowl_back(cr):
    cr.arc(BX, BY, BR, 0, 2 * math.pi); cr.set_source_rgba(0.85, 0.95, 1, 0.45); cr.fill()

def bowl_front(cr):
    cr.save(); cr.rectangle(0, BY - BR * 0.62, W, H); cr.clip()
    cr.arc(BX, BY, BR, 0, 2 * math.pi); stroke_dev(cr, OUT, 9)
    cr.arc(BX, BY, BR - 30, math.pi * 1.05, math.pi * 1.35); stroke_dev(cr, (1, 1, 1), 16, 0.85)
    cr.arc(BX, BY, BR - 30, math.pi * 0.25, math.pi * 0.32); stroke_dev(cr, (1, 1, 1), 14, 0.7)
    cr.restore()
    ellipse(cr, BX, BY - BR * 0.8, BR * 0.6, 26); stroke_dev(cr, OUT, 9)
    ellipse(cr, BX, BY - BR * 0.8, BR * 0.6, 26); stroke_dev(cr, (1, 1, 1), 4, 0.6)
    ellipse(cr, BX, BY + BR + 8, 150, 22); cr.set_source_rgba(0, 0, 0, 0.18); cr.fill()

def liquid(cr, level, ca, cb, mixp, t, swirl_cols=None):
    if level >= LEV_LO - 2: return
    cr.push_group()
    cr.save(); cr.arc(BX, BY, BR - 6, 0, 2 * math.pi); cr.clip()
    def surf(x): return level + 8 * math.sin(x / 40 + t * 3)
    # two halves
    for side, col in ((-1, ca), (1, cb)):
        first = True
        for y in range(int(level) - 20, int(BY + BR) + 20, 20):
            xb = BX + 40 * math.sin(y / 60 + t * 2) * (1 - mixp)
            if first: cr.move_to(xb, y); first = False
            else: cr.line_to(xb, y)
        cr.line_to(BX + side * 400, BY + BR + 20); cr.line_to(BX + side * 400, level - 20); cr.close_path()
        cr.set_source_rgba(*col, 1); cr.fill()
    if mixp > 0:
        res = mixc(ca, cb, 0.5) if swirl_cols is None else swirl_cols
        cr.rectangle(0, level - 20, W, 800); cr.set_source_rgba(*res, ease_io(mixp)); cr.fill()
        for k in range(3):
            a0 = t * 5 + k * 2.1
            cr.arc(BX, level + (BY + BR - level) * 0.55, 40 + k * 55, a0, a0 + 2.2)
            stroke_dev(cr, ca if k % 2 else cb, 14, 0.6 * (1 - mixp) + 0.25 * math.sin(math.pi * mixp))
    # surface top band
    cr.move_to(0, level - 40); cr.line_to(W, level - 40); cr.line_to(W, level)
    for x in range(W, -1, -10): cr.line_to(x, surf(x))
    cr.close_path(); cr.set_operator(cairo.OPERATOR_CLEAR); cr.fill(); cr.set_operator(cairo.OPERATOR_OVER)
    for x in range(int(BX - BR), int(BX + BR), 10):
        cr.line_to(x, surf(x)) if x > BX - BR else cr.move_to(x, surf(x))
    stroke_dev(cr, (1, 1, 1), 7, 0.6)
    cr.restore()
    cr.pop_group_to_source(); cr.paint()


def palette(cr, t, filled):
    cr.save(); cr.translate(800, 1560); cr.rotate(-0.12)
    cr.move_to(-210, 0); cr.curve_to(-210, -120, 180, -150, 210, -30); cr.curve_to(230, 60, 120, 40, 90, 90)
    cr.curve_to(60, 140, -210, 130, -210, 0); cr.close_path(); fs(cr, hexc('#E9B97A'))
    cr.arc(130, 20, 26, 0, 2 * math.pi); cr.set_source_rgb(*hexc('#9B6B43')); cr.fill()
    slots = [(-140, -10), (-60, -60), (30, -75), (-90, 60)]
    for k, (x, y) in enumerate(slots):
        if k < len(filled) and filled[k][1] > 0:
            s = ease_out_back(filled[k][1])
            cr.arc(x, y, 34 * s, 0, 2 * math.pi); fs(cr, C(filled[k][0]), 5)
            cr.arc(x - 10, y - 10, 9 * s, 0, 2 * math.pi); cr.set_source_rgba(1, 1, 1, 0.5); cr.fill()
        else:
            cr.arc(x, y, 30, 0, 2 * math.pi); cr.set_source_rgba(0, 0, 0, 0.08); cr.fill()
    cr.restore()


def brush(cr, t):
    cr.save(); cr.translate(150, -150); cr.rotate(-0.6)
    rrect(cr, -10, -150, 20, 150, 8); fs(cr, hexc('#C88A55'), 5)
    rrect(cr, -14, -175, 28, 30, 6); fs(cr, hexc('#C9D2DD'), 5)
    cr.move_to(-14, -175); cr.curve_to(-18, -220, 18, -220, 14, -175); cr.close_path(); fs(cr, hexc('#FF5FA2'), 5)
    cr.restore()


def splats_on(cr, t, amt):
    if amt <= 0: return
    for x, y, r in SPLATS:
        cr.arc(x, y, r * ease_out_back(amt), 0, 2 * math.pi); fs(cr, C('brown'), 4)


def frame(cr, t):
    m = TL['marks']
    te = 0.0 if t >= m['loop'] else t
    studio(cr, t)
    ri = 0
    for i in range(3):
        if te >= m[f's{i}']: ri = i
    final = te >= m['all']
    r = ROUNDS[ri]
    ca, cb, cres = C(r['a']), C(r['b']), C(r['r'])
    # bowl level & mix progress
    level = LEV_LO; mixp = 0; swirl = None
    if not final:
        p0 = m[f'p{ri}']; r0 = m[f'r{ri}']; e0 = m[f'e{ri}']
        level = lerp(LEV_LO, LEV_HI, smooth(p0 + 0.4, p0 + 1.8, te))
        mixp = smooth(r0, r0 + 1.0, te)
        if te >= e0: level = lerp(level, LEV_LO, smooth(e0, e0 + 0.6, te))
    else:
        a0 = m['all']
        level = lerp(LEV_LO, LEV_HI - 30, smooth(a0 + 0.5, a0 + 2.0, te))
        ca, cb = C('orange'), C('green')
        mixp = smooth(m['mixall'], m['mixall'] + 1.0, te); swirl = C('brown')
    bowl_back(cr)
    liquid(cr, level, ca, cb, mixp, te, swirl if final else cres)
    if final and te < m['mixall'] + 1.2:
        # rainbow shower of colour drops into the bowl
        u = te - m['all'] - 0.4
        if u > 0:
            for k, cn in enumerate(['red', 'yellow', 'blue', 'orange', 'green', 'purple']):
                ph = (u * 1.3 + k / 6) % 1
                x = BX - 150 + k * 60; y = lerp(700, level, ph)
                ellipse(cr, x, y, 24, 32); fs(cr, C(cn), 5)
    bowl_front(cr)
    # cans
    if not final:
        p0 = m[f'p{ri}']; e0 = m[f'e{ri}']
        app = ease_out_back((te - (m[f's{ri}'] if ri else -1)) / 0.5) if ri else 1.0
        leave = smooth(e0, e0 + 0.5, te)
        tilt = 1.15 * smooth(p0, p0 + 0.4, te) * (1 - smooth(p0 + 1.9, p0 + 2.3, te))
        for side, cn in ((-1, r['a']), (1, r['b'])):
            x = BX + side * 300 + side * 500 * leave; y = 760 - (1 - app) * 600
            tl_ = -side * tilt
            if 0.6 < tilt:
                lx, ly = lip(x, y, tl_, -side)
                stream(cr, lx, ly, BX + side * 60, level + 10, C(cn))
            can(cr, x, y, cn, tl_, te)
    else:
        u = te - m['all']
        for k, cn in enumerate(['red', 'yellow', 'blue']):
            side = -1 if k == 0 else (1 if k == 1 else 0)
            x = BX + side * 300; y = 700 if side else 640
            e = ease_out_back(u / 0.4) * (1 - smooth(m['mixall'] + 0.3, m['mixall'] + 0.8, te))
            if e > 0.01:
                cr.save(); cr.translate(x, y); cr.scale(e, e); can(cr, 0, 0, cn, (-side * 0.9 if side else 0.0) * smooth(0.3, 0.6, u), te); cr.restore()
    # splat burst
    if te >= m['splat']:
        u = te - m['splat']
        if u < 1.2:
            for vx, vy, rad in DROPS:
                x = BX + vx * 600 * u; y = level - 40 + vy * 1200 * u + 1300 * u * u
                cr.arc(x, y, rad, 0, 2 * math.pi); fs(cr, C('brown'), 4)
    # palette with results
    filled = []
    for i, rd in enumerate(ROUNDS):
        filled.append((rd['r'], clamp((te - m[f'r{i}'] - 1.2) / 0.4)))
    filled.append(('brown', clamp((te - m['splat'] - 0.5) / 0.4)))
    palette(cr, te, filled)
    # chick painter
    st = chick_talk(base_st(), te, TL); look = (0.7, -0.6); h = 0; sx = sy = 1
    for i in range(3):
        if m[f'c{i}'] <= te < m[f'r{i}']: look = (0.8 + 0.1 * math.sin(te * 3), -0.6)
        if m[f'r{i}'] + 0.6 <= te < m[f'r{i}'] + 1.5:
            h, sx, sy, air = hop_seq(te, m[f'r{i}'] + 0.6, 2, 0.45, 55); st.update(happy=1, wing=[0.3 + 0.9 * air, 0.9])
    st['wing'][1] = max(st['wing'][1], 0.9)
    splat_amt = smooth(m['splat'] + 0.35, m['splat'] + 0.6, te)
    if splat_amt > 0: st['happy'] = 1
    shadow_at(cr, 200, 1690, 105)
    chick(cr, 200, 1685, h, 0.84, st, te, look, sx, sy, acc='beret', extra=lambda c, tt_: (brush(c, tt_), splats_on(c, tt_, splat_amt)))
    # UI
    for i, rd in enumerate(ROUNDS):
        count_bubble(cr, m[f'c{i}'], te)
        word_pop(cr, rd['r'].upper() + '!', 540, 520, 160, rd['r'] and COLS[rd['r']], m[f'r{i}'] + 0.55, m[f'e{i}'], te)
    word_pop(cr, "BROWN!", 540, 520, 160, COLS['brown'], m['mixall'] + 1.0, m['splat'] + 0.6, te)
    word_pop(cr, "SPLAT!", 540, 520, 170, '#FF5FA2', m['splat'] + 0.6, m['again'] + 0.3, te)
    draw_text(cr, "Mix the Colors!", 250, 130, t, -1)
    loop_fade(cr, TL, t)

if __name__ == '__main__': episode_main(build, F)
