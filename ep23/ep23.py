"""Who's That Shadow? — shadow theatre: bunny, elephant, giraffe. Twist: a giant dinosaur shadow is just the snail on Chickpea's flashlight."""
import sys; sys.path.insert(0, '/home/claude/kit')
from common import *

F = '/home/claude/ep23'
SX0, SX1, SY0, SY1 = 90, 990, 400, 1250   # screen
GY = 1215                                   # animals' ground line
DARK = hexc('#2A2638')
ROUNDS = [dict(k='bunny', a="It's a bunny!", r="Hop, hop, hop!"),
          dict(k='elephant', a="It's an elephant!", r="Toot toot!"),
          dict(k='giraffe', a="It's a giraffe!", r="So tall!")]
FL = (700, 1640)   # flashlight head


def build():
    s = Script(F); t = 0.1
    t = s.say(t, 'hook', "Who's hiding behind the screen?") + 0.05
    t = s.say(t, 'ooh', "Ooh, shadows!", 1.0, True) + 0.15
    for i, r in enumerate(ROUNDS):
        s.mark(f's{i}', t); t += 0.7
        t = s.say(t, f'q{i}', "Who is this?") + 0.05
        s.mark(f'c{i}', t); t += 3.0; s.mark(f'r{i}', t)
        t = s.say(t + 0.55, f'a{i}', r['a']) + 0.05
        t = s.say(t, f'y{i}', r['r'], 1.0, True) + 0.3
        s.mark(f'x{i}', t); t += 0.6
    s.mark('tw', t)
    t = s.say(t, 'one', "One more shadow!") + 0.1
    s.mark('dino', t); t += 0.8
    t = s.say(t, 'big', "A big dinosaur?!") + 0.05
    t = s.say(t, 'eek', "Eek!", 1.05, True) + 0.25
    s.mark('up2', t); t += 1.0
    t = s.say(t, 'nobody', "Nobody's there...") + 0.2
    s.mark('look', t)
    t = s.say(t, 'snail', "Look! It's the little snail!") + 0.05
    t = s.say(t, 'silly', "Hee hee! Silly snail!", 1.0, True) + 0.25
    s.mark('again', t); t = s.say(t, 'again', "Again?", 1.0, True) + 0.25
    s.mark('loop', t); t += 0.9
    tl = s.save(t); m = tl['marks']; mx = Mix(tl['dur'])
    mx.music_loop(0, tl['dur'], 100, [([57, 60, 64], 45), ([53, 57, 60], 41), ([55, 59, 62], 43), ([57, 60, 64], 45)],
                  [[76, None, 72, None, 74, None, 71, None], [72, None, 69, None, None, 71, None, None]], 'soft', 0.7)
    for i in range(3):
        mx.add('sfx', m[f's{i}'], flick(), 0.25)
        countdown_ticks(mx, m[f'c{i}'])
        mx.add('sfx', m[f'r{i}'], slide_whistle(400, 1100, 0.5), 0.15)
        mx.add('sfx', m[f'r{i}'] + 0.55, ding(), 0.2); mx.add('sfx', m[f'r{i}'] + 0.7, chirp(), 0.12)
        mx.add('sfx', m[f'x{i}'], slide_whistle(1000, 500, 0.4), 0.1)
    for k in range(3): mx.add('sfx', m['r0'] + 1.7 + k * 0.3, boing(), 0.12)
    mx.add('sfx', m['r1'] + 1.9, slide_whistle(500, 900, 0.35), 0.12)
    mx.add('sfx', m['tw'], flick(), 0.25)
    mx.add('sfx', m['dino'], rumble(1.2), 0.45); mx.add('sfx', m['dino'] + 0.3, drumroll(0.6), 0.15)
    mx.add('sfx', m['up2'], slide_whistle(400, 1100, 0.6), 0.15)
    mx.add('sfx', m['look'], ding(), 0.25); mx.add('sfx', m['look'] + 0.2, chirp(), 0.15)
    mx.add('sfx', m['again'] + 0.2, jingle(), 0.22)
    mx.voices(F, tl['events'])
    mx.write(F + '/audio.wav', quiet=[(m[f'c{i}'], m[f'r{i}']) for i in range(3)]); return tl


TL = json.load(open(F + '/timeline.json')) if os.path.exists(F + '/timeline.json') else None


# ---------------- animals (facing right, ground at y=0) ----------------
def bunny(cr, t, p=0.0):
    Wc = hexc('#FFFFFF'); Pk = hexc('#FFB3C8'); Gr = hexc('#E9E4F2')
    cr.arc(-165, -120, 38, 0, 2 * math.pi); fs(cr, Wc)
    ellipse(cr, -70, -18, 95, 30); fs(cr, Gr)
    ellipse(cr, -40, -120, 145, 108); fs(cr, Wc)
    for ex, ang in ((55, -0.3 + 0.08 * math.sin(t * 3)), (110, 0.15 + 0.08 * math.sin(t * 3 + 1))):
        cr.save(); cr.translate(ex, -300); cr.rotate(ang)
        ellipse(cr, 0, -40, 32, 105); fs(cr, Wc); ellipse(cr, 0, -35, 15, 75); cr.set_source_rgb(*Pk); cr.fill(); cr.restore()
    ellipse(cr, 70, -14, 48, 20); fs(cr, Gr)
    cr.arc(95, -215, 88, 0, 2 * math.pi); fs(cr, Wc)
    cr.arc(130, -230, 13, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill()
    cr.arc(126, -235, 4.5, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()
    ellipse(cr, 180, -205, 12, 10); cr.set_source_rgb(*hexc('#FF7FA8')); cr.fill()
    cr.move_to(150, -180); cr.curve_to(160, -165, 175, -168, 180, -185); stroke_dev(cr, OUT, 5)
    ellipse(cr, 120, -185, 20, 12); cr.set_source_rgba(1, 0.45, 0.55, 0.5); cr.fill()

def elephant(cr, t, p=0.0):
    E = hexc('#A9B9DE'); Ed = hexc('#8FA0CC')
    cr.move_to(-225, -210); cr.curve_to(-250, -170, -255, -140, -265, -110); stroke_dev(cr, OUT, 12)
    for x in (-185, -95, 20, 100):
        rrect(cr, x, -150, 72, 150, 26); fs(cr, Ed if x in (-95, 100) else E)
    ellipse(cr, -50, -200, 200, 140); fs(cr, E)
    # trunk
    sw = 0.25 * math.sin(t * 2.4)
    cr.save(); cr.translate(250, -215); cr.rotate(sw)
    cr.move_to(0, 0); cr.curve_to(45, 60, 40, 150, 20, 175); cr.curve_to(10, 190, 40, 205, 60, 185)
    p_ = cr.copy_path(); stroke_dev(cr, OUT, 70); cr.append_path(p_); stroke_dev(cr, E, 56); cr.restore()
    cr.arc(160, -250, 115, 0, 2 * math.pi); fs(cr, E)
    ellipse(cr, 95, -245, 82, 105); fs(cr, Ed)
    ellipse(cr, 95, -245, 50, 70); cr.set_source_rgba(1, 0.6, 0.7, 0.45); cr.fill()
    cr.move_to(225, -175); cr.curve_to(260, -160, 280, -170, 290, -190); stroke_dev(cr, OUT, 20); cr.move_to(225, -175); cr.curve_to(260, -160, 280, -170, 290, -190); stroke_dev(cr, (1, 1, 1), 11)
    cr.arc(205, -280, 14, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill()
    cr.arc(201, -285, 5, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()
    ellipse(cr, 215, -230, 22, 13); cr.set_source_rgba(1, 0.45, 0.55, 0.5); cr.fill()

def giraffe(cr, t, p=0.0):
    Y = hexc('#FFC93C'); B = hexc('#C9772E')
    cr.move_to(-175, -330); cr.curve_to(-200, -280, -205, -250, -200, -210); stroke_dev(cr, OUT, 10)
    for x in (-150, -105, 55, 100):
        rrect(cr, x, -320, 38, 320, 16); fs(cr, Y if x in (-150, 55) else hexc('#F2B52A'))
        rrect(cr, x - 3, -30, 44, 30, 10); fs(cr, B)
    ellipse(cr, -30, -330, 175, 88); body = cr.copy_path(); fs(cr, Y)
    cr.save(); cr.append_path(body); cr.clip()
    for x, y, r in ((-120, -350, 28), (-50, -310, 24), (20, -360, 26), (90, -315, 22), (-150, -295, 18), (60, -385, 15)):
        cr.arc(x, y, r, 0, 2 * math.pi); cr.set_source_rgb(*B); cr.fill()
    cr.restore()
    nod = 0.06 * math.sin(t * 2.0)
    cr.save(); cr.translate(95, -360); cr.rotate(nod)
    cr.move_to(-40, 20); cr.line_to(40, 10); cr.line_to(130, -330); cr.line_to(75, -345); cr.close_path(); neck = cr.copy_path(); fs(cr, Y)
    cr.save(); cr.append_path(neck); cr.clip()
    for x, y, r in ((10, -40, 22), (45, -130, 20), (75, -220, 18), (100, -300, 15), (-20, 0, 18)):
        cr.arc(x, y, r, 0, 2 * math.pi); cr.set_source_rgb(*B); cr.fill()
    cr.restore()
    for ox in (85, 120):
        cr.move_to(ox, -390); cr.line_to(ox + 5, -440); stroke_dev(cr, OUT, 16); cr.move_to(ox, -390); cr.line_to(ox + 5, -440); stroke_dev(cr, Y, 8)
        cr.arc(ox + 5, -445, 13, 0, 2 * math.pi); fs(cr, B, 5)
    ellipse(cr, 60, -370, 32, 15); fs(cr, Y, 5)
    cr.save(); cr.translate(140, -360); cr.rotate(0.25); ellipse(cr, 0, 0, 82, 50); fs(cr, Y); ellipse(cr, 50, 12, 38, 30); fs(cr, hexc('#FFE08A'), 5); cr.restore()
    cr.arc(135, -380, 12, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill()
    cr.arc(131, -384, 4, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()
    cr.arc(195, -345, 5, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill()
    cr.restore()

def dino(cr, t, p=0.0):
    """only ever drawn as a shadow, facing left"""
    cr.move_to(330, -300); cr.curve_to(250, -330, 120, -330, 60, -300); cr.line_to(330, -230); cr.close_path(); cr.fill()  # tail
    cr.move_to(470, -150); cr.curve_to(400, -300, 200, -300, 100, -230); cr.line_to(330, -270); cr.close_path()
    ellipse(cr, 40, -280, 180, 140); cr.fill()
    for x, w in ((-60, 70), (90, 75)):
        rrect(cr, x, -200, w, 200, 25); cr.fill(); ellipse(cr, x + w / 2 - 25, -10, 60, 22); cr.fill()
    cr.move_to(470, -150); cr.curve_to(380, -260, 260, -330, 150, -330); cr.line_to(150, -230); cr.close_path(); cr.fill()
    jaw = 0.18 + 0.12 * math.sin(t * 6)
    cr.save(); cr.translate(-110, -430)
    rrect(cr, -230, -90, 260, 130, 50); cr.fill()
    cr.save(); cr.rotate(-jaw); rrect(cr, -220, 20, 230, 60, 25); cr.fill()
    for k in range(5): cr.move_to(-200 + k * 40, 20); cr.line_to(-185 + k * 40, -5); cr.line_to(-170 + k * 40, 20); cr.fill()
    cr.restore(); cr.restore()
    cr.move_to(-160, -420); cr.curve_to(-120, -300, -60, -280, 40, -380); cr.line_to(-40, -450); cr.close_path(); cr.fill()
    for k in range(6):
        x = -60 + k * 65; y = -425 + k * 20 + (k > 3) * 25
        cr.move_to(x - 28, y + 10); cr.line_to(x, y - 55); cr.line_to(x + 28, y + 10); cr.fill()
    for a in (0.0, 0.5):
        cr.save(); cr.translate(-120, -260); cr.rotate(0.6 + a * 0.3 + 0.15 * math.sin(t * 7)); rrect(cr, -12, 0, 24, 70, 12); cr.fill(); cr.restore()

ANIMS = dict(bunny=bunny, elephant=elephant, giraffe=giraffe)


def shadow(cr, fn, x, y, sc, t, alpha=0.92, flip=False):
    cr.push_group(); cr.save(); cr.translate(x, y); cr.scale(-sc if flip else sc, sc)
    cr.set_source_rgb(0, 0, 0); fn(cr, t); cr.restore()
    pat = cr.pop_group()
    cr.set_source_rgba(*DARK, alpha); cr.mask(pat)

def colour(cr, fn, x, y, sc, t):
    cr.save(); cr.translate(x, y); cr.scale(sc, sc); fn(cr, t); cr.restore()


# ---------------- theatre ----------------
def room(cr, t, dim):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *mixc(hexc('#6B4FA8'), hexc('#2E2350'), dim)); g.add_color_stop_rgb(1, *mixc(hexc('#3A2B6B'), hexc('#1C1533'), dim))
    cr.set_source(g); cr.paint()
    for k in range(18):
        x = (k * 263) % W; y = 120 + (k * 137) % 260
        star5(cr, x, y, 9 + (k % 3) * 3); cr.set_source_rgba(1, 0.95, 0.7, 0.4 + 0.4 * math.sin(t * 2 + k)); cr.fill()
    cr.rectangle(0, 1430, W, H - 1430); cr.set_source_rgb(*mixc(hexc('#8A5A3C'), hexc('#4A3020'), dim)); cr.fill()
    for k in range(9): cr.move_to(k * 135, 1430); cr.line_to(k * 135 - 60, H); stroke_dev(cr, (0, 0, 0), 4, 0.12)

def curtains(cr, t):
    for side in (-1, 1):
        x0 = 0 if side < 0 else W
        cr.move_to(x0, 330); cr.line_to(x0 + side * -150, 330)
        cr.curve_to(x0 + side * -110, 700, x0 + side * -70, 1100, x0 + side * -95, 1440)
        cr.line_to(x0, 1440); cr.close_path(); fs(cr, hexc('#E8414E'))
        for k in range(3):
            xx = x0 + side * -(30 + k * 38)
            cr.move_to(xx, 340); cr.curve_to(xx + side * 8, 800, xx - side * 8, 1100, xx, 1430); stroke_dev(cr, hexc('#B82A38'), 6)
    cr.rectangle(0, 300, W, 70); fs(cr, hexc('#E8414E'))
    for k in range(11): cr.arc(k * 108 + 30, 370, 34, 0, math.pi); fs(cr, hexc('#FFC93C'), 5)

def backdrop(cr, t):
    g = cairo.LinearGradient(0, SY0, 0, SY1); g.add_color_stop_rgb(0, *hexc('#8EDBFF')); g.add_color_stop_rgb(1, *hexc('#D8F3FF'))
    cr.rectangle(SX0, SY0, SX1 - SX0, SY1 - SY0); cr.set_source(g); cr.fill()
    cr.rectangle(SX0, GY - 10, SX1 - SX0, SY1 - GY + 10); cr.set_source_rgb(*hexc('#8FD872')); cr.fill()
    for x, y, sc in ((260, 560, 0.45), (800, 500, 0.38)): draw_cloud(cr, x + 10 * math.sin(t * 0.5), y, sc, (1, 1, 1))

def screen_glow(cr, t, dim):
    g = cairo.RadialGradient(540, 900, 50, 540, 850, 650)
    g.add_color_stop_rgb(0, *mixc(hexc('#FFF8DA'), hexc('#FFE7A0'), dim)); g.add_color_stop_rgb(1, *mixc(hexc('#FFE39A'), hexc('#F0C060'), dim))
    cr.rectangle(SX0, SY0, SX1 - SX0, SY1 - SY0); cr.set_source(g); cr.fill()

def frame_border(cr):
    cr.rectangle(SX0, SY0, SX1 - SX0, SY1 - SY0); stroke_dev(cr, OUT, 14)
    rrect(cr, SX0 - 30, SY1, SX1 - SX0 + 60, 40, 14); fs(cr, hexc('#8A5A3C'))

def blind(cr, yb):
    rrect(cr, SX0 - 12, yb - 22, SX1 - SX0 + 24, 40, 18); fs(cr, hexc('#E8414E'))
    cr.arc(540, yb + 40, 14, 0, 2 * math.pi); fs(cr, hexc('#FFC93C'), 5)
    cr.move_to(540, yb + 18); cr.line_to(540, yb + 26); stroke_dev(cr, OUT, 5)

def flashlight(cr, t, on=True):
    x, y = FL
    cr.save(); cr.translate(x, y); cr.rotate(-0.35)
    rrect(cr, -28, 0, 56, 170, 18); fs(cr, hexc('#3FB4FF'))
    cr.move_to(-48, 0); cr.line_to(48, 0); cr.line_to(30, 50); cr.line_to(-30, 50); cr.close_path(); fs(cr, hexc('#FFC93C'))
    ellipse(cr, 0, -2, 48, 14); fs(cr, hexc('#FFF6C2'), 6)
    rrect(cr, -10, 80, 20, 34, 8); fs(cr, hexc('#FF5A5F'), 4)
    cr.restore()

def beam(cr, t, a):
    x, y = FL
    cr.move_to(x - 30, y - 5); cr.line_to(SX0 + 80, SY1 - 20); cr.line_to(SX1 - 40, SY1 - 20); cr.line_to(x + 30, y + 5); cr.close_path()
    g = cairo.LinearGradient(0, y, 0, SY1); g.add_color_stop_rgba(0, 1, 0.97, 0.75, 0.35 * a); g.add_color_stop_rgba(1, 1, 0.97, 0.75, 0.05 * a)
    cr.set_source(g); cr.fill()


def frame(cr, t):
    m = TL['marks']
    te = 0.0 if t >= m['loop'] else t
    ri = 0
    for i in range(3):
        if te >= m[f's{i}']: ri = i
    twist = te >= m['tw']
    dim = 0.6 * smooth(m['dino'], m['dino'] + 0.4, te) * (1 - smooth(m['up2'] + 0.6, m['up2'] + 1.2, te))
    room(cr, t, dim)
    # what is behind the screen / on the screen
    if not twist:
        r = ROUNDS[ri]; fn = ANIMS[r['k']]
        sin_ = smooth(m[f's{ri}'], m[f's{ri}'] + 0.7, te)
        rv = m[f'r{ri}']
        yb = SY1 - (SY1 - SY0) * ease_io(clamp((te - rv) / 0.7))
        if te >= m[f'x{ri}']: yb = SY0 + (SY1 - SY0) * ease_io(clamp((te - m[f'x{ri}']) / 0.55))
        ax = lerp(-350, 540, ease_out_back(sin_, 1.2)) if ri == 0 or te < rv else 540
        if te >= m[f'x{ri}']: ax = 540 + 900 * smooth(m[f'x{ri}'] + 0.3, m[f'x{ri}'] + 0.6, te)
        hopy = 0
        if r['k'] == 'bunny': hopy = -abs(math.sin(te * 3.2)) * 50 * (1 if te < rv + 0.8 else 0.5)
        sc = {'bunny': 1.25, 'elephant': 1.05, 'giraffe': 0.92}[r['k']]
        ax_c = ax - {'bunny': 0, 'elephant': 40, 'giraffe': 90}[r['k']]
        # revealed part (below blind? no: blind rolls UP, reveal from bottom)
        cr.save(); cr.rectangle(SX0, yb, SX1 - SX0, SY1 - yb); cr.clip()
        backdrop(cr, t); colour(cr, fn, ax_c, GY + hopy, sc, te)
        if te >= rv + 0.6: sparkles(cr, 540, 800, rv + 0.6, te, 8, 250, 380)
        cr.restore()
        cr.save(); cr.rectangle(SX0, SY0, SX1 - SX0, yb - SY0); cr.clip()
        screen_glow(cr, t, 0); shadow(cr, fn, ax_c, GY + hopy, sc, te)
        cr.restore()
        if yb > SY0 + 5: blind(cr, yb)
    else:
        yb = SY1 - (SY1 - SY0) * ease_io(clamp((te - m['up2']) / 0.8))
        cr.save(); cr.rectangle(SX0, yb, SX1 - SX0, SY1 - yb); cr.clip(); backdrop(cr, t); cr.restore()
        cr.save(); cr.rectangle(SX0, SY0, SX1 - SX0, yb - SY0); cr.clip()
        screen_glow(cr, t, dim)
        if te >= m['dino']:
            grow = ease_out_back(clamp((te - m['dino']) / 0.6), 1.4)
            shake = 6 * math.sin(te * 40) * burst(m['dino'], m['dino'] + 1.0, te)
            shadow(cr, dino, 500 + shake, GY, 0.92 * grow, te, 0.95)
        cr.restore()
        if yb > SY0 + 5: blind(cr, yb)
    frame_border(cr)
    curtains(cr, t)
    # flashlight beam + chick
    beam_a = 1.0 if (not twist or te < m['up2'] + 0.8) else 0.5
    beam(cr, t, beam_a)
    st = chick_talk(base_st(), te, TL); h = 0; sx = sy = 1; look = (0.2, -0.9)
    for i in range(3):
        if m[f'c{i}'] <= te < m[f'r{i}']: look = (0.3 * math.sin(te * 2), -1.0)
        if m[f'r{i}'] + 0.55 <= te < m[f'r{i}'] + 1.5:
            h, sx, sy, air = hop_seq(te, m[f'r{i}'] + 0.55, 2, 0.45, 55); st.update(happy=1, wing=[0.3 + 0.8 * air] * 2)
    shake = 0
    if m['dino'] <= te < m['up2']:
        st['mood'] = 0.0; st['wing'] = [1.0, 1.0]; shake = 7 * math.sin(te * 45); look = (0, -1)
    if m['up2'] <= te < m['look']: look = (0.0, -0.9)
    if te >= m['look']: look = (0.9, 0.5); st['happy'] = 1 if te > m['look'] + 1.2 else st.get('happy', 0)
    shadow_at(cr, 480, 1823, 110)
    chick(cr, 480 + shake, 1820, h, 0.78, st, te, look, sx, sy, acc='explorer')
    flashlight(cr, t)
    # snail sneaking onto the flashlight
    if twist:
        sp = smooth(m['tw'], m['dino'], te)
        snx = lerp(1180, FL[0] - 5, sp); sny = lerp(1780, FL[1] - 10, sp)
        cr.save(); cr.translate(snx, sny); cr.scale(-1.05, 1.05); draw_snail(cr, 0, 0, te); cr.restore()
        if te >= m['look']: ring_mark(cr, FL[0] - 10, FL[1] - 55, 140, 105, smooth(m['look'], m['look'] + 0.5, te))
    for i in range(3):
        count_bubble(cr, m[f'c{i}'], te, "Say it!", y=1340, w=440)
    names = ['Bunny!', 'Elephant!', 'Giraffe!']
    cols = ['#FF5FA2', '#2EA7FF', '#FF9A1F']
    for i in range(3): word_pop(cr, names[i], 540, 1345, 120, cols[i], m[f'r{i}'] + 0.55, m[f'x{i}'] + 0.3, te)
    word_pop(cr, "ROAR?!", 540, 1345, 130, '#FF4D4D', m['dino'] + 0.2, m['up2'], te)
    word_pop(cr, "Snail!", 540, 1345, 130, '#3ECF5E', m['look'] + 0.2, m['again'] + 0.3, te)
    draw_text(cr, "Who's That Shadow?", 200, 112, t, -1)
    loop_fade(cr, TL, t)

if __name__ == '__main__': episode_main(build, F)
