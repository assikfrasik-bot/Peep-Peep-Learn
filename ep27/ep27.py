"""What's in the Box? — listen to the sound, guess the surprise: puppy, clock, bell. Twist: box in a box in a box... a butterfly!"""
import sys; sys.path.insert(0, '/home/claude/kit')
from common import *
sys.path.insert(0, '/home/claude/ep24')
from ep24 import puppy

F = '/home/claude/ep27'
BX, BY = 560, 1330          # box bottom centre
ROUNDS = [dict(k='puppy', box='#FF5A5F', rib='#FFC93C', hint='WOOF!', a="A puppy!", y="Hello, puppy!", col='#C9772E'),
          dict(k='clock', box='#2EA7FF', rib='#FF7EB6', hint='TICK TOCK', a="A clock!", y="Tick tock, tick tock!", col='#2EA7FF'),
          dict(k='bell', box='#3ECF5E', rib='#FF9A1F', hint='RING RING', a="A bell!", y="Ring-a-ling!", col='#FFB31F')]
NEST = [(460, 380, '#A15CFF', '#FFC93C'), (330, 270, '#FF9A1F', '#3FB4FF'), (220, 180, '#FF5FA2', '#FFFFFF')]


def build():
    s = Script(F); t = 0.1
    t = s.say(t, 'hook', "What's in the box? Listen!") + 0.05
    t = s.say(t, 'ooh', "Ooh, presents!", 1.0, True) + 0.15
    for i, r in enumerate(ROUNDS):
        s.mark(f's{i}', t); t += 0.6
        s.mark(f'snd{i}', t)
        if r['k'] == 'puppy': t = s.say(t, 'woof', "Woof! Woof!", 1.0, False, 'am_puck') + 0.2
        else: t += 1.4
        t = s.say(t, f'q{i}', "What's inside?") + 0.05
        s.mark(f'c{i}', t); t += 3.0; s.mark(f'r{i}', t)
        t = s.say(t + 0.55, f'a{i}', r['a']) + 0.05
        t = s.say(t, f'y{i}', r['y'], 1.0, True) + 0.3
        s.mark(f'x{i}', t); t += 0.55
    s.mark('tw', t); t += 0.5
    t = s.say(t, 'big', "And the big box?") + 0.15
    s.mark('o0', t); t += 0.7
    t = s.say(t, 'another', "Another box?") + 0.1
    s.mark('o1', t); t += 0.7
    t = s.say(t, 'and', "And another?!") + 0.1
    s.mark('o2', t); t += 0.9
    t = s.say(t, 'bfly', "A butterfly! Wheee!", 1.0, True) + 0.3
    s.mark('again', t); t = s.say(t, 'again', "Again?", 1.0, True) + 0.25
    s.mark('loop', t); t += 0.9
    tl = s.save(t); m = tl['marks']; mx = Mix(tl['dur'])
    mx.music_loop(0, tl['dur'], 112, [([60, 64, 67], 36), ([57, 60, 64], 45), ([65, 69, 72], 41), ([67, 71, 74], 43)],
                  [[76, None, 79, None, 81, 79, 76, None], [74, None, 72, None, None, None, None, None]], 'bouncy', 0.72)
    for i, r in enumerate(ROUNDS):
        mx.add('sfx', m[f's{i}'] + 0.35, kick(), 0.35)
        sn = m[f'snd{i}']
        if r['k'] == 'clock':
            for k in range(6): mx.add('sfx', sn + k * 0.22, tick(), 0.5)
        if r['k'] == 'bell':
            mx.add('sfx', sn, jingle(), 0.35); mx.add('sfx', sn + 0.6, bell(mtof(84), 0.8), 0.25)
        countdown_ticks(mx, m[f'c{i}'])
        mx.add('sfx', m[f'r{i}'], pop(300, 900, 0.12), 0.4); mx.add('sfx', m[f'r{i}'] + 0.15, slide_whistle(500, 1200, 0.4), 0.12)
        mx.add('sfx', m[f'r{i}'] + 0.5, ding(), 0.22)
        mx.add('sfx', m[f'x{i}'], whoosh(0.4), 0.1)
    mx.add('sfx', m['tw'] + 0.3, kick(), 0.4)
    for k in range(3): mx.add('sfx', m[f'o{k}'], pop(300, 900 + k * 200, 0.12), 0.4)
    mx.add('sfx', m['o2'] + 0.2, chime_up(), 0.25); mx.add('sfx', m['o2'] + 0.4, tada(72), 0.15)
    mx.add('sfx', m['again'] + 0.2, jingle(), 0.22)
    mx.voices(F, tl['events'])
    mx.write(F + '/audio.wav', quiet=[(m[f'c{i}'], m[f'r{i}']) for i in range(3)]); return tl


TL = json.load(open(F + '/timeline.json')) if os.path.exists(F + '/timeline.json') else None


def bow(cr, x, y, s, col):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    for sx in (-1, 1):
        cr.save(); cr.scale(sx, 1)
        cr.move_to(0, 0); cr.curve_to(40, -70, 110, -60, 95, -10); cr.curve_to(85, 20, 30, 15, 0, 0); cr.close_path(); fs(cr, hexc(col))
        cr.move_to(5, 5); cr.curve_to(30, 30, 50, 60, 60, 80); stroke_dev(cr, OUT, 20); cr.move_to(5, 5); cr.curve_to(30, 30, 50, 60, 60, 80); stroke_dev(cr, hexc(col), 11)
        cr.restore()
    cr.arc(0, -2, 22, 0, 2 * math.pi); fs(cr, hexc(col)); cr.restore()

def box_body(cr, x, yb, w, h, col, rib):
    rrect(cr, x - w / 2, yb - h, w, h, 18); fs(cr, hexc(col))
    cr.save(); rrect(cr, x - w / 2, yb - h, w, h, 18); cr.clip()
    cr.rectangle(x - w / 2, yb - h, w * 0.25, h); cr.set_source_rgba(1, 1, 1, 0.12); cr.fill()
    cr.restore()
    cr.rectangle(x - w * 0.08, yb - h, w * 0.16, h); fs(cr, hexc(rib), 6)
    for k in range(5):
        cr.arc(x - w * 0.33 + (k % 2) * w * 0.55, yb - h * (0.25 + 0.15 * k), 8 * w / 400, 0, 2 * math.pi); cr.set_source_rgba(1, 1, 1, 0.7); cr.fill()

def box_lid(cr, x, yt, w, col, rib, dx=0, dy=0, rot=0):
    cr.save(); cr.translate(x + dx, yt + dy); cr.rotate(rot)
    lw_ = w * 1.1; lh = max(50, w * 0.17)
    rrect(cr, -lw_ / 2, -lh, lw_, lh, 14); fs(cr, hexc(col))
    cr.rectangle(-w * 0.08, -lh, w * 0.16, lh); fs(cr, hexc(rib), 6)
    bow(cr, 0, -lh, w / 420, rib)
    cr.restore()

def clock(cr, t, happy=False):
    for sx in (-1, 1):
        cr.save(); cr.translate(sx * 105, -125); cr.rotate(sx * 0.5 + 0.15 * math.sin(t * 30) * (1 if not happy else 0.3))
        cr.arc(0, 0, 50, math.pi, 2 * math.pi); cr.close_path(); fs(cr, hexc('#FFC93C')); cr.restore()
        cr.move_to(sx * 95, 120); cr.line_to(sx * 125, 175); stroke_dev(cr, OUT, 16)
    cr.arc(0, 0, 160, 0, 2 * math.pi); fs(cr, hexc('#FF5A5F'))
    cr.arc(0, 0, 128, 0, 2 * math.pi); fs(cr, (1, 1, 1), 6)
    for k in range(12):
        a = k * math.pi / 6; cr.arc(105 * math.cos(a), 105 * math.sin(a), 6 if k % 3 else 10, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill()
    for ang, l, w in ((t * 6, 85, 8), (t * 0.6, 60, 11)):
        cr.move_to(0, 0); cr.line_to(l * math.sin(ang), -l * math.cos(ang)); stroke_dev(cr, OUT, w)
    for sx in (-1, 1):
        if happy: cr.arc(sx * 45, 40, 13, math.pi * 1.1, math.pi * 1.9); stroke_dev(cr, OUT, 6)
        else: cr.arc(sx * 45, 40, 12, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill()
        ellipse(cr, sx * 75, 65, 16, 10); cr.set_source_rgba(1, 0.45, 0.55, 0.5); cr.fill()
    cr.arc(0, 62, 18, 0.15 * math.pi, 0.85 * math.pi); stroke_dev(cr, OUT, 5)
    cr.arc(0, 0, 12, 0, 2 * math.pi); fs(cr, hexc('#FFC93C'), 5)

def bellx(cr, t, happy=False):
    cr.save(); cr.translate(0, -150); cr.rotate(0.25 * math.sin(t * 7)); cr.translate(0, 150)
    cr.arc(0, 140, 34, 0, 2 * math.pi); fs(cr, hexc('#C98A1F'))
    cr.move_to(-170, 120); cr.curve_to(-120, 90, -110, -60, -100, -80); cr.curve_to(-80, -180, 80, -180, 100, -80)
    cr.curve_to(110, -60, 120, 90, 170, 120); cr.close_path(); fs(cr, hexc('#FFC93C'))
    rrect(cr, -180, 100, 360, 40, 20); fs(cr, hexc('#FFB31F'))
    ellipse(cr, -50, -60, 18, 50); cr.set_source_rgba(1, 1, 1, 0.5); cr.fill()
    for sx in (-1, 1):
        if happy: cr.arc(sx * 40, 0, 13, math.pi * 1.1, math.pi * 1.9); stroke_dev(cr, OUT, 6)
        else: cr.arc(sx * 40, 0, 12, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill()
        ellipse(cr, sx * 70, 30, 16, 10); cr.set_source_rgba(1, 0.45, 0.55, 0.5); cr.fill()
    cr.arc(0, 25, 18, 0.15 * math.pi, 0.85 * math.pi); stroke_dev(cr, OUT, 5)
    bow(cr, 0, -165, 0.8, '#FF5A5F')
    cr.restore()

def item(cr, k, t, happy):
    if k == 'puppy': puppy(cr, t, 0, happy)
    elif k == 'clock': clock(cr, t, happy)
    else: bellx(cr, t, happy)

def room(cr, t):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *hexc('#CDEBFF')); g.add_color_stop_rgb(1, *hexc('#FFE3F0'))
    cr.set_source(g); cr.paint()
    for k in range(9):
        x = 60 + k * 120; y = 380 + 40 * math.sin(k * 1.3)
        cr.move_to(x - 120, y - 30); cr.curve_to(x - 60, y + 20, x, y + 20, x + 60, y - 30)
    stroke_dev(cr, hexc('#9AA7B8'), 3)
    for k in range(9):
        x = 60 + k * 120; y = 395 + 40 * math.sin(k * 1.3)
        cr.move_to(x - 25, y - 10); cr.line_to(x + 25, y - 10); cr.line_to(x, y + 40); cr.close_path(); fs(cr, hexc(CONF_COLS[k % 7]), 4)
    cr.rectangle(0, 1340, W, H - 1340); cr.set_source_rgb(*hexc('#F7C77A')); cr.fill()
    for k in range(10): cr.move_to(0, 1380 + k * 60); cr.line_to(W, 1380 + k * 60); stroke_dev(cr, hexc('#E8AE5C'), 4)
    cr.move_to(0, 1340); cr.line_to(W, 1340); stroke_dev(cr, OUT, 6)

def sound_waves(cr, x, y, t0, t1, t, side=1):
    if not (t0 <= t < t1): return
    for k in range(3):
        u = ((t - t0) * 1.5 + k / 3) % 1
        cr.arc(x, y, 60 + 120 * u, -0.6, 0.6) if side > 0 else cr.arc_negative(x, y, 60 + 120 * u, math.pi + 0.6, math.pi - 0.6)
        stroke_dev(cr, OUT, 9, 1 - u)


def frame(cr, t):
    m = TL['marks']
    te = 0.0 if t >= m['loop'] else t
    room(cr, t)
    twist = te >= m['tw']
    ri = 0
    for i in range(3):
        if te >= m[f's{i}']: ri = i
    shadow_at(cr, BX, BY + 5, 260)
    if not twist:
        r = ROUNDS[ri]; s0 = m[f's{ri}']; rv = m[f'r{ri}']; x0 = m[f'x{ri}']
        drop = clamp((te - s0) / 0.4)
        yoff = -1500 * (1 - drop) ** 2
        bnc = burst(s0 + 0.35, s0 + 0.7, te)
        sx_ = 1 + 0.12 * bnc; sy_ = 1 - 0.12 * bnc
        sn = m[f'snd{ri}']
        shake = 0
        if sn <= te < sn + 1.4: shake = math.sin(te * 40) * 0.05
        if m[f'c{ri}'] <= te < rv: shake = math.sin(te * 25) * 0.02
        slide = 1300 * smooth(x0, x0 + 0.5, te) ** 2
        w, h = 400, 330
        cr.save(); cr.translate(BX + slide, BY + yoff); cr.rotate(shake); cr.scale(sx_, sy_); cr.translate(-BX, -BY)
        # item (behind the box front)
        if te >= rv:
            u = ease_out_back(clamp((te - rv - 0.1) / 0.6), 1.5)
            iy = BY - h + 250 - 470 * u
            cr.save(); cr.rectangle(0, 0, W, BY - h + 5 if u < 0.9 else BY); cr.clip()
            cr.save(); cr.translate(BX, iy); cr.scale(0.82, 0.82); item(cr, r['k'], te, te > rv + 0.6); cr.restore()
            cr.restore()
        box_body(cr, BX, BY, w, h, r['box'], r['rib'])
        if te < rv:
            box_lid(cr, BX, BY - h, w, r['box'], r['rib'], 0, -10 * abs(math.sin(te * 30)) * (1 if sn <= te < sn + 1.4 else 0))
        else:
            u = clamp((te - rv) / 0.9)
            box_lid(cr, BX, BY - h, w, r['box'], r['rib'], 350 * u, -700 * u + 900 * u * u, 2.5 * u)
        cr.restore()
        sound_waves(cr, BX + 260, BY - 200, sn, sn + 1.4, te, 1); sound_waves(cr, BX - 260, BY - 200, sn, sn + 1.4, te, -1)
        word_pop(cr, r['hint'], 540, 640, 120, r['col'], sn, sn + 1.6, te, 0.08)
        if te >= rv + 0.6: sparkles(cr, BX, BY - 650, rv + 0.6, te, 8, 220, 340)
    else:
        tw = m['tw']; drop = clamp((te - tw) / 0.45); yoff = -1000 * (1 - drop) ** 2
        bnc = burst(tw + 0.4, tw + 0.8, te)
        cr.save(); cr.translate(BX, BY + yoff); cr.scale(1 + 0.12 * bnc, 1 - 0.12 * bnc); cr.translate(-BX, -BY)
        opened = [te >= m[f'o{k}'] for k in range(3)]
        if opened[2]:
            u = clamp((te - m['o2']) / 2.5)
            bx = BX + 260 * math.sin(u * 7) * u; by = BY - 150 - 560 * ease_io(min(1, u * 1.6)) + 40 * math.sin(te * 3)
            draw_bfly(cr, bx, by, te, 0.2 * math.sin(te * 2), 1.0 + 1.6 * ease_out_back(clamp(u * 3)))
        for k in range(3):
            w, h, col, rib = NEST[k]
            if k > 0 and not opened[k - 1]: continue
            if k < 2 and te >= m[f'o{k}'] + 0.7: continue
            yb = BY; sc_ = 1.0
            if k > 0:
                u = clamp((te - m[f'o{k - 1}']) / 0.6)
                ph, _ = NEST[k - 1][1], 0
                yb = BY - (ph + 250) * math.sin(math.pi * u) * (1 - u * 0.2) if u < 1 else BY
                sc_ = 0.6 + 0.4 * min(1, u * 1.5)
            gone = smooth(m[f'o{k}'] + 0.25, m[f'o{k}'] + 0.65, te) if k < 2 else 0
            ss_ = max(0.001, sc_ * (1 - gone))
            cr.save(); cr.translate(BX, yb); cr.scale(ss_, ss_); cr.translate(-BX, -yb)
            if ss_ > 0.01:
                box_body(cr, BX, yb, w, h, col, rib)
                if not opened[k]:
                    box_lid(cr, BX, yb - h, w, col, rib, 0, -8 * abs(math.sin(te * 28)) * burst(m[f'o{k}'] - 0.6, m[f'o{k}'], te))
            cr.restore()
            if opened[k] and te < m[f'o{k}'] + 1.2:
                u = clamp((te - m[f'o{k}']) / 0.9)
                box_lid(cr, BX, BY - h, w, col, rib, (-1) ** k * 330 * u, -650 * u + 850 * u * u, (-1) ** k * 2.4 * u)
        cr.restore()
        if te >= m['o2'] + 0.3: confetti(cr, m['o2'] + 0.3, te, 540, 700, 600)
    # chickpea
    st = chick_talk(base_st(), te, TL); h = 0; sx = sy = 1; look = (0.8, -0.3)
    for i in range(3):
        sn = m[f'snd{i}']
        if sn <= te < sn + 1.4: look = (0.9, -0.5); st['wing'] = [0.0, 0.9]
        if m[f'r{i}'] + 0.55 <= te < m[f'r{i}'] + 1.5:
            h, sx, sy, air = hop_seq(te, m[f'r{i}'] + 0.55, 2, 0.45, 55); st.update(happy=1, wing=[0.3 + 0.8 * air] * 2)
    if twist and te >= m['o2']: st.update(happy=1, wing=[0.8 + 0.4 * math.sin(te * 9)] * 2); look = (0.6, -1.0)
    shadow_at(cr, 190, 1823, 105)
    chick(cr, 190, 1820, h, 0.78, st, te, look, sx, sy, acc='crown')
    for i in range(3):
        count_bubble(cr, m[f'c{i}'], te, "Say it!", y=640, w=440)
        word_pop(cr, ROUNDS[i]['a'].replace('A ', '').title(), 540, 560, 130, ROUNDS[i]['col'], m[f'r{i}'] + 0.55, m[f'x{i}'] + 0.2, te)
    word_pop(cr, "Butterfly!", 600, 1480, 130, '#A15CFF', m['o2'] + 0.6, m['again'] + 0.3, te)
    draw_text(cr, "What's in the Box?", 250, 115, t, -1)
    loop_fade(cr, TL, t)

if __name__ == '__main__': episode_main(build, F)
