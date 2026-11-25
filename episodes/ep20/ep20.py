"""Spot the Difference! — two picnic pictures. Twist: Chickpea in the bottom picture waves at us."""
import sys; sys.path.insert(0, '/home/claude/kit')
from common import *

F = '/home/claude/ep20'
FW, FH = 840, 568            # frame size on screen
SC = FW / 1080                # local scene 1080 x 730
FRAMES = [(120, 335), (120, 925)]
DIFFS = [dict(k='kite', p=(780, 210), r=(95, 115), q="Can you find a difference?", a="The kite! One kite is red, one is blue!", w='KITE!', c='#2EA7FF'),
         dict(k='bfly', p=(330, 320), r=(80, 70), q="Find another one!", a="The butterfly! It flew away!", w='BUTTERFLY!', c='#A15CFF'),
         dict(k='sun', p=(930, 120), r=(95, 95), q="One more! Look closely!", a="The sun has sunglasses! Cool sun!", w='SUN!', c='#FFB400')]


def build():
    s = Script(F); t = 0.1
    t = s.say(t, 'hook', "Two pictures! Can you spot the difference?") + 0.15
    for i, d in enumerate(DIFFS):
        s.mark(f's{i}', t)
        if i: t = s.say(t, f'q{i}', d['q']) + 0.1
        s.mark(f'c{i}', t); t += 3.5; s.mark(f'r{i}', t)
        t = s.say(t + 0.45, f'a{i}', d['a']) + 0.4
    s.mark('wave', t)
    t = s.say(t, 'hey', "Hey! This Chickpea is waving!") + 0.1
    t = s.say(t, 'hi', "Hi! That's me! Hee hee!", 1.0, True) + 0.25
    s.mark('again', t); t = s.say(t, 'again', "Again?", 1.0, True) + 0.25
    s.mark('loop', t); t += 0.9
    tl = s.save(t); m = tl['marks']; mx = Mix(tl['dur'])
    mx.music_loop(0, tl['dur'], 104, [([60, 64, 67], 36), ([62, 65, 69], 38), ([57, 60, 64], 45), ([67, 71, 74], 43)],
                  [[72, None, 74, None, 76, None, 79, None], [77, None, 76, None, 72, None, None, None]], 'soft', 1.0)
    for i in range(3):
        for j in range(3): mx.add('sfx', m[f'c{i}'] + 0.5 + j, tick(1100 if j < 2 else 1500), 0.3)
        mx.add('sfx', m[f'r{i}'], whoosh(0.4), 0.2); mx.add('sfx', m[f'r{i}'] + 0.2, ding(), 0.22)
        mx.add('sfx', m[f'r{i}'] + 0.35, chirp(), 0.15)
    mx.add('sfx', m['wave'], boing(), 0.25); mx.add('sfx', m['wave'] + 1.2, tada(72), 0.18)
    mx.add('sfx', m['again'] + 0.2, jingle(), 0.22)
    mx.voices(F, tl['events'])
    mx.write(F + '/audio.wav', quiet=[(m[f'c{i}'], m[f'r{i}']) for i in range(3)]); return tl


TL = json.load(open(F + '/timeline.json')) if os.path.exists(F + '/timeline.json') else None
rr = random.Random(20)
FLW = [(rr.uniform(30, 1050), rr.uniform(610, 720), rr.choice(['#FF5A5F', '#FFFFFF', '#A66CFF', '#FFB400']), rr.uniform(0.45, 0.6)) for _ in range(9)]


def kite(cr, x, y, col, t):
    cr.save(); cr.translate(x, y); cr.rotate(0.15 * math.sin(t * 1.5))
    cr.move_to(0, 150)
    for k in range(1, 8): cr.line_to(25 * math.sin(k * 1.1 + t * 3), 150 + k * 26)
    stroke_dev(cr, OUT, 5)
    for k in range(3):
        yy = 190 + k * 50; xx = 25 * math.sin((1 + k * 2) * 1.1 + t * 3)
        cr.move_to(xx - 14, yy - 10); cr.line_to(xx + 14, yy + 10); cr.move_to(xx + 14, yy - 10); cr.line_to(xx - 14, yy + 10); stroke_dev(cr, hexc('#FFD93B'), 9)
    cr.move_to(0, -110); cr.line_to(80, 0); cr.line_to(0, 150); cr.line_to(-80, 0); cr.close_path(); fs(cr, hexc(col))
    cr.move_to(0, -110); cr.line_to(0, 150); cr.move_to(-80, 0); cr.line_to(80, 0); stroke_dev(cr, (1, 1, 1), 5, 0.7)
    face(cr, 0, 10, 0.7)
    cr.restore()

def sun_face(cr, t, shades):
    cx, cy, R = 930, 120, 72
    cr.save(); cr.translate(cx, cy); cr.rotate(t * 0.4)
    for i in range(12):
        cr.save(); cr.rotate(i * math.pi / 6); cr.move_to(-12, -R - 12); cr.line_to(0, -R - 45); cr.line_to(12, -R - 12); cr.close_path()
        cr.set_source_rgb(1, 0.72, 0.1); cr.fill(); cr.restore()
    cr.restore()
    cr.arc(cx, cy, R, 0, 2 * math.pi); fs(cr, hexc('#FFE14D'))
    if shades:
        for s in (-1, 1): rrect(cr, cx + s * 30 - 26, cy - 30, 52, 34, 12); fs(cr, hexc('#2B2B3A'), 5)
        cr.move_to(cx - 6, cy - 16); cr.line_to(cx + 6, cy - 16); stroke_dev(cr, OUT, 5)
    else:
        for s in (-1, 1): cr.arc(cx + s * 26, cy - 10, 11, math.pi * 1.1, math.pi * 1.9); stroke_dev(cr, OUT, 5)
    cr.arc(cx, cy + 14, 24, 0.15 * math.pi, 0.85 * math.pi); stroke_dev(cr, OUT, 5)

def blanket(cr):
    cr.move_to(300, 560); cr.line_to(820, 560); cr.line_to(900, 700); cr.line_to(220, 700); cr.close_path()
    p = cr.copy_path(); cr.set_source_rgb(1, 1, 1); cr.fill()
    cr.save(); cr.append_path(p); cr.clip()
    for k in range(-6, 14):
        cr.move_to(300 + k * 52, 560); cr.line_to(220 + k * 62, 700); stroke_dev(cr, hexc('#FF6B6B'), 22, 0.85)
    for y in (595, 640, 680): cr.move_to(200, y); cr.line_to(920, y); stroke_dev(cr, hexc('#FF6B6B'), 18, 0.6)
    cr.restore(); cr.append_path(p); stroke_dev(cr, OUT, 6)

def basket(cr):
    cr.move_to(600, 560); cr.curve_to(600, 470, 740, 470, 740, 560); stroke_dev(cr, OUT, 16); cr.move_to(600, 560); cr.curve_to(600, 470, 740, 470, 740, 560); stroke_dev(cr, hexc('#C88A55'), 8)
    rrect(cr, 580, 545, 180, 95, 18); fs(cr, hexc('#D9A05B'))
    for x in range(600, 760, 30): cr.move_to(x, 550); cr.line_to(x, 635); stroke_dev(cr, hexc('#B07A3A'), 4)
    cr.save(); cr.translate(625, 540); cr.scale(0.22, 0.22); obj_apple(cr, 1); cr.restore()

def scene(cr, t, variant, te, m):
    sky(cr, '#5EC2FF', '#E6F8FF', 600)
    clouds(cr, t, ((300, 120, 0.3), (620, 200, 0.25)), 8)
    sun_face(cr, t, variant)
    cr.move_to(0, 730)
    for x in range(0, 1101, 20): cr.line_to(x, 470 - 40 * math.sin(math.pi * x / 1080 * 1.4 + 0.2))
    cr.line_to(1080, 730); cr.close_path(); cr.set_source_rgb(*hexc('#8EDB6F')); cr.fill()
    tree(cr, 150, 560, 1.2, '#4CB944')
    blanket(cr)
    basket(cr)
    for i, (x, y, c, s) in enumerate(FLW): draw_flower(cr, x, y, s, hexc(c), t, i)
    kite(cr, 780, 210, '#2EA7FF' if variant else '#FF4D4D', t)
    cr.move_to(780, 360); cr.curve_to(700, 450, 600, 470, 520, 560); stroke_dev(cr, OUT, 3)
    if not variant: draw_bfly(cr, 330 + 10 * math.sin(t * 2), 320 + 8 * math.sin(t * 3), t, 0.1, 0.7)
    # chickpea on the blanket
    st = base_st(); look = (0.5, -0.5); waving = variant and te >= m['wave']
    if waving:
        st = chick_talk(st, te, TL); st.update(happy=1, wing=[0.0, 1.0 + 0.5 * math.sin(te * 12)]); look = (0, 0.3)
    else:
        st['wing'] = [0.0, 0.9]
    chick(cr, 480, 650, 0, 0.42, st, t, look)


def frame(cr, t):
    m = TL['marks']
    te = 0.0 if t >= m['loop'] else t
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *hexc('#FFE3EF')); g.add_color_stop_rgb(1, *hexc('#E3F1FF'))
    cr.set_source(g); cr.paint()
    for k in range(30):
        x = (k * 173) % 1080; y = (k * 311) % 1920
        star5(cr, x, y, 10); cr.set_source_rgba(1, 1, 1, 0.8); cr.fill()
    for fi, (fx, fy) in enumerate(FRAMES):
        rrect(cr, fx - 14, fy - 14, FW + 28, FH + 28, 30); fs(cr, (1, 1, 1), 8)
        cr.save(); rrect(cr, fx, fy, FW, FH, 20); cr.clip(); cr.translate(fx, fy); cr.scale(SC, SC)
        scene(cr, t, fi == 1, te, m)
        # found rings
        for i, d in enumerate(DIFFS):
            p = smooth(m[f'r{i}'], m[f'r{i}'] + 0.4, te)
            if p > 0:
                px, py = d['p']; rx, ry = d['r']
                cr.save(); cr.translate(px, py); cr.scale(rx, ry); cr.arc(0, 0, 1, -2.2, -2.2 + 2.15 * math.pi * p); cr.restore()
                stroke_dev(cr, hexc('#FF3B3B'), 11)
                if fi == 1: sparkles(cr, px, py, m[f'r{i}'], te, 6, 60, 140)
        if fi == 1 and te >= m['wave']:
            p = smooth(m['wave'] + 0.6, m['wave'] + 1.0, te)
            cr.save(); cr.translate(480, 560); cr.scale(110, 120); cr.arc(0, 0, 1, -2.2, -2.2 + 2.15 * math.pi * p); cr.restore()
            stroke_dev(cr, hexc('#FF9A1F'), 11)
        cr.restore()
        rrect(cr, fx, fy, FW, FH, 20); stroke_dev(cr, OUT, 7)
    # found counter (stars) between the frames
    busy = any(m[f'c{i}'] + 0.5 <= te < (m[f's{i + 1}'] if i < 2 else m['wave']) for i in range(3)) or te >= m['wave']
    for i in range(3 if not busy else 0):
        on = te >= m[f'r{i}']
        e = ease_out_back((te - m[f'r{i}']) / 0.4) if on else 1
        cx = 540 + (i - 1) * 110
        star5(cr, cx, 1560, 40 * (e if on else 1)); fs(cr, hexc('#FFD93B') if on else (0.85, 0.85, 0.9), 5)
    for i, d in enumerate(DIFFS):
        count_bubble(cr, m[f"c{i}"] + 0.5, te, "Find it!", y=1580, w=480)
        nxt = m[f's{i + 1}'] if i < 2 else m['wave']
        word_pop(cr, d["w"], 540, 1580, 120, d['c'], m[f'r{i}'] + 0.3, nxt - 0.1, te)
    word_pop(cr, "That's me!", 540, 1580, 120, '#FF9A1F', m['wave'] + 1.0, m['again'] + 0.3, te)
    # tiny chickpea guide in the corner peeking from below
    st = chick_talk(base_st(), te, TL); look = (0.0, -0.9)
    for i in range(3):
        if m[f'r{i}'] <= te < m[f'r{i}'] + 0.9: st.update(happy=1, wing=[0.9, 0.9])
    draw_text(cr, "Spot the Difference!", 250, 112, t, -1)
    loop_fade(cr, TL, t)

if __name__ == '__main__': episode_main(build, F)
