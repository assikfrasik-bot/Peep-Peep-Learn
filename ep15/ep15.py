"""Hide and Seek! — prepositions under / behind / on / in. Camera zooms to each found friend. Twist: Chickpea hides in his shell."""
import sys; sys.path.insert(0, '/home/claude/kit')
from common import *

F = '/home/claude/ep15'
GY = 1420
SPOTS = dict(frog=(280, 1560), snail=(800, 1250), bfly=(250, 1010), worm=(820, 1660))
ROUNDS = [dict(k='frog', q="Where is Frog hiding?", a="Under the bench! Frog is under the bench!", w='UNDER', c='#3ECF5E'),
          dict(k='snail', q="Where is Snail hiding?", a="Behind the tree! Snail is behind the tree!", w='BEHIND', c='#FF7EB6'),
          dict(k='bfly', q="Where is Butterfly?", a="On the flower! Butterfly is on the flower!", w='ON', c='#A15CFF'),
          dict(k='worm', q="Where is Worm hiding?", a="In the apple! Worm is in the apple!", w='IN', c='#FF4D4D')]


def build():
    s = Script(F); t = 0.1
    t = s.say(t, 'hook', "Hide and seek! Can you find my friends?", 1.0, True) + 0.15
    for i, r in enumerate(ROUNDS):
        s.mark(f's{i}', t)
        t = s.say(t, f'q{i}', r['q']) + 0.1
        s.mark(f'c{i}', t); t += 3.0; s.mark(f'r{i}', t)
        t = s.say(t + 0.4, f'a{i}', r['a']) + 0.2
        s.mark(f'x{i}', t); t += 0.5
    s.mark('hide', t)
    t = s.say(t, 'mine', "Now Chickpea hides!") + 0.6
    t = s.say(t, 'q4', "Where's Chickpea?") + 0.1
    s.mark('c4', t); t += 2.0; s.mark('r4', t)
    t = s.say(t + 0.35, 'here', "Here I am! In my shell! Hee hee!", 1.0, True) + 0.25
    s.mark('again', t); t = s.say(t, 'again', "Again?", 1.0, True) + 0.25
    s.mark('loop', t); t += 0.9
    tl = s.save(t); m = tl['marks']; mx = Mix(tl['dur'])
    mx.music_loop(0, tl['dur'], 104, [([60, 64, 67], 36), ([57, 60, 64], 45), ([62, 65, 69], 38), ([67, 71, 74], 43)],
                  [[72, None, None, 76, None, None, 79, None], [77, None, 76, None, 74, None, 71, None]], 'soft', 1.0)
    for i in range(4):
        countdown_ticks(mx, m[f'c{i}'])
        mx.add('sfx', m[f'r{i}'], boing(), 0.3); mx.add('sfx', m[f'r{i}'] + 0.2, ding(), 0.18)
        mx.add('sfx', m[f'r{i}'] + 0.05, whoosh(0.6), 0.15)
    mx.add('sfx', m['hide'] + 1.0, pop(900, 250, 0.2), 0.4)
    mx.add('sfx', m['c4'], tick(1100), 0.3); mx.add('sfx', m['c4'] + 1.0, tick(1500), 0.3)
    mx.add('sfx', m['r4'], pop(300, 1100, 0.15), 0.45); mx.add('sfx', m['r4'] + 0.1, tada(72), 0.2)
    mx.add('sfx', m['again'] + 0.2, jingle(), 0.22)
    mx.voices(F, tl['events'])
    mx.write(F + '/audio.wav', quiet=[(m[f'c{i}'], m[f'r{i}']) for i in range(4)]); return tl


TL = json.load(open(F + '/timeline.json')) if os.path.exists(F + '/timeline.json') else None
rr = random.Random(15)
FLW = [(rr.uniform(30, 1050), rr.uniform(1760, 1890), rr.choice(['#FF5A5F', '#FFFFFF', '#A66CFF', '#FFB400']), rr.uniform(0.6, 0.9)) for _ in range(8)]


# ---------------- props ----------------
def big_tree(cr, t):
    x, y = 820, GY + 10
    cr.move_to(x - 60, y); cr.curve_to(x - 50, y - 200, x - 45, y - 330, x - 40, y - 420); cr.line_to(x + 40, y - 420)
    cr.curve_to(x + 45, y - 330, x + 50, y - 200, x + 60, y); cr.close_path(); fs(cr, hexc('#9B6B43'))
    cr.arc(x + 5, y - 260, 14, 0, 2 * math.pi); cr.set_source_rgb(*hexc('#6E4A2C')); cr.fill()
    blobs = [(x - 130, y - 520, 120), (x + 110, y - 530, 120), (x, y - 640, 140), (x - 20, y - 470, 110), (x + 150, y - 430, 80)]
    for bx, by, r in blobs: cr.arc(bx, by, r, 0, 2 * math.pi); cr.new_sub_path()
    stroke_dev(cr, OUT, 12)
    for bx, by, r in blobs: cr.arc(bx, by, r, 0, 2 * math.pi); cr.new_sub_path()
    cr.set_source_rgb(*hexc('#4CB944')); cr.fill()
    for bx, by, r in ((x - 80, y - 650, 30), (x + 60, y - 560, 24)):
        cr.arc(bx, by, r, 0, 2 * math.pi); cr.set_source_rgba(1, 1, 1, 0.22); cr.fill()
    for ax, ay in ((x - 120, y - 470), (x + 90, y - 600), (x + 30, y - 460), (x - 40, y - 690), (x + 170, y - 450)):
        cr.arc(ax, ay, 18, 0, 2 * math.pi); fs(cr, hexc('#FF5A5F'), 5)

def bench(cr):
    x, y = 280, 1600
    for dx in (-150, 150):
        cr.rectangle(x + dx - 14, y - 110, 28, 115); fs(cr, hexc('#8A5D39'))
    rrect(cr, x - 200, y - 135, 400, 36, 10); fs(cr, hexc('#C88A55'))
    for k in range(2):
        rrect(cr, x - 200, y - 250 + k * 55, 400, 32, 10); fs(cr, hexc('#C88A55'))
    for dx in (-150, 150):
        cr.rectangle(x + dx - 12, y - 260, 24, 130); fs(cr, hexc('#8A5D39'))

def big_flower(cr, t):
    x, y = 250, 1010
    cr.move_to(x, GY + 10); cr.curve_to(x + 20, 1300, x - 20, 1150, x, y + 40); stroke_dev(cr, OUT, 26);
    cr.move_to(x, GY + 10); cr.curve_to(x + 20, 1300, x - 20, 1150, x, y + 40); stroke_dev(cr, hexc('#3E9E45'), 16)
    for s in (-1, 1):
        cr.save(); cr.translate(x + s * 50, 1250); cr.rotate(s * 0.5); ellipse(cr, 0, 0, 60, 24); fs(cr, hexc('#5BC85B')); cr.restore()
    cr.save(); cr.translate(x, y); cr.rotate(0.05 * math.sin(t * 1.5))
    for k in range(8):
        a = k * math.pi / 4
        cr.save(); cr.rotate(a); ellipse(cr, 0, -95, 48, 70); fs(cr, hexc('#FF8CC0')); cr.restore()
    cr.arc(0, 0, 70, 0, 2 * math.pi); fs(cr, hexc('#FFC93C'))
    for k in range(10):
        a = k * 0.63; cr.arc(30 * math.cos(a), 30 * math.sin(a), 6, 0, 2 * math.pi); cr.set_source_rgb(*hexc('#E0A020')); cr.fill()
    cr.restore()

def big_apple(cr, t, hole=True):
    cr.save(); cr.translate(820, 1640); cr.scale(0.85, 0.85)
    cr.move_to(10, -95); cr.curve_to(14, -120, 18, -135, 22, -150); stroke_dev(cr, hexc('#8B5A2B'), 14)
    cr.save(); cr.translate(62, -135); cr.rotate(-0.5); ellipse(cr, 0, 0, 46, 22); fs(cr, hexc('#3ECF5E')); cr.restore()
    cr.move_to(0, -95); cr.curve_to(60, -150, 170, -90, 150, 10); cr.curve_to(135, 120, 60, 165, 20, 150)
    cr.curve_to(10, 145, -10, 145, -20, 150); cr.curve_to(-60, 165, -135, 120, -150, 10)
    cr.curve_to(-170, -90, -60, -150, 0, -95); cr.close_path(); fs(cr, hexc('#FF4D4D'))
    cr.save(); cr.translate(-80, -40); cr.rotate(0.4); ellipse(cr, 0, 0, 20, 38); cr.set_source_rgba(1, 1, 1, 0.45); cr.fill(); cr.restore()
    if hole:
        ellipse(cr, 40, 20, 40, 34); fs(cr, hexc('#5A2E22'), 5)
    cr.restore()


def worm(cr, x, y, ext, t, happy=False):
    """ext 0..1 how far out of the hole; x,y = hole centre"""
    cr.save(); cr.translate(x, y)
    n = 5; segs = []
    for k in range(n):
        u = k / (n - 1)
        segs.append((math.sin(t * 3 + k) * 8 * u + 30 * ext * u, -u * 150 * ext))
    for k, (sx, sy) in enumerate(segs):
        cr.arc(sx, sy, 26 - k * 1.2, 0, 2 * math.pi); fs(cr, hexc('#FF9EBB'), 5)
    hx, hy = segs[-1]
    cr.arc(hx, hy - 10, 34, 0, 2 * math.pi); fs(cr, hexc('#FF9EBB'), 5)
    for sx in (-1, 1):
        if happy: cr.arc(hx + sx * 12, hy - 10, 8, math.pi * 1.1, math.pi * 1.9); stroke_dev(cr, OUT, 4)
        else:
            cr.arc(hx + sx * 12, hy - 14, 8, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill()
            cr.arc(hx + sx * 12 - 2, hy - 17, 3, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()
    cr.arc(hx, hy - 2, 10, 0.15 * math.pi, 0.85 * math.pi); stroke_dev(cr, OUT, 4)
    cr.restore()


# ---------------- camera ----------------
def cam(te, m):
    z = 1.0; cx, cy = 540, 1100
    for i, r in enumerate(ROUNDS):
        a, b = m[f'r{i}'], m[f'x{i}']
        if a <= te < b + 0.6:
            k = smooth(a, a + 0.6, te) * (1 - smooth(b, b + 0.6, te))
            sx, sy = SPOTS[r['k']]
            return lerp(1.0, 1.55, k), lerp(540, sx, k), lerp(1100, sy - 60, k)
    if m['r4'] <= te < m['again'] + 0.6:
        k = smooth(m['r4'], m['r4'] + 0.6, te) * (1 - smooth(m['again'], m['again'] + 0.6, te))
        return lerp(1.0, 1.5, k), lerp(540, 540, k), lerp(1100, 1520, k)
    return z, cx, cy


def found(i, te, m): return te >= m[f'r{i}']


def world(cr, t, te, m):
    sky(cr, '#5FC3FF', '#EAF9FF', GY)
    small_sun(cr, t, 150, 400, 0.55)
    clouds(cr, t, ((520, 360, 0.45), (950, 560, 0.35), (300, 640, 0.3)), 10)
    hills(cr, 1250, '#A6E58A', 40)
    bush(cr, 520, 1290, 0.7)
    ground(cr, GY, '#7CD35F', '#4AAE42')
    # snail: hidden behind tree until found (shell + antennae peek)
    sx, sy = SPOTS['snail']
    if not found(1, te, m):
        cr.save(); cr.translate(762, GY - 5); cr.scale(-1.2, 1.2); draw_snail(cr, 0, 0, t); cr.restore()
    big_tree(cr, t)
    if found(1, te, m):
        e = ease_out_back((te - m['r1']) / 0.5)
        x = lerp(780, 640, e)
        cr.save(); cr.translate(x, GY + 5); cr.scale(-1.25, 1.25); draw_snail(cr, 0, 0, t); cr.restore()
    big_flower(cr, t)
    # butterfly sits on the flower (folded wings) then flutters up
    bx, by = SPOTS['bfly']
    if not found(2, te, m):
        cr.save(); cr.translate(bx, by - 30); cr.scale(0.55, 0.55)
        draw_bfly(cr, 0, 0, 0.12 + 0.02 * math.sin(t * 2), 0, 1.0); cr.restore()
    elif te < m['x2']:
        e = ease_out_back((te - m['r2']) / 0.4)
        draw_bfly(cr, bx, by - 40 - 10 * abs(math.sin(t * 4)), t, 0.05 * math.sin(t * 2), 0.55 + 0.25 * e)
    else:
        u = te - m['x2']; e = ease_io(clamp(u / 0.8))
        x = bx + 120 * e + 30 * math.sin(t * 2.5) * e; y = by - 60 - 180 * e + 20 * math.sin(t * 3.1)
        draw_bfly(cr, x, y, t, 0.1 * math.sin(t * 2), 0.8)
    # frog under the bench
    fxs, fys = SPOTS['frog']
    bench(cr)
    if not found(0, te, m):
        cr.save(); cr.rectangle(80, 1500, 400, 120); cr.clip()
        cr.translate(fxs, 1560 + 40); cr.scale(0.42, 0.42); obj_frog(cr, 1); cr.restore()
    else:
        u = te - m['r0']; h = 160 * math.sin(math.pi * clamp(u / 0.6)) if u < 0.6 else 0
        x = lerp(fxs, 340, ease_io(clamp(u / 0.6)))
        shadow_at(cr, x, 1745, 60)
        cr.save(); cr.translate(x, 1685 - h); cr.scale(0.45, 0.45); obj_frog(cr, 1); cr.restore()
    # apple with worm
    big_apple(cr, t)
    hx, hy = 820 + 40 * 0.85, 1640 + 20 * 0.85
    if not found(3, te, m):
        cr.save(); ellipse(cr, hx, hy, 34, 29); cr.clip(); worm(cr, hx, hy + 30, 0.25, t); cr.restore()
    else:
        e = ease_out_back((te - m['r3']) / 0.5)
        worm(cr, hx, hy + 30, 0.2 + 0.8 * e, t, happy=True)
    for i, (x, y, c, s) in enumerate(FLW): draw_flower(cr, x, y, s, hexc(c), t, i)
    # chickpea
    st = chick_talk(base_st(), te, TL); look = (0.0, -0.3); h = 0; sxx = syy = 1
    for i, r in enumerate(ROUNDS):
        if m[f'c{i}'] <= te < m[f'r{i}']: look = (math.sin(te * 2.0), -0.3)
        if m[f'r{i}'] <= te < m[f'x{i}']:
            px, py = SPOTS[r['k']]; look = (clamp((px - 540) / 300, -1, 1), -0.6)
            h, sxx, syy, air = hop_seq(te, m[f'r{i}'] + 0.4, 2, 0.45, 50); st.update(happy=1, wing=[0.3 + 0.8 * air] * 2)
    cx, cb = 540, 1770
    hidden = smooth(m['hide'] + 0.8, m['hide'] + 1.2, te) * (1 - smooth(m['r4'], m['r4'] + 0.25, te))
    shadow_at(cr, cx, cb + 3, 100)
    if hidden < 0.02:
        chick(cr, cx, cb, h, 0.78, st, te, look, sxx, syy, acc='explorer')
        if m['r4'] <= te < m['r4'] + 0.9:
            u = te - m['r4']
            cr.save(); cr.translate(cx + 260 * u, cb - 260 - 500 * u + 700 * u * u); cr.rotate(5 * u); cr.scale(0.78, 0.78)
            cr.translate(0, 165); shell_part(cr, top=True); cr.restore()
    else:
        wob = 0.05 * math.sin(te * 14) * (1 if m['c4'] <= te else 0.3)
        cr.save(); cr.translate(cx, cb); cr.rotate(wob); cr.scale(0.78, 0.78)
        if hidden < 0.99:
            cr.push_group(); draw_body(cr, 0, -215 * (1 - 0.5 * hidden), 1.0 - 0.3 * hidden, st, te, look); cr.pop_group_to_source(); cr.paint_with_alpha(1 - hidden)
        draw_egg(cr, 1.0)
        cr.restore()
        if hidden < 0.98:
            u = 1 - hidden
            cr.save(); cr.translate(cx, cb - 600 * u); cr.scale(0.78, 0.78); cr.translate(0, 0); cr.restore()


def frame(cr, t):
    m = TL['marks']
    te = 0.0 if t >= m['loop'] else t
    z, cx, cy = cam(te, m)
    cx = clamp(cx, 540 / z, 1080 - 540 / z); cy = clamp(cy, 1100 / z, 1920 - 820 / z)
    cr.save(); cr.translate(540, 1100); cr.scale(z, z); cr.translate(-cx, -cy)
    world(cr, t, te, m)
    cr.restore()
    for i, r in enumerate(ROUNDS):
        count_bubble(cr, m[f'c{i}'], te, "Point to it!", w=560)
        word_pop(cr, r['w'], 540, 480, 170, r['c'], m[f'r{i}'] + 0.3, m[f'x{i}'], te)
    count_bubble(cr, m['c4'], te, "Look!", dur=2.0)
    word_pop(cr, "IN!", 540, 480, 170, '#FFB400', m['r4'] + 0.3, m['again'], te)
    draw_text(cr, "Hide and Seek!", 250, 135, t, -1)
    loop_fade(cr, TL, t)

if __name__ == '__main__': episode_main(build, F)
