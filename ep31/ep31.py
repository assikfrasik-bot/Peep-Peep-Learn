"""What Starts With...? — letter sounds B, F, S with three picture cards. Twist: C is for... Chickpea!"""
import sys; sys.path.insert(0, '/home/claude/kit')
from common import *
from anim2 import obj_banana, obj_apple, obj_frog
from anim3 import item_fish

F = '/home/claude/ep31'
CARD_X = [215, 540, 865]
CARD_Y = 1180
ROUNDS = [dict(L='B', snd="Buh, buh, buh!", items=['apple', 'banana', 'frog'], ans=1, a="Banana! B, banana!", col='#FFB31F'),
          dict(L='F', snd="Fff, fff, fff!", items=['sun', 'apple', 'fish'], ans=2, a="Fish! F, fish!", col='#FF7A1A'),
          dict(L='S', snd="Sss, sss, sss!", items=['sun', 'frog', 'banana'], ans=0, a="Sun! S, sun!", col='#FFC93C')]
LCOL = dict(B='#2EA7FF', F='#3ECF5E', S='#FF5FA2', C='#A15CFF')
WORDS = dict(banana='anana', fish='ish', sun='un')


def build():
    s = Script(F); t = 0.1
    s.mark('s0', 0.05)
    t = s.say(t, 'hook', "What starts with B?") + 0.05
    t = s.say(t, 'snd0', ROUNDS[0]['snd'], 0.95) + 0.1
    s.mark('c0', t); t += 3.0; s.mark('r0', t)
    t = s.say(t + 0.5, 'a0', ROUNDS[0]['a']) + 0.05
    t = s.say(t, 'y0', "Yummy!", 1.0, True) + 0.3
    s.mark('x0', t); t += 0.5
    for i in (1, 2):
        r = ROUNDS[i]
        s.mark(f's{i}', t); t += 0.6
        t = s.say(t, f'q{i}', f"What starts with {r['L']}?") + 0.05
        t = s.say(t, f'snd{i}', r['snd'], 0.95) + 0.1
        s.mark(f'c{i}', t); t += 3.0; s.mark(f'r{i}', t)
        t = s.say(t + 0.5, f'a{i}', r['a']) + 0.05
        t = s.say(t, f'y{i}', "Yay!" if i == 1 else "Hello, sunshine!", 1.0, True) + 0.3
        s.mark(f'x{i}', t); t += 0.5
    s.mark('s3', t); t += 0.6
    t = s.say(t, 'q3', "And what starts with C?") + 0.05
    t = s.say(t, 'snd3', "Cuh, cuh, cuh...", 0.95) + 0.2
    s.mark('r3', t); t += 0.8
    t = s.say(t, 'me', "Chickpea! That's me!", 1.0, True) + 0.1
    t = s.say(t, 'c4', "C is for Chickpea!") + 0.25
    s.mark('again', t); t = s.say(t, 'again', "Again?", 1.0, True) + 0.25
    s.mark('loop', t); t += 0.9
    tl = s.save(t); m = tl['marks']; mx = Mix(tl['dur'])
    mx.music_loop(0, tl['dur'], 114, [([60, 64, 67], 36), ([65, 69, 72], 41), ([60, 64, 67], 36), ([67, 71, 74], 43)],
                  [[72, None, 72, None, 79, None, 79, None], [81, None, 81, None, 79, None, None, None]], 'bouncy', 0.72)
    for i in range(4):
        mx.add('sfx', m[f's{i}'] + 0.05, boing(), 0.2)
        for k in range(3): mx.add('sfx', m[f's{i}'] + 0.35 + k * 0.12, pop(300, 900 + k * 150, 0.1), 0.2)
        if i < 3:
            countdown_ticks(mx, m[f'c{i}'])
            mx.add('sfx', m[f'r{i}'], whoosh(0.4), 0.12); mx.add('sfx', m[f'r{i}'] + 0.4, ding(), 0.22); mx.add('sfx', m[f'r{i}'] + 0.5, chirp(), 0.12)
            mx.add('sfx', m[f'x{i}'], flick(), 0.2)
    mx.add('sfx', m['r3'] - 1.0, drumroll(1.0), 0.15)
    mx.add('sfx', m['r3'], pop(300, 900, 0.12), 0.4); mx.add('sfx', m['r3'] + 0.2, tada(72), 0.18)
    mx.add('sfx', m['again'] + 0.2, jingle(), 0.22)
    mx.voices(F, tl['events'])
    mx.write(F + '/audio.wav', quiet=[(m[f'c{i}'], m[f'r{i}']) for i in range(3)]); return tl


TL = json.load(open(F + '/timeline.json')) if os.path.exists(F + '/timeline.json') else None


def sun(cr, t):
    cr.save(); cr.rotate(t * 0.4)
    for k in range(10):
        a = k * math.pi / 5
        cr.save(); cr.rotate(a); cr.move_to(-22, -105); cr.line_to(0, -150); cr.line_to(22, -105); cr.close_path(); fs(cr, hexc('#FF9A1F'), 5); cr.restore()
    cr.restore()
    cr.arc(0, 0, 100, 0, 2 * math.pi); fs(cr, hexc('#FFD93B'))
    for sx in (-1, 1): cr.arc(sx * 35, -15, 11, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill(); ellipse(cr, sx * 60, 18, 16, 10); cr.set_source_rgba(1, 0.45, 0.55, 0.5); cr.fill()
    cr.arc(0, 12, 28, 0.15 * math.pi, 0.85 * math.pi); stroke_dev(cr, OUT, 6)

ITEMS = dict(banana=(lambda cr, t: obj_banana(cr, 1), 0.8, (0, 30)), apple=(lambda cr, t: obj_apple(cr, 1), 0.78, (0, 20)),
             frog=(lambda cr, t: obj_frog(cr, 1), 0.85, (0, -10)), fish=(item_fish, 0.78, (20, 0)), sun=(sun, 0.9, (0, 0)))


def card(cr, x, y, s, kind, t, glow_a=0.0, dim=0.0, bob=0.0):
    if s <= 0.01: return
    cr.push_group()
    cr.save(); cr.translate(x, y + bob); cr.scale(s, s)
    if glow_a > 0: glow(cr, 0, 0, 230, (1, 0.9, 0.3), glow_a)
    rrect(cr, -145, -165, 290, 330, 40); fs(cr, (1, 1, 1))
    if kind:
        fn, sc, (ox, oy) = ITEMS[kind]
        cr.save(); cr.translate(ox * sc, oy * sc); cr.scale(sc, sc); fn(cr, t); cr.restore()
    cr.restore()
    cr.pop_group_to_source(); cr.paint_with_alpha(1 - 0.6 * dim)

def letter_tile(cr, L, x, y, s, t, rot=0.0):
    if s <= 0.01: return
    cr.save(); cr.translate(x, y); cr.rotate(rot); cr.scale(s, s)
    rrect(cr, -150, -150, 300, 300, 50); fs(cr, hexc(LCOL[L]))
    rrect(cr, -128, -132, 256, 70, 30); cr.set_source_rgba(1, 1, 1, 0.25); cr.fill()
    cr.restore()
    big_word(cr, L, x, y + 10 * s, 230 * s, (1, 1, 1), 1.0, rot)

def classroom(cr, t):
    cr.set_source_rgb(*hexc('#FFF4D6')); cr.paint()
    for k in range(0, W, 90): cr.rectangle(k, 300, 45, 1500); cr.set_source_rgba(1, 0.85, 0.6, 0.25); cr.fill()
    # alphabet bunting
    for k, L in enumerate("ABCDEFGHI"):
        x = 60 + k * 120; y = 380 + 18 * math.sin(k * 0.9)
        cr.move_to(x - 45, y - 25); cr.line_to(x + 45, y - 25); cr.line_to(x, y + 55); cr.close_path(); fs(cr, hexc(CONF_COLS[k % 7]), 4)
        big_word(cr, L, x, y, 36, (1, 1, 1), 1.0)
    cr.rectangle(0, 1420, W, H - 1420); cr.set_source_rgb(*hexc('#9ED79A')); cr.fill()
    cr.move_to(0, 1420); cr.line_to(W, 1420); stroke_dev(cr, OUT, 6)
    for k in range(6): rrect(cr, 60 + k * 170, 1470 + (k % 2) * 40, 90, 22, 10); cr.set_source_rgba(1, 1, 1, 0.35); cr.fill()


def frame(cr, t):
    m = TL['marks']
    te = 0.0 if t >= m['loop'] else t
    classroom(cr, t)
    ri = 0
    for i in range(4):
        if te >= m[f's{i}']: ri = i
    s0 = m[f's{ri}']; rv = m[f'r{ri}']
    x0 = m[f'x{ri}'] if ri < 3 else 1e9
    out_ = smooth(x0, x0 + 0.35, te)
    L = ROUNDS[ri]['L'] if ri < 3 else 'C'
    items = ROUNDS[ri]['items'] if ri < 3 else ['apple', 'fish', None]
    ans = ROUNDS[ri]['ans'] if ri < 3 else 2
    # letter tile (bounces on its sound)
    ls = ease_out_back(clamp((te - s0) / 0.45), 1.7) * (1 - out_)
    snd = None
    for ev in TL['events']:
        if ev['name'] == f'snd{ri}': snd = ev
    bounce = 0
    if snd and snd['t'] <= te < snd['t'] + snd['dur']: bounce = abs(math.sin((te - snd['t']) * 7.5)) * 50
    lx, ly = 540, 700 - bounce
    lsc = ls
    if te >= rv + 0.1 and ri < 3:
        u = ease_io(clamp((te - rv - 0.1) / 0.5))
        lx = lerp(540, CARD_X[ans] - 95, u); ly = lerp(700, CARD_Y - 175, u); lsc = ls * lerp(1, 0.38, u)
    if ri == 3 and te >= rv:
        u = ease_io(clamp((te - rv) / 0.5)); lx = lerp(540, CARD_X[2] - 95, u); ly = lerp(700, CARD_Y - 175, u); lsc = ls * lerp(1, 0.38, u)
    # cards
    for j, kind in enumerate(items):
        a = ease_out_back(clamp((te - s0 - 0.3 - j * 0.12) / 0.4), 1.6) * (1 - out_)
        correct = j == ans
        gl = 0.8 * burst(rv + 0.3, rv + 1.0, te) if correct else 0
        dim = smooth(rv, rv + 0.3, te) if not correct else 0
        pop_ = 1 + 0.1 * burst(rv + 0.4, rv + 0.8, te) if correct else 1
        bob = 6 * math.sin(te * 2 + j)
        if kind is None:
            card(cr, CARD_X[j], CARD_Y, a * pop_, None, te, gl, 0, bob)
            if te < rv:
                big_word(cr, "?", CARD_X[j], CARD_Y + bob, 200 * a, hexc('#A15CFF'), 1.0, 0.1 * math.sin(te * 3))
            else:
                st = base_st(); st.update(happy=1, wing=[0.2, 0.6 + 0.5 * math.sin(te * 10)])
                up = ease_out_back(clamp((te - rv) / 0.5), 1.8)
                cr.save(); cr.rectangle(CARD_X[j] - 140, CARD_Y - 160, 280, 320); cr.clip()
                chick(cr, CARD_X[j], CARD_Y + 150 + (1 - up) * 300, 0, 0.62, st, te, (0, 0.2))
                cr.restore()
        else:
            card(cr, CARD_X[j], CARD_Y, a * pop_, kind, te, gl, dim, bob)
    if te >= rv + 0.4: sparkles(cr, CARD_X[ans], CARD_Y, rv + 0.4, te, 8, 170, 260)
    letter_tile(cr, L, lx, ly, lsc, te, 0.05 * math.sin(te * 2.3))
    # word under the cards: big letter + rest
    if ri < 3:
        word = items[ans]
        wa = smooth(rv + 0.5, rv + 0.8, te) * (1 - out_)
        if wa > 0:
            big_word(cr, word.capitalize(), 540, 1500, 130, hexc(ROUNDS[ri]['col']), wa)
    else:
        if te >= rv + 0.6: big_word(cr, "Chickpea!", 540, 1500, 120, hexc('#A15CFF'), ease_out_back(clamp((te - rv - 0.6) / 0.4), 1.6))
        if te >= rv + 0.3: confetti(cr, rv + 0.3, te, 540, 900, 650)
    # chickpea teacher
    st = chick_talk(base_st(), te, TL); h = 0; sx = sy = 1; look = (0.8, -0.6)
    for i in range(3):
        if m[f'c{i}'] <= te < m[f'r{i}']: look = (0.6 + 0.3 * math.sin(te * 2), -0.7)
        if m[f'r{i}'] + 0.5 <= te < m[f'r{i}'] + 1.4:
            h, sx, sy, air = hop_seq(te, m[f'r{i}'] + 0.5, 2, 0.45, 50); st.update(happy=1, wing=[0.3 + 0.8 * air] * 2)
    if ri == 3 and te >= rv: look = (1.0, -0.8); st.update(happy=1, wing=[0.6 + 0.4 * math.sin(te * 9)] * 2)
    shadow_at(cr, 160, 1823, 95)
    chick(cr, 160, 1820, h, 0.68, st, te, look, sx, sy)
    for i in range(3): count_bubble(cr, m[f'c{i}'], te, "Say it!", y=1500, w=440)
    draw_text(cr, "What Starts With...?", 250, 105, t, -1)
    loop_fade(cr, TL, t)

if __name__ == '__main__': episode_main(build, F)
