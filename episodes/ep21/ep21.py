"""Where's the Ball? — cup shuffle game at a carnival stand, faster each round. Twist: snail under the cup."""
import sys; sys.path.insert(0, '/home/claude/kit')
from common import *

F = '/home/claude/ep21'
SLOTS = [235, 540, 845]
TABLE = 1330
ROUNDS = [dict(intro="Watch the ball!", swaps=[(0, 1), (1, 2)], d=0.75, a="Yes! There it is!"),
          dict(intro="Faster now! Watch closely!", swaps=[(1, 2), (0, 1), (0, 2), (1, 2)], d=0.55, a="You found it! Great job!"),
          dict(intro="Super fast! Ready?", swaps=[(0, 2), (0, 1), (1, 2), (0, 1), (0, 2), (1, 2)], d=0.4, a=None)]


def build():
    s = Script(F); t = 0.1
    for i, r in enumerate(ROUNDS):
        s.mark(f's{i}', t)
        t = s.say(t, f'in{i}', r['intro']) + 0.1
        s.mark(f'show{i}', t); t += 1.6
        s.mark(f'mix{i}', t); t += len(r['swaps']) * r['d'] + 0.2
        t = s.say(t, f'q{i}', "Where is the ball?") + 0.05
        s.mark(f'c{i}', t); t += 3.0; s.mark(f'r{i}', t)
        if r['a']: t = s.say(t + 0.35, f'a{i}', r['a']) + 0.35
    t = s.say(t + 0.45, 'wait', "Wait... that's not the ball!") + 0.05
    t = s.say(t, 'surp', "Surprise!", 1.05, False, 'am_puck') + 0.15
    s.mark('lift2', t)
    t = s.say(t + 0.3, 'here', "There's the ball! Hee hee!", 1.0, True) + 0.25
    s.mark('again', t); t = s.say(t, 'again', "Again?", 1.0, True) + 0.25
    s.mark('loop', t); t += 0.9
    tl = s.save(t); m = tl['marks']; mx = Mix(tl['dur'])
    mx.music_loop(0, tl['dur'], 118, [([60, 64, 67], 36), ([65, 69, 72], 41), ([67, 71, 74], 43), ([60, 64, 67], 36)],
                  [[79, None, 77, 76, None, 74, 72, None], [74, None, 76, None, 79, None, None, None]], 'bouncy', 0.75)
    for i, r in enumerate(ROUNDS):
        mx.add('sfx', m[f'show{i}'], pop(300, 900, 0.12), 0.3); mx.add('sfx', m[f'show{i}'] + 1.2, kick(), 0.3)
        for k in range(len(r['swaps'])): mx.add('sfx', m[f'mix{i}'] + k * r['d'], whoosh(r['d'] * 0.9), 0.25)
        countdown_ticks(mx, m[f'c{i}'])
        mx.add('sfx', m[f'r{i}'], pop(300, 900, 0.12), 0.35)
        if r['a']: mx.add('sfx', m[f'r{i}'] + 0.15, ding(), 0.2); mx.add('sfx', m[f'r{i}'] + 0.3, chirp(), 0.15)
    mx.add('sfx', m['r2'] + 0.2, boing(), 0.3)
    mx.add('sfx', m['lift2'], pop(300, 900, 0.12), 0.35); mx.add('sfx', m['lift2'] + 0.15, tada(72), 0.2)
    mx.add('sfx', m['again'] + 0.2, jingle(), 0.22)
    mx.voices(F, tl['events'])
    mx.write(F + '/audio.wav', quiet=[(m[f'c{i}'], m[f'r{i}']) for i in range(3)]); return tl


TL = json.load(open(F + '/timeline.json')) if os.path.exists(F + '/timeline.json') else None


def ball_cup_after(swaps):
    """cup 1 (middle) holds the ball; returns slot of each cup after swaps"""
    pos = [0, 1, 2]  # pos[cup] = slot
    for a, b in swaps:
        ca = pos.index(a); cb = pos.index(b); pos[ca], pos[cb] = b, a
    return pos


def cup_positions(i, te, m):
    """returns list of (x, y, scale) for cups 0..2 and lift amount for each"""
    r = ROUNDS[i]; pos = [0, 1, 2]
    st0 = m[f'mix{i}']; d = r['d']
    out = None
    for k, (a, b) in enumerate(r['swaps']):
        t0 = st0 + k * d
        ca = pos.index(a); cb = pos.index(b)
        if te < t0: break
        if te < t0 + d:
            u = ease_io((te - t0) / d)
            res = []
            for c in range(3):
                x = SLOTS[pos[c]]; y = TABLE; s = 1.0
                if c == ca: x = lerp(SLOTS[a], SLOTS[b], u); y = TABLE + 40 * math.sin(math.pi * u); s = 1 + 0.08 * math.sin(math.pi * u)
                if c == cb: x = lerp(SLOTS[b], SLOTS[a], u); y = TABLE - 60 * math.sin(math.pi * u); s = 1 - 0.08 * math.sin(math.pi * u)
                res.append((x, y, s, c == cb))
            return res, pos
        pos[ca], pos[cb] = b, a
    return [(SLOTS[pos[c]], TABLE, 1.0, False) for c in range(3)], pos


def cup(cr, x, y, s, lift, t):
    cr.save(); cr.translate(x, y - lift); cr.scale(s * 1.15, s * 1.15)
    cr.move_to(-120, 0); cr.line_to(-85, -270); cr.line_to(85, -270); cr.line_to(120, 0); cr.close_path()
    p = cr.copy_path()
    g = cairo.LinearGradient(-120, 0, 120, 0); g.add_color_stop_rgb(0, *hexc('#8E5CFF')); g.add_color_stop_rgb(0.5, *hexc('#A97BFF')); g.add_color_stop_rgb(1, *hexc('#6E3FE0'))
    cr.set_source(g); cr.fill_preserve(); stroke_dev(cr, OUT, 7)
    rrect(cr, -135, -18, 270, 34, 14); fs(cr, hexc('#FFD93B'))
    rrect(cr, -95, -285, 190, 26, 12); fs(cr, hexc('#FFD93B'))
    for k, (sx, sy) in enumerate(((-40, -190), (35, -120), (-15, -70))):
        star5(cr, sx, sy, 20); cr.set_source_rgba(1, 1, 1, 0.8); cr.fill()
    ellipse(cr, -70, -150, 12, 60); cr.set_source_rgba(1, 1, 1, 0.3); cr.fill()
    cr.restore()

def ball(cr, x, y, s, t, happy=True):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.arc(0, -75, 75, 0, 2 * math.pi); fs(cr, hexc('#FF4D4D'))
    cr.save(); cr.arc(0, -75, 72, 0, 2 * math.pi); cr.clip()
    cr.arc(0, -75, 75, -0.3, 0.3); cr.line_to(0, -75); cr.close_path()
    cr.move_to(-80, -90); cr.curve_to(-30, -60, 30, -60, 80, -90); stroke_dev(cr, (1, 1, 1), 12, 0.9); cr.restore()
    ellipse(cr, -28, -115, 16, 10); cr.set_source_rgba(1, 1, 1, 0.6); cr.fill()
    if happy:
        for sx in (-1, 1): cr.arc(sx * 24, -70, 10, math.pi * 1.1, math.pi * 1.9); stroke_dev(cr, OUT, 5)
        cr.arc(0, -55, 14, 0.15 * math.pi, 0.85 * math.pi); stroke_dev(cr, OUT, 5)
    else: face(cr, 0, -70, 0.8)
    cr.restore()


def stage(cr, t):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *hexc('#FFE7A8')); g.add_color_stop_rgb(1, *hexc('#FFD6E8'))
    cr.set_source(g); cr.paint()
    # tent stripes top
    for k in range(-1, 12):
        cr.move_to(k * 110, 0); cr.line_to(k * 110 + 110, 0); cr.line_to(540 + (k * 110 + 55 - 540) * 1.6, 330); cr.close_path()
        cr.set_source_rgb(*hexc('#FF5A5F' if k % 2 else '#FFFFFF')); cr.fill()
    for k in range(12):
        cr.arc(k * 100 + 50, 335, 50, 0, math.pi); fs(cr, hexc('#FF5A5F' if k % 2 else '#FFD93B'))
    # bunting lights
    for k in range(14):
        x = k * 80 + 20; y = 470 + 30 * math.sin(k * 0.8)
        cr.arc(x, y, 12, 0, 2 * math.pi); cr.set_source_rgba(*hexc(CONF_COLS[k % 7]), 0.6 + 0.4 * math.sin(t * 4 + k)); cr.fill()
    # table
    rrect(cr, 40, TABLE - 10, 1000, 60, 20); fs(cr, hexc('#3FB4FF'))
    cr.move_to(70, TABLE + 50); cr.line_to(1010, TABLE + 50); cr.line_to(980, 1640); cr.line_to(100, 1640); cr.close_path(); fs(cr, hexc('#2E8BD9'))
    for k in range(6): star5(cr, 160 + k * 150, 1500, 22); cr.set_source_rgba(1, 1, 1, 0.6); cr.fill()
    cr.rectangle(0, 1640, W, H - 1640); cr.set_source_rgb(*hexc('#C9965A')); cr.fill()
    cr.move_to(0, 1640); cr.line_to(W, 1640); stroke_dev(cr, OUT, 6)


def frame(cr, t):
    m = TL['marks']
    te = 0.0 if t >= m['loop'] else t
    stage(cr, t)
    ri = 0
    for i in range(3):
        if te >= m[f's{i}']: ri = i
    r = ROUNDS[ri]
    cups, pos = cup_positions(ri, te, m)
    final = ball_cup_after(r['swaps'])  # slot of each cup at end
    ball_slot = final[1]
    lifts = [0, 0, 0]
    sh = m[f'show{ri}']
    show_lift = 280 * smooth(sh, sh + 0.35, te) * (1 - smooth(sh + 1.0, sh + 1.4, te))
    lifts[1] = show_lift
    rv = m[f'r{ri}']
    end_r = m[f's{ri + 1}'] if ri < 2 else m['loop']
    if te >= rv:
        c_ball = final.index(ball_slot) if False else 1
        lifts[1] = 280 * smooth(rv, rv + 0.35, te) * (1 - smooth(end_r - 0.5, end_r - 0.1, te)) if ri < 2 else 280 * smooth(rv, rv + 0.35, te)
    twist = ri == 2 and te >= rv
    lift2 = 0
    if ri == 2 and te >= m['lift2']:
        lift2 = 280 * smooth(m['lift2'], m['lift2'] + 0.35, te)
    # contents under cups
    for c in range(3):
        x, y, s, back = cups[c]
        if c == 1 and lifts[1] > 5:
            if twist:
                cr.save(); cr.translate(x, TABLE + 5); cr.scale(-1.5, 1.5); draw_snail(cr, 0, 0, te); cr.restore()
            else:
                ball(cr, x, TABLE + 5, 1.15, te, happy=te >= rv or show_lift > 100)
    if ri == 2 and lift2 > 5:
        other = [c for c in range(3) if c != 1][0 if (final[0] < final[2]) else 1]
        x, y, s, back = cups[other]
        ball(cr, x, TABLE + 5, 1.15, te, True)
    # draw back cups first
    order = sorted(range(3), key=lambda c: 0 if cups[c][3] else 1)
    for c in order:
        x, y, s, back = cups[c]
        lf = lifts[c]
        if ri == 2 and lift2 > 0:
            other = [cc for cc in range(3) if cc != 1][0 if (final[0] < final[2]) else 1]
            if c == other: lf = lift2
        cup(cr, x, y, s, lf, te)
    # chickpea watching
    st = chick_talk(base_st(), te, TL); h = 0; sx = sy = 1
    bx = cups[1][0]
    look = (clamp((bx - 540) / 300, -1, 1), -0.6)
    if m[f'c{ri}'] <= te < rv: look = (math.sin(te * 2.5), -0.6)
    if te >= rv and ri < 2 and te < rv + 0.9:
        h, sx, sy, air = hop_seq(te, rv + 0.1, 2, 0.45, 55); st.update(happy=1, wing=[0.3 + 0.8 * air] * 2)
    if twist and te < m['lift2']: st['mood'] = 0.0; look = (clamp((cups[1][0] - 540) / 300, -1, 1), -0.8)
    if ri == 2 and te >= m['lift2']: st['happy'] = 1; st['wing'] = [0.9, 0.9]
    shadow_at(cr, 540, 1823, 100)
    chick(cr, 540, 1820, h, 0.72, st, te, look, sx, sy, acc='bow')
    for i in range(3):
        count_bubble(cr, m[f'c{i}'], te, "Point to it!", y=600, w=560)
    word_pop(cr, "Found it!", 540, 600, 140, '#3ECF5E', m['r0'] + 0.3, m['s1'] - 0.1, te)
    word_pop(cr, "Yay!", 540, 600, 150, '#FF9A1F', m['r1'] + 0.3, m['s2'] - 0.1, te)
    word_pop(cr, "Surprise!", 540, 600, 150, '#FF5FA2', m['r2'] + 0.8, m['again'] + 0.3, te)
    speed = ['', 'FASTER!', 'SUPER FAST!']
    if ri: word_pop(cr, speed[ri], 540, 600, 120, '#FF4D4D', m[f's{ri}'] + 0.1, m[f'mix{ri}'], te)
    draw_text(cr, "Where's the Ball?", 250, 120, t, -1)
    loop_fade(cr, TL, t)

if __name__ == '__main__': episode_main(build, F)
