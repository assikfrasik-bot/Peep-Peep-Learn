"""Where Do I Live? — bird→nest, bee→hive, fish→bowl. Twist: where does Chickpea live? In his shell! Night night."""
import sys; sys.path.insert(0, '/home/claude/kit')
from common import *
from anim3 import item_fish

F = '/home/claude/ep35'
HX = [215, 540, 865]
HY = 1370
AX, AY = 540, 760
ROUNDS = [dict(k='bird', order=['hive', 'nest', 'bowl'], ans=1, q="Where does the bird live?", a="In a nest!", y="Tweet tweet!", word='Nest!', col='#C9772E'),
          dict(k='bee', order=['bowl', 'nest', 'hive'], ans=2, q="Where does the bee live?", a="In a beehive!", y="Buzz, buzz!", word='Beehive!', col='#FFB31F'),
          dict(k='fish', order=['bowl', 'hive', 'nest'], ans=0, q="Where does the fish live?", a="In the water!", y="Splash!", word='Water!', col='#2EA7FF')]


def build():
    s = Script(F); t = 0.1
    s.mark('s0', 0.05)
    t = s.say(t, 'hook', "Everybody needs a home!") + 0.05
    for i, r in enumerate(ROUNDS):
        if i: s.mark(f's{i}', t); t += 0.6
        t = s.say(t, f'q{i}', r['q']) + 0.05
        s.mark(f'c{i}', t); t += 3.0; s.mark(f'r{i}', t)
        t = s.say(t + 0.5, f'a{i}', r['a']) + 0.05
        s.mark(f'home{i}', t - 0.2)
        t = s.say(t, f'y{i}', r['y'], 1.0, True) + 0.3
        s.mark(f'x{i}', t); t += 0.5
    s.mark('tw', t); t += 0.3
    t = s.say(t, 'q3', "And where does Chickpea live?") + 0.1
    s.mark('shell', t); t += 0.3
    t = s.say(t, 'me', "In my shell! It's cozy!", 1.0, True) + 0.1
    s.mark('lid', t); t += 0.6
    t = s.say(t, 'night', "Night night! Hee hee!", 1.0, True) + 0.25
    s.mark('again', t); t = s.say(t, 'again', "Again?", 1.0, True) + 0.25
    s.mark('loop', t); t += 0.9
    tl = s.save(t); m = tl['marks']; mx = Mix(tl['dur'])
    mx.music_loop(0, tl['dur'], 106, [([60, 64, 67], 36), ([57, 60, 64], 45), ([62, 65, 69], 38), ([67, 71, 74], 43)],
                  [[72, None, 76, 74, None, 72, 74, None], [76, None, 77, None, 76, None, None, None]], 'soft', 0.75)
    for i, r in enumerate(ROUNDS):
        mx.add('sfx', m[f's{i}'] + 0.05, chirp() if r['k'] == 'bird' else pop(300, 900, 0.12), 0.25)
        countdown_ticks(mx, m[f'c{i}'])
        mx.add('sfx', m[f'r{i}'], whoosh(0.5), 0.12); mx.add('sfx', m[f'r{i}'] + 0.4, ding(), 0.2)
        if r['k'] == 'fish': mx.add('sfx', m[f'home{i}'], splash_snd(0.6), 0.45)
        else: mx.add('sfx', m[f'home{i}'], chime_up(), 0.18)
        if r['k'] == 'bird':
            for k in range(3): mx.add('sfx', m[f'home{i}'] + 0.3 + k * 0.25, chirp(), 0.15)
        mx.add('sfx', m[f'x{i}'], flick(), 0.2)
    mx.add('sfx', m['shell'], boing(), 0.25)
    mx.add('sfx', m['lid'], pop(600, 200, 0.12), 0.35); mx.add('sfx', m['lid'] + 0.3, bell(mtof(84), 1.0), 0.12)
    mx.add('sfx', m['again'] + 0.2, jingle(), 0.22)
    mx.voices(F, tl['events'])
    mx.write(F + '/audio.wav', quiet=[(m[f'c{i}'], m[f'r{i}']) for i in range(3)]); return tl


TL = json.load(open(F + '/timeline.json')) if os.path.exists(F + '/timeline.json') else None


def bird(cr, t, fly=1.0, happy=False):
    B = hexc('#4FB3FF')
    fl = math.sin(t * 16) * fly
    for sx in (-1, 1):
        cr.save(); cr.translate(sx * 70, -10); cr.rotate(sx * (0.3 + 0.6 * fl)); ellipse(cr, sx * 55, 0, 65, 32); fs(cr, hexc('#2E8BD9')); cr.restore()
    cr.arc(0, 0, 95, 0, 2 * math.pi); fs(cr, B)
    ellipse(cr, 0, 35, 60, 45); cr.set_source_rgb(*hexc('#CFEFFF')); cr.fill()
    for sx in (-1, 1):
        if happy: cr.arc(sx * 35, -25, 12, math.pi * 1.1, math.pi * 1.9); stroke_dev(cr, OUT, 6)
        else: cr.arc(sx * 35, -25, 12, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill(); cr.arc(sx * 35 - 4, -29, 4, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()
        ellipse(cr, sx * 60, 5, 14, 8); cr.set_source_rgba(1, 0.45, 0.55, 0.5); cr.fill()
    cr.move_to(-18, 0); cr.line_to(18, 0); cr.line_to(0, 22); cr.close_path(); fs(cr, hexc('#FF9A1F'), 5)
    for k in range(3): cr.move_to(-10 + k * 10, -92); cr.line_to(-14 + k * 14, -125); stroke_dev(cr, OUT, 5)

def bee(cr, t, fly=1.0, happy=False):
    fl = abs(math.sin(t * 30)) * fly
    for sx in (-1, 1):
        cr.save(); cr.translate(sx * 30, -60); cr.rotate(sx * (0.5 + 0.3 * fl)); ellipse(cr, sx * 30, -30, 38, 55 * (0.6 + 0.4 * fl)); fs(cr, hexc('#E8F7FF'), 5); cr.restore()
    ellipse(cr, 0, 0, 105, 80); body = cr.copy_path(); fs(cr, hexc('#FFC93C'))
    cr.save(); cr.append_path(body); cr.clip()
    for x in (-30, 25, 80): cr.rectangle(x, -90, 26, 180); cr.set_source_rgb(*OUT); cr.fill()
    cr.restore(); cr.append_path(body); stroke_dev(cr, OUT, 7)
    cr.move_to(-105, 0); cr.line_to(-140, -6); cr.line_to(-105, 12); cr.close_path(); fs(cr, OUT, 4)
    cr.arc(80, -10, 55, 0, 2 * math.pi); fs(cr, hexc('#FFC93C'))
    for sx in (-1, 1):
        cr.move_to(80 + sx * 18, -60); cr.curve_to(80 + sx * 25, -90, 80 + sx * 40, -100, 80 + sx * 45, -95); stroke_dev(cr, OUT, 5)
        cr.arc(80 + sx * 45, -97, 8, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill()
    for sx in (-1, 1):
        if happy: cr.arc(80 + sx * 20, -15, 9, math.pi * 1.1, math.pi * 1.9); stroke_dev(cr, OUT, 5)
        else: cr.arc(80 + sx * 20, -15, 9, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill()
    cr.arc(80, 2, 13, 0.15 * math.pi, 0.85 * math.pi); stroke_dev(cr, OUT, 5)
    ellipse(cr, 112, 5, 11, 7); cr.set_source_rgba(1, 0.45, 0.55, 0.6); cr.fill()

def fish(cr, t, fly=1.0, happy=False):
    cr.save(); cr.scale(0.9, 0.9); item_fish(cr, t); cr.restore()

ANIMAL = dict(bird=bird, bee=bee, fish=fish)


def h_nest(cr, t, filled=0.0):
    cr.move_to(-150, -40); cr.curve_to(-140, 70, 140, 70, 150, -40); cr.close_path(); fs(cr, hexc('#C9965A'))
    for k in range(9):
        cr.move_to(-140 + k * 33, -30 + (k % 2) * 12); cr.curve_to(-120 + k * 33, 10, -100 + k * 33, -10, -90 + k * 33, 30); stroke_dev(cr, hexc('#9B6B43'), 6)
    for x, y in ((-50, -50), (10, -58), (60, -48)):
        if filled < 0.5: egg_tiny(cr, x, y)
    ellipse(cr, 0, -40, 152, 26); stroke_dev(cr, OUT, 7)

def egg_tiny(cr, x, y):
    ellipse(cr, x, y, 24, 30); fs(cr, hexc('#BFE8FF'), 5)

def h_hive(cr, t, filled=0.0):
    cr.move_to(0, -170); cr.line_to(0, -200); stroke_dev(cr, hexc('#9B6B43'), 10)
    for k in range(5):
        w = 70 + k * 22 if k < 4 else 120; y = -165 + k * 42
        rrect(cr, -w, y, 2 * w, 46, 23); fs(cr, hexc('#FFC93C' if k % 2 else '#FFB31F'))
    ellipse(cr, 0, 10, 30, 32); cr.set_source_rgb(*hexc('#5A3A1A')); cr.fill()
    for x, y in ((-60, -110), (55, -40)): cr.arc(x, y, 9, 0, 2 * math.pi); cr.set_source_rgba(1, 1, 1, 0.5); cr.fill()

def h_bowl(cr, t, filled=0.0):
    cr.save(); cr.arc(0, -40, 125, 0, 2 * math.pi); cr.clip()
    cr.rectangle(-130, -90 + 6 * math.sin(t * 2), 260, 200); cr.set_source_rgb(*hexc('#7FD3FF')); cr.fill()
    for k in range(3): cr.arc(-40 + k * 40, 20 - ((t * 0.7 + k * 0.33) % 1) * 100, 8, 0, 2 * math.pi); stroke_dev(cr, (1, 1, 1), 4, 0.8)
    for x in (-70, 60):
        cr.move_to(x, 85); cr.curve_to(x - 20, 40, x + 20, 20, x, -10); stroke_dev(cr, hexc('#3ECF5E'), 10)
    cr.restore()
    cr.arc(0, -40, 125, 0, 2 * math.pi); stroke_dev(cr, OUT, 7)
    ellipse(cr, 0, -150, 75, 16); fs(cr, hexc('#E8F7FF'), 6)
    cr.arc(0, -40, 105, math.pi * 1.15, math.pi * 1.45); stroke_dev(cr, (1, 1, 1), 10, 0.7)
    rrect(cr, -80, 78, 160, 26, 12); fs(cr, hexc('#C9965A'))

HOME = dict(nest=h_nest, hive=h_hive, bowl=h_bowl)


def scene(cr, t):
    sky(cr, '#8EDBFF', '#EEFBFF', 1300)
    clouds(cr, t, ((790, 430, 0.45), (210, 520, 0.36)))
    small_sun(cr, t, 930, 600, 0.45)
    hills(cr, 1200, '#A6E58A', 55); ground(cr, 1290)
    for x in (60, 1030): tree(cr, x, 1290, 1.1, '#3ECF5E')


def frame(cr, t):
    m = TL['marks']
    te = 0.0 if t >= m['loop'] else t
    scene(cr, t)
    twist = te >= m['tw']
    ri = 0
    for i in range(3):
        if te >= m[f's{i}']: ri = i
    if not twist:
        r = ROUNDS[ri]; s0 = m[f's{ri}']; rv = m[f'r{ri}']; x0 = m[f'x{ri}']; hm = m[f'home{ri}']
        out_ = smooth(x0, x0 + 0.35, te)
        for j, hk in enumerate(r['order']):
            a = ease_out_back(clamp((te - s0 - 0.2 - j * 0.12) / 0.4), 1.6) * (1 - out_)
            correct = j == r['ans']
            if a <= 0.01: continue
            dim = smooth(rv, rv + 0.3, te) if not correct else 0
            cr.push_group(); cr.save(); cr.translate(HX[j], HY); cr.scale(a * 1.2, a * 1.2)
            if correct and rv <= te: glow(cr, 0, -40, 240, (1, 0.9, 0.3), 0.7 * burst(rv, rv + 0.8, te))
            HOME[hk](cr, te, 1.0 if (correct and te >= hm) else 0.0); cr.restore()
            cr.pop_group_to_source(); cr.paint_with_alpha(1 - 0.6 * dim)
        # the animal
        pin = ease_out_back(clamp((te - s0) / 0.45), 1.6)
        hx = HX[r['ans']]
        u = ease_io(clamp((te - rv - 0.2) / max(0.4, hm - rv - 0.2)))
        dest = {'bird': (hx, HY - 115), 'bee': (hx, HY + 12), 'fish': (hx, HY - 48)}[r['k']]
        x = lerp(AX + 40 * math.sin(te * 1.7), dest[0], u); y = lerp(AY + 25 * math.sin(te * 2.3), dest[1], u) - 220 * math.sin(math.pi * u)
        sc = pin * lerp(1.3, {'bird': 0.9, 'bee': 0.4, 'fish': 0.65}[r['k']], u) * (1 - out_)
        if r['k'] == 'bee' and te >= hm: sc *= 1 - smooth(hm, hm + 0.3, te)
        if r['k'] == 'fish' and te >= hm:
            x = hx + 60 * math.sin(te * 2); y = HY - 36 + 10 * math.sin(te * 3)
        if sc > 0.01:
            if r['k'] == 'fish' and te >= hm:
                cr.save(); cr.arc(hx, HY - 48, 144, 0, 2 * math.pi); cr.clip()
                cr.save(); cr.translate(x, y); cr.scale(sc * (1 if math.cos(te * 2) > 0 else -1), sc); fish(cr, te); cr.restore(); cr.restore()
            else:
                cr.save(); cr.translate(x, y); cr.scale(sc, sc); ANIMAL[r['k']](cr, te, 1.0 if te < hm else 0.2, te >= hm); cr.restore()
        if r['k'] == 'bee' and te >= hm + 0.2:
            for k in range(3):
                uu = ((te - hm) * 0.8 + k / 3) % 1
                big_word(cr, "z", hx + 70 + 50 * uu, HY - 190 - 100 * uu, 36, hexc('#FFB31F'), 1.0, 0, 1 - uu)
        if te >= hm + 0.1: sparkles(cr, hx, HY - 60, hm + 0.1, te, 8, 130, 220)
        if not (rv <= te) and pin > 0.5:
            # thought bubble with a question mark
            cr.arc(AX + 190, AY - 150, 55, 0, 2 * math.pi); fs(cr, (1, 1, 1), 6)
            cr.arc(AX + 130, AY - 80, 16, 0, 2 * math.pi); fs(cr, (1, 1, 1), 5)
            big_word(cr, "?", AX + 190, AY - 147, 80, hexc('#A15CFF'), 1.0)
    else:
        tw = m['tw']; sh = m['shell']; ld = m['lid']
        # all three friends at home
        for j, (hk, ak, asc) in enumerate((('nest', 'bird', 0.75), ('hive', None, 0), ('bowl', 'fish', 0.55))):
            a = ease_out_back(clamp((te - tw - j * 0.1) / 0.4), 1.6) * (1 - smooth(sh, sh + 0.4, te))
            if a <= 0.01: continue
            cr.save(); cr.translate(HX[j], HY); cr.scale(a, a); HOME[hk](cr, te, 1.0); cr.restore()
            if ak == 'bird': cr.save(); cr.translate(HX[j], HY - 95); cr.scale(0.75 * a, 0.75 * a); bird(cr, te, 0.2, True); cr.restore()
            if ak == 'fish':
                cr.save(); cr.arc(HX[j], HY - 40, 120, 0, 2 * math.pi); cr.clip(); cr.translate(HX[j] + 40 * math.sin(te * 2), HY - 30); cr.scale(0.55 * a, 0.55 * a); fish(cr, te); cr.restore()
    # chickpea
    st = chick_talk(base_st(), te, TL); h = 0; sx = sy = 1; look = (0.4, -0.7)
    cx, cby, csc = 180, 1820, 0.75
    for i in range(3):
        if m[f'c{i}'] <= te < m[f'r{i}']: look = (0.5 + 0.3 * math.sin(te * 2), -0.6)
        if m[f'home{i}'] + 0.2 <= te < m[f'home{i}'] + 1.1:
            h, sx, sy, air = hop_seq(te, m[f'home{i}'] + 0.2, 2, 0.45, 50); st.update(happy=1, wing=[0.3 + 0.8 * air] * 2)
    lid = None
    if twist:
        u = ease_io(clamp((te - m['shell']) / 0.6)); cx = lerp(180, 540, u); csc = lerp(0.75, 1.15, u); cby = lerp(1820, 1800, u)
        if m['shell'] <= te < m['shell'] + 0.6: h = 200 * math.sin(math.pi * u)
        look = (0, 0.2)
        ld = m['lid']
        if te >= ld:
            lu = clamp((te - ld) / 0.5)
            lid = lu
            st['happy'] = 1
    shadow_at(cr, cx, cby + 3, 110 * csc / 0.75)
    chick(cr, cx, cby, h, csc, st, te, look, sx, sy, acc=None)
    if lid is not None:
        # the top half of the shell comes down like a lid
        y_top = cby - csc * 600 + ease_out_back(lid, 1.3) * csc * 395
        cr.save(); cr.translate(cx, y_top); cr.scale(csc, csc)
        cr.move_to(-150, 60); cr.curve_to(-150, -90, -80, -150, 0, -150); cr.curve_to(80, -150, 150, -90, 150, 60)
        for k in range(6): cr.line_to(150 - (k + 0.5) * 50, 60 + (25 if k % 2 == 0 else -5))
        cr.close_path(); fs(cr, hexc('#FFF6E0'))
        cr.arc(-40, -60, 12, 0, 2 * math.pi); cr.set_source_rgba(1, 0.85, 0.5, 0.6); cr.fill()
        cr.restore()
        if te >= m['lid'] + 0.6:
            for k in range(3):
                uu = ((te - m['lid']) * 0.6 + k / 3) % 1
                big_word(cr, "z", cx + 140 + 60 * uu, cby - 520 - 140 * uu, 50 + 30 * uu, hexc('#7A8BFF'), 1.0, 0.2, 1 - uu)
    for i, r in enumerate(ROUNDS):
        count_bubble(cr, m[f'c{i}'], te, "Say it!", y=470)
        word_pop(cr, r['word'], 540, 480, 130, r['col'], m[f'r{i}'] + 0.5, m[f'x{i}'] + 0.2, te)
    word_pop(cr, "Night night!", 540, 480, 120, '#7A8BFF', m['lid'] + 0.4, m['again'] + 0.3, te)
    draw_text(cr, "Where Do I Live?", 250, 120, t, -1)
    loop_fade(cr, TL, t)

if __name__ == '__main__': episode_main(build, F)
