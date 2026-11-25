"""Fast or Slow? — race track: bunny, snail, race car. Twist: slow turtle finds a rocket skateboard!"""
import sys; sys.path.insert(0, '/home/claude/kit')
from common import *
sys.path.insert(0, '/home/claude/ep23'); sys.path.insert(0, '/home/claude/ep26')
from ep23 import bunny
from ep26 import car

F = '/home/claude/ep32'
GY = 1150                 # running line
X0, XF = 190, 900          # start / finish
ROUNDS = [dict(k='bunny', fast=True, a="Fast!", y="Zoom!", d=1.1),
          dict(k='snail', fast=False, a="Slow!", y="Sloooow...", d=2.6),
          dict(k='car', fast=True, a="Fast!", y="Vroom, vroom!", d=0.9)]


def build():
    s = Script(F); t = 0.1
    s.mark('s0', 0.05)
    t = s.say(t, 'hook', "Fast or slow? Let's race!") + 0.05
    for i, r in enumerate(ROUNDS):
        if i: s.mark(f's{i}', t); t += 0.5
        t = s.say(t, f'go{i}', "Ready, set, go!" if i == 0 else "Go!", 1.0, True) + 0.05
        s.mark(f'run{i}', t); t += r['d'] + 0.35
        t = s.say(t, f'q{i}', "Is it fast or slow?") + 0.05
        s.mark(f'c{i}', t); t += 3.0; s.mark(f'r{i}', t)
        t = s.say(t + 0.4, f'a{i}', r['a']) + 0.05
        t = s.say(t, f'y{i}', r['y'], 1.0, True) + 0.3
        s.mark(f'x{i}', t); t += 0.5
    s.mark('tw', t); t += 0.4
    t = s.say(t, 'turtle', "And the turtle?") + 0.05
    s.mark('crawl', t)
    t = s.say(t, 'slow', "Slow... slow...", 0.85) + 0.15
    s.mark('rocket', t)
    t = s.say(t, 'wait', "Wait... a rocket skateboard?!") + 0.1
    s.mark('zoom', t); t += 1.0
    t = s.say(t, 'super', "Super fast turtle! Hee hee!", 1.0, True) + 0.25
    s.mark('again', t); t = s.say(t, 'again', "Again?", 1.0, True) + 0.25
    s.mark('loop', t); t += 0.9
    tl = s.save(t); m = tl['marks']; mx = Mix(tl['dur'])
    mx.music_loop(0, tl['dur'], 124, [([60, 64, 67], 36), ([67, 71, 74], 43), ([65, 69, 72], 41), ([67, 71, 74], 43)],
                  [[72, 76, 79, None, 79, 76, 72, None], [74, 77, 81, None, 79, None, None, None]], 'march', 0.72)
    for i, r in enumerate(ROUNDS):
        mx.add('sfx', m[f's{i}'] + 0.1, pop(300, 900, 0.12), 0.3)
        rn = m[f'run{i}']
        if r['fast']: mx.add('sfx', rn, whoosh(r['d']), 0.3); mx.add('sfx', rn, slide_whistle(500, 1500, r['d']), 0.1)
        else:
            for k in range(5): mx.add('sfx', rn + k * 0.5, marimba(mtof(60 + k), 0.4), 0.15)
        if r['k'] == 'bunny':
            for k in range(4): mx.add('sfx', rn + k * 0.27, boing(), 0.1)
        countdown_ticks(mx, m[f'c{i}'])
        mx.add('sfx', m[f'r{i}'], pop(300, 900, 0.12), 0.35); mx.add('sfx', m[f'r{i}'] + 0.1, ding(), 0.2)
        mx.add('sfx', m[f'x{i}'], flick(), 0.2)
    mx.add('sfx', m['tw'], pop(300, 900, 0.12), 0.3)
    for k in range(4): mx.add('sfx', m['crawl'] + k * 0.45, marimba(mtof(55 + k), 0.4), 0.15)
    mx.add('sfx', m['rocket'], pop(300, 1200, 0.12), 0.3)
    mx.add('sfx', m['zoom'], rumble(0.8), 0.35); mx.add('sfx', m['zoom'], slide_whistle(300, 1800, 0.9), 0.18); mx.add('sfx', m['zoom'], whoosh(0.8), 0.3)
    mx.add('sfx', m['zoom'] + 0.9, tada(72), 0.15)
    mx.add('sfx', m['again'] + 0.2, jingle(), 0.22)
    mx.voices(F, tl['events'])
    mx.write(F + '/audio.wav', quiet=[(m[f'c{i}'], m[f'r{i}']) for i in range(3)]); return tl


TL = json.load(open(F + '/timeline.json')) if os.path.exists(F + '/timeline.json') else None


def turtle(cr, t, walk=0.0):
    G = hexc('#7DD957'); S = hexc('#3EAF4A')
    for k, x in enumerate((-90, 80)):
        lift = 12 * max(0, math.sin(t * 6 + k * math.pi)) * walk
        rrect(cr, x - 25, -60 - lift, 50, 60, 18); fs(cr, G)
    cr.move_to(-150, -60); cr.line_to(-185, -45); cr.line_to(-150, -40); cr.close_path(); fs(cr, G, 5)
    ellipse(cr, 175, -105, 62, 52); fs(cr, G)
    cr.arc(195, -118, 12, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill(); cr.arc(191, -122, 4, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()
    cr.arc(205, -95, 16, 0.1 * math.pi, 0.7 * math.pi); stroke_dev(cr, OUT, 5)
    ellipse(cr, 172, -92, 13, 8); cr.set_source_rgba(1, 0.45, 0.55, 0.5); cr.fill()
    cr.move_to(-165, -55); cr.curve_to(-160, -200, 150, -200, 155, -55); cr.close_path(); shell = cr.copy_path(); fs(cr, S)
    cr.save(); cr.append_path(shell); cr.clip()
    for x, y in ((-80, -100), (0, -130), (80, -100), (-20, -75), (40, -75), (-110, -70), (110, -70)):
        cr.save(); cr.translate(x, y)
        cr.move_to(32, 0)
        for k in range(1, 6): cr.line_to(32 * math.cos(k * math.pi / 3), 28 * math.sin(k * math.pi / 3))
        cr.close_path(); cr.set_source_rgb(*hexc('#5BC24A')); cr.fill_preserve(); stroke_dev(cr, hexc('#2E8B3A'), 5); cr.restore()
    cr.restore()
    rrect(cr, -175, -65, 340, 22, 11); fs(cr, hexc('#C9E87A'), 5)

def skateboard(cr, t, fire=0.0):
    if fire > 0:
        for k, (c, w, l) in enumerate((('#FF5A1F', 30, 170), ('#FFC93C', 20, 120))):
            fl = l * fire * (1 + 0.2 * math.sin(t * 40 + k))
            cr.move_to(-230, -30 - w); cr.curve_to(-230 - fl * 0.6, -30 - w, -230 - fl, -30, -230 - fl, -30); cr.curve_to(-230 - fl, -30, -230 - fl * 0.6, -30 + w, -230, -30 + w); cr.close_path()
            cr.set_source_rgb(*hexc(c)); cr.fill()
    rrect(cr, -250, -65, 60, 70, 20); fs(cr, hexc('#C9D2DD'))
    rrect(cr, -230, -20, 470, 30, 15); fs(cr, hexc('#FF5FA2'))
    for x in (-150, 150):
        cr.arc(x, 25, 22, 0, 2 * math.pi); fs(cr, hexc('#3A3550')); cr.arc(x, 25, 8, 0, 2 * math.pi); cr.set_source_rgb(*hexc('#D0D6E0')); cr.fill()

def snailx(cr, t, walk=0.0):
    cr.save(); cr.scale(-2.2, 2.2); draw_snail(cr, 0, 0, t); cr.restore()

def runner(cr, k, x, t, moving, sc_mul=1.0):
    if k == 'bunny':
        hopy = -abs(math.sin(t * 11)) * 80 if moving else 0
        cr.save(); cr.translate(x, GY + hopy); cr.scale(0.95 * sc_mul, 0.95 * sc_mul); bunny(cr, t); cr.restore()
    elif k == 'snail':
        cr.save(); cr.translate(x, GY); cr.scale(1.35 * sc_mul, 1.35 * sc_mul); snailx(cr, t); cr.restore()
    elif k == 'car':
        cr.save(); cr.translate(x, GY - 20); cr.scale(0.9 * sc_mul, 0.9 * sc_mul); car(cr, t, 1.0 if moving else 0.0); cr.restore()

def speed_lines(cr, x, y, t, a=1.0, n=5, length=220):
    for k in range(n):
        yy = y - 40 - k * 45; xx = x - 200 - (k % 2) * 60 - (t * 900) % 60
        cr.move_to(xx, yy); cr.line_to(xx - length * (0.6 + 0.4 * (k % 3) / 2), yy); stroke_dev(cr, (1, 1, 1), 10, a)

def track(cr, t):
    sky(cr, '#7FD3FF', '#E6F8FF', 950)
    clouds(cr, t, ((780, 430, 0.45), (230, 560, 0.4)))
    # stands with cheering dots
    rrect(cr, -20, 650, W + 40, 260, 30); fs(cr, hexc('#FF9A5C'))
    for row in range(3):
        for k in range(15):
            x = 40 + k * 72 + (row % 2) * 36; y = 700 + row * 70 - abs(math.sin(t * 5 + k + row)) * 10
            cr.arc(x, y, 22, 0, 2 * math.pi); cr.set_source_rgb(*hexc(CONF_COLS[(k + row) % 7])); cr.fill()
    cr.rectangle(0, 900, W, 330); cr.set_source_rgb(*hexc('#E8704A')); cr.fill()
    for y in (960, 1060, 1170): cr.move_to(0, y); cr.line_to(W, y); stroke_dev(cr, (1, 1, 1), 6, 0.8)
    cr.move_to(0, 900); cr.line_to(W, 900); stroke_dev(cr, OUT, 6)
    cr.rectangle(0, 1230, W, H - 1230); cr.set_source_rgb(*hexc('#7ACB5A')); cr.fill()
    cr.move_to(0, 1230); cr.line_to(W, 1230); stroke_dev(cr, OUT, 6)
    for k, (fx, fy) in enumerate(((560, 1700), (700, 1790), (880, 1650), (1010, 1770), (450, 1810), (790, 1600))):
        draw_flower(cr, fx, fy, 1.1, hexc(CONF_COLS[k % 7]), t, k)
    # start line + finish checkers
    cr.rectangle(X0 + 160, 900, 14, 330); cr.set_source_rgb(1, 1, 1); cr.fill()
    for r_ in range(11):
        for c in range(2):
            cr.rectangle(XF + 120 + c * 22, 900 + r_ * 30, 22, 30); cr.set_source_rgb(*((0.15, 0.13, 0.2) if (r_ + c) % 2 else (1, 1, 1))); cr.fill()
    cr.move_to(XF + 186, 1230); cr.line_to(XF + 186, 780); stroke_dev(cr, OUT, 10)
    cr.move_to(XF + 186, 780); cr.line_to(XF + 186 - 110, 800 + 10 * math.sin(t * 4)); cr.line_to(XF + 186, 850); cr.close_path(); fs(cr, hexc('#FF4D4D'), 5)

def button(cr, x, y, label, col, s, glow_a=0.0, dim=0.0):
    if s <= 0.01: return
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    if glow_a > 0: glow(cr, 0, 0, 230, hexc(col), glow_a)
    rrect(cr, -175, -70, 350, 140, 70); fs(cr, mixc(hexc(col), (0.85, 0.85, 0.88), dim))
    rrect(cr, -150, -58, 300, 40, 20); cr.set_source_rgba(1, 1, 1, 0.25); cr.fill()
    cr.restore()
    big_word(cr, label, x, y + 4, 72 * s, (1, 1, 1), 1.0)


def frame(cr, t):
    m = TL['marks']
    te = 0.0 if t >= m['loop'] else t
    track(cr, t)
    twist = te >= m['tw']
    ri = 0
    for i in range(3):
        if te >= m[f's{i}']: ri = i
    if not twist:
        r = ROUNDS[ri]; s0 = m[f's{ri}']; rn = m[f'run{ri}']; rv = m[f'r{ri}']; x0 = m[f'x{ri}']
        pin = ease_out_back(clamp((te - s0) / 0.4), 1.6) * (1 - smooth(x0, x0 + 0.35, te))
        u = clamp((te - rn) / r['d'])
        if r['fast']: x = lerp(X0, XF, ease_io(u))
        else: x = lerp(X0, X0 + 330, u)
        moving = rn <= te < rn + r['d']
        if r['fast'] and moving: speed_lines(cr, x, GY, te, 1.0)
        if pin > 0.01: runner(cr, r['k'], x, te, moving, pin)
        if r['fast'] and te >= rn + r['d'] - 0.05:
            sparkles(cr, XF, GY - 120, rn + r['d'], te, 8, 120, 220)
        if not r['fast'] and moving:
            for k in range(3):
                cr.arc(x - 160 - k * 50, GY - 4, 8, 0, 2 * math.pi); cr.set_source_rgba(1, 1, 1, 0.6 - k * 0.15); cr.fill()
        rv_ok = te >= rv
        bs = pin
        button(cr, 300, 1440, "FAST", '#FF4D4D', bs * (1 + 0.12 * burst(rv, rv + 0.5, te) * r['fast']), 0.8 * burst(rv, rv + 0.6, te) * r['fast'], 0.6 if (rv_ok and not r['fast']) else 0)
        button(cr, 750, 1440, "SLOW", '#2EA7FF', bs * (1 + 0.12 * burst(rv, rv + 0.5, te) * (not r['fast'])), 0.8 * burst(rv, rv + 0.6, te) * (not r['fast']), 0.6 if (rv_ok and r['fast']) else 0)
    else:
        tw = m['tw']; cw = m['crawl']; rk = m['rocket']; zm = m['zoom']
        pin = ease_out_back(clamp((te - tw) / 0.4), 1.6)
        x = X0 + 160 * clamp((te - cw) / (rk - cw + 1.5))
        board_in = smooth(rk, rk + 0.5, te)
        if te >= zm: x = x + (1600) * clamp((te - zm) / 0.9) ** 2
        lift = 70 * board_in
        if te >= zm: speed_lines(cr, x, GY - lift, te, 1.0, 6, 320)
        if board_in > 0:
            bx = lerp(x - 700, x, board_in)
            cr.save(); cr.translate(bx, GY); cr.scale(1.0, 1.0); skateboard(cr, te, smooth(zm, zm + 0.2, te)); cr.restore()
        wob = 6 * math.sin(te * 40) * smooth(zm, zm + 0.1, te)
        cr.save(); cr.translate(x, GY - lift + wob); cr.scale(0.9 * pin, 0.9 * pin); turtle(cr, te, 1.0 if cw <= te < rk else 0.0); cr.restore()
        # comes back around from the left
        if te >= zm + 0.9:
            u = clamp((te - zm - 0.9) / 0.8)
            x2 = lerp(-400, 540, ease_io(u))
            cr.save(); cr.translate(x2, GY); skateboard(cr, te, 1 - u); cr.restore()
            cr.save(); cr.translate(x2, GY - 70); cr.scale(0.9, 0.9); turtle(cr, te, 0); cr.restore()
            if u >= 1: sparkles(cr, 540, GY - 200, zm + 1.7, te, 9, 160, 280)
    # chickpea referee
    st = chick_talk(base_st(), te, TL); h = 0; sx = sy = 1; look = (0.7, -0.6)
    for i, r in enumerate(ROUNDS):
        if m[f'c{i}'] <= te < m[f'r{i}']: look = (0.5 + 0.3 * math.sin(te * 2), -0.7)
        if m[f'r{i}'] + 0.4 <= te < m[f'r{i}'] + 1.3:
            h, sx, sy, air = hop_seq(te, m[f'r{i}'] + 0.4, 2, 0.45, 50); st.update(happy=1, wing=[0.3 + 0.8 * air] * 2)
        rn = m[f'run{i}']
        if rn <= te < rn + r['d']: look = (clamp(-0.5 + 1.5 * (te - rn) / r['d'], -1, 1), -0.6)
    if twist and te >= m['zoom']:
        if te < m['zoom'] + 0.9: st['mood'] = 0.0; st['wing'] = [1.0, 1.0]; look = (1.0, -0.6)
        else: st.update(happy=1, wing=[0.6 + 0.4 * math.sin(te * 9)] * 2)
    shadow_at(cr, 170, 1823, 100)
    chick(cr, 170, 1820, h, 0.8, st, te, look, sx, sy, acc='straw')
    for i, r in enumerate(ROUNDS):
        count_bubble(cr, m[f'c{i}'], te, "Say it!", y=470)
        word_pop(cr, r['a'].upper(), 540, 480, 150 if r['fast'] else 120, '#FF4D4D' if r['fast'] else '#2EA7FF', m[f'r{i}'] + 0.4, m[f'x{i}'] + 0.2, te)
    word_pop(cr, "SUPER FAST!", 540, 480, 130, '#FF9A1F', m['zoom'] + 0.3, m['again'] + 0.3, te, 0.08)
    word_pop(cr, "Go!", 540, 480, 150, '#3ECF5E', m['run0'] - 0.1, m['run0'] + 0.6, te)
    draw_text(cr, "Fast or Slow?", 250, 125, t, -1)
    loop_fade(cr, TL, t)

if __name__ == '__main__': episode_main(build, F)
