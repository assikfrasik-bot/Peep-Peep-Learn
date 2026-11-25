import sys, json, math, random
sys.path.insert(0, '/home/claude/cartoon'); sys.path.insert(0, '/home/claude/colors')
import cairo
from PIL import Image, ImageFilter
from anim import (hexc, lerp, clamp, ease_io, ease_out_back, smooth, mixc, ellipse, fs, stroke_dev,
                  draw_body, shell_part, draw_cloud, draw_sun, draw_flower, star, draw_text,
                  tree, bush, hop, burst, OUT, W, H, FPS)
from anim2 import obj_apple, obj_carrot, obj_banana, obj_grapes, obj_whale, face, big_word, glow

TL = json.load(open('/home/claude/odd/timeline.json'))
RS = TL['rounds']; OUTRO = TL['outro']; DUR = TL['dur']; TIMER = TL['timer']
DARK = hexc('#3B2A6B')
LVL_COL = ['#3ECF5E', '#2EA7FF', '#A15CFF', '#FF9A1F', '#FF4D4D']
CARD = 380; CR = 46
POS = [(320, 840), (760, 840), (320, 1280), (760, 1280)]
TILT = [-0.025, 0.02, 0.018, -0.02]
rr = random.Random(21)

# ---------------- pre-rendered blurred background ----------------
def build_bg():
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); cr = cairo.Context(s)
    g = cairo.LinearGradient(0, 0, 0, 1400)
    g.add_color_stop_rgb(0, *hexc('#46B8FF')); g.add_color_stop_rgb(0.6, *hexc('#9BE2FF')); g.add_color_stop_rgb(1, *hexc('#E2F8FF'))
    cr.set_source(g); cr.paint()
    cr.save(); cr.translate(130, 520)
    for i in range(16):
        a = i * 2 * math.pi / 16; cr.move_to(0, 0); cr.arc(0, 0, 2600, a, a + math.pi / 30); cr.close_path()
    cr.set_source_rgba(1, 1, 0.9, 0.12); cr.fill(); cr.restore()
    sc = 0.8; cr.save(); cr.translate(130 - 870 * sc, 560 - 270 * sc); cr.scale(sc, sc); draw_sun(cr, 0.4); cr.restore()
    for x, y, s_ in ((150, 420, 0.6), (620, 330, 0.5), (980, 560, 0.45), (380, 640, 0.4)):
        draw_cloud(cr, x, y, s_, (1, 1, 1), outline=False)
    def band(f, col):
        cr.move_to(0, H)
        for x in range(0, W + 21, 20): cr.line_to(x, f(x))
        cr.line_to(W, H); cr.close_path(); cr.set_source_rgb(*hexc(col)); cr.fill()
    band(lambda x: 1000 - 40 * math.sin(math.pi * x / 1080 * 2 + 1), '#C4EDB0')
    band(lambda x: 1110 - 50 * math.sin(math.pi * x / 1080 * 1.3 + 0.2), '#8EDB6A')
    for x, s_ in ((90, 0.9), (330, 0.65), (760, 0.7), (1000, 0.95)):
        tree(cr, x, 1110 - 50 * math.sin(math.pi * x / 1080 * 1.3 + 0.2) + 40, s_, '#4CB944' if x % 2 else '#5DC85A')
    band(lambda x: 1380 + 25 * math.sin(2 * math.pi * x / 1080 * 0.9 + 0.8), '#5FC44A')
    for i in range(40):
        x, y = rr.uniform(20, 1060), rr.uniform(1420, 1900)
        draw_flower(cr, x, y, rr.uniform(0.8, 1.2), hexc(rr.choice(['#FF5A5F', '#FFFFFF', '#A66CFF', '#FFB400', '#FF7EB6', '#2EA7FF'])), 0, i)
    s.flush()
    im = Image.frombuffer('RGBA', (W, H), bytes(s.get_data()), 'raw', 'BGRA', 0, 1).convert('RGB')
    im = im.filter(ImageFilter.GaussianBlur(7))
    data = bytearray(im.convert('RGBA').tobytes('raw', 'BGRA'))
    return cairo.ImageSurface.create_for_data(data, cairo.FORMAT_ARGB32, W, H), data
BG, _BGDATA = build_bg()
BOKEH = [(rr.uniform(0, 1080), rr.uniform(0, 1920), rr.uniform(18, 60), rr.uniform(10, 30), rr.uniform(0, 6.28), rr.uniform(0.10, 0.25)) for _ in range(22)]

# ---------------- items ----------------
def item_star(cr, t):
    cr.save(); cr.rotate(0.06 * math.sin(t * 2))
    cr.move_to(0, -150)
    for j in range(1, 10):
        a = j * math.pi / 5; r = 150 if j % 2 == 0 else 66
        cr.line_to(r * math.sin(a), -r * math.cos(a))
    cr.close_path(); fs(cr, hexc('#FFD93B'), 7)
    ellipse(cr, -40, -50, 14, 26); cr.set_source_rgba(1, 1, 1, 0.5); cr.fill()
    face(cr, 0, 15, 0.75); cr.restore()

def item_heart(cr, t):
    s = 1 + 0.05 * math.sin(t * 6); cr.save(); cr.scale(s, s)
    cr.move_to(0, 130); cr.curve_to(-175, 10, -140, -150, 0, -70); cr.curve_to(140, -150, 175, 10, 0, 130); cr.close_path()
    fs(cr, hexc('#FF5FA2'), 7)
    ellipse(cr, -70, -60, 16, 28); cr.set_source_rgba(1, 1, 1, 0.5); cr.fill()
    face(cr, 0, -5, 0.8); cr.restore()

def item_fish(cr, t):
    cr.save(); cr.translate(-10, 0); cr.rotate(0.05 * math.sin(t * 3))
    for j, (bx, by, r) in enumerate(((-150, -95, 12), (-170, -130, 8), (-150, -160, 6))):
        cr.arc(bx, by - 6 * math.sin(t * 3 + j), r, 0, 2 * math.pi); stroke_dev(cr, hexc('#7FD0FF'), 4)
    tw = 0.15 * math.sin(t * 8)
    cr.save(); cr.translate(100, 0); cr.rotate(tw)
    cr.move_to(0, 0); cr.line_to(80, -75); cr.curve_to(62, -20, 62, 20, 80, 75); cr.close_path(); fs(cr, hexc('#FF7A1A'), 6); cr.restore()
    cr.move_to(-30, -70); cr.curve_to(-10, -120, 50, -110, 60, -60); cr.close_path(); fs(cr, hexc('#FF7A1A'), 6)
    cr.move_to(-135, 0); cr.curve_to(-95, -100, 75, -100, 115, 0); cr.curve_to(75, 100, -95, 100, -135, 0); cr.close_path()
    p = cr.copy_path(); fs(cr, hexc('#FFA126'), 6)
    cr.save(); cr.append_path(p); cr.clip()
    for x in (-20, 40):
        cr.move_to(x, -90); cr.curve_to(x + 22, -30, x + 22, 30, x, 90); stroke_dev(cr, (1, 1, 1), 18)
    cr.restore(); cr.append_path(p); stroke_dev(cr, OUT, 6)
    cr.arc(-75, -18, 16, 0, 2 * math.pi); fs(cr, (1, 1, 1), 4); cr.arc(-79, -18, 8, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill()
    cr.arc(-100, 22, 16, 0.1 * math.pi, 0.7 * math.pi); stroke_dev(cr, OUT, 5)
    ellipse(cr, -55, 25, 12, 8); cr.set_source_rgba(1, 0.4, 0.5, 0.5); cr.fill()
    cr.restore()

def item_crab(cr, t):
    rc = hexc('#FF5A4D')
    for s in (-1, 1):
        for j in range(3):
            cr.move_to(s * 80, 40 + j * 22); cr.line_to(s * (140 + j * 8), 70 + j * 32); cr.line_to(s * (150 + j * 8), 110 + j * 28)
            stroke_dev(cr, OUT, 16);
            cr.move_to(s * 80, 40 + j * 22); cr.line_to(s * (140 + j * 8), 70 + j * 32); cr.line_to(s * (150 + j * 8), 110 + j * 28)
            stroke_dev(cr, rc, 8)
        sn = 0.12 * math.sin(t * 5 + s)
        cr.move_to(s * 85, 0); cr.line_to(s * 120, -60); stroke_dev(cr, OUT, 20); cr.move_to(s * 85, 0); cr.line_to(s * 120, -60); stroke_dev(cr, rc, 11)
        cr.save(); cr.translate(s * 125, -100); cr.rotate(s * sn)
        cr.move_to(0, 0); cr.arc(0, 0, 48, -math.pi / 2 + (0.35 if s > 0 else 0), -math.pi / 2 + 2 * math.pi - (0 if s > 0 else 0.35))
        cr.close_path(); fs(cr, rc, 6); cr.restore()
    for s in (-1, 1):
        cr.move_to(s * 32, -40); cr.line_to(s * 40, -100); stroke_dev(cr, OUT, 8)
        cr.arc(s * 40, -108, 20, 0, 2 * math.pi); fs(cr, (1, 1, 1), 5)
        cr.arc(s * 40 + 2, -105, 9, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill()
    ellipse(cr, 0, 30, 118, 82); fs(cr, rc, 7)
    ellipse(cr, -45, 0, 18, 10); cr.set_source_rgba(1, 1, 1, 0.4); cr.fill()
    cr.arc(0, 40, 26, 0.15 * math.pi, 0.85 * math.pi); stroke_dev(cr, OUT, 5)
    for s in (-1, 1):
        ellipse(cr, s * 60, 50, 14, 9); cr.set_source_rgba(1, 0.75, 0.8, 0.7); cr.fill()

CHICK_ST = dict(wing=[0.3, 0.3], beak=0.3, happy=0, mood=0.0)
def item_chick(cr, t):
    cr.save(); cr.translate(0, 135); cr.scale(0.62, 0.62)
    draw_body(cr, 0, -215, 1.0, CHICK_ST, t, (0, 0.2)); shell_part(cr, top=False); cr.restore()

def bfly_c(cr, t, up, low):
    f = 0.3 + 0.7 * abs(math.sin(t * 7))
    cr.save(); cr.scale(1.85, 1.85)
    for s in (-1, 1):
        cr.save(); cr.scale(s * f, 1)
        cr.save(); cr.translate(48, -22); cr.rotate(-0.5); ellipse(cr, 0, 0, 52, 40); fs(cr, hexc(up)); cr.restore()
        ellipse(cr, 58, -26, 16, 13); cr.set_source_rgba(1, 1, 1, 0.55); cr.fill()
        cr.save(); cr.translate(36, 26); cr.rotate(0.5); ellipse(cr, 0, 0, 34, 28); fs(cr, hexc(low)); cr.restore()
        ellipse(cr, 40, 28, 9, 8); cr.set_source_rgba(1, 1, 1, 0.8); cr.fill()
        cr.restore()
    ellipse(cr, 0, 8, 10, 36); fs(cr, hexc('#4A2D6B'), 5)
    for s in (-1, 1):
        cr.move_to(s * 5, -44); cr.curve_to(s * 12, -70, s * 26, -78, s * 30, -74); stroke_dev(cr, OUT, 4)
        cr.arc(s * 30, -74, 6, 0, 2 * math.pi); cr.set_source_rgb(*hexc('#FF7EB6')); cr.fill()
    cr.arc(0, -36, 16, 0, 2 * math.pi); fs(cr, hexc('#4A2D6B'), 5)
    for s in (-1, 1):
        cr.arc(s * 6, -38, 3.5, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()
    cr.restore()

def num_tile(n, col):
    def f(cr, t):
        cr.save(); cr.rotate(0.04 * math.sin(t * 2 + n))
        cr.new_sub_path(); r = 40; w = 120
        cr.arc(w - r, -w + r, r, -math.pi / 2, 0); cr.arc(w - r, w - r, r, 0, math.pi / 2)
        cr.arc(-w + r, w - r, r, math.pi / 2, math.pi); cr.arc(-w + r, -w + r, r, math.pi, 1.5 * math.pi); cr.close_path()
        fs(cr, hexc(col), 7)
        cr.rectangle(-w + 18, -w + 18, 2 * w - 36, 2 * w - 36); stroke_dev(cr, (1, 1, 1), 4, 0.5)
        big_word(cr, str(n), 0, 0, 200, (1, 1, 1), 1.0)
        cr.restore()
    return f

ITEMS = dict(star=item_star, heart=item_heart, apple=lambda c, t: obj_apple(c, 1), carrot=lambda c, t: obj_carrot(c, 1),
             banana=lambda c, t: obj_banana(c, 1), grapes=lambda c, t: obj_grapes(c, 1),
             whale=lambda c, t: (c.save(), c.scale(0.82, 0.82), obj_whale(c, 1), c.restore()),
             fish=item_fish, crab=item_crab, chick=item_chick,
             bfly=lambda c, t: bfly_c(c, t, '#FF7EB6', '#B57BFF'), bfly_swap=lambda c, t: bfly_c(c, t, '#B57BFF', '#FF7EB6'),
             n4=num_tile(4, '#2EA7FF'), n8=num_tile(8, '#3ECF5E'), n7=num_tile(7, '#FF9A1F'), n2=num_tile(2, '#FF5FA2'))

# ---------------- card ----------------
def rrect(cr, x, y, w, h, r):
    cr.new_sub_path()
    cr.arc(x + w - r, y + r, r, -math.pi / 2, 0); cr.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    cr.arc(x + r, y + h - r, r, math.pi / 2, math.pi); cr.arc(x + r, y + r, r, math.pi, 1.5 * math.pi); cr.close_path()

def card_front(cr, lvl, item, t):
    c = hexc(LVL_COL[lvl]); h = CARD / 2
    rrect(cr, -h, -h, CARD, CARD, CR)
    g = cairo.LinearGradient(0, -h, 0, h); g.add_color_stop_rgb(0, 1, 1, 1); g.add_color_stop_rgb(1, *mixc(c, (1, 1, 1), 0.82))
    cr.set_source(g); cr.fill_preserve(); stroke_dev(cr, OUT, 7)
    rrect(cr, -h + 14, -h + 14, CARD - 28, CARD - 28, CR - 12); stroke_dev(cr, c, 8, 0.85)
    cr.save(); cr.scale(0.8, 0.8); ITEMS[item](cr, t); cr.restore()

def card_back(cr, t):
    h = CARD / 2
    rrect(cr, -h, -h, CARD, CARD, CR)
    g = cairo.LinearGradient(-h, -h, h, h); g.add_color_stop_rgb(0, *hexc('#8E5CFF')); g.add_color_stop_rgb(1, *hexc('#5B3BD6'))
    cr.set_source(g); cr.fill_preserve(); stroke_dev(cr, OUT, 7)
    for j in range(9):
        x, y = -120 + (j % 3) * 120, -120 + (j // 3) * 120
        star(cr, x, y, 14); cr.set_source_rgba(1, 1, 1, 0.18); cr.fill()
    big_word(cr, "?", 0, 0, 230, hexc('#FFD93B'), 1.0)

def shadow(cr, x, y, sx):
    for j in range(6):
        e = 6 + j * 7
        rrect(cr, x - CARD / 2 * sx - e / 2 + 8, y - CARD / 2 + 18 - e / 2, CARD * sx + e, CARD + e, CR + e / 2)
        cr.set_source_rgba(0.05, 0.1, 0.2, 0.05); cr.fill()

def round_at(t):
    cur = None
    for r in RS:
        if t >= r['start']: cur = r
    return cur

def chick_det(cr, x, by, h, sx, sy, sc, st, t, look):
    cr.save(); cr.translate(x, by - h); cr.scale(sx * sc, sy * sc)
    draw_body(cr, 0, -215, 1.0, st, t, look)
    # detective hat
    cr.save(); cr.translate(0, -322)
    cr.move_to(-100, 8); cr.curve_to(-100, -95, 100, -95, 100, 8); cr.close_path()
    p = cr.copy_path(); cr.set_source_rgb(*hexc('#B07A4A')); cr.fill()
    cr.save(); cr.append_path(p); cr.clip()
    for x in range(-100, 101, 28):
        cr.move_to(x, -100); cr.line_to(x, 20); cr.move_to(-110, x * 0.6 - 10); cr.line_to(110, x * 0.6 - 10)
    stroke_dev(cr, hexc('#7E5230'), 4, 0.7); cr.restore()
    cr.append_path(p); stroke_dev(cr, OUT, 6)
    ellipse(cr, 0, 10, 122, 22); fs(cr, hexc('#8A5A32'))
    cr.arc(0, -78, 12, 0, 2 * math.pi); fs(cr, hexc('#8A5A32'), 5)
    cr.restore()
    shell_part(cr, top=False); cr.restore()

def magnifier(cr, x, y, a=1.0):
    cr.push_group()
    cr.move_to(x + 60, y + 60); cr.line_to(x + 140, y + 140); stroke_dev(cr, OUT, 34)
    cr.move_to(x + 60, y + 60); cr.line_to(x + 140, y + 140); stroke_dev(cr, hexc('#8A5A32'), 22)
    cr.arc(x, y, 88, 0, 2 * math.pi); cr.set_source_rgba(0.8, 0.93, 1, 0.28); cr.fill()
    cr.arc(x, y, 88, 0, 2 * math.pi); stroke_dev(cr, OUT, 16)
    cr.arc(x, y, 88, 0, 2 * math.pi); stroke_dev(cr, hexc('#D9DEE6'), 8)
    cr.arc(x, y, 62, math.pi * 1.1, math.pi * 1.45); stroke_dev(cr, (1, 1, 1), 9, 0.9)
    cr.pop_group_to_source(); cr.paint_with_alpha(a)

def check_badge(cr, x, y, s):
    if s <= 0: return
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.arc(0, 0, 46, 0, 2 * math.pi); fs(cr, hexc('#2DC653'), 6)
    cr.move_to(-20, 2); cr.line_to(-6, 18); cr.line_to(22, -14); stroke_dev(cr, (1, 1, 1), 11)
    cr.restore()

CONF_COLS = ['#FF4D4D', '#FF9A1F', '#FFD93B', '#3ECF5E', '#2EA7FF', '#A15CFF', '#FF5FA2']
BURST = [(rr.uniform(0, 6.28), rr.uniform(450, 950), rr.choice(CONF_COLS), rr.uniform(0, 6.28)) for _ in range(46)]
RAIN = [(rr.uniform(0, 1080), rr.uniform(0, 1.8), rr.uniform(280, 520), rr.uniform(0, 6.28), rr.choice(CONF_COLS)) for _ in range(120)]


def star5(cr, x, y, r):
    cr.move_to(x, y - r)
    for j in range(1, 10):
        a = j * math.pi / 5; rr_ = r if j % 2 == 0 else r * 0.45
        cr.line_to(x + rr_ * math.sin(a), y - rr_ * math.cos(a))
    cr.close_path()

def clean_text(cr, text, cx, cy, size, col, outline=10, ocol=None):
    cr.select_font_face("Nunito ExtraLight"); cr.set_font_size(size)
    e = cr.text_extents(text)
    cr.move_to(cx - e.x_advance / 2, cy + size * 0.36); cr.text_path(text)
    p = cr.copy_path(); cr.new_path()
    cr.append_path(p); stroke_dev(cr, ocol or DARK, outline)
    cr.append_path(p); cr.set_source_rgb(*col); cr.fill()

# ---------------- frame ----------------
def frame(cr, t):
    cr.set_source_surface(BG, 0, 0); cr.paint()
    for x, y0, r, sp, ph, a in BOKEH:
        y = (y0 - t * sp) % 2000 - 40; xx = x + 20 * math.sin(t * 0.5 + ph)
        glow(cr, xx, y, r, (1, 1, 1), a * (0.7 + 0.3 * math.sin(t * 1.5 + ph)))
    gg = cairo.RadialGradient(540, 1060, 100, 540, 1060, 720)
    gg.add_color_stop_rgba(0, 1, 1, 1, 0.35); gg.add_color_stop_rgba(1, 1, 1, 1, 0)
    cr.set_source(gg); cr.paint()
    rd = round_at(t)
    in_outro = t >= OUTRO['start']
    # expert pulse
    if rd and rd['i'] == 4 and rd['timer'] <= t < rd['reveal']:
        pu = 0.5 + 0.5 * math.sin((t - rd['timer']) * 2 * math.pi * 1.2)
        vg = cairo.RadialGradient(540, 960, 500, 540, 960, 1200)
        vg.add_color_stop_rgba(0, 1, 0.2, 0.2, 0); vg.add_color_stop_rgba(1, 1, 0.15, 0.1, 0.18 + 0.12 * pu)
        cr.set_source(vg); cr.paint()

    # ---- cards
    out_k = smooth(OUTRO['start'], OUTRO['start'] + 0.6, t) if in_outro else 0
    if out_k < 1:
        if not rd:
            for j, (px, py) in enumerate(POS):
                sb = ease_out_back((t - 0.05 * j) / 0.35)
                if sb <= 0.01: continue
                shadow(cr, px, py, sb)
                cr.save(); cr.translate(px, py + 6 * math.sin(t * 2 + j * 1.3)); cr.rotate(TILT[j]); cr.scale(sb, sb); card_back(cr, t); cr.restore()
        for j, (px, py) in enumerate(POS):
            if not rd: break
            i = rd['i']; prev = RS[i - 1] if i > 0 else None
            u = (t - (rd['start'] + 0.08 * j)) / 0.45
            if u < 0:
                showing = ('prev', prev); sx = 1
            elif u < 0.5:
                showing = ('prev', prev); sx = math.cos(math.pi * u)
            elif u < 1:
                showing = ('cur', rd); sx = abs(math.cos(math.pi * u))
            else:
                showing = ('cur', rd); sx = 1
            which, r_ = showing
            if which == 'prev' and r_ is None: r_ = None
            # reveal state
            dim = 0; hl = 0; scl = 1
            if r_ is not None and t >= r_['reveal'] and (which == 'cur' or True):
                k = smooth(r_['reveal'], r_['reveal'] + 0.3, t)
                if which == 'prev': k *= 1  # stays until flipped
                if j == r_['odd']: hl = k; scl = 1 + 0.07 * k + 0.05 * burst(r_['reveal'], r_['reveal'] + 0.35, t)
                else: dim = k; scl = 1 - 0.06 * k
            bob = 6 * math.sin(t * 2 + j * 1.3)
            scl *= (1 - out_k * 0.9)
            ox = lerp(px, 540, out_k); oy = lerp(py, 1060, out_k) + bob
            if scl <= 0.02 or sx <= 0.01: continue
            if hl > 0: glow(cr, ox, oy, 330, (1, 0.9, 0.3), 0.55 * hl)
            shadow(cr, ox, oy, sx * scl)
            cr.save(); cr.translate(ox, oy); cr.rotate(TILT[j] * (1 - hl)); cr.scale(sx * scl, scl)
            if r_ is None: card_back(cr, t)
            else: card_front(cr, r_['i'], r_['items'][j], t)
            if dim > 0:
                rrect(cr, -CARD / 2, -CARD / 2, CARD, CARD, CR); cr.set_source_rgba(1, 1, 1, 0.55 * dim); cr.fill()
            cr.restore()
            if hl > 0 and sx > 0.95:
                pr = smooth(r_['reveal'] + 0.05, r_['reveal'] + 0.45, t)
                cr.save(); cr.translate(ox, oy); cr.rotate(-0.12)
                cr.save(); cr.scale(1.0, 0.95); cr.arc(0, 0, 232, -2.2, -2.2 + 2.15 * math.pi * pr); cr.restore()
                stroke_dev(cr, hexc('#FF3B3B'), 14); cr.restore()
                check_badge(cr, ox + 165 * scl, oy - 165 * scl, ease_out_back((t - r_['reveal'] - 0.25) / 0.35))
    # ---- magnifier during timer
    if rd and rd['timer'] - 0.2 <= t < rd['reveal'] and not in_outro:
        u = t - rd['timer']
        a = smooth(rd['timer'] - 0.2, rd['timer'] + 0.1, t) * (1 - smooth(rd['reveal'] - 0.2, rd['reveal'], t))
        mx = 540 + 230 * math.sin(u * 1.7 + rd['i']); my = 1060 + 230 * math.sin(u * 3.4 + 0.5)
        magnifier(cr, mx, my, a)
    # ---- confetti burst from odd card
    if rd and t >= rd['reveal'] and not in_outro:
        tt = t - rd['reveal']
        if tt < 1.4:
            px, py = POS[rd['odd']]
            for ang, sp, c, ph in BURST:
                x = px + math.cos(ang) * sp * tt; y = py + math.sin(ang) * sp * tt + 900 * tt * tt
                cr.save(); cr.translate(x, y); cr.rotate(tt * 8 + ph); cr.scale(1, abs(math.sin(tt * 9 + ph)) + 0.2)
                cr.rectangle(-11, -7, 22, 14); cr.set_source_rgba(*hexc(c), 1 - smooth(1.0, 1.4, tt)); cr.fill(); cr.restore()

    # ---- level badge
    if rd and not in_outro:
        i = rd['i']; c = hexc(LVL_COL[i])
        bs = max(0.01, ease_out_back((t - rd["start"]) / 0.45)) if t < rd["start"] + 0.5 else 1
        pulse = 1 + (0.05 * math.sin(t * 8) if i == 4 else 0)
        cr.save(); cr.translate(540, 455); cr.scale(bs * pulse, bs * pulse)
        if i == 4: glow(cr, 0, 0, 240, (1, 0.3, 0.2), 0.5)
        rrect(cr, -190, -55, 380, 110, 55); fs(cr, c, 7)
        rrect(cr, -178, -45, 356, 40, 20); cr.set_source_rgba(1, 1, 1, 0.25); cr.fill()
        clean_text(cr, "EXPERT!" if i == 4 else f"LEVEL {i + 1}", 0, 0, 70, (1, 1, 1), 10)
        for s in range(5):
            star5(cr, -96 + s * 48, 94, 24); fs(cr, hexc('#FFD93B') if s <= i else (0.86, 0.88, 0.92), 4)
        cr.restore()
    # ---- timer bar / label
    if rd and not in_outro:
        bx, by, bw, bh = 540 - 330, 1530, 660, 56
        if rd['timer'] - 0.3 <= t < rd['reveal'] + 0.15:
            a = smooth(rd['timer'] - 0.3, rd['timer'], t) * (1 - smooth(rd['reveal'], rd['reveal'] + 0.15, t))
            u = clamp((t - rd['timer']) / TIMER)
            cr.push_group()
            rrect(cr, bx, by, bw, bh, bh / 2); cr.set_source_rgba(0.1, 0.1, 0.25, 0.45); cr.fill_preserve(); stroke_dev(cr, OUT, 6)
            col = mixc(hexc('#3ECF5E'), hexc('#FFD93B'), clamp(u * 2)) if u < 0.5 else mixc(hexc('#FFD93B'), hexc('#FF4D4D'), clamp((u - 0.5) * 2))
            fw = (bw - 12) * (1 - u)
            if fw > 30:
                rrect(cr, bx + 6, by + 6, fw, bh - 12, (bh - 12) / 2); cr.set_source_rgb(*col); cr.fill()
                rrect(cr, bx + 14, by + 10, max(0, fw - 16), 12, 6); cr.set_source_rgba(1, 1, 1, 0.35); cr.fill()
            n = max(1, math.ceil(TIMER * (1 - u) - 1e-6))
            ph = (TIMER * (1 - u)) % 1
            bsz = 1 + 0.2 * max(0, (ph - 0.75) * 4)
            cr.arc(bx - 10, by + bh / 2, 52 * bsz, 0, 2 * math.pi); fs(cr, (1, 1, 1), 6, DARK)
            clean_text(cr, str(n), bx - 10, by + bh / 2 - 2, 64 * bsz, hexc('#FF4D4D') if n == 1 else DARK, 3)
            cr.pop_group_to_source(); cr.paint_with_alpha(a)
        if t >= rd['reveal']:
            ws = ease_out_back((t - rd['reveal'] - 0.15) / 0.4) if t > rd['reveal'] + 0.15 else 0
            wa = 1 - smooth(rd['end'] - 0.25, rd['end'], t)
            big_word(cr, rd['label'], 540, 1560 + 6 * math.sin(t * 4), 100, hexc(LVL_COL[rd['i']]), ws, 0.03 * math.sin(t * 3), wa)

    # ---- outro medal
    if in_outro:
        ms = ease_out_back((t - OUTRO['start'] - 0.4) / 0.6) if t > OUTRO['start'] + 0.4 else 0
        if ms > 0:
            cr.save(); cr.translate(540, 840); cr.rotate(0.06 * math.sin(t * 2)); cr.scale(ms, ms)
            cr.save(); cr.rotate(t * 0.3)
            for j in range(12):
                a = j * math.pi / 6; cr.move_to(0, 0); cr.arc(0, 0, 330, a, a + math.pi / 12); cr.close_path()
            cr.set_source_rgba(1, 0.9, 0.4, 0.35); cr.fill(); cr.restore()
            for s, c in ((-1, '#2EA7FF'), (1, '#FF4D4D')):
                cr.move_to(s * 30, -120); cr.line_to(s * 110, -330); cr.line_to(s * 20, -330); cr.line_to(s * -40, -150); cr.close_path(); fs(cr, hexc(c), 6)
            cr.arc(0, 0, 175, 0, 2 * math.pi); fs(cr, hexc('#FFC93B'), 8)
            cr.arc(0, 0, 140, 0, 2 * math.pi); fs(cr, hexc('#FFDF6B'), 5, hexc('#D9A21F'))
            star(cr, 0, 0, 95); fs(cr, hexc('#FFF3B0'), 6, hexc('#D9A21F'))
            ellipse(cr, -70, -80, 20, 34); cr.set_source_rgba(1, 1, 1, 0.5); cr.fill()
            cr.restore()
            big_word(cr, "Super Detective!", 540, 1125, 112, hexc('#FF9A1F'), ease_out_back((t - OUTRO['start'] - 0.8) / 0.5) if t > OUTRO['start'] + 0.8 else 0)
        for x0, dl, sp, ph, c in RAIN:
            tt = t - OUTRO['start'] - dl
            if tt < 0: continue
            y = -40 + tt * sp
            if y > H + 40: continue
            x = x0 + 40 * math.sin(tt * 3 + ph)
            cr.save(); cr.translate(x, y); cr.rotate(tt * 5 + ph); cr.scale(1, abs(math.sin(tt * 6 + ph)) + 0.2)
            cr.rectangle(-11, -7, 22, 14); cr.set_source_rgb(*hexc(c)); cr.fill(); cr.restore()

    # ---- chick
    st = dict(wing=[0.0, 0.0], beak=0.0, happy=0, mood=0.0)
    hh, sxx, syy = 0, 1, 1
    cx, cb, csc = 868, 668, 0.5
    look = (-0.6, 0.7)
    if rd and not in_outro:
        if rd['timer'] <= t < rd['reveal']:
            u = t - rd['timer']; mx = 540 + 230 * math.sin(u * 1.7 + rd['i']); my = 1060 + 230 * math.sin(u * 3.4 + 0.5)
            dx, dy = mx - cx, my - (cb - 110); d = math.hypot(dx, dy) + 1e-6; look = (dx / d, dy / d)
        t0 = rd['reveal'] + 0.1
        if rd['i'] == 2 and t0 <= t < t0 + 1.0:
            st.update(wing=[1.2, 1.2], beak=0.9); look = (-0.5, 0.8)
            hh = 20 * burst(t0, t0 + 0.3, t)
        elif rd['i'] == 2 and t0 + 1.0 <= t < t0 + 1.9 or rd['i'] != 2 and t0 <= t < t0 + 0.9:
            tb = t0 + (1.0 if rd['i'] == 2 else 0)
            kk = int((t - tb) / 0.45)
            _, hh, sxx, syy, _, air = hop(t, tb + 0.45 * kk, 0.45, 70, 0, 0)
            st.update(happy=1, wing=[0.4 + 0.8 * air, 0.4 + 0.8 * air], beak=0.6 * air)
    if in_outro:
        u = clamp((t - OUTRO['start'] - 0.15) / 0.7)
        e = ease_io(u)
        cx = lerp(868, 540, e); cb = lerp(668, 1590, e); csc = lerp(0.5, 0.82, e)
        hh = 380 * 4 * u * (1 - u) if u < 1 else 0
        look = (0, 0.2)
        if u >= 1 and t < OUTRO['bye']:
            kk = int((t - OUTRO['start'] - 0.85) / 0.5)
            _, hh, sxx, syy, _, air = hop(t, OUTRO['start'] + 0.85 + 0.5 * kk, 0.5, 90, 0, 0)
            st.update(happy=1, wing=[0.4 + 0.9 * air, 0.4 + 0.9 * air], beak=0.6 * air)
        elif u >= 1:
            st.update(happy=1, wing=[0.1, 1.1 + 0.45 * math.sin(t * 13)], beak=0.5 * abs(math.sin(t * 7)))
        if u >= 1:
            ellipse(cr, cx, cb + 2, 95, 16); cr.set_source_rgba(0.1, 0.25, 0.05, 0.25); cr.fill()
    chick_det(cr, cx, cb, hh, sxx, syy, csc, st, t, look)

    # vignette + title
    vg = cairo.RadialGradient(540, 960, 700, 540, 960, 1300)
    vg.add_color_stop_rgba(0, 0, 0, 0, 0); vg.add_color_stop_rgba(1, 0.05, 0.05, 0.2, 0.25)
    cr.set_source(vg); cr.paint()
    draw_text(cr, "Find the Odd One Out!", 245, 110, t, 0.15)

def make_surface():
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); return s, cairo.Context(s)

if __name__ == '__main__':
    if sys.argv[1] == 'png':
        for tt in sys.argv[2:]:
            s, cr = make_surface(); frame(cr, float(tt)); s.write_to_png(f'/home/claude/odd/t_{tt}.png')
    else:
        f0, f1 = int(sys.argv[2]), int(sys.argv[3]); out = sys.stdout.buffer
        for n in range(f0, f1):
            s, cr = make_surface(); frame(cr, n / FPS); s.flush(); out.write(bytes(s.get_data()))
