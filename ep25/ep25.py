"""Zoom In! What Is It? — extreme close-ups in a magnifying glass: watermelon, frog, butterfly. Twist: it's Chickpea himself."""
import sys; sys.path.insert(0, '/home/claude/kit')
from common import *
from anim2 import obj_frog

F = '/home/claude/ep25'
LX, LY, LR = 540, 860, 390
ROUNDS = [dict(k='melon', q="Look closely! What is it?", a="It's a watermelon!", y="Yummy!", col='#FF4D6A', word='Watermelon!'),
          dict(k='frog', q="What could this be?", a="It's a frog!", y="Ribbit, ribbit!", col='#3ECF5E', word='Frog!'),
          dict(k='bfly', q="Hmm... what is it?", a="It's a butterfly!", y="So pretty!", col='#A15CFF', word='Butterfly!')]
# object, full-view scale, focus point (object coords), start zoom, lens bg
VIEW = dict(melon=(1.45, (60, 10), 5.0, '#DFF7D8'), frog=(1.6, (62, -64), 5.0, '#D8F1FF'),
            bfly=(4.2, (52, -26), 4.2, '#FFF1C9'), me=(1.35, (40, -238), 4.8, '#FFE2EE'))
CENTER = dict(melon=(0, 20), frog=(0, 30), bfly=(0, 0), me=(0, -190))


def build():
    s = Script(F); t = 0.1
    t = s.say(t, 'hook', "Zoom in! What is it?") + 0.05
    t = s.say(t, 'hmm', "Hmm...", 0.95, True) + 0.15
    for i, r in enumerate(ROUNDS):
        s.mark(f's{i}', t); t += 0.45
        t = s.say(t, f'q{i}', r['q']) + 0.05
        s.mark(f'c{i}', t); t += 3.0; s.mark(f'r{i}', t); t += 0.9
        t = s.say(t, f'a{i}', r['a']) + 0.05
        t = s.say(t, f'y{i}', r['y'], 1.0, True) + 0.3
        s.mark(f'x{i}', t); t += 0.5
    s.mark('s3', t); t += 0.45
    t = s.say(t, 'last', "Last one! What is it?") + 0.05
    s.mark('c3', t); t += 1.8
    s.mark('r3', t); t += 1.1
    t = s.say(t, 'me', "It's me!", 1.0, True) + 0.1
    t = s.say(t, 'hello', "Hello, Chickpea!") + 0.05
    t = s.say(t, 'hee', "Hee hee!", 1.0, True) + 0.25
    s.mark('again', t); t = s.say(t, 'again', "Again?", 1.0, True) + 0.25
    s.mark('loop', t); t += 0.9
    tl = s.save(t); m = tl['marks']; mx = Mix(tl['dur'])
    mx.music_loop(0, tl['dur'], 108, [([62, 65, 69], 38), ([60, 64, 67], 36), ([58, 62, 65], 34), ([60, 64, 67], 36)],
                  [[74, None, 77, None, 76, 74, None, 72], [74, None, None, 69, None, None, None, None]], 'soft', 0.75)
    for i in range(4):
        mx.add('sfx', m[f's{i}'], pop(300, 900, 0.12), 0.3)
        if i < 3: countdown_ticks(mx, m[f'c{i}'])
        else: mx.add('sfx', m['c3'], drumroll(1.7), 0.15)
        mx.add('sfx', m[f'r{i}'], slide_whistle(1200, 400, 0.9), 0.14)
        mx.add('sfx', m[f'r{i}'] + 0.9, ding(), 0.22); mx.add('sfx', m[f'r{i}'] + 1.0, chirp(), 0.12)
        if i < 3: mx.add('sfx', m[f'x{i}'], flick(), 0.2)
    mx.add('sfx', m['r3'] + 1.0, tada(72), 0.18)
    mx.add('sfx', m['again'] + 0.2, jingle(), 0.22)
    mx.voices(F, tl['events'])
    mx.write(F + '/audio.wav', quiet=[(m[f'c{i}'], m[f'r{i}']) for i in range(3)]); return tl


TL = json.load(open(F + '/timeline.json')) if os.path.exists(F + '/timeline.json') else None


def melon(cr, t):
    cr.save(); cr.translate(0, -70)
    cr.arc(0, 0, 215, 0, math.pi); cr.close_path(); fs(cr, hexc('#3EAF4A'))
    cr.arc(0, 0, 196, 0, math.pi); cr.close_path(); cr.set_source_rgb(*hexc('#C9F5B5')); cr.fill()
    cr.arc(0, 0, 178, 0, math.pi); cr.close_path(); cr.set_source_rgb(*hexc('#FF4D6A')); cr.fill()
    cr.move_to(-215, 0); cr.line_to(215, 0); stroke_dev(cr, OUT, 7)
    for x, y, a in ((-110, 45, 0.3), (-40, 95, 0.0), (40, 95, 0.0), (110, 45, -0.3), (0, 140, 0.0), (-75, 120, 0.2), (75, 120, -0.2), (60, 25, -0.1), (-120, 90, 0.4), (120, 90, -0.4)):
        cr.save(); cr.translate(x, y); cr.rotate(a)
        cr.move_to(0, -12); cr.curve_to(10, -2, 9, 12, 0, 13); cr.curve_to(-9, 12, -10, -2, 0, -12); cr.set_source_rgb(*OUT); cr.fill()
        cr.restore()
    cr.arc(-34, 48, 11, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill()
    cr.arc(34, 48, 11, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill()
    cr.arc(-37, 44, 4, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()
    cr.arc(31, 44, 4, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()
    cr.arc(0, 58, 18, 0.15 * math.pi, 0.85 * math.pi); stroke_dev(cr, OUT, 5)
    for sx in (-1, 1): ellipse(cr, sx * 62, 66, 14, 8); cr.set_source_rgba(1, 0.8, 0.85, 0.7); cr.fill()
    cr.restore()

def frog(cr, t): obj_frog(cr, 1)

def bfly(cr, t): draw_bfly(cr, 0, 0, t * 0.25, 0, 1.0)

def me(cr, t, st=None, look=(0, 0)):
    chick(cr, 0, 0, 0, 1.0, st or base_st(), t, look)

OBJ = dict(melon=melon, frog=frog, bfly=bfly, me=me)


def lens_content(cr, k, z, fx, fy, t, st=None, look=(0, 0)):
    sc, foc, z0, bg = VIEW[k]
    cr.save(); cr.arc(LX, LY, LR, 0, 2 * math.pi); cr.clip()
    cr.set_source_rgb(*hexc(bg)); cr.paint()
    for k2 in range(6):
        cr.arc(LX - 300 + k2 * 120, LY + 250 - (k2 % 2) * 520, 60, 0, 2 * math.pi); cr.set_source_rgba(1, 1, 1, 0.35); cr.fill()
    cr.translate(LX, LY); cr.scale(sc * z, sc * z); cr.translate(-fx, -fy)
    if k == 'me': me(cr, t, st, look)
    else: OBJ[k](cr, t)
    cr.restore()

def lens_frame(cr, t, wob=0.0):
    cr.save(); cr.translate(LX, LY); cr.rotate(wob)
    # handle
    cr.save(); cr.rotate(math.pi / 4)
    rrect(cr, LR + 10, -38, 90, 76, 20); fs(cr, hexc('#C9D2DD'))
    rrect(cr, LR + 95, -45, 330, 90, 45); fs(cr, hexc('#FF9A1F'))
    for k in range(4): cr.move_to(LR + 150 + k * 60, -40); cr.line_to(LR + 150 + k * 60, 40); stroke_dev(cr, hexc('#E07A0A'), 7)
    cr.restore()
    cr.arc(0, 0, LR + 20, 0, 2 * math.pi); cr.new_sub_path(); cr.arc_negative(0, 0, LR, 2 * math.pi, 0)
    cr.set_source_rgb(*hexc('#3FB4FF')); cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD); cr.fill(); cr.set_fill_rule(cairo.FILL_RULE_WINDING)
    cr.arc(0, 0, LR + 20, 0, 2 * math.pi); stroke_dev(cr, OUT, 9); cr.arc(0, 0, LR, 0, 2 * math.pi); stroke_dev(cr, OUT, 7)
    cr.arc(0, 0, LR - 40, math.pi * 1.1, math.pi * 1.45); stroke_dev(cr, (1, 1, 1), 16, 0.6)
    cr.restore()


def room(cr, t):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *hexc('#FFE9C7')); g.add_color_stop_rgb(1, *hexc('#FFD3E0'))
    cr.set_source(g); cr.paint()
    for k in range(30):
        x = (k * 173) % W; y = 330 + (k * 241) % 1200
        cr.arc(x, y, 6 + (k % 3) * 3, 0, 2 * math.pi); cr.set_source_rgba(1, 1, 1, 0.5); cr.fill()
    cr.rectangle(0, 1560, W, H - 1560); cr.set_source_rgb(*hexc('#B98CF0')); cr.fill()
    cr.move_to(0, 1560); cr.line_to(W, 1560); stroke_dev(cr, OUT, 6)


def frame(cr, t):
    m = TL['marks']
    te = 0.0 if t >= m['loop'] else t
    room(cr, t)
    ri = 0
    for i in range(4):
        if te >= m[f's{i}']: ri = i
    k = ROUNDS[ri]['k'] if ri < 3 else 'me'
    sc, foc, z0, bg = VIEW[k]; cen = CENTER[k]
    c0, rv = m[f'c{ri}'], m[f'r{ri}']
    hint = smooth(c0, rv, te)
    zs = z0 * (1 - 0.22 * hint)
    u = ease_io(clamp((te - rv) / 0.9))
    z = lerp(zs, 1.0, u) if te >= rv else zs
    # zoom-out interpolates the focus toward the centre in screen space
    fx = lerp(foc[0], cen[0], u if te >= rv else 0); fy = lerp(foc[1], cen[1], u if te >= rv else 0)
    pop_in = ease_out_back(clamp((te - m[f's{ri}']) / 0.4), 1.5)
    wipe = smooth(m[f'x{ri}'], m[f'x{ri}'] + 0.4, te) if ri < 3 else 0
    st_in = None; look_in = (0, 0)
    if k == 'me':
        st_in = base_st(); look_in = (-0.3, 0.2)
        if te >= rv + 1.0: st_in.update(happy=1, wing=[0.2, 0.6 + 0.5 * math.sin(te * 10)])
    tl_ = 0.1208 / 0.25 if (k == 'bfly' and te < rv + 0.9) else te
    lens_content(cr, k, z * (0.6 + 0.4 * pop_in) if te < rv else z, fx, fy, tl_, st_in, look_in)
    if wipe > 0:
        cr.save(); cr.arc(LX, LY, LR * wipe, 0, 2 * math.pi); cr.set_source_rgb(*hexc('#FFFFFF')); cr.fill(); cr.restore()
    if te >= rv + 0.9 and ri < 3: sparkles(cr, LX, LY, rv + 0.9, te, 9, 300, 430)
    wob = 0.03 * math.sin(te * 1.7)
    lens_frame(cr, t, wob)
    # chickpea, bottom left, with glasses
    st = chick_talk(base_st(), te, TL); h = 0; sx = sy = 1; look = (0.6, -0.8)
    for i in range(3):
        if m[f'c{i}'] <= te < m[f'r{i}']: look = (0.6 + 0.3 * math.sin(te * 2), -0.9)
        if m[f'r{i}'] + 0.9 <= te < m[f'r{i}'] + 1.8:
            h, sx, sy, air = hop_seq(te, m[f'r{i}'] + 0.9, 2, 0.45, 55); st.update(happy=1, wing=[0.3 + 0.8 * air] * 2)
    if ri == 3 and te >= m['r3'] + 0.3:
        look = (0.8, -0.6)
        if te >= m['r3'] + 1.0: st.update(happy=1, wing=[0.6 + 0.5 * math.sin(te * 10), 0.2])
    shadow_at(cr, 230, 1823, 110)
    chick(cr, 230, 1820, h, 0.8, st, te, look, sx, sy, acc='explorer')
    for i in range(3):
        count_bubble(cr, m[f'c{i}'], te, "Say it!", y=1400, w=440)
        word_pop(cr, ROUNDS[i]['word'], 540, 1400, 120, ROUNDS[i]['col'], m[f'r{i}'] + 0.9, m[f'x{i}'] + 0.2, te)
    word_pop(cr, "It's me!", 600, 1400, 130, '#FF9A1F', m['r3'] + 1.0, m['again'] + 0.3, te)
    if m['r3'] + 1.0 <= te: confetti(cr, m['r3'] + 1.0, te, 540, 420, 700)
    draw_text(cr, "Zoom In! What Is It?", 250, 105, t, -1)
    loop_fade(cr, TL, t)

if __name__ == '__main__': episode_main(build, F)
