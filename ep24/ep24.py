"""Who Eats What? — feed the monkey, the puppy and the panda. Twist: baby brother gobbles the leftovers and BURPS."""
import sys; sys.path.insert(0, '/home/claude/kit')
from common import *
import numpy as np
from kit import SR, tt, lp, att
from anim2 import obj_banana, obj_carrot, obj_apple

F = '/home/claude/ep24'
AX, AY = 540, 880            # animal face centre
ASC = 1.25
BABY_BY, BABY_SC = 1190, 0.95
BEAK = (540, 1000)
BUSH_Y = 1215
CARD_Y = 1360
CARD_X = [215, 540, 865]
ROUNDS = [dict(k='monkey', name='monkey', foods=['carrot', 'banana', 'bone'], ans=1, a="A banana!", v="Ooh ooh, ah ah!"),
          dict(k='puppy', name='puppy', foods=['bone', 'bamboo', 'apple'], ans=0, a="A bone!", v="Woof woof!"),
          dict(k='panda', name='panda', foods=['apple', 'bone', 'bamboo'], ans=2, a="Bamboo!", v="Yum, yum, yum!")]
LEFT = ['carrot', 'apple', 'banana']


def burp(d=0.75):
    t = tt(d); f = 95 - 35 * (t / d) + 8 * np.sin(2 * np.pi * 7 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sign(np.sin(ph)) * 0.5 + np.sin(ph * 2) * 0.3
    s = s * (0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 23 * t)))
    s = lp(s, 900) * np.sin(np.pi * t / d) ** 0.6 * att(t, 0.02)
    return (s / (np.abs(s).max() + 1e-6)).astype(np.float32)

def gulp():
    t = tt(0.22); f = 500 * np.exp(-t / 0.05) + 160
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.07) * att(t, 0.003)).astype(np.float32)

def munch(n=4, gap=0.18):
    out = np.zeros(int((n * gap + 0.2) * SR), np.float32)
    for k in range(n):
        tk = tt(0.09); s = lp(np.random.default_rng(k).standard_normal(len(tk)), 1800) * np.exp(-tk / 0.025)
        i = int(k * gap * SR); out[i:i + len(s)] += s.astype(np.float32) * 0.8
    return out


def build():
    s = Script(F); t = 0.1
    t = s.say(t, 'hook', "Feeding time! Who eats what?") + 0.05
    t = s.say(t, 'yum', "Yum yum!", 1.0, True) + 0.15
    for i, r in enumerate(ROUNDS):
        s.mark(f's{i}', t); t += 0.6
        t = s.say(t, f'q{i}', f"What does the {r['name']} eat?") + 0.05
        s.mark(f'c{i}', t); t += 3.0; s.mark(f'r{i}', t)
        t = s.say(t + 0.35, f'a{i}', r['a']) + 0.1
        s.mark(f'eat{i}', t - 0.3)
        t = s.say(t + 0.5, f'v{i}', r['v'], 1.05, False, 'am_puck') + 0.3
        s.mark(f'x{i}', t); t += 0.5
    s.mark('tw', t)
    t = s.say(t + 0.4, 'peep', "Peep! Peep!", 1.05, True) + 0.1
    t = s.say(t, 'uhoh', "Uh oh... the baby is hungry!") + 0.1
    s.mark('gulp', t); t += 1.3
    s.mark('burp', t); t += 1.0
    t = s.say(t, 'excuse', "Excuse you! Hee hee!", 1.0, True) + 0.25
    s.mark('again', t); t = s.say(t, 'again', "Again?", 1.0, True) + 0.25
    s.mark('loop', t); t += 0.9
    tl = s.save(t); m = tl['marks']; mx = Mix(tl['dur'])
    mx.music_loop(0, tl['dur'], 116, [([60, 64, 67], 36), ([65, 69, 72], 41), ([62, 65, 69], 38), ([67, 71, 74], 43)],
                  [[72, None, 76, 79, None, 76, 77, None], [74, None, 71, None, 72, None, None, None]], 'bouncy', 0.75)
    for i in range(3):
        mx.add('sfx', m[f's{i}'], boing(), 0.18)
        countdown_ticks(mx, m[f'c{i}'])
        mx.add('sfx', m[f'r{i}'], pop(300, 900, 0.12), 0.35); mx.add('sfx', m[f'r{i}'] + 0.1, ding(), 0.2)
        mx.add('sfx', m[f'r{i}'] + 0.15, slide_whistle(500, 1200, 0.45), 0.12)
        mx.add('sfx', m[f'eat{i}'], munch(5), 0.45)
        mx.add('sfx', m[f'x{i}'], slide_whistle(900, 400, 0.4), 0.1)
    mx.add('sfx', m['tw'] + 0.2, pop(300, 900, 0.12), 0.35)
    for k in range(3): mx.add('sfx', m['gulp'] + 0.1 + k * 0.38, gulp(), 0.55)
    mx.add('sfx', m['burp'], burp(), 0.7)
    mx.add('sfx', m['burp'] + 0.85, tada(72), 0.15)
    mx.add('sfx', m['again'] + 0.2, jingle(), 0.22)
    mx.voices(F, tl['events'])
    mx.write(F + '/audio.wav', quiet=[(m[f'c{i}'], m[f'r{i}']) for i in range(3)]); return tl


TL = json.load(open(F + '/timeline.json')) if os.path.exists(F + '/timeline.json') else None


# ---------------- animals (face centre at origin; mouth near (0, 110)) ----------------
def eyes2(cr, sp, y, s=1.0, happy=False, col=OUT, white=True):
    for sx in (-1, 1):
        if happy:
            cr.arc(sx * sp, y + 6, 16 * s, math.pi * 1.1, math.pi * 1.9); stroke_dev(cr, col, 7)
        else:
            cr.arc(sx * sp, y, 18 * s, 0, 2 * math.pi); cr.set_source_rgb(*col); cr.fill()
            if white: cr.arc(sx * sp - 5, y - 6, 6 * s, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()

def mouth(cr, y, talk, w=40):
    if talk > 0.08:
        ellipse(cr, 0, y + 10 * talk, w * 0.8, 6 + 34 * talk); fs(cr, hexc('#7A2B3A'), 6)
        ellipse(cr, 0, y + 10 * talk + 18 * talk, w * 0.5, 9 * talk + 2); cr.set_source_rgb(*hexc('#FF7F9A')); cr.fill()
    else:
        cr.arc(0, y - 12, w * 0.7, 0.2 * math.pi, 0.8 * math.pi); stroke_dev(cr, OUT, 7)

def blush(cr, sp, y):
    for sx in (-1, 1): ellipse(cr, sx * sp, y, 24, 14); cr.set_source_rgba(1, 0.45, 0.55, 0.5); cr.fill()

def monkey(cr, t, talk=0, happy=False):
    B = hexc('#A8703F'); Bg = hexc('#F6D3A6')
    for sx in (-1, 1):
        cr.arc(sx * 195, 10, 72, 0, 2 * math.pi); fs(cr, B); cr.arc(sx * 195, 10, 42, 0, 2 * math.pi); cr.set_source_rgb(*Bg); cr.fill()
    cr.arc(0, 0, 195, 0, 2 * math.pi); fs(cr, B)
    for k in range(3): cr.move_to(-20 + k * 20, -190); cr.curve_to(-30 + k * 25, -240, 10 + k * 15, -250, 0 + k * 20, -215); stroke_dev(cr, OUT, 16); cr.move_to(-20 + k * 20, -190); cr.curve_to(-30 + k * 25, -240, 10 + k * 15, -250, 0 + k * 20, -215); stroke_dev(cr, B, 8)
    cr.new_path()
    for sx in (-1, 1): cr.arc(sx * 62, -30, 85, 0, 2 * math.pi); cr.new_sub_path()
    ellipse(cr, 0, 80, 140, 95); stroke_dev(cr, OUT, 12)
    for sx in (-1, 1): cr.arc(sx * 62, -30, 85, 0, 2 * math.pi); cr.new_sub_path()
    ellipse(cr, 0, 80, 140, 95); cr.set_source_rgb(*Bg); cr.fill()
    eyes2(cr, 60, -35, 1.0, happy)
    for sx in (-1, 1): ellipse(cr, sx * 14, 40, 7, 10); cr.set_source_rgb(*hexc('#7A4A28')); cr.fill()
    mouth(cr, 105, talk, 55); blush(cr, 115, 50)

def puppy(cr, t, talk=0, happy=False):
    C = hexc('#F2C48D'); Br = hexc('#8B5A3C')
    for sx in (-1, 1):
        cr.save(); cr.translate(sx * 165, -40); cr.rotate(sx * (0.25 + 0.08 * math.sin(t * 4))); ellipse(cr, 0, 90, 62, 140); fs(cr, Br); cr.restore()
    ellipse(cr, 0, 0, 185, 175); fs(cr, C)
    cr.save(); ellipse(cr, 0, 0, 182, 172); cr.clip(); ellipse(cr, 75, -60, 70, 65); cr.set_source_rgb(*hexc('#E3A66A')); cr.fill(); cr.restore()
    ellipse(cr, 0, 80, 115, 80); fs(cr, (1, 1, 1))
    eyes2(cr, 70, -35, 1.05, happy)
    ellipse(cr, 0, 35, 40, 27); cr.set_source_rgb(*OUT); cr.fill(); ellipse(cr, -10, 27, 12, 7); cr.set_source_rgb(1, 1, 1); cr.fill()
    cr.move_to(0, 60); cr.line_to(0, 80); stroke_dev(cr, OUT, 6)
    if talk < 0.08 and happy:
        ellipse(cr, 0, 128, 26, 34); fs(cr, hexc('#FF7F9A'), 6)
    mouth(cr, 105, talk, 50); blush(cr, 120, 50)

def panda(cr, t, talk=0, happy=False):
    K = hexc('#2A2638')
    for sx in (-1, 1): cr.arc(sx * 140, -150, 62, 0, 2 * math.pi); fs(cr, K)
    ellipse(cr, 0, 0, 200, 182); fs(cr, (1, 1, 1))
    for sx in (-1, 1):
        cr.save(); cr.translate(sx * 72, -25); cr.rotate(sx * -0.5); ellipse(cr, 0, 0, 50, 66); cr.set_source_rgb(*K); cr.fill(); cr.restore()
    for sx in (-1, 1):
        if happy: cr.arc(sx * 72, -18, 15, math.pi * 1.1, math.pi * 1.9); stroke_dev(cr, (1, 1, 1), 7)
        else:
            cr.arc(sx * 72, -25, 17, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()
            cr.arc(sx * 72, -23, 10, 0, 2 * math.pi); cr.set_source_rgb(*K); cr.fill()
            cr.arc(sx * 72 - 3, -27, 4, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()
    ellipse(cr, 0, 45, 32, 21); cr.set_source_rgb(*K); cr.fill()
    mouth(cr, 105, talk, 50); blush(cr, 125, 55)

ANIM = dict(monkey=monkey, puppy=puppy, panda=panda)


def obj_bone(cr, k=1):
    cr.save(); cr.rotate(-0.4)
    cr.new_path()
    for sx in (-1, 1):
        for sy in (-1, 1): cr.arc(sx * 110, sy * 32, 40, 0, 2 * math.pi); cr.new_sub_path()
    cr.rectangle(-110, -32, 220, 64)
    stroke_dev(cr, OUT, 14)
    for sx in (-1, 1):
        for sy in (-1, 1): cr.arc(sx * 110, sy * 32, 40, 0, 2 * math.pi); cr.new_sub_path()
    cr.rectangle(-110, -32, 220, 64); cr.set_source_rgb(*hexc('#FFF4DE')); cr.fill()
    cr.move_to(-70, -12); cr.line_to(60, -12); stroke_dev(cr, (1, 1, 1), 8)
    cr.restore()

def obj_bamboo(cr, k=1):
    cr.save(); cr.rotate(0.3)
    for x, h in ((-35, 300), (35, 260)):
        rrect(cr, x - 28, -h / 2, 56, h, 22); fs(cr, hexc('#7DD957'))
        for y in range(int(-h / 2) + 70, int(h / 2) - 20, 80):
            cr.move_to(x - 28, y); cr.line_to(x + 28, y); stroke_dev(cr, hexc('#3E9E3A'), 8)
    cr.save(); cr.translate(40, -140); cr.rotate(-0.6); ellipse(cr, 0, 0, 55, 20); fs(cr, hexc('#3ECF5E')); cr.restore()
    cr.save(); cr.translate(-80, -70); cr.rotate(0.5); ellipse(cr, 0, 0, 50, 18); fs(cr, hexc('#3ECF5E')); cr.restore()
    cr.restore()

FOODS = dict(banana=lambda cr: obj_banana(cr, 1), carrot=lambda cr: obj_carrot(cr, 1), apple=lambda cr: obj_apple(cr, 1),
             bone=obj_bone, bamboo=obj_bamboo)
FOOD_SC = dict(banana=0.55, carrot=0.55, apple=0.6, bone=0.62, bamboo=0.55)


def food(cr, kind, x, y, s, rot=0.0):
    if s <= 0.01: return
    cr.save(); cr.translate(x, y); cr.rotate(rot); cr.scale(s * FOOD_SC[kind], s * FOOD_SC[kind]); FOODS[kind](cr); cr.restore()

def card(cr, x, y, s, alpha=1.0, glow_a=0.0):
    if s <= 0.01: return
    cr.push_group(); cr.save(); cr.translate(x, y); cr.scale(s, s)
    if glow_a > 0: glow(cr, 0, 0, 220, (1, 0.9, 0.3), glow_a)
    rrect(cr, -135, -135, 270, 270, 40); fs(cr, (1, 1, 1))
    cr.restore(); cr.pop_group_to_source(); cr.paint_with_alpha(alpha)


def scene(cr, t):
    sky(cr, '#7FD6FF', '#E6F8FF', 1250)
    clouds(cr, t, ((760, 430, 0.45), (220, 600, 0.38)))
    hills(cr, 1150, '#9BE07A', 50)
    tree(cr, 70, 1190, 1.5, '#3ECF5E'); tree(cr, 1010, 1190, 1.35, '#2FB54E')
    ground(cr, 1230, '#7ACB5A', '#55A844')
    # picnic blanket
    cr.move_to(40, 1250); cr.line_to(1040, 1250); cr.line_to(1080, 1530); cr.line_to(0, 1530); cr.close_path()
    cr.save(); cr.clip()
    for i in range(12):
        for j in range(4):
            if (i + j) % 2: cr.rectangle(i * 95 - 20, 1250 + j * 72, 95, 72)
    cr.set_source_rgb(*hexc('#FF6B6B')); cr.fill()
    cr.rectangle(0, 1250, W, 290); cr.set_source_rgba(1, 1, 1, 0.0); cr.fill()
    cr.restore()


def big_bush(cr, t):
    bl = [(250, BUSH_Y, 95), (360, BUSH_Y - 35, 105), (480, BUSH_Y - 50, 110), (600, BUSH_Y - 50, 110), (720, BUSH_Y - 35, 105), (830, BUSH_Y, 95)]
    for bx, by, r in bl: cr.arc(bx, by, r, 0, 2 * math.pi); cr.new_sub_path()
    stroke_dev(cr, OUT, 12)
    for bx, by, r in bl: cr.arc(bx, by, r, 0, 2 * math.pi); cr.new_sub_path()
    cr.set_source_rgb(*hexc('#46A845')); cr.fill()
    for bx, by in ((300, 1180), (420, 1130), (560, 1120), (680, 1150), (790, 1185)):
        cr.arc(bx, by, 10, 0, 2 * math.pi); cr.set_source_rgba(1, 1, 1, 0.8); cr.fill()
    for bx, by in ((370, 1210), (640, 1200), (500, 1235)):
        cr.arc(bx, by, 13, 0, 2 * math.pi); fs(cr, hexc('#FF5FA2'), 4)


def frame(cr, t):
    m = TL['marks']
    te = 0.0 if t >= m['loop'] else t
    scene(cr, t)
    twist = te >= m['tw']
    ri = 0
    for i in range(3):
        if te >= m[f's{i}']: ri = i
    # animal
    if not twist:
        r = ROUNDS[ri]
        up = ease_out_back(clamp((te - m[f's{ri}']) / 0.55), 1.6) if ri else 1.0
        down = smooth(m[f'x{ri}'], m[f'x{ri}'] + 0.45, te)
        talk = 0; happy = te >= m[f'r{ri}']
        e0 = m[f'eat{ri}']
        if e0 <= te < e0 + 1.0: talk = abs(math.sin((te - e0) * 18))
        else:
            for ev in TL['events']:
                if ev['name'] == f'v{ri}' and ev['t'] <= te < ev['t'] + ev['dur']: talk = 0.5 + 0.5 * math.sin(te * 22)
        y = AY + (1 - up) * 700 + down * 700
        bob = 8 * math.sin(te * 2.6)
        sq = 1 + 0.05 * math.sin(te * 20) * (1 if e0 <= te < e0 + 1.0 else 0)
        cr.save(); cr.rectangle(0, 0, W, 1250); cr.clip()
        cr.save(); cr.translate(AX, y + bob); cr.scale(ASC * sq, ASC * (2 - sq)); ANIM[r['k']](cr, te, talk, happy); cr.restore()
        cr.restore()
        big_bush(cr, t)
        if te >= m[f'eat{ri}'] + 0.3:
            for k in range(3):
                u = (te - m[f'eat{ri}'] - 0.3 - k * 0.25)
                if 0 < u < 1.4:
                    hx = AX + (k - 1) * 170 + 20 * math.sin(u * 6); hy = AY - 300 - u * 160
                    star5(cr, hx, hy, 26 * (1 - u / 1.4) + 6); cr.set_source_rgba(1, 0.4, 0.6, 1 - u / 1.4); cr.fill()
        # cards
        app = smooth(m[f's{ri}'] + 0.1, m[f's{ri}'] + 0.6, te) if ri else 1.0
        for j, kind in enumerate(r['foods']):
            x = CARD_X[j]; correct = j == r['ans']
            rv = m[f'r{ri}']
            fade = smooth(rv, rv + 0.3, te) if not correct else 0
            out_ = smooth(m[f'x{ri}'], m[f'x{ri}'] + 0.3, te)
            cs = ease_out_back(clamp(app * 1.0 - j * 0.0)) * (1 - out_)
            gl = 0.7 * burst(rv, rv + 0.5, te) if correct else 0
            card(cr, x, CARD_Y, cs * (1 + 0.08 * gl), 1 - fade * 0.7, gl)
            fx, fy, fs_, rot = x, CARD_Y, cs, 0.08 * math.sin(te * 2 + j)
            if correct and te >= rv + 0.2:
                u = ease_io(clamp((te - rv - 0.2) / (m[f'eat{ri}'] - rv - 0.2)))
                fx = lerp(x, AX, u); fy = lerp(CARD_Y, AY + 110 * ASC, u) - 260 * math.sin(math.pi * u); fs_ = cs * (1 - 0.5 * u); rot = 2 * math.pi * u
                if te >= m[f'eat{ri}']: fs_ = 0
            if not correct: fs_ = fs_ * (1 - fade * 0.25)
            cr.push_group(); food(cr, kind, fx, fy, fs_, rot); cr.pop_group_to_source(); cr.paint_with_alpha(1 - fade * 0.6 if not correct else 1)
    else:
        # baby brother peeks out of the bush and gobbles the leftovers
        bu = ease_out_back(clamp((te - m['tw'] - 0.2) / 0.5), 1.5)
        fat = 1 + 0.15 * smooth(m['gulp'], m['gulp'] + 1.2, te) * (1 - 0.8 * smooth(m['burp'] + 0.3, m['burp'] + 0.9, te))
        bst = base_st(); bst.update(wing=[0.6 + 0.4 * math.sin(te * 9), 0.6 + 0.4 * math.sin(te * 9 + 1)], beak=0, happy=0)
        for ev in TL['events']:
            if ev['name'] == 'peep' and ev['t'] <= te < ev['t'] + ev['dur']: bst['beak'] = 0.5 + 0.5 * math.sin(te * 24)
        for j in range(3):
            tg = m['gulp'] + 0.1 + j * 0.38
            if tg - 0.15 <= te < tg + 0.06: bst['beak'] = 1.0
        if te >= m['burp']:
            bst['beak'] = 1.0 if te < m['burp'] + 0.7 else 0; bst['happy'] = 1 if te >= m['burp'] + 0.7 else 0
        shake = 6 * math.sin(te * 50) * burst(m['burp'], m['burp'] + 0.7, te)
        by = BABY_BY + (1 - bu) * 600
        cr.save(); cr.rectangle(0, 0, W, 1250); cr.clip()
        chick(cr, AX + shake, by, 0, BABY_SC, bst, te, (0.0, 0.3), fat, 1 / fat ** 0.3, acc=None)
        cr.restore()
        big_bush(cr, t)
        g0 = m['gulp']
        for j, kind in enumerate(LEFT):
            tg = g0 + 0.1 + j * 0.38
            x = CARD_X[j]; y = CARD_Y
            app = smooth(m['tw'], m['tw'] + 0.4, te)
            if te < tg - 0.32:
                food(cr, kind, x, y, ease_out_back(app), 0.08 * math.sin(te * 2 + j))
            elif te < tg:
                u = ease_io((te - tg + 0.32) / 0.32)
                food(cr, kind, lerp(x, BEAK[0], u), lerp(y, BEAK[1], u) - 220 * math.sin(math.pi * u), 1 - 0.75 * u, u * 6)
    # chickpea (bottom left)
    st = chick_talk(base_st(), te, TL); h = 0; sx = sy = 1; look = (0.5, -0.6)
    for i in range(3):
        if m[f'c{i}'] <= te < m[f'r{i}']: look = (math.sin(te * 2), -0.4)
        if m[f'r{i}'] + 0.3 <= te < m[f'r{i}'] + 1.2:
            h, sx, sy, air = hop_seq(te, m[f'r{i}'] + 0.3, 2, 0.45, 50); st.update(happy=1, wing=[0.3 + 0.8 * air] * 2)
    if twist:
        look = (0.6, -0.8)
        if m['burp'] <= te < m['burp'] + 0.9: st['mood'] = 0.0; st['wing'] = [1.0, 1.0]
    shadow_at(cr, 230, 1823, 95)
    chick(cr, 230, 1820, h, 0.66, st, te, look, sx, sy, acc='bow')
    for i in range(3):
        count_bubble(cr, m[f'c{i}'], te, "Say it!", y=470)
    names = ['Banana!', 'Bone!', 'Bamboo!']; cols = ['#FFB31F', '#8B5A3C', '#3ECF5E']
    for i in range(3): word_pop(cr, names[i], 540, 470, 140, cols[i], m[f'r{i}'] + 0.3, m[f'x{i}'] + 0.2, te)
    word_pop(cr, "Yum!", 540, 470, 150, '#FF5FA2', m['gulp'] + 0.2, m['burp'] - 0.35, te)
    word_pop(cr, "BURP!", 540, 600, 200, '#A15CFF', m['burp'], m['again'] + 0.3, te, 0.12)
    draw_text(cr, "Who Eats What?", 250, 120, t, -1)
    loop_fade(cr, TL, t)

if __name__ == '__main__': episode_main(build, F)
