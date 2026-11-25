import cairo, math, random, sys

W, H, FPS = 1080, 1920, 30
OUT = (0.23, 0.16, 0.12)
LW = 6

def hexc(h):
    h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))

YEL = hexc('#FFD93B'); YEL2 = hexc('#FFC71F'); BEAK = hexc('#FF9A1F')
EGG = hexc('#FFF6E5'); EGGSPOT = hexc('#FFE1B0')
PINK = hexc('#FF7EB6'); PURP = hexc('#B57BFF'); BDARK = hexc('#4A2D6B')
LEAF = hexc('#5BC85B'); LEAFD = hexc('#3E9E45')

def lerp(a, b, t): return a + (b - a) * t
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease_io(t): t = clamp(t); return t * t * (3 - 2 * t)
def ease_out_back(t, s=1.9):
    t = clamp(t) - 1; return t * t * ((s + 1) * t + s) + 1
def smooth(a, b, t): return ease_io((t - a) / (b - a))
def mixc(c1, c2, t): return tuple(lerp(a, b, t) for a, b in zip(c1, c2))

def gloom(t): return smooth(14.2, 15.2, t) * (1 - smooth(17.7, 19.0, t))
def rain_amt(t): return smooth(14.8, 15.4, t) * (1 - smooth(17.5, 18.3, t))

def yf(x): return 1490 + 28 * math.sin(2 * math.pi * x / 1080 * 0.9 + 0.8)
def yb(x): return 1330 - 60 * math.sin(math.pi * x / 1080 * 1.3 + 0.2)

def ellipse(cr, cx, cy, rx, ry):
    cr.save(); cr.translate(cx, cy); cr.scale(rx, ry); cr.arc(0, 0, 1, 0, 2 * math.pi); cr.restore()

def fs(cr, fill, lw=LW, stroke=OUT, alpha=1.0):
    cr.set_source_rgba(*fill, alpha); cr.fill_preserve()
    cr.save(); cr.identity_matrix(); cr.set_line_width(lw)
    cr.set_line_join(cairo.LINE_JOIN_ROUND); cr.set_source_rgb(*stroke); cr.stroke(); cr.restore()

def stroke_dev(cr, col, lw, alpha=1.0, cap=cairo.LINE_CAP_ROUND):
    cr.save(); cr.identity_matrix(); cr.set_line_width(lw); cr.set_line_cap(cap)
    cr.set_line_join(cairo.LINE_JOIN_ROUND); cr.set_source_rgba(*col, alpha); cr.stroke(); cr.restore()

rnd = random.Random(7)
GRASS = [(x + rnd.uniform(-5, 5), rnd.uniform(28, 52), rnd.uniform(0, 6)) for x in range(-10, 1100, 13)]
CLOUDS = [(150, 520, 0.8), (620, 700, 0.6), (980, 450, 0.7)]
DROPS = [(rnd.uniform(-100, 1250), rnd.uniform(1500, 2100), rnd.uniform(0, 2300), rnd.uniform(35, 60)) for _ in range(170)]
SPARK = [(rnd.uniform(60, 1020), rnd.uniform(650, 1350), rnd.uniform(0, 6.28), rnd.uniform(0.6, 1.2)) for _ in range(16)]
POP_FLOWERS = [(90, '#FF5A5F'), (215, '#A66CFF'), (330, '#2EA7FF'), (760, '#FF7EB6'),
               (880, '#FFB400'), (1000, '#FF5A5F'), (440, '#FFFFFF'), (650, '#A66CFF')]
STATIC_FLOWERS = [(40, '#FFFFFF'), (1045, '#FF7EB6')]
FG_FLOWERS = [(120, 1790, '#FFB400', 1.15), (300, 1700, '#FFFFFF', 0.85), (860, 1720, '#FF5A5F', 1.0), (990, 1820, '#A66CFF', 1.2), (620, 1830, '#FF7EB6', 0.9)]
TITLE_COLS = [hexc(c) for c in ('#FF5A5F', '#FFB400', '#3ECF8E', '#2EA7FF', '#A66CFF', '#FF7EB6')]


SPLASH = [(rnd.uniform(30, 1050), rnd.uniform(30, 400), rnd.uniform(0, 1)) for _ in range(30)]
def yfar(x): return 1250 - 45 * math.sin(math.pi * x / 1080 * 2 + 1)

def tree(cr, x, y, s, col):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.rectangle(-16, -120, 32, 120); fs(cr, hexc('#9B6B43'))
    blobs = [(-55, -150, 62), (55, -150, 62), (0, -205, 72), (0, -140, 60)]
    for bx, by, r in blobs: cr.arc(bx, by, r, 0, 2*math.pi); cr.new_sub_path()
    stroke_dev(cr, OUT, 12)
    for bx, by, r in blobs: cr.arc(bx, by, r, 0, 2*math.pi); cr.new_sub_path()
    cr.set_source_rgb(*hexc(col)); cr.fill()
    for bx, by, r in ((-30, -215, 18), (40, -170, 14), (-60, -150, 12)):
        cr.arc(bx, by, r, 0, 2*math.pi); cr.set_source_rgba(1, 1, 1, 0.25); cr.fill()
    for ax, ay in ((-40, -130), (35, -200), (20, -120), (-70, -175)):
        cr.arc(ax, ay, 11, 0, 2*math.pi); fs(cr, hexc('#FF5A5F'), 4)
    cr.restore()

def bush(cr, x, y, s):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    bl = [(-50, -30, 45), (0, -55, 55), (50, -30, 45)]
    for bx, by, r in bl: cr.arc(bx, by, r, 0, 2*math.pi); cr.new_sub_path()
    stroke_dev(cr, OUT, 10)
    for bx, by, r in bl: cr.arc(bx, by, r, 0, 2*math.pi); cr.new_sub_path()
    cr.set_source_rgb(*hexc('#46A845')); cr.fill()
    for bx, by in ((-40, -45), (10, -75), (45, -40)):
        cr.arc(bx, by, 8, 0, 2*math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()
        cr.arc(bx, by, 3.5, 0, 2*math.pi); cr.set_source_rgb(1, 0.85, 0.2); cr.fill()
    cr.restore()

def draw_snail(cr, x, y, t):
    cr.save(); cr.translate(x, y); cr.scale(1 + 0.05 * math.sin(t * 6), 1)
    cr.move_to(75, 0); cr.curve_to(40, -22, -40, -24, -60, -20); cr.curve_to(-85, -18, -90, 0, -70, 0); cr.close_path()
    fs(cr, hexc('#F7CF92'))
    for s, (bx, by, ex, ey) in enumerate(((-62, -30, -76, -72), (-48, -30, -48, -70))):
        cr.move_to(bx, by); cr.line_to(ex, ey + 3 * math.sin(t * 4 + s)); stroke_dev(cr, OUT, 5)
        cr.arc(ex, ey + 3 * math.sin(t * 4 + s), 9, 0, 2*math.pi); fs(cr, (1, 1, 1), 4)
        cr.arc(ex - 2, ey + 3 * math.sin(t * 4 + s), 4, 0, 2*math.pi); cr.set_source_rgb(*OUT); cr.fill()
    cr.arc(-62, -14, 10, 0.2, math.pi - 0.2); stroke_dev(cr, OUT, 4)
    cr.arc(10, -42, 44, 0, 2*math.pi); fs(cr, hexc('#FF8FA3'))
    for k, r in enumerate((32, 22, 12)):
        cr.arc(10 + k * 3, -42 + k * 2, r, 0.3, 2*math.pi - 0.6); stroke_dev(cr, hexc('#D9536E'), 5)
    cr.restore()

# ---------------- choreography ----------------
P = [540, 360, 560, 740, 560, 360, 540]

def hop(t, t0, dur, height, x0, x1):
    u = (t - t0) / dur
    if u < 0.15:
        p = u / 0.15; return x0, 0, 1 + 0.12 * math.sin(math.pi * p), 1 - 0.18 * math.sin(math.pi * p), 0, 0
    if u < 0.8:
        p = (u - 0.15) / 0.65
        st = 1 - abs(2 * p - 1)
        return lerp(x0, x1, ease_io(p)), height * 4 * p * (1 - p), 1 - 0.06 * st, 1 + 0.10 * st, \
            (x1 - x0) * 0.0006 * math.sin(math.pi * p), math.sin(math.pi * p)
    p = (u - 0.8) / 0.2
    return x1, 0, 1 + 0.14 * math.sin(math.pi * p), 1 - 0.2 * math.sin(math.pi * p), 0, 0

def chickX_S2(t):
    if t <= 7 or t >= 13: return 540
    k = int(t - 7); u = (t - 7) - k
    return lerp(P[k], P[k + 1], ease_io((u - 0.15) / 0.65))

def burst(a, b, t): return math.sin(math.pi * clamp((t - a) / (b - a)))
def wobble_amp(t): return 0.10 * burst(1.2, 1.8, t) + 0.14 * burst(2.4, 3.0, t) + 0.2 * burst(3.3, 4.4, t)

LEAF_Y = 1060

def bfly_path(t): return chickX_S2(t + 0.7) + 40, 900 + 55 * math.sin(t * 3.1)
def circ13(t): a = 3 * (t - 13); return 540 + 190 * math.cos(a), 960 + 50 * math.sin(2 * a)
def hover(t): return 540 + 15 * math.sin(t * 2.5), LEAF_Y - 125 + 8 * math.sin(t * 4)
def orbit(t): a = 1.7 * (t - 19.4); return 540 + 240 * math.cos(a), 1010 + 90 * math.sin(2 * a)

def bfly(t):
    """returns (x, y) or None, and leaf (x, y, rot, alpha) or None"""
    leaf = None
    if t < 6.0: return None, None
    if t < 7.0:
        q = ease_io(t - 6); px, py = bfly_path(t); return (lerp(1250, px, q), lerp(880, py, q)), None
    if t < 13: return bfly_path(t), None
    if t < 14.0:
        q = ease_io((t - 13) / 0.6); a = bfly_path(t); b = circ13(t)
        return (lerp(a[0], b[0], q), lerp(a[1], b[1], q)), None
    if t < 14.9:
        q = ease_io((t - 14.0) / 0.9); a = circ13(14.0)
        return (lerp(a[0], -200, q), lerp(a[1], 760, q)), None
    if t < 15.6: return None, None
    if t < 16.4:
        q = ease_io((t - 15.6) / 0.8); h = hover(16.4)
        x, y = lerp(-220, h[0], q), lerp(880, h[1], q) - 60 * math.sin(math.pi * q)
        return (x, y), (x, y + 125, 0.15 * (1 - q), 1)
    if t < 18.6:
        x, y = hover(t); return (x, y), (x, y + 125, 0, 1)
    h = hover(18.6)
    u = t - 18.6
    leaf = (h[0] + 260 * u, h[1] + 125 - 420 * u, 0.7 * u, 1 - smooth(18.8, 19.7, t)) if t < 19.8 else None
    if t < 19.4:
        q = ease_io(u / 0.8); a = hover(t); b = orbit(19.4)
        return (lerp(a[0], b[0], q), lerp(a[1], b[1], q)), leaf
    return orbit(t), leaf

def chick_state(t):
    st = dict(x=540, h=0, sx=1, sy=1, rot=0, phase='chick', crack=0, hatch=1, mood=0,
              wing=[0, 0], beak=0, happy=0, shiver=0)
    if t < 4.5:
        st['phase'] = 'egg'
        st['rot'] = wobble_amp(t) * math.sin(18 * t)
        st['crack'] = clamp((t - 3.6) / 0.8)
    else:
        st['hatch'] = (t - 4.5) / 0.5
        surprise = 0.9 * (1 - smooth(5.0, 5.7, t)) * smooth(4.55, 4.8, t)
        st['wing'] = [surprise, surprise]
        st['beak'] = 0.8 * burst(4.85, 5.15, t) + 0.8 * burst(6.3, 6.6, t)
    if 7 <= t < 13:
        k = int(t - 7)
        x, h, sx, sy, rot, air = hop(t, 7 + k, 1.0, 260, P[k], P[k + 1])
        st.update(x=x, h=h, sx=sx, sy=sy, rot=rot)
        st['wing'] = [0.6 * air, 0.6 * air]
    # rain
    covered = smooth(16.0, 16.4, t)
    st['mood'] = smooth(14.9, 15.3, t) * (1 - 0.6 * covered) * (1 - smooth(18.0, 18.6, t))
    st['shiver'] = rain_amt(t) * (1 - covered)
    if 15.0 < t < 18.6:
        st['beak'] = 0
    # celebrate
    if 20.2 <= t < 24.1: st['happy'] = 1
    if 21.0 <= t < 24.0:
        k = int((t - 21.0) / 0.5)
        x, h, sx, sy, rot, air = hop(t, 21.0 + 0.5 * k, 0.5, 90, 540, 540)
        st.update(h=h, sx=sx, sy=sy)
        st['wing'] = [0.3 + 0.8 * air, 0.3 + 0.8 * air]
        st['beak'] = 0.7 * air
    if t >= 24.1:
        st['wing'] = [0.0, 1.1 + 0.45 * math.sin(t * 13)]
        st['beak'] = 0.6 * burst(24.3, 24.8, t) + 0.6 * burst(25.0, 25.5, t)
    st['by'] = yf(st['x']) + 25
    return st

# ---------------- drawing ----------------
ZIG = [(-160, -150)] + [(-135 + 30 * i, -150 + (18 if i % 2 == 0 else -18)) for i in range(10)] + [(160, -150)]

def zig_path(cr):
    cr.move_to(*ZIG[0])
    for p in ZIG[1:]: cr.line_to(*p)

def egg_spots(cr):
    for (sx, sy, r) in ((-60, -230, 16), (40, -270, 11), (70, -120, 14), (-45, -90, 10), (10, -180, 9)):
        cr.arc(sx, sy, r, 0, 2 * math.pi); cr.set_source_rgb(*EGGSPOT); cr.fill()

def draw_egg(cr, crack):
    ellipse(cr, 0, -165, 130, 165); fs(cr, EGG)
    cr.save(); ellipse(cr, 0, -165, 127, 162); cr.clip(); egg_spots(cr); cr.restore()
    if crack > 0:
        n = len(ZIG); mid = n / 2
        pts = [p for i, p in enumerate(ZIG[1:-1]) if abs(i + 1 - mid) <= crack * mid]
        if len(pts) > 1:
            cr.move_to(*pts[0])
            for p in pts[1:]: cr.line_to(*p)
            stroke_dev(cr, OUT, 5)

def shell_part(cr, top):
    cr.save()
    zig_path(cr)
    if top: cr.line_to(160, -400); cr.line_to(-160, -400)
    else: cr.line_to(160, 20); cr.line_to(-160, 20)
    cr.close_path(); cr.clip()
    ellipse(cr, 0, -165, 130, 165); fs(cr, EGG)
    cr.save(); ellipse(cr, 0, -165, 127, 162); cr.clip(); egg_spots(cr); cr.restore()
    cr.restore()
    cr.save(); ellipse(cr, 0, -165, 131, 166); cr.clip()
    zig_path(cr); stroke_dev(cr, OUT, LW)
    cr.restore()

def draw_body(cr, cx, cy, sc, st, t, look):
    cr.save(); cr.translate(cx, cy); cr.scale(sc, sc)
    R = 120
    for i, s in enumerate((-1, 1)):
        cr.save(); cr.translate(s * 104, 20)
        cr.rotate(s * (-0.35 + st['wing'][i]))
        ellipse(cr, 0, 22, 32, 50); fs(cr, YEL2)
        cr.restore()
    for a in (-0.45, 0, 0.45):
        cr.save(); cr.translate(0, -R + 10); cr.rotate(a); ellipse(cr, 0, -26, 12, 28); fs(cr, YEL); cr.restore()
    cr.arc(0, 0, R, 0, 2 * math.pi); fs(cr, YEL)
    ellipse(cr, 0, 48, 72, 52); cr.set_source_rgba(1, 0.96, 0.7, 0.7); cr.fill()
    for s in (-1, 1):
        ellipse(cr, s * 74, 22, 22, 14); cr.set_source_rgba(1, 0.45, 0.5, 0.45); cr.fill()
    lx, ly = look
    blink = (t % 3.3) < 0.13 and t > 5.3
    for s in (-1, 1):
        ex, ey = s * 40 + lx * 12, -22 + ly * 9
        if st['happy'] > 0.5:
            cr.arc(ex, ey + 8, 16, math.pi * 1.1, math.pi * 1.9); stroke_dev(cr, OUT, 7)
        elif blink:
            cr.move_to(ex - 15, ey); cr.line_to(ex + 15, ey); stroke_dev(cr, OUT, 6)
        else:
            cr.arc(ex, ey, 17, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill()
            cr.arc(ex - 5, ey - 6, 6, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()
            cr.arc(ex + 6, ey + 6, 2.5, 0, 2 * math.pi); cr.fill()
        if st['mood'] > 0.02:
            cr.move_to(s * 20, -58); cr.line_to(s * 58, -46); stroke_dev(cr, OUT, 6, st['mood'])
    op = st['beak'] * 16
    cr.move_to(-22, 12); cr.line_to(0, -4); cr.line_to(22, 12); cr.close_path(); fs(cr, BEAK, 5)
    if op > 1:
        cr.move_to(-16, 13); cr.line_to(16, 13); cr.line_to(0, 13 + op); cr.close_path()
        cr.set_source_rgb(0.75, 0.2, 0.25); cr.fill()
    cr.move_to(-22, 12 + op); cr.line_to(22, 12 + op); cr.line_to(0, 28 + op); cr.close_path(); fs(cr, BEAK, 5)
    cr.restore()

def draw_chick(cr, st, t, look):
    cr.save()
    sh = math.sin(t * 45) * 4 * st['shiver']
    cr.translate(st['x'] + sh, st['by'] - st['h'])
    cr.rotate(st['rot']); cr.scale(st['sx'], st['sy'])
    if st['phase'] == 'egg':
        draw_egg(cr, st['crack'])
    else:
        u = st['hatch']
        rise = ease_out_back(u)
        cy = lerp(-110, -215, rise)
        sc = lerp(0.6, 1.0, rise)
        draw_body(cr, 0, cy, sc, st, t, look)
        shell_part(cr, top=False)
    cr.restore()
    # flying top shell
    if 4.5 <= t < 5.5:
        u = t - 4.5; a = 1 - smooth(0.55, 0.9, u)
        if a > 0:
            cr.push_group()
            cr.translate(540 + 380 * u, yf(540) + 25 - 650 * u + 500 * u * u)
            cr.rotate(4 * u)
            shell_part(cr, top=True)
            cr.pop_group_to_source(); cr.paint_with_alpha(a)

def draw_bfly(cr, x, y, t, tilt=0, sc=1.0):
    cr.save(); cr.translate(x, y); cr.rotate(tilt); cr.scale(sc, sc)
    f = 0.25 + 0.75 * abs(math.sin(t * 13))
    for s in (-1, 1):
        cr.save(); cr.scale(s * f, 1)
        cr.save(); cr.translate(48, -22); cr.rotate(-0.5); ellipse(cr, 0, 0, 52, 40); fs(cr, PINK); cr.restore()
        ellipse(cr, 58, -26, 16, 13); cr.set_source_rgba(1, 0.85, 0.93, 1); cr.fill()
        cr.save(); cr.translate(36, 26); cr.rotate(0.5); ellipse(cr, 0, 0, 34, 28); fs(cr, PURP); cr.restore()
        ellipse(cr, 40, 28, 9, 8); cr.set_source_rgba(1, 1, 1, 0.8); cr.fill()
        cr.restore()
    ellipse(cr, 0, 8, 10, 36); fs(cr, BDARK, 5)
    for s in (-1, 1):
        cr.move_to(s * 5, -44); cr.curve_to(s * 12, -70, s * 26, -78, s * 30, -74); stroke_dev(cr, OUT, 4)
        cr.arc(s * 30, -74, 6, 0, 2 * math.pi); cr.set_source_rgb(*PINK); cr.fill()
    cr.arc(0, -36, 16, 0, 2 * math.pi); fs(cr, BDARK, 5)
    for s in (-1, 1):
        cr.arc(s * 6, -38, 3.5, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()
    cr.restore()

def draw_leaf(cr, x, y, rot, alpha):
    cr.push_group()
    cr.translate(x, y); cr.rotate(rot)
    cr.move_to(0, -62); cr.line_to(0, -112); stroke_dev(cr, LEAFD, 9)
    cr.move_to(-160, 10); cr.curve_to(-110, -95, 110, -95, 160, 10)
    cr.curve_to(90, -12, -90, -12, -160, 10); cr.close_path(); fs(cr, LEAF)
    cr.move_to(0, -66); cr.line_to(0, -8); stroke_dev(cr, LEAFD, 5)
    for s in (-1, 1):
        for k in (40, 85):
            cr.move_to(0, -60 + k * 0.35); cr.line_to(s * k, -40 + k * 0.45); stroke_dev(cr, LEAFD, 4)
    cr.pop_group_to_source(); cr.paint_with_alpha(alpha)

def draw_cloud(cr, x, y, sc, col, outline=True, face=0.0):
    circ = [(-170, 25, 85), (-70, -40, 115), (70, -35, 110), (175, 20, 88), (0, 45, 105), (-110, 55, 70), (110, 55, 75)]
    cr.save(); cr.translate(x, y); cr.scale(sc, sc)
    if outline:
        for cx, cy, r in circ:
            cr.arc(cx, cy, r, 0, 2 * math.pi); cr.new_sub_path()
        stroke_dev(cr, OUT, 12)
    for cx, cy, r in circ:
        cr.arc(cx, cy, r, 0, 2 * math.pi); cr.new_sub_path()
    cr.set_source_rgba(*col, 1 if outline else 0.92); cr.fill()
    if face > 0:
        for s in (-1, 1):
            cr.arc(s * 50, 10, 18, math.pi * 0.1, math.pi * 0.9); stroke_dev(cr, OUT, 7, face)
        cr.arc(0, 75, 22, math.pi * 1.15, math.pi * 1.85); stroke_dev(cr, OUT, 6, face)
    cr.restore()

def draw_sun(cr, t):
    cx, cy, R = 870, 270, 95
    cr.save(); cr.translate(cx, cy); cr.rotate(t * 0.4)
    for i in range(12):
        a = i * math.pi / 6
        cr.save(); cr.rotate(a)
        cr.move_to(-16, -R - 18); cr.line_to(0, -R - 62 - 8 * math.sin(t * 3 + i)); cr.line_to(16, -R - 18); cr.close_path()
        cr.set_source_rgb(1, 0.72, 0.1); cr.fill(); cr.restore()
    cr.restore()
    cr.arc(cx, cy, R, 0, 2 * math.pi); fs(cr, hexc('#FFE14D'))
    for s in (-1, 1):
        cr.arc(cx + s * 32, cy - 12, 14, math.pi * 1.1, math.pi * 1.9); stroke_dev(cr, OUT, 6)
        ellipse(cr, cx + s * 55, cy + 18, 16, 10); cr.set_source_rgba(1, 0.5, 0.3, 0.45); cr.fill()
    cr.arc(cx, cy + 15, 30, math.pi * 0.15, math.pi * 0.85); stroke_dev(cr, OUT, 6)

def draw_flower(cr, x, y, sc, col, t, seed):
    if sc <= 0.01: return
    cr.save(); cr.translate(x, y); cr.rotate(math.sin(t * 2.2 + seed) * 0.08); cr.scale(sc, sc)
    cr.move_to(0, 0); cr.curve_to(6, -30, -6, -60, 0, -92); stroke_dev(cr, LEAFD, 7 * min(1, sc))
    cr.save(); cr.translate(10, -40); cr.rotate(-0.6); ellipse(cr, 14, 0, 18, 8); cr.set_source_rgb(*LEAF); cr.fill(); cr.restore()
    for i in range(5):
        a = i * 2 * math.pi / 5 + seed
        cr.arc(24 * math.cos(a), -95 + 24 * math.sin(a), 19, 0, 2 * math.pi); cr.new_sub_path()
    cr.set_source_rgb(*col); cr.fill_preserve(); stroke_dev(cr, OUT, 4 * min(1, sc))
    cr.arc(0, -95, 14, 0, 2 * math.pi); fs(cr, hexc('#FFD93B'), 4 * min(1, sc))
    cr.restore()

def star(cr, x, y, r):
    cr.move_to(x, y - r)
    for i in range(1, 8):
        a = i * math.pi / 4; rr = r if i % 2 == 0 else r * 0.3
        cr.line_to(x + rr * math.sin(a), y - rr * math.cos(a))
    cr.close_path()

def draw_text(cr, text, cy, size, t, t_in, t_out=None, fade=0.4):
    a = 1.0 if t_out is None else 1 - smooth(t_out, t_out + fade, t)
    if t < t_in or a <= 0: return
    cr.push_group()
    cr.select_font_face("Nunito ExtraLight", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(size)
    advs = [cr.text_extents(ch).x_advance for ch in text]
    total = sum(advs); k = min(1.0, 980 / total)
    cr.set_font_size(size * k); advs = [v * k for v in advs]; total *= k
    x = 540 - total / 2
    paths = []
    for i, ch in enumerate(text):
        loc = t - t_in - i * 0.05
        s = ease_out_back(loc / 0.4) if loc > 0 else 0
        if s > 0 and ch != ' ':
            bob = math.sin(t * 5 - i * 0.6) * 10
            cr.save(); cr.translate(x + advs[i] / 2, cy + bob); cr.scale(s, s)
            cr.move_to(-advs[i] / 2, size * k * 0.36); cr.text_path(ch); cr.restore()
            p = cr.copy_path(); cr.new_path(); paths.append((p, TITLE_COLS[i % len(TITLE_COLS)]))
        x += advs[i]
    for p, c in paths:
        cr.append_path(p); stroke_dev(cr, hexc('#3B2A6B'), 20)
    for p, c in paths:
        cr.append_path(p); cr.set_source_rgb(*c); cr.fill()
    cr.pop_group_to_source(); cr.paint_with_alpha(a)

def frame(cr, t):
    g = gloom(t)
    grad = cairo.LinearGradient(0, 0, 0, 1400)
    grad.add_color_stop_rgb(0, *mixc(hexc('#5EC8FF'), hexc('#7A8794'), g))
    grad.add_color_stop_rgb(1, *mixc(hexc('#CFF3FF'), hexc('#B0B9C0'), g))
    cr.set_source(grad); cr.paint()
    cr.save(); cr.translate(870, 270); cr.rotate(t * 0.05)
    for i in range(16):
        a = i * 2 * math.pi / 16
        cr.move_to(0, 0); cr.arc(0, 0, 2600, a, a + math.pi / 30); cr.close_path()
    cr.set_source_rgba(1, 1, 0.9, (0.09 + 0.06 * smooth(19, 20.5, t)) * (1 - g)); cr.fill(); cr.restore()
    draw_sun(cr, t)
    for i, (cx, cy, s) in enumerate(CLOUDS):
        x = (cx + t * (14 + 6 * i) + 300) % 1500 - 300
        draw_cloud(cr, x, cy, s * 0.6, (1, 1, 1), outline=False)
    for i, (by, sp, ph) in enumerate(((420, 120, 0), (470, 120, 60), (390, 110, 130))):
        bx = -100 + sp * t + ph
        if -60 < bx < 1140 and t < 12:
            f = 18 * math.sin(t * 9 + i)
            cr.move_to(bx - 22, by - f * 0.5); cr.curve_to(bx - 10, by - 14, bx - 4, by - 4, bx, by)
            cr.curve_to(bx + 4, by - 4, bx + 10, by - 14, bx + 22, by - f * 0.5); stroke_dev(cr, OUT, 4)
    # rainbow
    p = smooth(19.8, 21.0, t)
    if p > 0:
        cols = ['#FF5A5F', '#FF9F1C', '#FFE14D', '#3ECF8E', '#2EA7FF', '#A66CFF']
        for i, c in enumerate(cols):
            cr.arc(540, 1560, 760 - i * 44, math.pi, math.pi + math.pi * p)
            stroke_dev(cr, hexc(c), 46, 0.95, cairo.LINE_CAP_BUTT)
    # rain cloud
    if 13.9 < t < 19.0:
        cx = lerp(1550, 560, ease_io((t - 13.9) / 1.1)) if t < 17.6 else lerp(560, -650, ease_io((t - 17.6) / 1.3))
        draw_cloud(cr, cx, 330 + 10 * math.sin(t * 2), 1.25, hexc('#8E99A6'), face=1.0)
    dk0 = lerp(1, 0.78, g)
    cr.move_to(0, H)
    for x in range(0, W + 21, 20): cr.line_to(x, yfar(x))
    cr.line_to(W, H); cr.close_path(); cr.set_source_rgb(*(v * dk0 for v in hexc('#C4EDB0'))); cr.fill()
    # hills
    dk = lerp(1, 0.78, g)
    cr.move_to(0, H)
    for x in range(0, W + 21, 20): cr.line_to(x, yb(x))
    cr.line_to(W, H); cr.close_path(); cr.set_source_rgb(*(v * dk for v in hexc('#8EDB6A'))); cr.fill()
    tree(cr, 95, yb(95) + 40, 0.8, '#4CB944'); tree(cr, 990, yb(990) + 45, 0.9, '#5DC85A')
    bush(cr, 230, yb(230) + 40, 0.7); bush(cr, 850, yb(850) + 45, 0.65)
    cr.move_to(0, H)
    for x in range(0, W + 21, 20): cr.line_to(x, yf(x))
    cr.line_to(W, H); cr.close_path()
    hg = cairo.LinearGradient(0, 1450, 0, H)
    hg.add_color_stop_rgb(0, *(v * dk for v in hexc('#5FC44A'))); hg.add_color_stop_rgb(1, *(v * dk for v in hexc('#3E9E3A')))
    cr.set_source(hg); cr.fill()
    for x, h, ph in GRASS:
        y = yf(x) + 4; sw = math.sin(t * 2 + x * 0.02 + ph) * 6
        cr.move_to(x - 7, y); cr.line_to(x + sw, y - h); cr.line_to(x + 7, y); cr.close_path()
    cr.set_source_rgb(*(v * dk for v in hexc('#4DB23C'))); cr.fill()
    for i, (x, c) in enumerate(STATIC_FLOWERS):
        draw_flower(cr, x, yf(x) + 30, 0.9, hexc(c), t, i * 1.3)
    for i, (x, c) in enumerate(POP_FLOWERS):
        s = ease_out_back((t - (20.3 + 0.15 * i)) / 0.45) if t > 20.3 + 0.15 * i else 0
        draw_flower(cr, x, yf(x) + 40, s * (0.95 if i < 6 else 0.8), hexc(c), t, i * 1.7)
    for i, (x, y, c, sc) in enumerate(FG_FLOWERS):
        draw_flower(cr, x, y, sc, hexc(c), t, i * 2.1 + 0.5)
    for i, x in enumerate((210, 470, 760, 1040)):
        y = 1640 + 70 * (i % 2)
        for j in range(-4, 5):
            cr.move_to(x + j * 9 - 6, y); cr.line_to(x + j * 14 + math.sin(t * 2 + j) * 5, y - 50 + abs(j) * 6); cr.line_to(x + j * 9 + 6, y); cr.close_path()
        cr.set_source_rgb(*(v * dk for v in hexc('#3E9E3A'))); cr.fill()
    draw_snail(cr, lerp(1180, -140, t / 26), 1775, t)
    # characters
    st = chick_state(t)
    bpos, leaf = bfly(t)
    head = (st['x'], st['by'] - st['h'] - 215)
    if bpos:
        dx, dy = bpos[0] - head[0], bpos[1] - head[1]; d = math.hypot(dx, dy) + 1e-6
        look = (dx / d, dy / d)
    elif rain_amt(t) > 0.1: look = (0, -0.8)
    else: look = (0, 0.1)
    sha = max(0.2, 1 - st['h'] / 350)
    ellipse(cr, st['x'], st['by'] + 2, 115 * sha, 20 * sha); cr.set_source_rgba(0.1, 0.25, 0.05, 0.22 * sha); cr.fill()
    draw_chick(cr, st, t, look)
    if leaf: draw_leaf(cr, *leaf)
    if bpos:
        for k in range(1, 8):
            pp, _ = bfly(t - k * 0.06)
            if pp:
                star(cr, pp[0], pp[1] + 20, 14 * (1 - k / 8)); cr.set_source_rgba(1, 0.95, 0.6, 0.7 * (1 - k / 8)); cr.fill()
        tilt = 0.25 * math.sin(t * 3) if t > 6 else 0
        draw_bfly(cr, bpos[0], bpos[1], t, tilt, 0.95)
    # gloom overlay
    if g > 0: cr.set_source_rgba(0.12, 0.17, 0.28, 0.25 * g); cr.paint()
    # rain
    r = rain_amt(t)
    if r > 0:
        for x0, sp, ph, ln in DROPS:
            y = (ph + t * sp) % 2300 - 150; x = x0 - 0.18 * y
            if leaf and leaf[3] > 0.5 and abs(x - leaf[0]) < 165 and y > leaf[1] - 60: continue
            cr.move_to(x, y); cr.line_to(x + 0.18 * ln, y - ln)
        stroke_dev(cr, hexc('#D6F0FF'), 5, 0.85 * r)
        for sx, sy, ph in SPLASH:
            u = (t * 2.2 + ph) % 1
            yy = yf(sx) + sy
            ellipse(cr, sx, yy, 8 + 30 * u, 3 + 9 * u); stroke_dev(cr, hexc('#E6F6FF'), 3, r * (1 - u) * 0.9)
    # sparkles
    sp = smooth(20.0, 20.6, t)
    if sp > 0:
        for x, y, ph, s in SPARK:
            k = max(0, math.sin(t * 4 * s + ph))
            if k > 0.05:
                star(cr, x, y, 26 * k); cr.set_source_rgba(1, 1, 0.85, sp * k); cr.fill()
    if t >= 4.5 and t < 5.6:
        k = burst(4.5, 5.0, t)
        for i in range(8):
            a = i * math.pi / 4; rr = 150 + 120 * (t - 4.5) * 2
            star(cr, 540 + rr * math.cos(a), yf(540) - 200 + rr * math.sin(a), 22 * k)
        cr.set_source_rgba(1, 0.95, 0.5, 1); cr.fill()
    vg = cairo.RadialGradient(540, 960, 600, 540, 960, 1250)
    vg.add_color_stop_rgba(0, 0, 0, 0, 0); vg.add_color_stop_rgba(1, 0.05, 0.05, 0.2, 0.22)
    cr.set_source(vg); cr.paint()
    # texts
    draw_text(cr, "Chickpea & the Rainbow", 600, 130, t, 0.4, 5.3)
    draw_text(cr, "Oh, a butterfly!", 600, 115, t, 6.3, 7.7)
    draw_text(cr, "Oh no, rain!", 600, 115, t, 15.0, 17.3)
    draw_text(cr, "Yay, a rainbow!", 520, 125, t, 20.6, 23.8)
    draw_text(cr, "Bye-bye!", 520, 130, t, 24.25)

def make_surface():
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); return s, cairo.Context(s)

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'png':
        for tt in sys.argv[2:]:
            s, cr = make_surface(); frame(cr, float(tt)); s.write_to_png(f'/home/claude/cartoon/test_{tt}.png')
    elif mode == 'raw':
        f0, f1 = int(sys.argv[2]), int(sys.argv[3])
        out = sys.stdout.buffer
        for n in range(f0, f1):
            s, cr = make_surface(); frame(cr, n / FPS); s.flush(); out.write(bytes(s.get_data()))
