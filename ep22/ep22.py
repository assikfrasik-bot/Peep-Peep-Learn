"""Pop the Number! — bath time, number bubbles; find and pop the right number. Twist: giant bubble lifts Chickpea."""
import sys; sys.path.insert(0, '/home/claude/kit')
from common import *

F = '/home/claude/ep22'
TUB_Y = 1420
NUMCOL = {1: '#FF4D4D', 2: '#FF9A1F', 3: '#3ECF5E', 4: '#2EA7FF', 5: '#A15CFF'}
ROUNDS = [dict(nums=[1, 2, 3], ans=2, q="Pop number two!", a="Two! Pop!"),
          dict(nums=[4, 1, 3, 5], ans=4, q="Now pop number four!", a="Four! Pop!"),
          dict(nums=[3, 5, 2, 1, 4], ans=5, q="Can you find number five?", a="Five! Pop, pop!")]
LAYOUT = {3: [(240, 920), (540, 780), (840, 920)],
          4: [(210, 960), (420, 760), (660, 980), (870, 760)],
          5: [(190, 800), (400, 1000), (540, 720), (680, 1000), (890, 800)]}


def build():
    s = Script(F); t = 0.1
    t = s.say(t, 'hook', "Bath time! Let's pop the numbers!", 0.95, True) + 0.15
    for i, r in enumerate(ROUNDS):
        s.mark(f's{i}', t if i else 0.0)
        t = s.say(t + (0.2 if i else 0), f'q{i}', r['q']) + 0.1
        s.mark(f'c{i}', t); t += 3.0; s.mark(f'r{i}', t)
        t = s.say(t + 0.45, f'a{i}', r['a']) + 0.3
        s.mark(f'x{i}', t); t += 0.6
    s.mark('giant', t)
    t = s.say(t, 'whoa', "Whoa! A giant bubble!", 1.0, True) + 0.1
    s.mark('up', t); t += 1.4
    s.mark('popg', t); t += 0.8
    t = s.say(t, 'splash', "Splash! Hee hee!", 1.0, True) + 0.25
    s.mark('again', t); t = s.say(t, 'again', "Again?", 1.0, True) + 0.25
    s.mark('loop', t); t += 0.9
    tl = s.save(t); m = tl['marks']; mx = Mix(tl['dur'])
    mx.music_loop(0, tl['dur'], 112, [([60, 64, 67], 36), ([57, 60, 64], 45), ([65, 69, 72], 41), ([67, 71, 74], 43)],
                  [[84, None, 79, None, 76, None, 79, None], [81, None, 79, None, 77, None, None, None]], 'bouncy', 0.75)
    for i in range(3):
        mx.add('sfx', m[f's{i}'] + 0.1, bubbles_snd(5, 0.8), 0.25)
        countdown_ticks(mx, m[f'c{i}'])
        mx.add('sfx', m[f'r{i}'] + 0.3, pop(900, 300, 0.1), 0.6); mx.add('sfx', m[f'r{i}'] + 0.35, ding(), 0.2)
        if i == 2: mx.add('sfx', m[f'r{i}'] + 1.0, pop(900, 300, 0.1), 0.5)
        mx.add('sfx', m[f'x{i}'], pop(700, 300, 0.08), 0.3)
    mx.add('sfx', m['giant'], bubbles_snd(8, 1.2), 0.3); mx.add('sfx', m['up'], slide_whistle(300, 1200, 1.3), 0.2)
    mx.add('sfx', m['popg'], pop(900, 200, 0.18), 0.7); mx.add('sfx', m['popg'] + 0.55, splash_snd(0.7), 0.6)
    mx.add('sfx', m['popg'] + 0.7, tada(72), 0.18)
    mx.add('sfx', m['again'] + 0.2, jingle(), 0.22)
    mx.voices(F, tl['events'])
    mx.write(F + '/audio.wav', quiet=[(m[f'c{i}'], m[f'r{i}']) for i in range(3)]); return tl


TL = json.load(open(F + '/timeline.json')) if os.path.exists(F + '/timeline.json') else None
rr = random.Random(22)
FOAM = [(x, rr.uniform(-20, 20), rr.uniform(34, 60)) for x in range(110, 990, 46)]
SMALL = [(rr.uniform(60, 1020), rr.uniform(0, 1), rr.uniform(10, 26), rr.uniform(0, 6.28)) for _ in range(16)]


def bubble(cr, x, y, r, num, t, a=1.0):
    cr.push_group()
    g = cairo.RadialGradient(x - r * 0.3, y - r * 0.3, r * 0.1, x, y, r)
    g.add_color_stop_rgba(0, 1, 1, 1, 0.25); g.add_color_stop_rgba(0.75, 0.8, 0.95, 1, 0.18); g.add_color_stop_rgba(1, 0.75, 0.6, 1, 0.55)
    cr.arc(x, y, r, 0, 2 * math.pi); cr.set_source(g); cr.fill()
    cr.arc(x, y, r, 0, 2 * math.pi); stroke_dev(cr, hexc('#7FC8FF'), 6, 0.9)
    cr.arc(x, y, r - 8, math.pi * 1.1, math.pi * 1.5); stroke_dev(cr, (1, 1, 1), 10, 0.9)
    cr.arc(x + r * 0.45, y - r * 0.5, r * 0.08, 0, 2 * math.pi); cr.set_source_rgba(1, 1, 1, 0.9); cr.fill()
    if num: big_word(cr, str(num), x, y + 4, r * 1.25, hexc(NUMCOL[num]), 1.0)
    cr.pop_group_to_source(); cr.paint_with_alpha(a)

def pop_fx(cr, x, y, r, t0, t):
    u = t - t0
    if u < 0 or u > 0.6: return
    a = 1 - u / 0.6
    for k in range(10):
        ang = k * math.pi / 5
        r0 = r * (0.8 + u * 1.2); r1 = r0 + 40
        cr.move_to(x + r0 * math.cos(ang), y + r0 * math.sin(ang)); cr.line_to(x + r1 * math.cos(ang), y + r1 * math.sin(ang))
        stroke_dev(cr, hexc('#7FC8FF'), 9, a)
    for k in range(8):
        ang = k * math.pi / 4 + 0.3; d = r * (0.6 + u * 2)
        cr.arc(x + d * math.cos(ang), y + d * math.sin(ang) + 300 * u * u, 10, 0, 2 * math.pi); cr.set_source_rgba(0.7, 0.9, 1, a); cr.fill()


def bathroom(cr, t):
    cr.set_source_rgb(*hexc('#DFF3FF')); cr.paint()
    for y in range(300, 1500, 100):
        for x in range(0, W, 100):
            rrect(cr, x + 5, y + 5, 90, 90, 12); cr.set_source_rgb(*hexc('#C9EAFF' if ((x + y) // 100) % 2 else '#EAF7FF')); cr.fill()
    cr.rectangle(0, 1560, W, H - 1560); cr.set_source_rgb(*hexc('#9AD7F0')); cr.fill()
    # shower head
    cr.move_to(980, 300); cr.line_to(980, 420); cr.line_to(900, 470); stroke_dev(cr, OUT, 22); cr.move_to(980, 300); cr.line_to(980, 420); cr.line_to(900, 470); stroke_dev(cr, hexc('#C9D2DD'), 12)
    ellipse(cr, 885, 485, 55, 22); fs(cr, hexc('#C9D2DD'))
    for x0, ph, r, sp in SMALL:
        y = 1350 - ((t * 0.12 + ph) % 1) * 1050
        cr.arc(x0 + 20 * math.sin(t + sp), y, r, 0, 2 * math.pi); stroke_dev(cr, (1, 1, 1), 4, 0.7)

def tub_back(cr):
    rrect(cr, 60, TUB_Y - 60, 960, 60, 30); fs(cr, (1, 1, 1))
    cr.rectangle(100, TUB_Y - 20, 880, 40); cr.set_source_rgb(*hexc('#8FD3FF')); cr.fill()

def tub_front(cr, t):
    for x, dy, r in FOAM:
        cr.arc(x, TUB_Y - 10 + dy + 6 * math.sin(t * 2 + x), r, 0, 2 * math.pi); cr.new_sub_path()
    stroke_dev(cr, OUT, 10)
    for x, dy, r in FOAM:
        cr.arc(x, TUB_Y - 10 + dy + 6 * math.sin(t * 2 + x), r, 0, 2 * math.pi); cr.new_sub_path()
    cr.set_source_rgb(1, 1, 1); cr.fill()
    cr.move_to(70, TUB_Y); cr.line_to(1010, TUB_Y); cr.curve_to(1010, 1700, 900, 1730, 800, 1730); cr.line_to(280, 1730)
    cr.curve_to(180, 1730, 70, 1700, 70, TUB_Y); cr.close_path(); fs(cr, (1, 1, 1))
    rrect(cr, 70, TUB_Y - 10, 940, 40, 20); fs(cr, hexc('#FFFFFF'))
    for x in (220, 860): rrect(cr, x - 30, 1720, 60, 70, 20); fs(cr, hexc('#FFC93C'))
    # rubber duck on the rim
    cr.save(); cr.translate(900, TUB_Y - 50); cr.scale(0.35, 0.35)
    cr.arc(0, 0, 90, 0, 2 * math.pi); fs(cr, hexc('#FFDE3B')); cr.arc(50, -90, 55, 0, 2 * math.pi); fs(cr, hexc('#FFDE3B'))
    ellipse(cr, 115, -80, 38, 15); fs(cr, hexc('#FF8A1F'), 5); cr.arc(62, -105, 10, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill()
    cr.restore()

def shower_cap(cr, t):
    cr.save(); cr.translate(0, -320)
    cr.move_to(-125, 20); cr.curve_to(-120, -110, 120, -110, 125, 20); cr.curve_to(60, 0, -60, 0, -125, 20); cr.close_path()
    p = cr.copy_path(); fs(cr, hexc('#FF9EC7'))
    cr.save(); cr.append_path(p); cr.clip()
    for x, y in ((-70, -30), (-10, -60), (50, -30), (80, -70), (-50, -80)): cr.arc(x, y, 12, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()
    cr.restore()
    for k in range(9):
        cr.arc(-120 + k * 30, 18 + 4 * math.sin(k), 14, 0, math.pi); stroke_dev(cr, hexc('#FF7EB6'), 6)
    cr.restore()


def frame(cr, t):
    m = TL['marks']
    te = 0.0 if t >= m['loop'] else t
    bathroom(cr, t)
    tub_back(cr)
    # chick in the tub (or in giant bubble)
    st = chick_talk(base_st(), te, TL); look = (0.0, -0.7); h = 0; sx = sy = 1
    cx, cb = 540, TUB_Y + 30
    ri = 0
    for i in range(3):
        if te >= m[f's{i}']: ri = i
    in_bubble = m['giant'] + 0.6 <= te < m['popg']
    if not (m['giant'] <= te):
        r = ROUNDS[ri]
        for i in range(3):
            if m[f'c{i}'] <= te < m[f'r{i}']: look = (math.sin(te * 2.2), -0.8)
            if m[f'r{i}'] <= te < m[f'r{i}'] + 0.9:
                h, sx, sy, air = hop_seq(te, m[f'r{i}'] + 0.3, 2, 0.45, 40); st.update(happy=1, wing=[0.3 + 0.8 * air] * 2)
    lift = 0
    if te >= m['giant']:
        lift = 650 * smooth(m['up'], m['up'] + 1.3, te)
        if te >= m['popg']:
            u = te - m['popg']; lift = max(0, 650 - 2600 * u * u) if u < 0.6 else 0
        st.update(happy=1, wing=[0.9 + 0.4 * math.sin(te * 9), 0.9 + 0.4 * math.sin(te * 9 + 1)]); look = (0, -0.3)
    chick(cr, cx, cb - lift, h, 0.72, st, te, look, sx, sy, extra=shower_cap, shell=True)
    tub_front(cr, t)
    if te >= m['giant']:
        gr = 270 * ease_out_back((te - m['giant']) / 0.6)
        if te < m['popg']:
            bubble(cr, cx + 8 * math.sin(te * 3), cb - lift - 175 + 10 * math.sin(te * 2.5), gr, None, te, 0.95)
        pop_fx(cr, cx, cb - 650 - 175 + 90, 270, m['popg'], te)
        if te >= m['popg'] + 0.5 and te < m['popg'] + 1.5:
            for k in range(10):
                u = te - m['popg'] - 0.5; ang = math.pi * (0.15 + 0.7 * k / 9)
                x = cx + math.cos(ang) * 500 * u * (1 if k % 2 else -1); y = TUB_Y - math.sin(ang) * 900 * u + 1300 * u * u
                if y < TUB_Y + 10: cr.arc(x, y, 14, 0, 2 * math.pi); fs(cr, hexc('#BFEAFF'), 4)
    # number bubbles
    if te < m['giant']:
        r = ROUNDS[ri]; lay = LAYOUT[len(r['nums'])]
        app = smooth(m[f's{ri}'], m[f's{ri}'] + 0.7, te) if ri else 1.0
        clear = smooth(m[f'x{ri}'], m[f'x{ri}'] + 0.4, te)
        for j, n in enumerate(r['nums']):
            bx, by = lay[j]
            yy = by + 30 * math.sin(te * 1.6 + j * 1.3) + (1 - app) * 600
            xx = bx + 15 * math.sin(te * 1.1 + j)
            rad = 125 if len(r['nums']) < 5 else 112
            popped = n == r['ans'] and te >= m[f'r{ri}'] + 0.3
            if popped:
                pop_fx(cr, xx, yy, rad, m[f'r{ri}'] + 0.3, te)
                continue
            if clear > 0:
                if clear >= 1: continue
                pop_fx(cr, xx, yy, rad, m[f'x{ri}'], te)
            wob = 1 + (0.06 * math.sin(te * 25) * burst(m[f'r{ri}'], m[f'r{ri}'] + 0.3, te) if n == r['ans'] else 0)
            bubble(cr, xx, yy, rad * wob * app, n, te, 1 - clear)
    for i, r in enumerate(ROUNDS):
        count_bubble(cr, m[f'c{i}'], te, "Point to it!", y=440, w=560)
        word_pop(cr, str(r['ans']), 540, 470, 200, NUMCOL[r['ans']], m[f'r{i}'] + 0.35, m[f'x{i}'] + 0.2, te)
    word_pop(cr, "POP!", 540, 470, 180, '#FF5FA2', m['popg'], m['again'] + 0.3, te)
    draw_text(cr, "Pop the Number!", 250, 130, t, -1)
    loop_fade(cr, TL, t)

if __name__ == '__main__': episode_main(build, F)
