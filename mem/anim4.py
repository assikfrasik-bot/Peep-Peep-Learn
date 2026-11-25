import sys, json, math, random
sys.path.insert(0, '/home/claude/cartoon'); sys.path.insert(0, '/home/claude/colors'); sys.path.insert(0, '/home/claude/odd')
import cairo
from PIL import Image, ImageFilter
from anim import (hexc, lerp, clamp, ease_io, ease_out_back, smooth, mixc, ellipse, fs, stroke_dev,
                  draw_body, shell_part, star, draw_text, hop, burst, OUT, W, H, FPS)
from anim2 import obj_frog, big_word, glow, face
from anim3 import ITEMS as ITEMS0, rrect, clean_text, star5, check_badge, CONF_COLS

TL = json.load(open('/home/claude/mem/timeline.json'))
RS = TL['rounds']; OUTRO = TL['outro']; DUR = TL['dur']; TIMER = TL['timer']
DARK = hexc('#3B2A6B')
LVL = ['#3ECF5E', '#2EA7FF', '#A15CFF', '#FF4D4D']
ITEMS = dict(ITEMS0); ITEMS['frog'] = lambda c, t: (c.save(), c.scale(0.9, 0.9), obj_frog(c, 1), c.restore())
ITEMS['butterfly'] = ITEMS0['bfly']
NAMES = dict(fish='fish', grapes='grapes', butterfly='butterfly')
PANEL = (60, 640, 960, 840)
rr = random.Random(33)

def geo(grid):
    if grid == (2, 2): return 330, [(355, 875), (725, 875), (355, 1245), (725, 1245)]
    if grid == (3, 2): return 270, [(x, y) for y in (910, 1210) for x in (240, 540, 840)]
    return 240, [(x, y) for y in (790, 1058, 1326) for x in (262, 540, 818)]

# ---------------- studio background ----------------
def build_bg():
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); cr = cairo.Context(s)
    g = cairo.RadialGradient(540, 760, 50, 540, 900, 1300)
    g.add_color_stop_rgb(0, *hexc('#8A4DF0')); g.add_color_stop_rgb(0.55, *hexc('#4B1FA8')); g.add_color_stop_rgb(1, *hexc('#1C0B4A'))
    cr.set_source(g); cr.paint()
    for i in range(70):
        x, y = rr.uniform(0, W), rr.uniform(120, 1450)
        star(cr, x, y, rr.uniform(4, 10)); cr.set_source_rgba(1, 1, 1, rr.uniform(0.15, 0.45)); cr.fill()
    # floor
    fg = cairo.LinearGradient(0, 1500, 0, H); fg.add_color_stop_rgb(0, *hexc('#3A1580')); fg.add_color_stop_rgb(1, *hexc('#14062F'))
    cr.rectangle(0, 1500, W, H - 1500); cr.set_source(fg); cr.fill()
    for k in range(9):
        x = -200 + k * 190
        cr.move_to(540 + (x - 540) * 0.35, 1500); cr.line_to(x, H); stroke_dev(cr, (1, 1, 1), 2, 0.07)
    for k in range(5):
        y = 1500 + (k + 1) ** 1.6 * 22
        cr.move_to(0, y); cr.line_to(W, y); stroke_dev(cr, (1, 1, 1), 2, 0.06)
    cr.move_to(0, 1500); cr.line_to(W, 1500); stroke_dev(cr, hexc('#FFC93B'), 8)
    ellipse(cr, 540, 1560, 460, 70); cr.set_source_rgba(1, 0.9, 1, 0.10); cr.fill()
    # curtains
    for side in (-1, 1):
        cr.save()
        if side == 1: cr.translate(W, 0); cr.scale(-1, 1)
        cr.move_to(0, 0); cr.line_to(150, 0); cr.curve_to(120, 600, 60, 1100, 135, 1520); cr.line_to(0, 1520); cr.close_path()
        cg = cairo.LinearGradient(0, 0, 150, 0)
        for j in range(7):
            cg.add_color_stop_rgb(j / 6, *(hexc('#D6203C') if j % 2 == 0 else hexc('#8E0F24')))
        cr.set_source(cg); cr.fill_preserve(); stroke_dev(cr, hexc('#5C0716'), 5)
        cr.move_to(118, 900); cr.curve_to(150, 920, 150, 960, 112, 975); stroke_dev(cr, hexc('#FFC93B'), 12)
        cr.restore()
    # valance
    cr.move_to(0, 0); cr.line_to(W, 0); cr.line_to(W, 95)
    for j in range(12, -1, -1):
        x = j * 90; cr.curve_to(x + 60, 150, x + 30, 150, x, 95)
    cr.close_path()
    vg = cairo.LinearGradient(0, 0, 0, 150); vg.add_color_stop_rgb(0, *hexc('#E0294A')); vg.add_color_stop_rgb(1, *hexc('#9C1029'))
    cr.set_source(vg); cr.fill_preserve(); stroke_dev(cr, hexc('#FFC93B'), 8)
    s.flush()
    im = Image.frombuffer('RGBA', (W, H), bytes(s.get_data()), 'raw', 'BGRA', 0, 1).convert('RGB').filter(ImageFilter.GaussianBlur(2))
    data = bytearray(im.convert('RGBA').tobytes('raw', 'BGRA'))
    return cairo.ImageSurface.create_for_data(data, cairo.FORMAT_ARGB32, W, H), data
BG, _BD = build_bg()

BULBS = []
def _bulbs():
    x0, y0, w, h = PANEL; step = 56
    pts = []
    for x in range(int(x0 + 40), int(x0 + w - 30), step): pts.append((x, y0))
    for y in range(int(y0 + 40), int(y0 + h - 30), step): pts.append((x0 + w, y))
    for x in range(int(x0 + w - 40), int(x0 + 30), -step): pts.append((x, y0 + h))
    for y in range(int(y0 + h - 40), int(y0 + 30), -step): pts.append((x0, y))
    return pts
BULBS = _bulbs()

def panel(cr, t):
    x0, y0, w, h = PANEL
    rrect(cr, x0 - 8, y0 - 8, w + 16, h + 16, 58); cr.set_source_rgba(0, 0, 0, 0.35); cr.fill()
    rrect(cr, x0, y0, w, h, 50)
    pg = cairo.LinearGradient(0, y0, 0, y0 + h); pg.add_color_stop_rgb(0, *hexc('#2A1C6E')); pg.add_color_stop_rgb(1, *hexc('#170F45'))
    cr.set_source(pg); cr.fill_preserve(); stroke_dev(cr, hexc('#FFC93B'), 22)
    rrect(cr, x0, y0, w, h, 50); stroke_dev(cr, hexc('#B8860B'), 4)
    gg = cairo.RadialGradient(540, 1060, 50, 540, 1060, 520)
    gg.add_color_stop_rgba(0, 0.6, 0.5, 1, 0.25); gg.add_color_stop_rgba(1, 0.6, 0.5, 1, 0)
    rrect(cr, x0 + 12, y0 + 12, w - 24, h - 24, 40); cr.set_source(gg); cr.fill()
    ph = int(t * 8)
    for j, (bx, by) in enumerate(BULBS):
        on = (j + ph) % 3 == 0
        if on: glow(cr, bx, by, 34, (1, 0.95, 0.6), 0.6)
        cr.arc(bx, by, 11, 0, 2 * math.pi); cr.set_source_rgb(*(hexc('#FFF6C8') if on else hexc('#B98A22'))); cr.fill()

def spotlights(cr, t):
    for k, (bx, sp, col) in enumerate(((180, 0.6, (1, 0.6, 0.9)), (900, 0.7, (0.6, 0.8, 1)), (540, 0.4, (1, 1, 0.8)))):
        a = math.pi / 2 + 0.35 * math.sin(t * sp + k * 2)
        L = 2200; wdt = 0.13
        cr.move_to(bx, -60)
        cr.line_to(bx + L * math.cos(a - wdt), -60 + L * math.sin(a - wdt)); cr.line_to(bx + L * math.cos(a + wdt), -60 + L * math.sin(a + wdt))
        cr.close_path(); cr.set_source_rgba(*col, 0.07); cr.fill()

# ---------------- cards ----------------
def card_front(cr, S, lvl, item, t):
    c = hexc(LVL[lvl]); h = S / 2; r = S * 0.12
    rrect(cr, -h, -h, S, S, r)
    g = cairo.LinearGradient(0, -h, 0, h); g.add_color_stop_rgb(0, 1, 1, 1); g.add_color_stop_rgb(1, *mixc(c, (1, 1, 1), 0.8))
    cr.set_source(g); cr.fill_preserve(); stroke_dev(cr, OUT, 6)
    rrect(cr, -h + 11, -h + 11, S - 22, S - 22, r - 8); stroke_dev(cr, c, 6, 0.85)
    k = S / 380 * 0.8; cr.save(); cr.scale(k, k); ITEMS[item](cr, t); cr.restore()

def card_back(cr, S, t, j):
    h = S / 2; r = S * 0.12
    rrect(cr, -h, -h, S, S, r)
    g = cairo.LinearGradient(-h, -h, h, h); g.add_color_stop_rgb(0, *hexc('#FF5FA2')); g.add_color_stop_rgb(1, *hexc('#C21877'))
    cr.set_source(g); cr.fill_preserve(); stroke_dev(cr, OUT, 6)
    rrect(cr, -h + 10, -h + 10, S - 20, S - 20, r - 7); stroke_dev(cr, hexc('#FFC93B'), 5)
    for q in range(4):
        star5(cr, (-1 if q % 2 else 1) * h * 0.62, (-1 if q < 2 else 1) * h * 0.62, S * 0.05); cr.set_source_rgba(1, 0.9, 0.5, 0.7); cr.fill()
    big_word(cr, "?", 0, 0, S * 0.6, hexc('#FFD93B'), 1.0)

def flip_state(t, flips):
    """flips: list of (t0, dur, to_front). returns (sx, front)"""
    front = False; sx = 1
    for t0, d, tf in flips:
        if t < t0: break
        u = (t - t0) / d
        if u >= 1: front = tf; sx = 1; continue
        if u < 0.5: sx = math.cos(math.pi * u)   # still old side
        else: front = tf; sx = abs(math.cos(math.pi * u))
        return max(sx, 0.0), front
    return sx, front

def cur_round(t):
    c = None
    for r in RS:
        if t >= r['start']: c = r
    return c if c and t < c['end'] else None

def check(cr, x, y, s): check_badge(cr, x, y, s)

BURST = [(rr.uniform(0, 6.28), rr.uniform(450, 950), rr.choice(CONF_COLS), rr.uniform(0, 6.28)) for _ in range(46)]
RAIN = [(rr.uniform(0, 1080), rr.uniform(0, 1.8), rr.uniform(280, 520), rr.uniform(0, 6.28), rr.choice(CONF_COLS)) for _ in range(120)]

def host(cr, x, by, h, sx, sy, sc, st, t, look):
    cr.save(); cr.translate(x, by - h); cr.scale(sx * sc, sy * sc)
    draw_body(cr, 0, -215, 1.0, st, t, look)
    # top hat
    cr.save(); cr.translate(18, -330); cr.rotate(0.12)
    ellipse(cr, 0, 0, 78, 16); fs(cr, hexc('#2B1B5A'))
    cr.rectangle(-48, -95, 96, 95); fs(cr, hexc('#3A2775'))
    cr.rectangle(-48, -32, 96, 20); cr.set_source_rgb(*hexc('#FF4D6D')); cr.fill()
    ellipse(cr, 0, -95, 48, 12); fs(cr, hexc('#4A3590'))
    star5(cr, 28, -60, 12); cr.set_source_rgb(*hexc('#FFD93B')); cr.fill()
    cr.restore()
    shell_part(cr, top=False)
    # bow tie
    cr.save(); cr.translate(0, -150)
    for s in (-1, 1):
        cr.move_to(0, 0); cr.line_to(s * 58, -30); cr.line_to(s * 58, 30); cr.close_path(); fs(cr, hexc('#FF4D6D'), 5)
    cr.arc(0, 0, 16, 0, 2 * math.pi); fs(cr, hexc('#E0294A'), 5)
    cr.restore()
    cr.restore()

def trophy(cr, x, y, s, t):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.save(); cr.rotate(t * 0.3)
    for j in range(12):
        a = j * math.pi / 6; cr.move_to(0, 0); cr.arc(0, 0, 360, a, a + math.pi / 12); cr.close_path()
    cr.set_source_rgba(1, 0.9, 0.4, 0.3); cr.fill(); cr.restore()
    gold = hexc('#FFC93B'); dg = hexc('#D9A21F')
    for sgn in (-1, 1):
        cr.arc(sgn * 150, -90, 62, 0, 2 * math.pi); stroke_dev(cr, OUT, 34); cr.arc(sgn * 150, -90, 62, 0, 2 * math.pi); stroke_dev(cr, gold, 20)
    rrect(cr, -130, 210, 260, 70, 18); fs(cr, hexc('#7A4A2A'))
    rrect(cr, -80, 160, 160, 60, 14); fs(cr, gold, 6, OUT)
    cr.rectangle(-28, 70, 56, 100); fs(cr, gold)
    cr.move_to(-170, -190); cr.line_to(170, -190); cr.curve_to(170, 0, 90, 90, 0, 95); cr.curve_to(-90, 90, -170, 0, -170, -190); cr.close_path()
    g = cairo.LinearGradient(-170, 0, 170, 0); g.add_color_stop_rgb(0, *dg); g.add_color_stop_rgb(0.4, *hexc('#FFE27A')); g.add_color_stop_rgb(1, *dg)
    cr.set_source(g); cr.fill_preserve(); stroke_dev(cr, OUT, 8)
    ellipse(cr, 0, -190, 170, 26); fs(cr, hexc('#FFE27A'), 6)
    star5(cr, 0, -60, 62); fs(cr, hexc('#FFF3B0'), 6, dg)
    ellipse(cr, -105, -110, 16, 45); cr.set_source_rgba(1, 1, 1, 0.5); cr.fill()
    cr.restore()

# ---------------- frame ----------------
def frame(cr, t):
    cr.set_source_surface(BG, 0, 0); cr.paint()
    spotlights(cr, t)
    rd = cur_round(t); in_outro = t >= OUTRO['start']
    pk = 1 - smooth(OUTRO['start'], OUTRO['start'] + 0.5, t)
    if pk > 0.01:
        cr.save(); cr.translate(540, 1060); cr.scale(pk, pk); cr.translate(-540, -1060); panel(cr, t); cr.restore()
    if rd and rd['i'] == 3 and rd['timer'] <= t < rd['reveal']:
        pu = 0.5 + 0.5 * math.sin((t - rd['timer']) * 2 * math.pi * 1.2)
        vg = cairo.RadialGradient(540, 960, 500, 540, 960, 1200)
        vg.add_color_stop_rgba(0, 1, 0.2, 0.2, 0); vg.add_color_stop_rgba(1, 1, 0.1, 0.1, 0.15 + 0.12 * pu)
        cr.set_source(vg); cr.paint()

    # ---- cards
    if t < RS[0]['start']:
        S0, P0 = geo((2, 2))
        for j, (px, py) in enumerate(P0):
            sb = ease_out_back((t - 0.15 - 0.06 * j) / 0.35)
            if sb <= 0.02: continue
            cr.save(); cr.translate(px, py + 4 * math.sin(t * 2 + j)); cr.rotate(0.03 * math.sin(t * 5 + j)); cr.scale(sb, sb); card_back(cr, S0, t, j); cr.restore()
    if rd:
        S, P = geo(tuple(rd['grid'])); n = len(P); tg = rd['target']
        for j, (px, py) in enumerate(P):
            pop = 1.0 if rd['i'] == 0 else ease_out_back((t - rd['start'] - 0.03 * j) / 0.3)
            out_s = 1 - ease_io((t - (rd['end'] - 0.32 + 0.0)) / 0.32)
            sc = max(0, pop) * out_s
            if sc <= 0.02: continue
            flips = [(rd['start'] + 0.3 + 0.05 * j, 0.35, True), (rd['mem1'] + 0.04 * j, 0.35, False)]
            if j == tg: flips.append((rd['reveal'], 0.4, True))
            else: flips.append((rd['all_up'] + 0.05 * j, 0.35, True))
            sx, front = flip_state(t, flips)
            hl = smooth(rd['reveal'] + 0.2, rd['reveal'] + 0.45, t) if j == tg else 0
            wig = 0
            if rd['timer'] <= t < rd['reveal']: wig = 0.025 * math.sin(t * 9 + j * 1.7)
            if rd['kind'] == 'under' and j == tg and rd['mem1'] + 0.4 <= t < rd['reveal']:
                glow(cr, px, py, S * 0.95, (1, 0.9, 0.4), 0.5 + 0.2 * math.sin(t * 6))
            if hl > 0: glow(cr, px, py, S * 1.05, (1, 0.9, 0.3), 0.6 * hl)
            bob = 4 * math.sin(t * 2 + j)
            big = 1 + 0.08 * hl + 0.06 * burst(rd['reveal'] + 0.2, rd['reveal'] + 0.5, t)
            cr.save(); cr.translate(px, py + bob); cr.rotate(wig); cr.scale(sx * sc * big, sc * big)
            if sx > 0.01:
                if front: card_front(cr, S, rd['i'], rd['items'][j], t)
                else: card_back(cr, S, t, j)
            cr.restore()
            if hl > 0 and sx > 0.95:
                pr = smooth(rd['reveal'] + 0.3, rd['reveal'] + 0.7, t)
                cr.save(); cr.translate(px, py + bob); cr.rotate(-0.12)
                cr.arc(0, 0, S * 0.64, -2.2, -2.2 + 2.15 * math.pi * pr); cr.restore()
                stroke_dev(cr, hexc('#FF3B3B'), 13)
                check(cr, px + S * 0.44, py - S * 0.44, ease_out_back((t - rd['reveal'] - 0.45) / 0.35))
        # bouncing arrow for 'under'
        if rd['kind'] == 'under' and rd['mem1'] + 0.4 <= t < rd['reveal'] + 0.2:
            px, py = P[tg]; a = smooth(rd['mem1'] + 0.4, rd['mem1'] + 0.7, t) * (1 - smooth(rd['reveal'], rd['reveal'] + 0.2, t))
            yy = py - S * 0.5 - 70 - 22 * abs(math.sin(t * 6))
            cr.push_group()
            cr.move_to(px, yy + 60); cr.line_to(px - 50, yy); cr.line_to(px - 20, yy); cr.line_to(px - 20, yy - 60)
            cr.line_to(px + 20, yy - 60); cr.line_to(px + 20, yy); cr.line_to(px + 50, yy); cr.close_path()
            fs(cr, hexc('#FFD93B'), 7)
            cr.pop_group_to_source(); cr.paint_with_alpha(a)
        # confetti burst
        if t >= rd['reveal'] + 0.2:
            tt = t - rd['reveal'] - 0.2
            if tt < 1.4:
                px, py = P[tg]
                for ang, sp, c, ph in BURST:
                    x = px + math.cos(ang) * sp * tt; y = py + math.sin(ang) * sp * tt + 900 * tt * tt
                    cr.save(); cr.translate(x, y); cr.rotate(tt * 8 + ph); cr.scale(1, abs(math.sin(tt * 9 + ph)) + 0.2)
                    cr.rectangle(-11, -7, 22, 14); cr.set_source_rgba(*hexc(c), 1 - smooth(1.0, 1.4, tt)); cr.fill(); cr.restore()

    # ---- top: level badge / question bubble
    if rd:
        i = rd['i']
        qa = smooth(rd['mem1'] + 0.35, rd['mem1'] + 0.6, t) * (1 - smooth(rd['end'] - 0.35, rd['end'] - 0.1, t))
        ba = (1 - qa) * (smooth(rd['start'], rd['start'] + 0.2, t)) * (1 - smooth(rd['end'] - 0.3, rd['end'], t))
        if ba > 0.01:
            bs = max(0.01, ease_out_back((t - rd['start']) / 0.45)) if t < rd['start'] + 0.5 else 1
            cr.push_group(); cr.translate(410, 470); cr.scale(bs, bs)
            if i == 3: glow(cr, 0, 0, 240, (1, 0.3, 0.2), 0.5)
            rrect(cr, -190, -55, 380, 110, 55); fs(cr, hexc(LVL[i]), 7)
            rrect(cr, -178, -45, 356, 40, 20); cr.set_source_rgba(1, 1, 1, 0.25); cr.fill()
            clean_text(cr, "EXPERT!" if i == 3 else f"LEVEL {i + 1}", 0, 0, 70, (1, 1, 1), 10)
            for s in range(4):
                star5(cr, -72 + s * 48, 94, 24); fs(cr, hexc('#FFD93B') if s <= i else (0.86, 0.88, 0.92), 4)
            cr.pop_group_to_source(); cr.paint_with_alpha(ba)
        if qa > 0.01:
            qs = ease_out_back((t - rd['mem1'] - 0.35) / 0.35)
            cr.push_group(); cr.translate(420, 480); cr.scale(qs, qs)
            rrect(cr, -340, -95, 680, 190, 60); fs(cr, (1, 1, 1), 7)
            cr.move_to(330, -20); cr.line_to(400, 10); cr.line_to(330, 30); cr.close_path(); cr.set_source_rgb(1, 1, 1); cr.fill()
            cr.move_to(334, -20); cr.line_to(400, 10); cr.line_to(334, 30); stroke_dev(cr, OUT, 7)
            cr.arc(-245, 0, 72, 0, 2 * math.pi); fs(cr, mixc(hexc(LVL[i]), (1, 1, 1), 0.75), 5)
            if rd['kind'] == 'where':
                cr.save(); cr.translate(-245, 0); cr.scale(0.36, 0.36); ITEMS[rd['items'][rd['target']]](cr, t); cr.restore()
                txt = "Where is it?"
            else:
                cr.save(); cr.translate(-245, 0); card_back(cr, 100, t, 0); cr.restore()
                txt = "What's under?"
            clean_text(cr, txt, 60, 0, 66, DARK, 0.1, (1, 1, 1))
            cr.pop_group_to_source(); cr.paint_with_alpha(qa)

    # ---- bottom bars / labels
    if rd:
        bx, by, bw, bh = 540 - 300, 1540, 600, 54
        def bar(t0, t1, col_fn, label):
            a = smooth(t0 - 0.25, t0, t) * (1 - smooth(t1, t1 + 0.15, t))
            if a <= 0.01: return
            u = clamp((t - t0) / (t1 - t0)); D = t1 - t0
            cr.push_group()
            rrect(cr, bx, by, bw, bh, bh / 2); cr.set_source_rgba(0.05, 0.02, 0.15, 0.6); cr.fill_preserve(); stroke_dev(cr, hexc('#FFC93B'), 5)
            fw = (bw - 12) * (1 - u)
            if fw > 30:
                rrect(cr, bx + 6, by + 6, fw, bh - 12, (bh - 12) / 2); cr.set_source_rgb(*col_fn(u)); cr.fill()
                rrect(cr, bx + 14, by + 10, max(0, fw - 16), 11, 5); cr.set_source_rgba(1, 1, 1, 0.35); cr.fill()
            n = max(1, math.ceil(D * (1 - u) - 1e-6)); ph = (D * (1 - u)) % 1
            bsz = 1 + 0.2 * max(0, (ph - 0.75) * 4)
            cr.arc(bx - 10, by + bh / 2, 50 * bsz, 0, 2 * math.pi); fs(cr, (1, 1, 1), 6, DARK)
            clean_text(cr, str(n), bx - 10, by + bh / 2 - 2, 62 * bsz, hexc('#FF4D4D') if n == 1 else DARK, 3)
            clean_text(cr, label, 540, by + bh + 58, 58, (1, 1, 1), 9)
            cr.pop_group_to_source(); cr.paint_with_alpha(a)
        bar(rd['mem0'], rd['mem1'], lambda u: hexc('#5FD0FF'), "REMEMBER!")
        def warm(u):
            return mixc(hexc('#3ECF5E'), hexc('#FFD93B'), clamp(u * 2)) if u < 0.5 else mixc(hexc('#FFD93B'), hexc('#FF4D4D'), clamp((u - 0.5) * 2))
        bar(rd['timer'], rd['reveal'], warm, "THINK!")
        if t >= rd['reveal'] + 0.2:
            ws = ease_out_back((t - rd['reveal'] - 0.25) / 0.4) if t > rd['reveal'] + 0.25 else 0
            wa = 1 - smooth(rd['end'] - 0.3, rd['end'], t)
            big_word(cr, rd['label'], 540, 1585 + 6 * math.sin(t * 4), 100, hexc('#FFD93B'), max(0.01, ws), 0.03 * math.sin(t * 3), wa)

    # ---- outro
    if in_outro:
        ms = ease_out_back((t - OUTRO['start'] - 0.4) / 0.6) if t > OUTRO['start'] + 0.4 else 0
        if ms > 0.01:
            trophy(cr, 540, 860, 0.95 * ms, t)
            ts = ease_out_back((t - OUTRO['start'] - 0.8) / 0.5) if t > OUTRO['start'] + 0.8 else 0
            big_word(cr, "Memory Master!", 540, 1195, 118, hexc('#FFD93B'), max(0.01, ts))
        for x0, dl, sp, ph, c in RAIN:
            tt = t - OUTRO['start'] - dl
            if tt < 0: continue
            y = -40 + tt * sp
            if y > H + 40: continue
            x = x0 + 40 * math.sin(tt * 3 + ph)
            cr.save(); cr.translate(x, y); cr.rotate(tt * 5 + ph); cr.scale(1, abs(math.sin(tt * 6 + ph)) + 0.2)
            cr.rectangle(-11, -7, 22, 14); cr.set_source_rgb(*hexc(c)); cr.fill(); cr.restore()

    # ---- host chick
    st = dict(wing=[0.0, 0.6], beak=0.0, happy=0, mood=0.0)
    hh, sxx, syy = 0, 1, 1
    cx, cb, csc = 905, 652, 0.5
    look = (-0.7, 0.6)
    for e in TL['events']:
        if e['name'].startswith(('pre', 'q', 'hook')) and e['t'] <= t < e['t'] + e['dur']:
            st['beak'] = 0.45 * abs(math.sin(t * 14)); st['wing'] = [0.0, 0.9 + 0.3 * math.sin(t * 6)]
    if rd:
        S, P = geo(tuple(rd['grid']))
        if rd['mem0'] <= t < rd['mem1'] or rd['timer'] <= t < rd['reveal']:
            k = int(t * 1.2) % len(P); px, py = P[k]
            dx, dy = px - cx, py - (cb - 110); d = math.hypot(dx, dy) + 1e-6; look = (dx / d, dy / d)
        t0 = rd['reveal'] + 0.2
        if t0 <= t < t0 + 0.9:
            kk = int((t - t0) / 0.45)
            _, hh, sxx, syy, _, air = hop(t, t0 + 0.45 * kk, 0.45, 70, 0, 0)
            st.update(happy=1, wing=[0.4 + 0.8 * air, 0.4 + 0.8 * air], beak=0.6 * air)
    if in_outro:
        u = clamp((t - OUTRO['start'] - 0.15) / 0.7); e = ease_io(u)
        cx = lerp(905, 540, e); cb = lerp(652, 1640, e); csc = lerp(0.5, 0.78, e)
        hh = 380 * 4 * u * (1 - u) if u < 1 else 0; look = (0, 0.2)
        if u >= 1 and t < OUTRO['bye']:
            kk = int((t - OUTRO['start'] - 0.85) / 0.5)
            _, hh, sxx, syy, _, air = hop(t, OUTRO['start'] + 0.85 + 0.5 * kk, 0.5, 90, 0, 0)
            st.update(happy=1, wing=[0.4 + 0.9 * air, 0.4 + 0.9 * air], beak=0.6 * air)
        elif u >= 1:
            st.update(happy=1, wing=[0.1, 1.1 + 0.45 * math.sin(t * 13)], beak=0.5 * abs(math.sin(t * 7)))
        if u >= 1:
            ellipse(cr, cx, cb + 2, 90, 15); cr.set_source_rgba(0, 0, 0, 0.3); cr.fill()
    host(cr, cx, cb, hh, sxx, syy, csc, st, t, look)

    vg = cairo.RadialGradient(540, 960, 700, 540, 960, 1300)
    vg.add_color_stop_rgba(0, 0, 0, 0, 0); vg.add_color_stop_rgba(1, 0, 0, 0.1, 0.3)
    cr.set_source(vg); cr.paint()
    draw_text(cr, "Memory Challenge!", 250, 118, t, 0.1)

def make_surface():
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); return s, cairo.Context(s)

if __name__ == '__main__':
    if sys.argv[1] == 'png':
        for tt in sys.argv[2:]:
            s, cr = make_surface(); frame(cr, float(tt)); s.write_to_png(f'/home/claude/mem/t_{tt}.png')
    else:
        f0, f1 = int(sys.argv[2]), int(sys.argv[3]); out = sys.stdout.buffer
        for n in range(f0, f1):
            s, cr = make_surface(); frame(cr, n / FPS); s.flush(); out.write(bytes(s.get_data()))
