import sys, json, math, random
sys.path.insert(0, '/home/claude/cartoon')
import cairo
from anim import (hexc, lerp, clamp, ease_io, ease_out_back, smooth, mixc, ellipse, fs, stroke_dev,
                  draw_body, shell_part, draw_bfly, draw_cloud, draw_sun, draw_flower, star, draw_text,
                  tree, bush, draw_snail, hop, burst, OUT, W, H, FPS)

TL = json.load(open('/home/claude/colors/timeline.json'))
R = TL['rounds']; OUTRO = TL['outro']; RECAP = TL['recap']; DUR = TL['dur']
COL = dict(red='#FF4D4D', orange='#FF9A1F', yellow='#FFD93B', green='#3ECF5E', blue='#2EA7FF', purple='#A15CFF')
ORDER = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
NAMES = dict(red='Red', orange='Orange', yellow='Yellow', green='Green', blue='Blue', purple='Purple')
RC = (540, 860); R_OUT = 470; BW = 52
STAGE = (540, 1170)
DARK = hexc('#3B2A6B')
rr = random.Random(5)

def F(x): return 1400 + 22 * math.sin(2 * math.pi * x / 1080 * 0.9 + 0.8)
def B(x): return 1255 - 45 * math.sin(math.pi * x / 1080 * 1.3 + 0.2)
def FAR(x): return 1150 - 35 * math.sin(math.pi * x / 1080 * 2 + 1)
GR = [(x + rr.uniform(-5, 5), rr.uniform(28, 50), rr.uniform(0, 6)) for x in range(-10, 1100, 13)]
MEADOW = [(rr.uniform(40, 1040), rr.uniform(1560, 1880), rr.choice(list(COL.values()) + ['#FFFFFF', '#FF7EB6']), rr.uniform(0.8, 1.15)) for _ in range(14)]
MEADOW.sort(key=lambda m: m[1])
CONF = [(rr.uniform(0, 1080), rr.uniform(0, 1.6), rr.uniform(280, 560), rr.uniform(0, 6.28), rr.choice(list(COL.values()))) for _ in range(110)]
SPK = [(rr.uniform(0, 6.28), rr.uniform(150, 230), rr.uniform(0.7, 1.4)) for _ in range(7)]

def band_r(i): return R_OUT - BW / 2 - BW * i
def fill_amt(i, t): return smooth(R[i]['fly'] + 0.6, R[i]['fly'] + 1.3, t)
def sat(t): return sum(fill_amt(i, t) for i in range(6)) / 6

def G(h, k):
    c = hexc(h); l = 0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2]; g = l * 0.75 + 0.2
    return mixc((g, g, g * 1.02), c, k)

def face(cr, x, y, s=1.0):
    for sx in (-1, 1):
        cr.arc(x + sx * 32 * s, y, 11 * s, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill()
        cr.arc(x + sx * 32 * s - 3 * s, y - 4 * s, 4 * s, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()
        ellipse(cr, x + sx * 56 * s, y + 18 * s, 14 * s, 9 * s); cr.set_source_rgba(1, 0.45, 0.55, 0.5); cr.fill()
    cr.arc(x, y + 8 * s, 15 * s, 0.15 * math.pi, 0.85 * math.pi); stroke_dev(cr, OUT, 5)

# ---------------- objects ----------------
def obj_apple(cr, k):
    cr.move_to(10, -95); cr.curve_to(14, -120, 18, -135, 22, -150); stroke_dev(cr, G('#8B5A2B', k), 14)
    cr.save(); cr.translate(62, -135); cr.rotate(-0.5); ellipse(cr, 0, 0, 46, 22); fs(cr, G('#3ECF5E', k))
    cr.move_to(-40, 0); cr.line_to(40, 0); stroke_dev(cr, G('#2A9E45', k), 4); cr.restore()
    cr.move_to(0, -95); cr.curve_to(60, -150, 170, -90, 150, 10); cr.curve_to(135, 120, 60, 165, 20, 150)
    cr.curve_to(10, 145, -10, 145, -20, 150); cr.curve_to(-60, 165, -135, 120, -150, 10)
    cr.curve_to(-170, -90, -60, -150, 0, -95); cr.close_path(); fs(cr, G('#FF4D4D', k))
    cr.save(); cr.translate(-80, -40); cr.rotate(0.4); ellipse(cr, 0, 0, 20, 38); cr.set_source_rgba(1, 1, 1, 0.45); cr.fill(); cr.restore()
    face(cr, 0, 25)

def obj_carrot(cr, k):
    cr.save(); cr.rotate(0.35)
    for a, l in ((-0.5, 70), (0, 85), (0.5, 70)):
        cr.save(); cr.translate(0, -105); cr.rotate(a); ellipse(cr, 0, -l / 2 - 10, 18, l / 2 + 8); fs(cr, G('#3ECF5E', k)); cr.restore()
    cr.move_to(-78, -80); cr.curve_to(-82, -125, 82, -125, 78, -80); cr.curve_to(62, 20, 20, 135, 0, 175)
    cr.curve_to(-20, 135, -62, 20, -78, -80); cr.close_path(); fs(cr, G('#FF9A1F', k))
    for y, w in ((20, 30), (70, 22), (115, 14)):
        cr.move_to(-w - 20, y); cr.line_to(-20, y + 4); stroke_dev(cr, G('#D9730A', k), 5)
        cr.move_to(w + 15, y + 22); cr.line_to(15, y + 26); stroke_dev(cr, G('#D9730A', k), 5)
    ellipse(cr, -40, -70, 12, 25); cr.set_source_rgba(1, 1, 1, 0.4); cr.fill()
    face(cr, 0, -45, 0.85)
    cr.restore()

def obj_banana(cr, k):
    cr.save(); cr.translate(0, -10)
    cr.move_to(150, -72); cr.line_to(172, -108); stroke_dev(cr, G('#7A5A2A', k), 16, cap=cairo.LINE_CAP_BUTT)
    cr.move_to(-150, -50); cr.curve_to(-110, 115, 110, 125, 155, -70); cr.curve_to(100, 30, -90, 30, -150, -50); cr.close_path()
    fs(cr, G('#FFD93B', k))
    cr.move_to(-120, -20); cr.curve_to(-60, 60, 60, 66, 125, -30); stroke_dev(cr, G('#E9B81A', k), 5)
    cr.arc(-148, -48, 9, 0, 2 * math.pi); cr.set_source_rgb(*G('#6B4A1F', k)); cr.fill()
    face(cr, 0, 62, 0.65)
    cr.restore()

def obj_frog(cr, k):
    gc = G('#3ECF5E', k)
    for s in (-1, 1):
        ellipse(cr, s * 85, 140, 45, 20); fs(cr, gc)
    for s in (-1, 1):
        cr.arc(s * 62, -62, 46, 0, 2 * math.pi); fs(cr, gc)
    ellipse(cr, 0, 40, 145, 108); fs(cr, gc)
    for s in (-1, 1):
        cr.arc(s * 62, -62, 46, math.pi * 1.05, math.pi * 1.95); cr.close_path(); cr.set_source_rgb(*gc); cr.fill()
        cr.arc(s * 62, -64, 30, 0, 2 * math.pi); fs(cr, (1, 1, 1), 5)
        cr.arc(s * 62 + 4, -60, 15, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill()
        cr.arc(s * 62 - 1, -66, 5, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()
    ellipse(cr, 0, 85, 85, 48); cr.set_source_rgb(*G('#A8F0B4', k)); cr.fill()
    cr.arc(0, 0, 70, 0.22 * math.pi, 0.78 * math.pi); stroke_dev(cr, OUT, 6)
    for s in (-1, 1):
        ellipse(cr, s * 95, 25, 18, 11); cr.set_source_rgba(1, 0.45, 0.55, 0.55); cr.fill()
        for d in (0, 1, 2):
            cr.arc(s * (30 + d * 22), -5 + d * 6, 4, 0, 2 * math.pi)
    cr.set_source_rgb(*G('#2A9E45', k)); cr.fill()

def obj_whale(cr, k):
    cr.save(); cr.translate(-25, 15)
    bc = G('#2EA7FF', k); lc = G('#B8E4FF', k)
    for dx, h in ((-30, 40), (-55, 30), (-5, 30)):
        cr.move_to(-40, -100); cr.curve_to(-40 + dx * 0.3, -130, dx, -100 - h * 1.6, dx, -100 - h * 1.8)
        stroke_dev(cr, lc, 10)
        cr.arc(dx, -100 - h * 1.8, 9, 0, 2 * math.pi); cr.set_source_rgb(*lc); cr.fill()
    cr.move_to(115, 10); cr.curve_to(150, -20, 160, -50, 172, -92); cr.curve_to(190, -60, 215, -62, 232, -80)
    cr.curve_to(222, -30, 182, 2, 128, 42); cr.close_path(); fs(cr, bc)
    cr.move_to(-150, 0); cr.curve_to(-150, -110, 90, -120, 130, -10); cr.curve_to(150, 40, 120, 100, 20, 105)
    cr.curve_to(-90, 110, -150, 70, -150, 0); cr.close_path()
    p = cr.copy_path(); fs(cr, bc)
    cr.save(); cr.append_path(p); cr.clip(); ellipse(cr, -10, 92, 140, 45); cr.set_source_rgb(*lc); cr.fill(); cr.restore()
    cr.append_path(p); stroke_dev(cr, OUT, 6)
    cr.save(); cr.translate(-10, 55); cr.rotate(0.5); ellipse(cr, 0, 0, 30, 14); fs(cr, bc); cr.restore()
    cr.arc(-85, -18, 12, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill()
    cr.arc(-88, -22, 4, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()
    cr.arc(-110, 10, 22, 0.1 * math.pi, 0.6 * math.pi); stroke_dev(cr, OUT, 5)
    ellipse(cr, -60, 15, 14, 9); cr.set_source_rgba(1, 0.45, 0.55, 0.55); cr.fill()
    ellipse(cr, -40, -70, 30, 12); cr.set_source_rgba(1, 1, 1, 0.4); cr.fill()
    cr.restore()

def obj_grapes(cr, k):
    cr.move_to(0, -100); cr.curve_to(0, -120, 10, -135, 20, -150); stroke_dev(cr, G('#7A5A2A', k), 12)
    cr.save(); cr.translate(58, -125); cr.rotate(-0.3); ellipse(cr, 0, 0, 42, 24); fs(cr, G('#3ECF5E', k)); cr.restore()
    rows = [(-75, [-78, -26, 26, 78]), (-22, [-52, 0, 52]), (31, [-26, 26]), (84, [0])]
    pc = G('#A15CFF', k)
    for y, xs in rows:
        for x in xs:
            cr.arc(x, y, 33, 0, 2 * math.pi); fs(cr, pc)
            cr.arc(x - 11, y - 12, 8, 0, 2 * math.pi); cr.set_source_rgba(1, 1, 1, 0.5); cr.fill()
    face(cr, 0, -18, 0.75)

OBJ = dict(apple=obj_apple, carrot=obj_carrot, banana=obj_banana, frog=obj_frog, whale=obj_whale, grapes=obj_grapes)

# ---------------- helpers ----------------
def big_word(cr, text, cx, cy, size, col, s, rot=0.0, alpha=1.0):
    if s <= 0.01 or alpha <= 0: return
    cr.push_group()
    cr.select_font_face("Nunito ExtraLight"); cr.set_font_size(size)
    e = cr.text_extents(text)
    cr.save(); cr.translate(cx, cy); cr.rotate(rot); cr.scale(s, s)
    cr.move_to(-e.x_advance / 2, size * 0.36); cr.text_path(text); cr.restore()
    p = cr.copy_path(); cr.new_path()
    cr.append_path(p); stroke_dev(cr, DARK, 30)
    cr.append_path(p); stroke_dev(cr, (1, 1, 1), 14)
    cr.append_path(p); cr.set_source_rgb(*col); cr.fill()
    cr.save(); cr.append_path(p); cr.clip()
    cr.rectangle(0, cy - size * 0.45 * s, W, size * 0.2 * s); cr.set_source_rgba(1, 1, 1, 0.3); cr.fill(); cr.restore()
    cr.pop_group_to_source(); cr.paint_with_alpha(alpha)

def glow(cr, x, y, r, col, a):
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, *col, a); g.add_color_stop_rgba(1, *col, 0)
    cr.set_source(g); cr.arc(x, y, r, 0, 2 * math.pi); cr.fill()

def chick(cr, x, by, h, sx, sy, sc, st, t, look):
    cr.save(); cr.translate(x, by - h); cr.scale(sx * sc, sy * sc)
    draw_body(cr, 0, -215, 1.0, st, t, look); shell_part(cr, top=False); cr.restore()

def cur_round(t):
    for r in R:
        if r['appear'] <= t < r['end']: return r
    return None

# ---------------- frame ----------------
def frame(cr, t):
    s_ = sat(t)
    g = cairo.LinearGradient(0, 0, 0, 1300)
    g.add_color_stop_rgb(0, *hexc('#3FB4FF')); g.add_color_stop_rgb(0.65, *hexc('#8ADCFF')); g.add_color_stop_rgb(1, *hexc('#DDF7FF'))
    cr.set_source(g); cr.paint()
    cr.save(); cr.translate(960, 420); cr.rotate(t * 0.05)
    for i in range(16):
        a = i * 2 * math.pi / 16; cr.move_to(0, 0); cr.arc(0, 0, 2600, a, a + math.pi / 30); cr.close_path()
    cr.set_source_rgba(1, 1, 0.9, 0.04 + 0.1 * s_); cr.fill(); cr.restore()
    sc = 0.72; cr.save(); cr.translate(960 - 870 * sc, 420 - 270 * sc); cr.scale(sc, sc); draw_sun(cr, t); cr.restore()
    for i, (cx, cy, s) in enumerate(((120, 560, 0.55), (560, 300, 0.45), (900, 700, 0.4), (300, 1000, 0.35))):
        x = (cx + t * (10 + 4 * i) + 300) % 1500 - 300
        draw_cloud(cr, x, cy, s, (1, 1, 1), outline=False)
    # hills
    cr.move_to(0, H)
    for x in range(0, W + 21, 20): cr.line_to(x, FAR(x))
    cr.line_to(W, H); cr.close_path(); cr.set_source_rgb(*hexc('#C4EDB0')); cr.fill()
    cr.move_to(0, H)
    for x in range(0, W + 21, 20): cr.line_to(x, B(x))
    cr.line_to(W, H); cr.close_path(); cr.set_source_rgb(*hexc('#8EDB6A')); cr.fill()
    tree(cr, 70, B(70) + 40, 0.75, '#4CB944'); tree(cr, 1010, B(1010) + 40, 0.8, '#5DC85A')
    bush(cr, 290, B(290) + 40, 0.6); bush(cr, 800, B(800) + 40, 0.6)
    cr.move_to(0, H)
    for x in range(0, W + 21, 20): cr.line_to(x, F(x))
    cr.line_to(W, H); cr.close_path()
    hg = cairo.LinearGradient(0, 1380, 0, H); hg.add_color_stop_rgb(0, *hexc('#62C64C')); hg.add_color_stop_rgb(1, *hexc('#3E9E3A'))
    cr.set_source(hg); cr.fill()
    for x, h, ph in GR:
        y = F(x) + 4; sw = math.sin(t * 2 + x * 0.02 + ph) * 6
        cr.move_to(x - 7, y); cr.line_to(x + sw, y - h); cr.line_to(x + 7, y); cr.close_path()
    cr.set_source_rgb(*hexc('#4DB23C')); cr.fill()
    for i, x in enumerate((40, 345, 720, 960, 1050)):
        draw_flower(cr, x, F(x) + 35, 0.85, hexc(['#FFFFFF', '#FF7EB6', '#FFB400', '#2EA7FF', '#FF4D4D'][i]), t, i * 1.3)
    for i, (x, y, c, s) in enumerate(MEADOW):
        draw_flower(cr, x, y, s, hexc(c), t, i * 0.9)
    draw_snail(cr, lerp(1180, -140, t / DUR), 1840, t)
    # butterfly (gains color with the world)
    if t < OUTRO['start']:
        bx, by = 860 + 45 * math.sin(0.8 * t), 1180 + 60 * math.sin(1.4 * t)
    else:
        a = 1.6 * (t - OUTRO['start'])
        q = smooth(OUTRO['start'], OUTRO['start'] + 0.8, t)
        bx = lerp(860 + 45 * math.sin(0.8 * t), 540 + 330 * math.cos(a), q)
        by = lerp(1180 + 60 * math.sin(1.4 * t), 1170 + 120 * math.sin(2 * a), q)
    draw_bfly(cr, bx, by, t, 0.25 * math.sin(t * 3), 0.8)
    # desaturate world
    a = 0.9 * (1 - s_)
    if a > 0.01:
        cr.set_operator(cairo.OPERATOR_HSL_SATURATION); cr.set_source_rgba(0.5, 0.5, 0.5, a); cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER); cr.set_source_rgba(0.35, 0.38, 0.45, 0.18 * (1 - s_)); cr.paint()

    # ---- rainbow
    cx, cy = RC
    for i, c in enumerate(ORDER):
        r = band_r(i); f = fill_amt(i, t)
        cr.arc(cx, cy, r, math.pi, 2 * math.pi); stroke_dev(cr, hexc('#D5D9E0'), BW + 1, cap=cairo.LINE_CAP_BUTT)
        fl = 0.0
        if RECAP[i] <= t < RECAP[i] + 0.6: fl = burst(RECAP[i], RECAP[i] + 0.6, t)
        if f > 0:
            cr.arc(cx, cy, r, math.pi, math.pi + math.pi * f); stroke_dev(cr, hexc(COL[c]), BW + 1 + 10 * fl, cap=cairo.LINE_CAP_BUTT)
            if fl > 0:
                cr.arc(cx, cy, r, math.pi, 2 * math.pi); stroke_dev(cr, (1, 1, 1), BW, 0.45 * fl, cairo.LINE_CAP_BUTT)
        if 0 < f < 1:
            ang = math.pi + math.pi * f
            star(cr, cx + r * math.cos(ang), cy + r * math.sin(ang), 38); cr.set_source_rgb(1, 1, 0.85); cr.fill()
    for i in range(1, 6):
        cr.arc(cx, cy, R_OUT - BW * i, math.pi, 2 * math.pi); stroke_dev(cr, OUT, 2, 0.25)
    cr.arc(cx, cy, R_OUT, math.pi, 2 * math.pi); stroke_dev(cr, OUT, 6)
    cr.arc(cx, cy, R_OUT - BW * 6, math.pi, 2 * math.pi); stroke_dev(cr, OUT, 6)
    cr.move_to(cx - R_OUT, cy); cr.line_to(cx - R_OUT + BW * 6, cy); stroke_dev(cr, OUT, 6)
    cr.move_to(cx + R_OUT, cy); cr.line_to(cx + R_OUT - BW * 6, cy); stroke_dev(cr, OUT, 6)
    m = lerp(-1, 1, smooth(0, 1, s_ * 1.2 + (0.2 if t > TL['title'] else 0)))
    for x in (cx - (R_OUT - BW * 3), cx + (R_OUT - BW * 3)):
        y = cy + 20 + 6 * math.sin(t * 2 + x)
        draw_cloud(cr, x, y, 0.5, (1, 1, 1), outline=True)
        for sx in (-1, 1):
            cr.arc(x + sx * 28, y + 8, 8, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill()
            cr.arc(x + sx * 28 - 2, y + 5, 3, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()
            ellipse(cr, x + sx * 50, y + 26, 12, 7); cr.set_source_rgba(1, 0.45, 0.55, 0.5 * max(0, m)); cr.fill()
        cr.move_to(x - 20, y + 35 - 6 * m); cr.curve_to(x - 7, y + 35 + 10 * m, x + 7, y + 35 + 10 * m, x + 20, y + 35 - 6 * m)
        stroke_dev(cr, OUT, 5)

    # ---- stage
    sx0, sy0 = STAGE
    gg = cairo.RadialGradient(sx0, sy0, 0, sx0, sy0, 270)
    gg.add_color_stop_rgba(0, 1, 1, 1, 0.8); gg.add_color_stop_rgba(0.72, 1, 1, 1, 0.5); gg.add_color_stop_rgba(1, 1, 1, 1, 0)
    cr.set_source(gg); cr.arc(sx0, sy0, 270, 0, 2 * math.pi); cr.fill()
    cr.arc(sx0, sy0, 218, 0, 2 * math.pi); stroke_dev(cr, (1, 1, 1), 5, 0.8)
    rd = cur_round(t)
    if rd:
        i = rd['i']; col = hexc(COL[rd['color']])
        k = smooth(rd['reveal'], rd['reveal'] + 0.25, t)
        s_in = ease_out_back((t - rd['appear']) / 0.45)
        s_out = 1 - ease_io((t - (rd['end'] - 0.3)) / 0.3)
        s = s_in * s_out
        if k > 0: glow(cr, sx0, sy0, 240, col, 0.35 * k * s)
        if s > 0.01:
            cr.save(); cr.translate(sx0, sy0 + 8 * math.sin(t * 3)); cr.rotate(0.04 * math.sin(t * 2))
            pop = 1 + 0.15 * burst(rd['reveal'], rd['reveal'] + 0.35, t)
            cr.scale(s * pop, s * pop); OBJ[rd['obj']](cr, k); cr.restore()
        # question mark
        if rd['appear'] + 0.3 < t < rd['reveal']:
            qa = smooth(rd['appear'] + 0.3, rd['appear'] + 0.6, t) * (1 - smooth(rd['reveal'] - 0.15, rd['reveal'], t))
            big_word(cr, "?", 735, 1010 + 12 * math.sin(t * 6), 170, hexc("#FFD93B"), qa, 0.15 * math.sin(t * 4))
        # timer
        if rd['wait'] <= t < rd['reveal'] + 0.1:
            u = clamp((t - rd['wait']) / 2.1)
            cr.arc(sx0, sy0, 238, 0, 2 * math.pi); stroke_dev(cr, OUT, 24, 0.25)
            cr.arc(sx0, sy0, 238, -math.pi / 2, -math.pi / 2 + 2 * math.pi * (1 - u))
            stroke_dev(cr, hexc('#FFD93B'), 16)
            n = 3 - min(2, int(u * 3)); ph = (u * 3) % 1
            bs = 1 + 0.25 * max(0, 1 - ph * 4)
            cr.arc(sx0, sy0 - 238, 46 * bs, 0, 2 * math.pi); fs(cr, (1, 1, 1), 6, DARK)
            big_word(cr, str(n), sx0, sy0 - 238, 70, hexc('#FF4D4D'), bs)
        # splash
        if rd['reveal'] <= t < rd['reveal'] + 0.6:
            u = (t - rd['reveal']) / 0.6; e = 1 - (1 - u) ** 3
            glow(cr, sx0, sy0, 120 + 220 * e, (1, 1, 1), 0.6 * (1 - u))
            for j in range(12):
                ang = j * math.pi / 6 + 0.2 * math.sin(j * 7.3)
                d = 140 + (180 + 40 * math.sin(j * 3.1)) * e
                cr.arc(sx0 + d * math.cos(ang), sy0 + d * math.sin(ang), 36 * (1 - u) + 6, 0, 2 * math.pi)
                cr.set_source_rgba(*col, 1 - u * u); cr.fill()
        if rd['reveal'] + 0.2 < t < rd['end'] - 0.2:
            for ph, d, sp in SPK:
                kk = max(0, math.sin(t * 5 * sp + ph * 3))
                star(cr, sx0 + d * math.cos(ph), sy0 + d * math.sin(ph), 24 * kk); cr.set_source_rgba(1, 1, 0.85, kk); cr.fill()
        # orb flying to rainbow
        if rd['fly'] <= t < rd['fly'] + 0.62:
            r_ = band_r(i); ex, ey = cx - r_, cy  # left end of band, where the fill starts
            c1x, c1y = sx0 - 420, sy0 - 120
            for kk in range(6, -1, -1):
                u = clamp((t - kk * 0.035 - rd['fly']) / 0.6); e = ease_io(u)
                x = (1 - e) ** 2 * sx0 + 2 * (1 - e) * e * c1x + e * e * ex
                y = (1 - e) ** 2 * sy0 + 2 * (1 - e) * e * c1y + e * e * ey
                if kk == 0:
                    glow(cr, x, y, 75, col, 0.8); cr.arc(x, y, 26, 0, 2 * math.pi); fs(cr, col, 5, (1, 1, 1))
                else:
                    star(cr, x, y, 22 * (1 - kk / 7)); cr.set_source_rgba(1, 1, 0.8, 0.8 * (1 - kk / 7)); cr.fill()
        # answer word
        if t >= rd['reveal']:
            ws = ease_out_back((t - rd['reveal']) / 0.4)
            wa = 1 - smooth(rd['end'] - 0.3, rd['end'], t)
            big_word(cr, NAMES[rd['color']], 540, 1555 + 8 * math.sin(t * 4), 175, col, ws, 0.05 * math.sin(t * 3), wa)
    # outro: all objects around the stage
    if t >= OUTRO['start']:
        q = ease_out_back((t - OUTRO['start']) / 0.6)
        for i, rd2 in enumerate(R):
            ang = -math.pi / 2 + i * math.pi / 3 + 0.3 * (t - OUTRO['start'])
            hl = burst(RECAP[i], RECAP[i] + 0.6, t)
            s = q * (0.34 + 0.16 * hl)
            cr.save(); cr.translate(sx0 + 150 * math.cos(ang) * q, sy0 + 150 * math.sin(ang) * q); cr.scale(s, s)
            OBJ[rd2['obj']](cr, 1.0); cr.restore()
        for i in range(6):
            if RECAP[i] <= t < (RECAP[i + 1] if i < 5 else OUTRO['bye']):
                big_word(cr, NAMES[ORDER[i]], 540, 1555, 175, hexc(COL[ORDER[i]]), ease_out_back((t - RECAP[i]) / 0.3))

    # ---- chick
    st = dict(wing=[0.0, 0.0], beak=0.0, happy=0, mood=0.0)
    hh, sxx, syy = 0, 1, 1
    st['mood'] = 1 - smooth(TL['title'], TL['title'] + 0.6, t)
    look = (0.4, -0.9) if t < TL['title'] else (0.95, 0.0)
    for rd2 in R:
        if rd2['fly'] <= t < rd2['fly'] + 0.9: look = (0.3, -0.95)
        t0 = rd2['reveal'] + 0.05
        if t0 <= t < t0 + 0.9:
            kk = int((t - t0) / 0.45)
            _, hh, sxx, syy, _, air = hop(t, t0 + 0.45 * kk, 0.45, 90, 0, 0)
            st.update(happy=1, wing=[0.4 + 0.8 * air, 0.4 + 0.8 * air], beak=0.7 * air)
        if rd2['wait'] <= t < rd2['reveal']:
            st['beak'] = 0.0; look = (0.95, -0.15 + 0.1 * math.sin(t * 3))
    if OUTRO['start'] <= t < OUTRO['bye']:
        kk = int((t - OUTRO['start']) / 0.5)
        _, hh, sxx, syy, _, air = hop(t, OUTRO['start'] + 0.5 * kk, 0.5, 100, 0, 0)
        st.update(happy=1, wing=[0.4 + 0.9 * air, 0.4 + 0.9 * air], beak=0.6 * air)
    if t >= OUTRO['bye']:
        st.update(happy=1, wing=[0.1, 1.1 + 0.45 * math.sin(t * 13)], beak=0.5 * abs(math.sin(t * 6)))
    chx = 175; chb = F(chx) + 22
    shs = max(0.2, 1 - hh / 350)
    ellipse(cr, chx, chb + 2, 95 * shs, 17 * shs); cr.set_source_rgba(0.1, 0.25, 0.05, 0.25 * shs); cr.fill()
    chick(cr, chx, chb, hh, sxx, syy, 0.78, st, t, look)

    # ---- confetti
    if t >= OUTRO['start']:
        for x0, dl, sp, ph, c in CONF:
            tt = t - OUTRO['start'] - dl
            if tt < 0: continue
            y = -40 + tt * sp
            if y > H + 40: continue
            x = x0 + 40 * math.sin(tt * 3 + ph)
            cr.save(); cr.translate(x, y); cr.rotate(tt * 5 + ph); cr.scale(1, abs(math.sin(tt * 6 + ph)) + 0.2)
            cr.rectangle(-10, -6, 20, 12); cr.set_source_rgb(*hexc(c)); cr.fill(); cr.restore()
    # vignette
    vg = cairo.RadialGradient(540, 960, 650, 540, 960, 1300)
    vg.add_color_stop_rgba(0, 0, 0, 0, 0); vg.add_color_stop_rgba(1, 0.05, 0.05, 0.2, 0.22)
    cr.set_source(vg); cr.paint()
    # titles
    draw_text(cr, "Oh no!", 250, 130, t, 0.35, TL['title'] - 0.3, 0.3)
    draw_text(cr, "Guess the Color!", 250, 115, t, TL['title'], OUTRO['bye'] - 0.3, 0.3)
    draw_text(cr, "Bye-bye!", 250, 135, t, OUTRO['bye'])

def make_surface():
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); return s, cairo.Context(s)

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'png':
        for tt in sys.argv[2:]:
            s, cr = make_surface(); frame(cr, float(tt)); s.write_to_png(f'/home/claude/colors/t_{tt}.png')
    else:
        f0, f1 = int(sys.argv[2]), int(sys.argv[3]); out = sys.stdout.buffer
        for n in range(f0, f1):
            s, cr = make_surface(); frame(cr, n / FPS); s.flush(); out.write(bytes(s.get_data()))
