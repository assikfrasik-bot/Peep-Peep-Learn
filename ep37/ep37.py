"""Find My Mommy! — baby duck, piglet and lamb look for their mommies. Twist: Chickpea finds his mommy hen. Big hug!"""
import sys; sys.path.insert(0, '/home/claude/kit')
from common import *
sys.path.insert(0, '/home/claude/ep13')
from ep13 import a_cow, a_duck, a_pig, a_sheep

F = '/home/claude/ep37'
MX = [215, 540, 865]
MY = 1180
BX, BY = 540, 1560
ROUNDS = [dict(k='duck', order=['pig', 'duck', 'cow'], ans=1, a="Mommy Duck!", y="Quack quack!", word='Duck!', col='#FF9A1F'),
          dict(k='pig', order=['sheep', 'cow', 'pig'], ans=2, a="Mommy Pig!", y="Oink oink!", word='Pig!', col='#FF7EB6'),
          dict(k='sheep', order=['sheep', 'duck', 'pig'], ans=0, a="Mommy Sheep!", y="Baa baa!", word='Sheep!', col='#7A8BCC')]
ANIM = dict(cow=a_cow, duck=a_duck, pig=a_pig, sheep=a_sheep)


def build():
    s = Script(F); t = 0.1
    s.mark('s0', 0.05)
    t = s.say(t, 'hook', "Oh no! The babies lost their mommies!") + 0.05
    for i, r in enumerate(ROUNDS):
        if i: s.mark(f's{i}', t); t += 0.6
        t = s.say(t, f'q{i}', f"Who is the baby {r['k']}'s mommy?") + 0.05
        s.mark(f'c{i}', t); t += 3.0; s.mark(f'r{i}', t)
        t = s.say(t + 0.4, f'a{i}', r['a']) + 0.05
        s.mark(f'hug{i}', t - 0.2)
        t = s.say(t + 0.2, f'y{i}', r['y'], 1.05, False, 'am_puck') + 0.3
        s.mark(f'x{i}', t); t += 0.5
    s.mark('tw', t); t += 0.3
    t = s.say(t, 'me', "Where's my mommy?", 0.95, True) + 0.2
    s.mark('hen', t); t += 0.6
    t = s.say(t, 'mommy', "Mommy!", 1.0, True) + 0.05
    s.mark('hug3', t); t += 0.3
    t = s.say(t, 'love', "Everybody found their mommy!") + 0.1
    t = s.say(t, 'hee', "Love you, Mommy!", 1.0, True) + 0.25
    s.mark('again', t); t = s.say(t, 'again', "Again?", 1.0, True) + 0.25
    s.mark('loop', t); t += 0.9
    tl = s.save(t); m = tl['marks']; mx = Mix(tl['dur'])
    mx.music_loop(0, tl['dur'], 98, [([60, 64, 67], 36), ([57, 60, 64], 45), ([65, 69, 72], 41), ([67, 71, 74], 43)],
                  [[76, None, 74, 72, None, 74, 76, None], [79, None, 77, None, 76, None, None, None]], 'soft', 0.78)
    for i in range(3):
        mx.add('sfx', m[f's{i}'] + 0.1, pop(300, 900, 0.12), 0.25)
        for k in range(3): mx.add('sfx', m[f's{i}'] + 0.4 + k * 0.12, pop(400, 1000, 0.1), 0.15)
        countdown_ticks(mx, m[f'c{i}'])
        mx.add('sfx', m[f'r{i}'], ding(), 0.2)
        for k in range(4): mx.add('sfx', m[f'r{i}'] + 0.3 + k * 0.15, pluck(mtof(72 + k * 2), 0.2), 0.15)
        mx.add('sfx', m[f'hug{i}'], chime_up(), 0.2)
        mx.add('sfx', m[f'x{i}'], flick(), 0.18)
    mx.add('sfx', m['hen'], kick(), 0.25); mx.add('sfx', m['hen'] + 0.3, chirp(), 0.15)
    mx.add('sfx', m['hug3'], chime_up(), 0.25); mx.add('sfx', m['hug3'] + 0.3, tada(72), 0.15)
    mx.add('sfx', m['again'] + 0.2, jingle(), 0.22)
    mx.voices(F, tl['events'])
    mx.write(F + '/audio.wav', quiet=[(m[f'c{i}'], m[f'r{i}']) for i in range(3)]); return tl


TL = json.load(open(F + '/timeline.json')) if os.path.exists(F + '/timeline.json') else None


def heart(cr, x, y, s, a=1.0, col='#FF5FA2'):
    if s <= 0.01 or a <= 0.01: return
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.move_to(0, 30); cr.curve_to(-60, -10, -40, -60, 0, -30); cr.curve_to(40, -60, 60, -10, 0, 30); cr.close_path()
    cr.set_source_rgba(*hexc(col), a); cr.fill_preserve(); stroke_dev(cr, OUT, 5, a)
    cr.restore()

def tear(cr, x, y, t):
    u = (t * 1.3) % 1
    cr.move_to(x, y + u * 40 - 12); cr.curve_to(x + 8, y + u * 40, x + 7, y + u * 40 + 10, x, y + u * 40 + 10)
    cr.curve_to(x - 7, y + u * 40 + 10, x - 8, y + u * 40, x, y + u * 40 - 12); cr.set_source_rgba(*hexc('#4FB3FF'), 1 - u); cr.fill()

def hen(cr, t, happy=True):
    W_ = hexc('#FFFFFF'); R = hexc('#FF5A5F')
    cr.move_to(-150, -120); cr.curve_to(-230, -230, -170, -280, -120, -210); cr.curve_to(-150, -300, -60, -300, -80, -190); cr.close_path(); fs(cr, W_)
    ellipse(cr, 0, -120, 170, 125); fs(cr, W_)
    for sx in (-1, 1):
        cr.save(); cr.translate(sx * 140, -120); cr.rotate(sx * (0.3 + 0.15 * math.sin(t * 6))); ellipse(cr, sx * 20, 0, 50, 85); fs(cr, hexc('#F2F2F7')); cr.restore()
    cr.arc(0, -300, 110, 0, 2 * math.pi); fs(cr, W_)
    for k in range(3): cr.arc(-30 + k * 30, -410 - (k == 1) * 15, 26, 0, 2 * math.pi); fs(cr, R, 5)
    for sx in (-1, 1):
        if happy: cr.arc(sx * 40, -305, 14, math.pi * 1.1, math.pi * 1.9); stroke_dev(cr, OUT, 6)
        else: cr.arc(sx * 40, -310, 13, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill()
        ellipse(cr, sx * 75, -270, 18, 11); cr.set_source_rgba(1, 0.45, 0.55, 0.5); cr.fill()
    cr.move_to(-22, -275); cr.line_to(22, -275); cr.line_to(0, -245); cr.close_path(); fs(cr, hexc('#FF9A1F'), 5)
    ellipse(cr, 0, -235, 16, 22); fs(cr, R, 4)
    for sx in (-1, 1): cr.move_to(sx * 50, 0); cr.line_to(sx * 50, 30); stroke_dev(cr, hexc('#FF9A1F'), 10)

def farm(cr, t):
    sky(cr, '#9FDCFF', '#F0FBFF', 1200)
    clouds(cr, t, ((780, 420, 0.42), (230, 560, 0.36)))
    small_sun(cr, t, 940, 580, 0.45)
    hills(cr, 1050, '#A6E58A', 50); ground(cr, 1110)
    for k in range(9):
        x = 40 + k * 125
        cr.rectangle(x - 10, 1050, 20, 110); fs(cr, hexc('#FFFFFF'), 5)
    cr.rectangle(0, 1080, W, 18); fs(cr, hexc('#FFFFFF'), 5)
    for k, (fx, fy) in enumerate(((120, 1700), (960, 1720), (300, 1830), (820, 1840))):
        draw_flower(cr, fx, fy, 1.0, hexc(['#FF5FA2', '#FFC93C', '#A15CFF', '#FF9A1F'][k]), t, k)

def animal(cr, k, x, y, s, t, happy=False, talk=0.0):
    if s <= 0.01: return
    cr.save(); cr.translate(x, y); cr.scale(s, s); ANIM[k](cr, t, talk, happy); cr.restore()


def frame(cr, t):
    m = TL['marks']
    te = 0.0 if t >= m['loop'] else t
    farm(cr, t)
    twist = te >= m['tw']
    ri = 0
    for i in range(3):
        if te >= m[f's{i}']: ri = i
    if not twist:
        r = ROUNDS[ri]; s0 = m[f's{ri}']; rv = m[f'r{ri}']; x0 = m[f'x{ri}']; hg = m[f'hug{ri}']
        out_ = smooth(x0, x0 + 0.35, te)
        talk = 0.0
        for ev in TL['events']:
            if ev['name'] == f'y{ri}' and ev['t'] <= te < ev['t'] + ev['dur']: talk = 0.5 + 0.5 * math.sin(te * 22)
        for j, k in enumerate(r['order']):
            a = ease_out_back(clamp((te - s0 - 0.3 - j * 0.12) / 0.4), 1.6) * (1 - out_)
            correct = j == r['ans']
            dim = smooth(rv, rv + 0.3, te) if not correct else 0
            if a <= 0.01: continue
            bob = 6 * math.sin(te * 2 + j)
            cr.push_group()
            if correct and te >= rv: glow(cr, MX[j], MY - 230, 300, (1, 0.85, 0.4), 0.6 * burst(rv, rv + 0.8, te))
            animal(cr, k, MX[j], MY + bob, 0.85 * a * (1 + 0.08 * burst(rv, rv + 0.5, te) * correct), te, correct and te >= hg, talk if correct else 0)
            cr.pop_group_to_source(); cr.paint_with_alpha(1 - 0.65 * dim)
        # the baby
        bp = ease_out_back(clamp((te - s0) / 0.45), 1.6) * (1 - out_)
        u = ease_io(clamp((te - rv - 0.2) / max(0.4, hg - rv - 0.2)))
        tx = MX[r['ans']] + (95 if r['ans'] < 2 else -95); ty = MY + 15
        x = lerp(BX, tx, u) ; y = lerp(BY, ty, u) - 120 * abs(math.sin(math.pi * u * 3)) * (u < 1)
        bs = lerp(0.55, 0.4, u) * bp
        animal(cr, r['k'], x, y, bs, te, te >= hg, 0)
        if te < rv and bp > 0.5:
            tear(cr, x - 40 * bs, y - 260 * bs, te); tear(cr, x + 40 * bs, y - 260 * bs, te + 0.4)
            cr.arc(x + 150, y - 280, 50, 0, 2 * math.pi); fs(cr, (1, 1, 1), 5)
            cr.arc(x + 95, y - 215, 14, 0, 2 * math.pi); fs(cr, (1, 1, 1), 4)
            big_word(cr, "?", x + 150, y - 277, 70, hexc('#A15CFF'), 1.0)
        if te >= hg:
            for k in range(5):
                uu = (te - hg - k * 0.2)
                if 0 < uu < 1.6:
                    heart(cr, MX[r['ans']] + (k - 2) * 60 + 20 * math.sin(uu * 5), MY - 400 - uu * 200, 0.7 + 0.2 * k % 2, 1 - uu / 1.6)
    else:
        hn = m['hen']; hg = m['hug3']
        # all three families together in the background
        for j, k in enumerate(('duck', 'pig', 'sheep')):
            a = ease_out_back(clamp((te - m['tw'] - j * 0.1) / 0.4), 1.6) * (1 - 0.0)
            animal(cr, k, MX[j], MY - 30, 0.5 * a, te, True)
            animal(cr, k, MX[j] + 75, MY, 0.25 * a, te, True)
        hu = ease_out_back(clamp((te - hn) / 0.6), 1.3)
        if hu > 0.01:
            hx = lerp(1300, 740, hu)
            cr.save(); cr.translate(hx, 1700); cr.scale(0.9, 0.9); hen(cr, te, te >= hg); cr.restore()
            if te >= hg:
                for sx in (-1, 1):
                    pass
        if te >= hg:
            for k in range(7):
                uu = (te - hg - k * 0.18) % 2.2
                heart(cr, 560 + (k - 3) * 70 + 30 * math.sin(uu * 4 + k), 1300 - uu * 300, 0.8, max(0, 1 - uu / 2.2))
    # chickpea
    st = chick_talk(base_st(), te, TL); h = 0; sx = sy = 1; look = (0.5, -0.7); cx = 170; cby = 1820
    for i in range(3):
        if m[f'c{i}'] <= te < m[f'r{i}']: look = (0.5 + 0.3 * math.sin(te * 2), -0.8)
        if m[f'hug{i}'] <= te < m[f'hug{i}'] + 0.9:
            h, sx, sy, air = hop_seq(te, m[f'hug{i}'], 2, 0.45, 50); st.update(happy=1, wing=[0.3 + 0.8 * air] * 2)
    if twist:
        hn, hg = m['hen'], m['hug3']
        u = ease_io(clamp((te - m['tw']) / 0.6)); cx = lerp(170, 420, u)
        if te < hn: st['mood'] = 0.0; look = (0.2, -0.3)
        if hn <= te < hg: look = (1.0, -0.6)
        if te >= hg:
            uu = ease_io(clamp((te - hg) / 0.4)); cx = lerp(420, 500, uu)
            st.update(happy=1, wing=[0.9, 0.9]); look = (1.0, -0.5)
    shadow_at(cr, cx, cby + 3, 100)
    chick(cr, cx, cby, h, 0.78, st, te, look, sx, sy)
    if twist and te < m['hen']:
        tear(cr, cx - 30, cby - 180, te); tear(cr, cx + 30, cby - 180, te + 0.4)
    for i, r in enumerate(ROUNDS):
        count_bubble(cr, m[f'c{i}'], te, "Say it!", y=470)
        word_pop(cr, r['a'], 540, 480, 110, r['col'], m[f'r{i}'] + 0.4, m[f'x{i}'] + 0.2, te)
    word_pop(cr, "Mommy!", 540, 480, 150, '#FF5FA2', m['hug3'], m['again'] + 0.3, te)
    draw_text(cr, "Find My Mommy!", 250, 120, t, -1)
    loop_fade(cr, TL, t)

if __name__ == '__main__': episode_main(build, F)
