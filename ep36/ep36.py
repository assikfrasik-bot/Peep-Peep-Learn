"""Blow the Candles! — count the birthday candles, then BLOW. Twist: a trick candle keeps lighting up again!"""
import sys; sys.path.insert(0, '/home/claude/kit')
from common import *

F = '/home/claude/ep36'
CAKE_Y = 1270
ROUNDS = [dict(n=3, cake='#FF9EC7', frost='#FFFFFF', a="Three candles!", word='3', col='#FF5FA2'),
          dict(n=4, cake='#9FD8FF', frost='#FFF6C2', a="Four candles!", word='4', col='#2EA7FF'),
          dict(n=5, cake='#FFD27A', frost='#FFB3D1', a="Five candles!", word='5', col='#FF9A1F')]
CCOL = ['#FF5A5F', '#3ECF5E', '#2EA7FF', '#A15CFF', '#FFC93C']


def build():
    s = Script(F); t = 0.1
    s.mark('s0', 0.05)
    t = s.say(t, 'hook', "It's party time! Count the candles!") + 0.05
    for i, r in enumerate(ROUNDS):
        if i: s.mark(f's{i}', t); t += 0.7
        t = s.say(t, f'q{i}', "How many candles?") + 0.05
        s.mark(f'c{i}', t); t += 3.0; s.mark(f'r{i}', t)
        t += 0.2 + 0.32 * r['n']
        t = s.say(t, f'a{i}', r['a']) + 0.05
        t = s.say(t, f'w{i}', "Big breath... and blow!", 0.95) + 0.05
        s.mark(f'blow{i}', t); t += 1.0
        t = s.say(t, f'y{i}', "Yay!", 1.0, True) + 0.3
        s.mark(f'x{i}', t); t += 0.5
    s.mark('tw', t); t += 0.6
    t = s.say(t, 'last', "One more! Blow!", 1.0, True) + 0.05
    s.mark('b1', t); t += 0.9
    s.mark('re1', t); t += 0.5
    t = s.say(t, 'huh', "Huh? Blow again!", 1.0, True) + 0.05
    s.mark('b2', t); t += 0.9
    s.mark('re2', t); t += 0.5
    t = s.say(t, 'trick', "A trick candle! Everybody blow together!") + 0.05
    t = s.say(t, 'one', "One, two, three... BLOW!", 1.0, True) + 0.05
    s.mark('b3', t); t += 1.3
    t = s.say(t, 'hb', "Hooray! Happy birthday!", 1.0, True) + 0.25
    s.mark('again', t); t = s.say(t, 'again', "Again?", 1.0, True) + 0.25
    s.mark('loop', t); t += 0.9
    tl = s.save(t); m = tl['marks']; mx = Mix(tl['dur'])
    mx.music_loop(0, tl['dur'], 112, [([60, 64, 67], 36), ([67, 71, 74], 43), ([65, 69, 72], 41), ([60, 64, 67], 36)],
                  [[72, None, 72, 74, None, 72, 77, 76], [72, None, 72, 74, None, 72, 79, 77]], 'bouncy', 0.7)
    for i, r in enumerate(ROUNDS):
        mx.add('sfx', m[f's{i}'] + 0.2, kick(), 0.3)
        for k in range(r['n']): mx.add('sfx', m[f's{i}'] + 0.5 + k * 0.12, pop(500, 1200, 0.08), 0.18)
        countdown_ticks(mx, m[f'c{i}'])
        for k in range(r['n']): mx.add('sfx', m[f'r{i}'] + 0.2 + k * 0.32, marimba(mtof(72 + [0, 2, 4, 5, 7][k]), 0.4), 0.3)
        mx.add('sfx', m[f'blow{i}'], whoosh(0.8), 0.45)
        mx.add('sfx', m[f'blow{i}'] + 0.6, tada(72), 0.15)
        mx.add('sfx', m[f'x{i}'], flick(), 0.2)
    for k in (1, 2, 3): mx.add('sfx', m[f'b{k}'], whoosh(0.8 if k < 3 else 1.2), 0.45 if k < 3 else 0.7)
    for k in (1, 2): mx.add('sfx', m[f're{k}'], pop(300, 1500, 0.1), 0.35); mx.add('sfx', m[f're{k}'] + 0.05, boing(), 0.2)
    mx.add('sfx', m['b3'] + 0.7, tada(72), 0.2); mx.add('sfx', m['b3'] + 0.7, chime_up(), 0.2)
    mx.add('sfx', m['again'] + 0.2, jingle(), 0.22)
    mx.voices(F, tl['events'])
    mx.write(F + '/audio.wav', quiet=[(m[f'c{i}'], m[f'r{i}']) for i in range(3)]); return tl


TL = json.load(open(F + '/timeline.json')) if os.path.exists(F + '/timeline.json') else None


def flame(cr, x, y, t, s=1.0, k=0):
    if s <= 0.01: return
    fl = 1 + 0.12 * math.sin(t * 17 + k * 2)
    cr.save(); cr.translate(x, y); cr.scale(s, s * fl); cr.rotate(0.12 * math.sin(t * 9 + k))
    glow(cr, 0, -20, 70, (1, 0.8, 0.3), 0.35)
    cr.move_to(0, -60); cr.curve_to(28, -25, 24, 6, 0, 8); cr.curve_to(-24, 6, -28, -25, 0, -60); cr.close_path(); fs(cr, hexc('#FFB31F'), 5)
    cr.move_to(0, -30); cr.curve_to(12, -12, 10, 4, 0, 5); cr.curve_to(-10, 4, -12, -12, 0, -30); cr.close_path(); cr.set_source_rgb(*hexc('#FFF2A8')); cr.fill()
    cr.restore()

def smoke(cr, x, y, t0, t):
    u = t - t0
    if u < 0 or u > 1.4: return
    for k in range(3):
        uu = u - k * 0.15
        if uu <= 0: continue
        cr.arc(x + 18 * math.sin(uu * 6 + k), y - 40 - uu * 160, 10 + uu * 14, 0, 2 * math.pi); cr.set_source_rgba(0.75, 0.75, 0.8, max(0, 0.6 - uu * 0.45)); cr.fill()

def cake(cr, r, t, s, lit, t_out, nums=None, trick=None):
    n = r['n']
    if s <= 0.01: return []
    cr.save(); cr.translate(540, CAKE_Y); cr.scale(s, s); cr.translate(-540, -CAKE_Y)
    ellipse(cr, 540, CAKE_Y + 10, 360, 50); fs(cr, hexc('#E8EEF5'))
    rrect(cr, 260, CAKE_Y - 260, 560, 260, 40); fs(cr, hexc(r['cake']))
    rrect(cr, 300, CAKE_Y - 420, 480, 180, 36); fs(cr, hexc(r['cake']))
    for yy, x0_, x1_ in ((CAKE_Y - 260, 260, 820), (CAKE_Y - 420, 300, 780)):
        cr.move_to(x0_, yy + 10)
        k = 0
        for x in range(int(x0_), int(x1_) + 1, 40):
            cr.line_to(x, yy + 10); cr.curve_to(x + 5, yy + 55, x + 35, yy + 55, x + 40, yy + 10); k += 1
        cr.line_to(x1_, yy - 5); cr.line_to(x0_, yy - 5); cr.close_path(); fs(cr, hexc(r['frost']), 6)
    for k in range(9):
        x = 300 + k * 60; y = CAKE_Y - 110 + (k % 2) * 40
        cr.arc(x, y, 12, 0, 2 * math.pi); cr.set_source_rgb(*hexc(CCOL[k % 5])); cr.fill()
    # candles
    xs = [540 + (k - (n - 1) / 2) * 92 for k in range(n)]
    for k, x in enumerate(xs):
        top = CAKE_Y - 560
        rrect(cr, x - 18, top, 36, 140, 12); fs(cr, hexc(CCOL[k % 5]))
        for y in range(int(top) + 20, int(top) + 140, 36):
            cr.move_to(x - 18, y + 12); cr.line_to(x + 18, y - 6); stroke_dev(cr, (1, 1, 1), 7, 0.8)
        cr.move_to(x, top); cr.line_to(x, top - 16); stroke_dev(cr, OUT, 4)
        on = lit if trick is None or k != trick[0] else trick[1]
        if on: flame(cr, x, top - 14, t, 1.35, k)
        else: smoke(cr, x, top - 14, t_out if trick is None or k != trick[0] else trick[2], t)
        if nums and k < nums[0]:
            u = clamp((t - nums[1] - k * 0.32) / 0.3)
            if u > 0:
                cr.arc(x, top + 70, 40 * ease_out_back(u, 1.8), 0, 2 * math.pi); fs(cr, hexc('#FFFFFF'), 6)
                big_word(cr, str(k + 1), x, top + 73, 52 * ease_out_back(u, 1.8), hexc(r['col']), 1.0)
    cr.restore()
    return xs

def room(cr, t, dark):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *mixc(hexc('#FFE1EE'), hexc('#5A4A8A'), dark)); g.add_color_stop_rgb(1, *mixc(hexc('#FFF2D6'), hexc('#3A2E66'), dark))
    cr.set_source(g); cr.paint()
    # garland and balloons
    for k in range(9):
        x = 60 + k * 120; y = 390 + 30 * math.sin(k)
        cr.move_to(x - 40, y - 20); cr.line_to(x + 40, y - 20); cr.line_to(x, y + 45); cr.close_path(); fs(cr, hexc(CCOL[k % 5]), 4)
    for k, (bx, by) in enumerate(((110, 700), (970, 650), (190, 900), (900, 900))):
        by2 = by + 20 * math.sin(t * 1.5 + k)
        cr.move_to(bx, by2 + 90); cr.curve_to(bx - 20, by2 + 200, bx + 20, by2 + 300, bx, by2 + 420); stroke_dev(cr, OUT, 3)
        ellipse(cr, bx, by2, 70, 85); fs(cr, hexc(CCOL[(k + 2) % 5])); ellipse(cr, bx - 25, by2 - 30, 14, 24); cr.set_source_rgba(1, 1, 1, 0.5); cr.fill()
    cr.rectangle(0, 1290, W, H - 1290); cr.set_source_rgb(*mixc(hexc('#C9A0FF'), hexc('#3A2E66'), dark * 0.6)); cr.fill()
    cr.move_to(0, 1290); cr.line_to(W, 1290); stroke_dev(cr, OUT, 6)

def wind(cr, t0, t, big=False):
    u = t - t0
    if u < 0 or u > (1.2 if big else 0.9): return
    a = 1 - u / (1.2 if big else 0.9)
    for k in range(6 if big else 4):
        y = 820 + k * 70 - (k % 2) * 30
        x = 200 + u * 900 + k * 20
        cr.move_to(x - 260, y); cr.curve_to(x - 150, y - 40, x - 60, y + 40, x, y); stroke_dev(cr, (1, 1, 1), 12 if big else 9, a)


def frame(cr, t):
    m = TL['marks']
    te = 0.0 if t >= m['loop'] else t
    twist = te >= m['tw']
    ri = 0
    for i in range(3):
        if te >= m[f's{i}']: ri = i
    dark = 0.0
    if not twist:
        lit_ = te < m[f'blow{ri}'] + 0.25
        dark = 0.0 if lit_ else 0.0
    room(cr, t, 0.15 if (not twist and te < m[f'blow{ri}'] + 0.25) or (twist and te < m['b3'] + 0.25) else 0.0)
    if not twist:
        r = ROUNDS[ri]; s0 = m[f's{ri}']; rv = m[f'r{ri}']; x0 = m[f'x{ri}']; bl = m[f'blow{ri}']
        s = ease_out_back(clamp((te - s0) / 0.5), 1.4) * (1 - smooth(x0, x0 + 0.4, te))
        cake(cr, r, te, s * 1.15, te < bl + 0.25, bl + 0.25, (r['n'], rv + 0.2) if te >= rv else None)
        wind(cr, bl, te)
        if te >= bl + 0.5: confetti(cr, bl + 0.5, te, 540, 700, 600)
    else:
        r = dict(n=1, cake='#B9F2A1', frost='#FFFFFF', col='#A15CFF')
        tw = m['tw']
        s = ease_out_back(clamp((te - tw) / 0.5), 1.4)
        b1, b2, b3, r1, r2 = m['b1'], m['b2'], m['b3'], m['re1'], m['re2']
        if te < b1 + 0.25: on, off_t = True, 0
        elif te < r1: on, off_t = False, b1 + 0.25
        elif te < b2 + 0.25: on, off_t = True, 0
        elif te < r2: on, off_t = False, b2 + 0.25
        elif te < b3 + 0.3: on, off_t = True, 0
        else: on, off_t = False, b3 + 0.3
        cr.save(); cr.translate(540, CAKE_Y); cr.scale(1.0, 1.0); cr.translate(-540, -CAKE_Y)
        xs = cake(cr, r, te, s * 1.15, on, off_t)
        cr.restore()
        for k in (1, 2):
            if m[f're{k}'] <= te < m[f're{k}'] + 0.6: sparkles(cr, 540, CAKE_Y - 600, m[f're{k}'], te, 7, 60, 140)
        wind(cr, b1, te); wind(cr, b2, te); wind(cr, b3, te, True)
        if te >= b3 + 0.6: confetti(cr, b3 + 0.6, te, 540, 650, 700)
    # chickpea (party hat = crown) blows
    st = chick_talk(base_st(), te, TL); h = 0; sx = sy = 1; look = (0.8, -0.6)
    blows = [m[f'blow{i}'] for i in range(3)] + [m['b1'], m['b2'], m['b3']]
    for b in blows:
        if b - 0.2 <= te < b + 0.6:
            st['beak'] = 0.3; sx = 1 + 0.12 * math.sin(math.pi * clamp((te - b + 0.2) / 0.8)); sy = 2 - sx; st['happy'] = 0
    for i in range(3):
        if m[f'c{i}'] <= te < m[f'r{i}']: look = (0.6 + 0.3 * math.sin(te * 2), -0.7)
        if m[f'blow{i}'] + 0.6 <= te < m[f'blow{i}'] + 1.5:
            h, sx, sy, air = hop_seq(te, m[f'blow{i}'] + 0.6, 2, 0.45, 55); st.update(happy=1, wing=[0.3 + 0.8 * air] * 2)
    for k in (1, 2):
        if m[f're{k}'] <= te < m[f're{k}'] + 0.8: st['mood'] = 0.0; look = (0.8, -1.0)
    if twist and te >= m['b3'] + 0.6: st.update(happy=1, wing=[0.6 + 0.4 * math.sin(te * 9)] * 2); h = 40 * abs(math.sin(te * 6))
    shadow_at(cr, 170, 1823, 100)
    chick(cr, 170, 1820, h, 0.78, st, te, look, sx, sy, acc='crown')
    for i, r in enumerate(ROUNDS):
        count_bubble(cr, m[f'c{i}'], te, "Count them!", y=470, w=520)
        word_pop(cr, r['a'], 620, 1500, 110, r['col'], m[f'r{i}'] + 0.3 + 0.32 * r['n'], m[f'blow{i}'] - 0.5, te)
        word_pop(cr, "BLOW!", 540, 480, 150, '#7FD3FF', m[f'blow{i}'] - 0.3, m[f'blow{i}'] + 0.9, te, 0.08)
    for k in (1, 2): word_pop(cr, "Huh?", 540, 480, 140, '#FF9A1F', m[f're{k}'], m[f're{k}'] + 0.9, te, 0.1)
    word_pop(cr, "BLOW!", 540, 480, 180, '#7FD3FF', m['b3'] - 0.3, m['b3'] + 0.9, te, 0.08)
    word_pop(cr, "Happy Birthday!", 540, 480, 100, '#FF5FA2', m['b3'] + 0.9, m['again'] + 0.3, te, 0.06)
    draw_text(cr, "Blow the Candles!", 250, 115, t, -1)
    loop_fade(cr, TL, t)

if __name__ == '__main__': episode_main(build, F)
