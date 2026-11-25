"""What Happens Next? (growing up) — seed→sprout→flower, caterpillar→cocoon→butterfly, egg→crack→chick. Twist: big spotty egg → baby dino!"""
import sys; sys.path.insert(0, '/home/claude/kit')
from common import *

F = '/home/claude/ep28'
C1, C2, C3 = (300, 650), (780, 650), (540, 1150)
ROUNDS = [dict(steps=('seed', 'sprout', 'flower'), intro="A seed... a little sprout...", a="A flower!", y="So pretty!", word='Flower!', col='#FF5FA2'),
          dict(steps=('cater', 'cocoon', 'bfly'), intro="A caterpillar... a cocoon...", a="A butterfly!", y="Flutter, flutter!", word='Butterfly!', col='#A15CFF'),
          dict(steps=('egg', 'crack', 'chick'), intro="An egg... crack, crack...", a="A baby chick!", y="Just like me!", word='Chick!', col='#FFB31F')]
TW = ('degg', 'dcrack', 'dino')


def build():
    s = Script(F); t = 0.1
    t = s.say(t, 'hook', "What happens next? Let's find out!") + 0.05
    t = s.say(t, 'ooh', "Ooh!", 1.0, True) + 0.15
    for i, r in enumerate(ROUNDS):
        s.mark(f's{i}', t if i else 0.05); t += 0.5 if i else 0.1
        t = s.say(t, f'in{i}', r['intro']) + 0.1
        t = s.say(t, f'q{i}', "What happens next?") + 0.05
        s.mark(f'c{i}', t); t += 3.0; s.mark(f'r{i}', t)
        t = s.say(t + 0.55, f'a{i}', r['a']) + 0.05
        t = s.say(t, f'y{i}', r['y'], 1.0, True) + 0.3
        s.mark(f'x{i}', t); t += 0.55
    s.mark('s3', t); t += 0.5
    t = s.say(t, 'in3', "A big, spotty egg... crack, crack...") + 0.1
    t = s.say(t, 'q3', "What happens next?") + 0.1
    s.mark('r3', t); t += 0.9
    t = s.say(t, 'rawr', "Rawr!", 1.0, False, 'am_puck') + 0.1
    t = s.say(t, 'dino', "A baby dinosaur! Hee hee!", 1.0, True) + 0.25
    s.mark('again', t); t = s.say(t, 'again', "Again?", 1.0, True) + 0.25
    s.mark('loop', t); t += 0.9
    tl = s.save(t); m = tl['marks']; mx = Mix(tl['dur'])
    mx.music_loop(0, tl['dur'], 104, [([60, 64, 67], 36), ([65, 69, 72], 41), ([64, 67, 71], 40), ([62, 65, 69], 38)],
                  [[72, None, 74, None, 76, None, 79, None], [77, None, 76, None, 74, None, None, None]], 'soft', 0.75)
    for i in range(4):
        mx.add('sfx', m[f's{i}'], pop(300, 900, 0.12), 0.25); mx.add('sfx', m[f's{i}'] + 0.25, pop(300, 1000, 0.12), 0.25)
        if i < 3: countdown_ticks(mx, m[f'c{i}'])
        mx.add('sfx', m[f'r{i}'], flick(), 0.3); mx.add('sfx', m[f'r{i}'] + 0.3, chime_up(), 0.22)
        if i < 3: mx.add('sfx', m[f'r{i}'] + 0.55, ding(), 0.18)
    mx.add('sfx', m['r3'] - 1.2, drumroll(1.2), 0.15)
    mx.add('sfx', m['r3'] + 0.3, tada(72), 0.15)
    mx.add('sfx', m['again'] + 0.2, jingle(), 0.22)
    mx.voices(F, tl['events'])
    mx.write(F + '/audio.wav', quiet=[(m[f'c{i}'], m[f'r{i}']) for i in range(3)]); return tl


TL = json.load(open(F + '/timeline.json')) if os.path.exists(F + '/timeline.json') else None


def soil(cr):
    cr.move_to(-150, 90); cr.curve_to(-120, 40, 120, 40, 150, 90); cr.close_path(); fs(cr, hexc('#9B6B43'))
    for x in (-60, 10, 70): cr.arc(x, 72, 6, 0, 2 * math.pi); cr.set_source_rgb(*hexc('#7A4F2E')); cr.fill()

def happy_face(cr, x, y, s=1.0, col=OUT):
    for sx in (-1, 1): cr.arc(x + sx * 18 * s, y, 7 * s, 0, 2 * math.pi); cr.set_source_rgb(*col); cr.fill()
    cr.arc(x, y + 8 * s, 10 * s, 0.15 * math.pi, 0.85 * math.pi); stroke_dev(cr, col, 4)

def p_seed(cr, t, g=1.0):
    soil(cr)
    cr.save(); cr.translate(0, 30); cr.rotate(0.3); ellipse(cr, 0, 0, 38, 26); fs(cr, hexc('#C9965A')); cr.restore()
    happy_face(cr, 2, 28, 0.8)

def p_sprout(cr, t, g=1.0):
    soil(cr)
    sw = 0.08 * math.sin(t * 2)
    cr.save(); cr.translate(0, 55); cr.rotate(sw)
    cr.move_to(0, 0); cr.curve_to(5, -40, -5, -70, 0, -100); stroke_dev(cr, OUT, 16); cr.move_to(0, 0); cr.curve_to(5, -40, -5, -70, 0, -100); stroke_dev(cr, hexc('#5BC24A'), 9)
    for sx in (-1, 1):
        cr.save(); cr.translate(0, -100); cr.rotate(sx * 0.5); ellipse(cr, sx * 38, 0, 40, 20); fs(cr, hexc('#7DD957')); cr.restore()
    cr.restore()

def p_flower(cr, t, g=1.0):
    soil(cr)
    sw = 0.06 * math.sin(t * 2)
    cr.save(); cr.translate(0, 55); cr.rotate(sw); cr.scale(g, g)
    cr.move_to(0, 0); cr.curve_to(10, -80, -10, -140, 0, -210); stroke_dev(cr, OUT, 18); cr.move_to(0, 0); cr.curve_to(10, -80, -10, -140, 0, -210); stroke_dev(cr, hexc('#5BC24A'), 10)
    for sx, y in ((-1, -70), (1, -110)):
        cr.save(); cr.translate(0, y); cr.rotate(sx * 0.5); ellipse(cr, sx * 40, 0, 42, 19); fs(cr, hexc('#7DD957')); cr.restore()
    cr.save(); cr.translate(0, -235); cr.rotate(t * 0.3)
    for k in range(6):
        a = k * math.pi / 3
        cr.save(); cr.rotate(a); ellipse(cr, 0, -62, 38, 52); fs(cr, hexc('#FF7EB6')); cr.restore()
    cr.restore()
    cr.arc(0, -235, 50, 0, 2 * math.pi); fs(cr, hexc('#FFD93B'))
    happy_face(cr, 0, -240, 1.1)
    cr.restore()

def p_cater(cr, t, g=1.0):
    cr.move_to(-150, 70); cr.line_to(150, 70); stroke_dev(cr, hexc('#9B6B43'), 16)
    for k in range(5):
        x = -110 + k * 48; y = 30 - 12 * abs(math.sin(t * 3 + k * 0.7))
        cr.arc(x, y, 34, 0, 2 * math.pi); fs(cr, hexc('#7DD957' if k % 2 else '#5BC24A'))
    hx, hy = 135, 5
    cr.arc(hx, hy, 44, 0, 2 * math.pi); fs(cr, hexc('#7DD957'))
    for sx in (-1, 1): cr.move_to(hx + sx * 15, hy - 40); cr.line_to(hx + sx * 28, hy - 75); stroke_dev(cr, OUT, 5); cr.arc(hx + sx * 28, hy - 78, 8, 0, 2 * math.pi); fs(cr, hexc('#FF5FA2'), 4)
    happy_face(cr, hx, hy, 0.9)

def p_cocoon(cr, t, g=1.0):
    cr.move_to(-150, -110); cr.line_to(150, -110); stroke_dev(cr, hexc('#9B6B43'), 16)
    cr.save(); cr.translate(0, -105); cr.rotate(0.08 * math.sin(t * 1.5))
    cr.move_to(0, 0); cr.line_to(0, 15); stroke_dev(cr, OUT, 4)
    cr.move_to(0, 15); cr.curve_to(70, 30, 65, 170, 0, 205); cr.curve_to(-65, 170, -70, 30, 0, 15); cr.close_path(); fs(cr, hexc('#D9A86C'))
    for y in (60, 100, 140): cr.move_to(-45, y); cr.curve_to(-15, y + 12, 15, y + 12, 45, y); stroke_dev(cr, hexc('#B98450'), 5)
    happy_face(cr, 0, 85, 0.8)
    cr.restore()

def p_bfly(cr, t, g=1.0):
    draw_bfly(cr, 0, -10 + 12 * math.sin(t * 2), t * 0.5, 0.1 * math.sin(t), 2.6 * g)

def egg_shape(cr, w=95, h=125, y0=0):
    cr.move_to(0, y0 - h); cr.curve_to(w * 0.75, y0 - h, w, y0 - h * 0.1, w, y0 + h * 0.2)
    cr.curve_to(w, y0 + h * 0.8, w * 0.55, y0 + h, 0, y0 + h); cr.curve_to(-w * 0.55, y0 + h, -w, y0 + h * 0.8, -w, y0 + h * 0.2)
    cr.curve_to(-w, y0 - h * 0.1, -w * 0.75, y0 - h, 0, y0 - h); cr.close_path()

def nest(cr):
    ellipse(cr, 0, 95, 150, 45); fs(cr, hexc('#C9965A'))
    for k in range(8): cr.move_to(-140 + k * 38, 80); cr.line_to(-110 + k * 38, 110); stroke_dev(cr, hexc('#9B6B43'), 5)

def p_egg(cr, t, g=1.0, dino=False, crack=False):
    nest(cr)
    cr.save(); cr.translate(0, -5); cr.rotate((0.12 if crack else 0.03) * math.sin(t * (14 if crack else 2)))
    w, h = (110, 140) if dino else (85, 110)
    egg_shape(cr, w, h); fs(cr, hexc('#FFF6E0'))
    if dino:
        cr.save(); egg_shape(cr, w - 3, h - 3); cr.clip()
        for x, y, r in ((-50, -60, 22), (40, -20, 28), (-20, 50, 24), (55, 70, 16), (-60, 20, 14)):
            cr.arc(x, y, r, 0, 2 * math.pi); cr.set_source_rgb(*hexc('#7DD957')); cr.fill()
        cr.restore()
    if crack:
        cr.move_to(-w * 0.9, -10); cr.line_to(-40, -40); cr.line_to(-10, 0); cr.line_to(25, -45); cr.line_to(55, -5); cr.line_to(w * 0.9, -30)
        stroke_dev(cr, OUT, 7)
    cr.restore()

def p_crack(cr, t, g=1.0): p_egg(cr, t, g, False, True)
def p_degg(cr, t, g=1.0): p_egg(cr, t, g, True, False)
def p_dcrack(cr, t, g=1.0): p_egg(cr, t, g, True, True)

def p_chick(cr, t, g=1.0):
    nest(cr)
    st = base_st(); st.update(happy=1, wing=[0.6 + 0.4 * math.sin(t * 8)] * 2)
    chick(cr, 0, 120, 0, 0.62 * g, st, t, (0, 0.2))

def p_dino(cr, t, g=1.0):
    nest(cr)
    cr.save(); cr.translate(0, 0); cr.scale(g, g)
    G = hexc('#7DD957'); Gd = hexc('#5BC24A')
    # tail and body
    cr.move_to(60, 40); cr.curve_to(140, 30, 170, -20, 185, -50); cr.curve_to(160, 10, 120, 70, 60, 80); cr.close_path(); fs(cr, G)
    ellipse(cr, 0, 20, 95, 85); fs(cr, G)
    ellipse(cr, 0, 45, 55, 45); cr.set_source_rgb(*hexc('#E3F7B0')); cr.fill()
    for k in range(5):
        x = -60 + k * 30; y = -150 + abs(k - 2) * 12
        cr.move_to(x - 16, y + 30); cr.line_to(x, y); cr.line_to(x + 16, y + 30); cr.close_path(); fs(cr, hexc('#FF9A1F'), 5)
    ellipse(cr, 0, -95, 92, 75); fs(cr, G)
    for sx in (-1, 1):
        cr.arc(sx * 34, -105, 15, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill()
        cr.arc(sx * 34 - 5, -110, 5, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()
        ellipse(cr, sx * 62, -75, 15, 9); cr.set_source_rgba(1, 0.45, 0.55, 0.5); cr.fill()
    roar = 0.5 + 0.5 * math.sin(t * 12)
    ellipse(cr, 0, -55, 34, 8 + 16 * roar); fs(cr, hexc('#7A2B3A'), 5)
    for sx in (-1, 1): cr.move_to(sx * 18, -60 - 8 * roar); cr.line_to(sx * 10, -48 - 8 * roar); cr.line_to(sx * 2, -60 - 8 * roar); cr.close_path(); cr.set_source_rgb(1, 1, 1); cr.fill()
    for sx in (-1, 1): ellipse(cr, sx * 70, 30, 22, 30); fs(cr, Gd)
    cr.restore()
    # shell halves
    cr.save(); cr.translate(0, -5)
    cr.move_to(-110, 30); cr.line_to(-70, 0); cr.line_to(-35, 30); cr.line_to(0, 0); cr.line_to(35, 30); cr.line_to(70, 0); cr.line_to(110, 30)
    cr.curve_to(110, 110, 60, 140, 0, 140); cr.curve_to(-60, 140, -110, 110, -110, 30); cr.close_path(); fs(cr, hexc('#FFF6E0'))
    cr.restore()

PIC = dict(seed=p_seed, sprout=p_sprout, flower=p_flower, cater=p_cater, cocoon=p_cocoon, bfly=p_bfly,
           egg=p_egg, crack=p_crack, chick=p_chick, degg=p_degg, dcrack=p_dcrack, dino=p_dino)


def panel(cr, x, y, w, h, s, fn, t, sc=1.0, flip=1.0, q=False, num=None, glow_a=0.0):
    if s <= 0.01: return
    cr.save(); cr.translate(x, y); cr.scale(s * max(0.02, abs(flip)), s)
    if glow_a > 0: glow(cr, 0, 0, max(w, h) * 0.75, (1, 0.9, 0.3), glow_a)
    rrect(cr, -w / 2, -h / 2, w, h, 36); fs(cr, (1, 1, 1))
    if q:
        rrect(cr, -w / 2 + 14, -h / 2 + 14, w - 28, h - 28, 26); cr.set_source_rgb(*hexc('#FFE7A8')); cr.fill()
        big_word(cr, "?", 0, 10, h * 0.6, hexc('#FF9A1F'), 1.0, 0.1 * math.sin(t * 3))
    else:
        cr.save(); rrect(cr, -w / 2 + 6, -h / 2 + 6, w - 12, h - 12, 30); cr.clip()
        cr.set_source_rgb(*hexc('#EAF8FF')); cr.paint()
        cr.translate(0, h * 0.08); cr.scale(sc, sc); fn(cr, t)
        cr.restore()
    if num:
        cr.arc(-w / 2 + 34, -h / 2 + 34, 26, 0, 2 * math.pi); fs(cr, hexc('#3FB4FF'), 5)
        big_word(cr, str(num), -w / 2 + 34, -h / 2 + 36, 34, (1, 1, 1), 1.0)
    cr.restore()

def arrow(cr, x0, y0, x1, y1, p, t):
    if p <= 0.01: return
    xm, ym = lerp(x0, x1, p), lerp(y0, y1, p)
    cr.move_to(x0, y0); cr.line_to(xm, ym); stroke_dev(cr, OUT, 18); cr.move_to(x0, y0); cr.line_to(xm, ym); stroke_dev(cr, hexc('#FFC93C'), 10)
    a = math.atan2(y1 - y0, x1 - x0)
    cr.save(); cr.translate(xm, ym); cr.rotate(a); cr.move_to(16, 0); cr.line_to(-20, -22); cr.line_to(-20, 22); cr.close_path(); fs(cr, hexc('#FFC93C'), 6); cr.restore()


def frame(cr, t):
    m = TL['marks']
    te = 0.0 if t >= m['loop'] else t
    sky(cr, '#9FE0FF', '#F0FBFF', 1500)
    clouds(cr, t, ((800, 420, 0.4), (200, 440, 0.35)))
    hills(cr, 1430, '#A6E58A', 50); ground(cr, 1520)
    ri = 0
    for i in range(4):
        if te >= m[f's{i}']: ri = i
    steps = ROUNDS[ri]['steps'] if ri < 3 else TW
    s0 = m[f's{ri}']; rv = m[f'r{ri}']
    x0 = m[f'x{ri}'] if ri < 3 else 1e9
    out_ = smooth(x0, x0 + 0.3, te)
    a1 = ease_out_back(clamp((te - s0) / 0.4), 1.6) * (1 - out_)
    a2 = ease_out_back(clamp((te - s0 - 0.25) / 0.4), 1.6) * (1 - out_)
    a3 = ease_out_back(clamp((te - s0 - 0.5) / 0.4), 1.6) * (1 - out_)
    panel(cr, *C1, 400, 330, a1, PIC[steps[0]], te, 0.85)
    panel(cr, *C2, 400, 330, a2, PIC[steps[1]], te, 0.85)
    if te < x0:
        arrow(cr, C1[0] + 205, C1[1], C2[0] - 215, C2[1], smooth(s0 + 0.25, s0 + 0.5, te), te)
        arrow(cr, C2[0] - 40, C2[1] + 175, C3[0] + 120, C3[1] - 285, smooth(s0 + 0.5, s0 + 0.75, te), te)
    fu = clamp((te - rv) / 0.45)
    flip = math.cos(math.pi * fu) if te >= rv else 1.0
    revealed = te >= rv + 0.225
    grow = ease_out_back(clamp((te - rv - 0.25) / 0.6), 1.7) if revealed else 0
    gl = 0.8 * burst(rv + 0.2, rv + 1.0, te)
    panel(cr, *C3, 620, 540, a3, PIC[steps[2]], te, 1.35 * max(0.3, grow), flip, q=not revealed, glow_a=gl)
    if te >= rv + 0.3: sparkles(cr, C3[0], C3[1], rv + 0.3, te, 9, 300, 420)
    if ri == 3 and te >= rv + 0.3: confetti(cr, rv + 0.3, te, 540, 900, 650)
    # chickpea
    st = chick_talk(base_st(), te, TL); h = 0; sx = sy = 1; look = (0.6, -0.8)
    for i in range(3):
        if m[f'c{i}'] <= te < m[f'r{i}']: look = (0.5 + 0.3 * math.sin(te * 2), -1.0)
        if m[f'r{i}'] + 0.55 <= te < m[f'r{i}'] + 1.5:
            h, sx, sy, air = hop_seq(te, m[f'r{i}'] + 0.55, 2, 0.45, 55); st.update(happy=1, wing=[0.3 + 0.8 * air] * 2)
    if ri == 3 and te >= rv:
        if te < rv + 1.6: st['mood'] = 0.0; st['wing'] = [0.9, 0.9]; sx = 1 + 0.03 * math.sin(te * 40)
        else: st.update(happy=1, wing=[0.6 + 0.4 * math.sin(te * 9)] * 2)
    shadow_at(cr, 170, 1823, 100)
    chick(cr, 170, 1820, h, 0.72, st, te, look, sx, sy, acc='straw')
    for i in range(3):
        count_bubble(cr, m[f'c{i}'], te, "Say it!", y=1500, w=440)
        word_pop(cr, ROUNDS[i]['word'], 600, 1520, 130, ROUNDS[i]['col'], m[f'r{i}'] + 0.55, m[f'x{i}'] + 0.2, te)
    word_pop(cr, "Rawr!", 600, 1520, 150, '#3ECF5E', m['r3'] + 0.5, m['again'] + 0.3, te, 0.1)
    draw_text(cr, "What Happens Next?", 250, 115, t, -1)
    loop_fade(cr, TL, t)

if __name__ == '__main__': episode_main(build, F)
