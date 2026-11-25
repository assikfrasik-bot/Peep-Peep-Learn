"""Shared helpers for new Chickpea episodes (12+). Same visual language as episodes 1-11."""
import sys, math, json, random, os
sys.path.insert(0, '/home/claude/kit')
from kit import *
import cairo
from anim import (hexc, lerp, clamp, ease_io, ease_out_back, smooth, mixc, ellipse, fs, stroke_dev, draw_body, shell_part,
                  star, draw_text, hop, burst, draw_sun, draw_cloud, draw_flower, tree, bush, draw_snail, draw_bfly, draw_egg,
                  OUT, W, H, YEL, YEL2, BEAK, EGG)
from anim2 import big_word, glow, face, obj_apple, obj_carrot, obj_banana, obj_frog, obj_whale, obj_grapes
from anim3 import rrect, clean_text, star5, item_star, item_heart, item_fish, item_crab, bfly_c, check_badge, magnifier

DARK = hexc('#3B2A6B')
CONF_COLS = ['#FF4D4D', '#FF9A1F', '#FFD93B', '#3ECF5E', '#2EA7FF', '#A15CFF', '#FF5FA2']
_r = random.Random(99)
CONF = [(_r.uniform(-1, 1), _r.uniform(-1.25, -0.45), _r.choice(CONF_COLS), _r.uniform(0, 6.28), _r.uniform(0.7, 1.3)) for _ in range(60)]


def chick_talk(st, t, TL):
    for e in TL['events']:
        if e['chick'] and e['t'] <= t < e['t'] + e['dur']:
            st['beak'] = 0.5 * abs(math.sin(t * 14)); st['happy'] = 1
    return st


def base_st():
    return dict(wing=[0.0, 0.0], beak=0.0, happy=0, mood=0.0)


def hop_seq(t, t0, n=2, d=0.45, hgt=60):
    """n little hops starting at t0. returns (h, sx, sy, air)."""
    if t < t0 or t >= t0 + n * d: return 0, 1, 1, 0
    k = int((t - t0) / d); _, h, sx, sy, _, air = hop(t, t0 + d * k, d, hgt, 0, 0)
    return h, sx, sy, air


# ---------------- accessories (drawn in chick body space, body centre at (0,-215)) ----------------
def acc_sailor(cr, t):
    cr.save(); cr.translate(0, -335)
    cr.move_to(-92, 10); cr.curve_to(-92, -60, 92, -60, 92, 10); cr.close_path(); fs(cr, (1, 1, 1))
    rrect(cr, -100, -4, 200, 30, 14); fs(cr, hexc('#2E6BD9'))
    cr.arc(0, -52, 13, 0, 2 * math.pi); fs(cr, hexc('#FF4D4D'), 5)
    cr.restore()

def acc_straw(cr, t):
    cr.save(); cr.translate(0, -330)
    ellipse(cr, 0, 6, 150, 30); fs(cr, hexc('#F2C14E'))
    cr.move_to(-78, 6); cr.curve_to(-78, -80, 78, -80, 78, 6); cr.close_path(); fs(cr, hexc('#F7D46B'))
    rrect(cr, -79, -18, 158, 20, 8); fs(cr, hexc('#E8573F'), 5)
    for x in (-50, -15, 20, 55):
        cr.move_to(x, -55); cr.line_to(x + 6, -25); stroke_dev(cr, hexc('#D9A93A'), 3)
    cr.restore()

def acc_chef(cr, t):
    cr.save(); cr.translate(0, -330)
    rrect(cr, -70, -40, 140, 50, 12); fs(cr, (1, 1, 1))
    for bx, by, r in ((-48, -78, 44), (0, -100, 52), (48, -78, 44)):
        cr.arc(bx, by, r, 0, 2 * math.pi); cr.new_sub_path()
    stroke_dev(cr, OUT, 12)
    for bx, by, r in ((-48, -78, 44), (0, -100, 52), (48, -78, 44)):
        cr.arc(bx, by, r, 0, 2 * math.pi); cr.new_sub_path()
    cr.set_source_rgb(1, 1, 1); cr.fill()
    rrect(cr, -70, -40, 140, 50, 12); cr.set_source_rgb(1, 1, 1); cr.fill()
    cr.move_to(-70, -40); cr.line_to(70, -40); stroke_dev(cr, hexc('#DDE3EA'), 4)
    cr.restore()

def acc_beret(cr, t):
    cr.save(); cr.translate(0, -330); cr.rotate(-0.18)
    ellipse(cr, 0, -10, 105, 42); fs(cr, hexc('#E8455A'))
    cr.move_to(0, -52); cr.line_to(4, -76); stroke_dev(cr, OUT, 8)
    cr.restore()

def acc_explorer(cr, t):
    cr.save(); cr.translate(0, -328)
    ellipse(cr, 0, 6, 135, 26); fs(cr, hexc('#D8B57A'))
    cr.move_to(-82, 6); cr.curve_to(-82, -92, 82, -92, 82, 6); cr.close_path(); fs(cr, hexc('#E9CB8E'))
    rrect(cr, -83, -16, 166, 20, 8); fs(cr, hexc('#7A5A3A'), 5)
    cr.restore()

def acc_astro(cr, t):
    """space helmet bubble around head + antenna"""
    cr.save(); cr.translate(0, -215)
    cr.arc(0, -10, 168, 0, 2 * math.pi); cr.set_source_rgba(0.75, 0.9, 1, 0.22); cr.fill()
    cr.arc(0, -10, 168, 0, 2 * math.pi); stroke_dev(cr, OUT, 7)
    cr.arc(0, -10, 150, math.pi * 1.15, math.pi * 1.45); stroke_dev(cr, (1, 1, 1), 10, 0.8)
    cr.move_to(0, -178); cr.line_to(0, -232); stroke_dev(cr, OUT, 6)
    cr.arc(0, -240, 14 + 2 * math.sin(t * 6), 0, 2 * math.pi); fs(cr, hexc('#FF4D4D'), 5)
    cr.restore()

def acc_raincoat(cr, t):
    cr.save(); cr.translate(0, -325)
    cr.move_to(-120, 30); cr.curve_to(-110, -90, 110, -90, 120, 30); cr.curve_to(60, 10, -60, 10, -120, 30); cr.close_path()
    fs(cr, hexc('#FFD21F'))
    cr.move_to(-60, -40); cr.curve_to(-20, -62, 20, -62, 60, -40); stroke_dev(cr, hexc('#E3B400'), 4)
    cr.restore()

def acc_crown(cr, t):
    cr.save(); cr.translate(0, -330)
    cr.move_to(-70, 10); cr.line_to(-80, -60); cr.line_to(-40, -25); cr.line_to(0, -75); cr.line_to(40, -25); cr.line_to(80, -60); cr.line_to(70, 10)
    cr.close_path(); fs(cr, hexc('#FFC93C'))
    for x, c in ((-40, '#FF4D4D'), (0, '#2EA7FF'), (40, '#3ECF5E')):
        cr.arc(x, -8, 10, 0, 2 * math.pi); fs(cr, hexc(c), 4)
    cr.restore()

def acc_nightcap(cr, t):
    cr.save(); cr.translate(0, -330)
    cr.move_to(-90, 15); cr.curve_to(-60, -80, 40, -120, 120, -40); cr.curve_to(60, -50, 40, -10, 90, 15); cr.close_path()
    fs(cr, hexc('#6C7BFF'))
    for x, y in ((-30, -30), (20, -60), (55, -30)):
        star5(cr, x, y, 10); cr.set_source_rgb(*hexc('#FFE27A')); cr.fill()
    rrect(cr, -100, 0, 200, 30, 15); fs(cr, (1, 1, 1))
    cr.arc(125, -40, 18, 0, 2 * math.pi); fs(cr, (1, 1, 1))
    cr.restore()

def acc_bow(cr, t):
    cr.save(); cr.translate(55, -320); cr.rotate(0.3)
    for s in (-1, 1):
        cr.move_to(0, 0); cr.curve_to(s * 40, -40, s * 70, -20, s * 60, 0); cr.curve_to(s * 70, 20, s * 40, 40, 0, 0); cr.close_path(); fs(cr, hexc('#FF5FA2'))
    cr.arc(0, 0, 13, 0, 2 * math.pi); fs(cr, hexc('#FF8CC0'), 5)
    cr.restore()

def acc_glasses(cr, t):
    for s in (-1, 1):
        rrect(cr, s * 40 - 30, -255, 60, 40, 16); fs(cr, hexc('#2B2B3A'), 5)
        cr.move_to(s * 40 - 18, -246); cr.line_to(s * 40 - 4, -246); stroke_dev(cr, (1, 1, 1), 4, 0.7)
    cr.move_to(-10, -238); cr.line_to(10, -238); stroke_dev(cr, OUT, 6)

ACC = dict(sailor=acc_sailor, straw=acc_straw, chef=acc_chef, beret=acc_beret, explorer=acc_explorer, astro=acc_astro,
           raincoat=acc_raincoat, crown=acc_crown, nightcap=acc_nightcap, bow=acc_bow, glasses=acc_glasses)


def chick(cr, x, by, h, sc, st, t, look, sx=1, sy=1, acc=None, rot=0.0, shell=True, extra=None):
    cr.save(); cr.translate(x, by - h); cr.rotate(rot); cr.scale(sc * sx, sc * sy)
    draw_body(cr, 0, -215, 1.0, st, t, look)
    accs = acc if isinstance(acc, (list, tuple)) else ([acc] if acc else [])
    for a in accs: ACC[a](cr, t)
    if extra: extra(cr, t)
    if shell: shell_part(cr, top=False)
    cr.restore()


def shadow_at(cr, x, y, rx, a=0.22):
    ellipse(cr, x, y, rx, rx * 0.17); cr.set_source_rgba(0, 0, 0, a); cr.fill()


# ---------------- UI ----------------
def count_bubble(cr, t0, t, label="Say it!", y=470, dur=3.0, w=480):
    u = (t - t0) / dur
    if not (0 <= u < 1): return
    n = 3 - min(2, int(u * 3)); ph = (u * 3) % 1; s = 1 + 0.25 * max(0, 1 - ph * 5)
    a = smooth(t0, t0 + 0.2, t) * (1 - smooth(t0 + dur - 0.2, t0 + dur, t))
    x0 = 540 - w / 2
    cr.push_group()
    rrect(cr, x0, y - 75, w, 150, 75); fs(cr, (1, 1, 1), 7, DARK)
    cr.arc(x0 + 90, y, 52 * s, 0, 2 * math.pi); fs(cr, hexc('#FFD93B'), 6, DARK)
    clean_text(cr, str(n), x0 + 90, y - 4, 70 * s, hexc('#FF4D4D'), 3)
    clean_text(cr, label, x0 + 90 + (w - 90) / 2 + 10, y, 62, DARK, 0.1, (1, 1, 1))
    cr.pop_group_to_source(); cr.paint_with_alpha(a)


def word_pop(cr, text, cx, cy, size, col, t0, t1, t, rot_amp=0.04):
    if not (t0 <= t < t1 + 0.3): return
    e = ease_out_back((t - t0) / 0.45); a = 1 - smooth(t1, t1 + 0.3, t)
    big_word(cr, text, cx, cy, size, hexc(col) if isinstance(col, str) else col, e, rot_amp * math.sin(t * 3), a)


def confetti(cr, t0, t, cx=540, cy=900, spread=650, dur=2.2):
    u = t - t0
    if u < 0 or u > dur: return
    a = 1 - smooth(dur - 0.5, dur, t0 + u) if False else 1 - clamp((u - dur + 0.5) / 0.5)
    for vx, vy, c, ph, sp in CONF:
        x = cx + vx * spread * u * sp; y = cy + vy * 1100 * u * sp + 900 * u * u
        cr.save(); cr.translate(x, y); cr.rotate(ph + u * 6 * vx)
        cr.rectangle(-9, -15, 18, 30); cr.set_source_rgba(*hexc(c), a); cr.fill(); cr.restore()


def sparkles(cr, cx, cy, t0, t, n=7, r0=120, r1=230, col=(1, 0.95, 0.5)):
    u = t - t0
    if u < 0 or u > 0.9: return
    a = 1 - clamp(u / 0.9)
    for k in range(n):
        ang = k / n * 2 * math.pi + 0.3
        r = lerp(r0, r1, ease_io(u / 0.9))
        star(cr, cx + r * math.cos(ang), cy + r * math.sin(ang), 26 * (1 - u * 0.6)); cr.set_source_rgba(*col, a); cr.fill()


def ring_mark(cr, x, y, rx, ry, p, col='#FF3B3B', lw=12):
    if p <= 0: return
    cr.save(); cr.translate(x, y); cr.scale(rx, ry); cr.arc(0, 0, 1, -2.2, -2.2 + 2.15 * math.pi * p); cr.restore()
    stroke_dev(cr, hexc(col), lw)


def loop_fade(cr, TL, t):
    """quick white blink at the loop point so the end flows into the first frame"""
    m = TL['marks']
    if 'loop' in m:
        a = burst(m['loop'] - 0.25, m['loop'] + 0.25, t) if t < m['loop'] + 0.25 else 0
        if a > 0: cr.set_source_rgba(1, 1, 1, 0.55 * a); cr.paint()


# ---------------- scenery ----------------
def sky(cr, top='#4DB8FF', bot='#E0F7FF', y1=1400):
    g = cairo.LinearGradient(0, 0, 0, y1); g.add_color_stop_rgb(0, *hexc(top)); g.add_color_stop_rgb(1, *hexc(bot))
    cr.set_source(g); cr.paint()


def clouds(cr, t, items=((700, 420, 0.5), (250, 650, 0.4), (950, 760, 0.35)), speed=14, col=(1, 1, 1)):
    for x, y, s in items:
        draw_cloud(cr, (x + t * speed + 300) % 1500 - 300, y, s, col, outline=False)


def hills(cr, y0=1200, col='#A6E58A', amp=60):
    cr.move_to(0, H)
    for x in range(0, W + 21, 20): cr.line_to(x, y0 - amp * math.sin(math.pi * x / 1080 * 1.4 + 0.2))
    cr.line_to(W, H); cr.close_path(); cr.set_source_rgb(*hexc(col)); cr.fill()


def ground(cr, y0=1430, top='#62C64C', bot='#3E9E3A'):
    cr.move_to(0, H)
    for x in range(0, W + 21, 20): cr.line_to(x, y0 + 14 * math.sin(x / 180))
    cr.line_to(W, H); cr.close_path()
    hg = cairo.LinearGradient(0, y0, 0, H); hg.add_color_stop_rgb(0, *hexc(top)); hg.add_color_stop_rgb(1, *hexc(bot))
    cr.set_source(hg); cr.fill()


def small_sun(cr, t, x=140, y=420, sc=0.6):
    cr.save(); cr.translate(x - 870 * sc, y - 270 * sc); cr.scale(sc, sc); draw_sun(cr, t); cr.restore()


# ---------------- sound helpers ----------------
def countdown_ticks(mx, t0, g=0.33):
    for j in range(3): mx.add('sfx', t0 + j, tick(1100 if j < 2 else 1500), g)


def splash_snd(d=0.6):
    t = tt(d); out = bp(rng.standard_normal(len(t)), 300, 4000) * np.exp(-t / 0.12) * 0.8
    p = pop(500, 120, 0.18); out[:len(p)] += p * 0.6
    return out


def bubbles_snd(n=6, d=1.4):
    out = np.zeros(int(d * SR))
    for k in range(n):
        s = pop(600 + 300 * (k % 3), 1400 + 200 * k, 0.06); i = int((k * d / n + 0.03 * (k % 2)) * SR)
        out[i:i + len(s)] += s[:len(out) - i] * 0.6
    return out


def zap(f0=300, f1=1800, d=0.35):
    return slide_whistle(f0, f1, d)


def chime_up():
    out = np.zeros(int(1.2 * SR))
    for j, m in enumerate((79, 83, 86, 91)):
        s = bell(mtof(m), 0.9); i = int(j * 0.07 * SR); out[i:i + len(s)] += s * 0.7
    return out


def episode_main(build, F):
    if len(sys.argv) > 1 and sys.argv[1] == 'build':
        tl = build(); print(tl['dur'], tl['marks'])
