"""Clean Up Time! — muddy pig needs soap, yucky hippo teeth need a toothbrush, wet puppy needs a towel. Twist: clean Chickpea jumps in a mud puddle!"""
import sys; sys.path.insert(0, '/home/claude/kit')
from common import *
sys.path.insert(0, '/home/claude/ep13'); sys.path.insert(0, '/home/claude/ep24')
from ep13 import a_pig
from ep24 import puppy

F = '/home/claude/ep34'
AX, AY = 540, 820
CARD_X = [215, 540, 865]
CARD_Y = 1330
ROUNDS = [dict(k='pig', q="The piggy is muddy! What does he need?", items=['towel', 'soap', 'brush'], ans=1, a="Soap! Scrub, scrub!", y="Bubbles!", word='Soap!', col='#FF7EB6'),
          dict(k='hippo', q="Hippo's teeth are yucky! What does he need?", items=['brush', 'towel', 'soap'], ans=0, a="A toothbrush! Brush, brush!", y="Sparkly teeth!", word='Toothbrush!', col='#2EA7FF'),
          dict(k='puppy', q="The puppy is all wet! What does he need?", items=['soap', 'brush', 'towel'], ans=2, a="A towel! Rub, rub!", y="All dry!", word='Towel!', col='#FF9A1F')]


def build():
    s = Script(F); t = 0.1
    s.mark('s0', 0.05)
    t = s.say(t, 'hook', "Clean up time!", 1.0) + 0.05
    for i, r in enumerate(ROUNDS):
        if i: s.mark(f's{i}', t); t += 0.6
        t = s.say(t, f'q{i}', r['q']) + 0.05
        s.mark(f'c{i}', t); t += 3.0; s.mark(f'r{i}', t)
        t = s.say(t + 0.4, f'a{i}', r['a']) + 0.05
        s.mark(f'clean{i}', t - 0.9)
        t = s.say(t + 0.5, f'y{i}', r['y'], 1.0, True) + 0.3
        s.mark(f'x{i}', t); t += 0.5
    s.mark('tw', t); t += 0.4
    t = s.say(t, 'all', "Everyone is clean! Yay!") + 0.1
    t = s.say(t, 'puddle', "Ooh, a puddle!", 1.0, True) + 0.1
    s.mark('jump', t); t += 0.7
    s.mark('splat', t); t += 0.6
    t = s.say(t, 'oh', "Oh no, Chickpea!") + 0.05
    t = s.say(t, 'hee', "Hee hee! Clean up time again!", 1.0, True) + 0.25
    s.mark('again', t); t = s.say(t, 'again', "Again?", 1.0, True) + 0.25
    s.mark('loop', t); t += 0.9
    tl = s.save(t); m = tl['marks']; mx = Mix(tl['dur'])
    mx.music_loop(0, tl['dur'], 112, [([60, 64, 67], 36), ([65, 69, 72], 41), ([62, 65, 69], 38), ([67, 71, 74], 43)],
                  [[76, None, 74, None, 72, None, 74, 76], [77, None, 76, None, 74, None, None, None]], 'bouncy', 0.72)
    for i, r in enumerate(ROUNDS):
        mx.add('sfx', m[f's{i}'] + 0.1, pop(300, 900, 0.12), 0.3)
        countdown_ticks(mx, m[f'c{i}'])
        mx.add('sfx', m[f'r{i}'], pop(300, 900, 0.12), 0.35); mx.add('sfx', m[f'r{i}'] + 0.1, ding(), 0.2)
        cl = m[f'clean{i}']
        if r['k'] == 'pig': mx.add('sfx', cl, bubbles_snd(8, 1.4), 0.35)
        else:
            for k in range(6): mx.add('sfx', cl + k * 0.2, shaker(), 0.4)
        mx.add('sfx', cl + 1.3, chime_up(), 0.2)
        mx.add('sfx', m[f'x{i}'], flick(), 0.2)
    mx.add('sfx', m['tw'] + 0.2, tada(72), 0.12)
    mx.add('sfx', m['jump'], slide_whistle(500, 1200, 0.35), 0.15); mx.add('sfx', m['jump'] + 0.35, slide_whistle(1200, 400, 0.35), 0.15)
    mx.add('sfx', m['splat'], splash_snd(0.8), 0.7); mx.add('sfx', m['splat'], kick(), 0.4)
    mx.add('sfx', m['again'] + 0.2, jingle(), 0.22)
    mx.voices(F, tl['events'])
    mx.write(F + '/audio.wav', quiet=[(m[f'c{i}'], m[f'r{i}']) for i in range(3)]); return tl


TL = json.load(open(F + '/timeline.json')) if os.path.exists(F + '/timeline.json') else None
MUD = hexc('#8B5A2B')


def hippo(cr, t, clean=0.0, talk=0.0):
    P = hexc('#B9A6E8'); Pd = hexc('#9C86D6')
    for sx in (-1, 1):
        cr.arc(sx * 120, -230, 40, 0, 2 * math.pi); fs(cr, P); cr.arc(sx * 120, -230, 20, 0, 2 * math.pi); cr.set_source_rgb(*hexc('#FFB3C8')); cr.fill()
    ellipse(cr, 0, -120, 175, 135); fs(cr, P)
    for sx in (-1, 1): cr.arc(sx * 60, -175, 16, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill(); cr.arc(sx * 60 - 5, -180, 5, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()
    # open mouth
    ellipse(cr, 0, 40, 210, 140); fs(cr, Pd)
    ellipse(cr, 0, 50, 165, 95); fs(cr, hexc('#7A2B3A'), 6)
    ellipse(cr, 0, 95, 90, 35); cr.set_source_rgb(*hexc('#FF7F9A')); cr.fill()
    tc = mixc(hexc('#B8C94A'), (1, 1, 1), clean)
    for sx in (-1, 1):
        for k in range(2):
            x = sx * (45 + k * 55); rrect(cr, x - 22, -45 + k * 8, 44, 55, 12); fs(cr, tc, 5)
            rrect(cr, x - 20, 85 - k * 10, 40, 45, 12); fs(cr, tc, 5)
    if clean < 0.5:
        for x, y in ((-70, -10), (60, 0), (-10, 110), (100, 100)):
            cr.arc(x, y, 9, 0, 2 * math.pi); cr.set_source_rgba(0.45, 0.6, 0.1, 1 - 2 * clean); cr.fill()
    for sx in (-1, 1): ellipse(cr, sx * 30, -60, 13, 9); cr.set_source_rgb(*hexc('#7A62B8')); cr.fill()
    for sx in (-1, 1): ellipse(cr, sx * 120, -110, 22, 13); cr.set_source_rgba(1, 0.45, 0.55, 0.5); cr.fill()
    if clean > 0.5:
        for x, y in ((-90, -20), (90, 70), (10, -40)):
            star5(cr, x, y, 18 * (clean - 0.5) * 2); cr.set_source_rgb(1, 1, 1); cr.fill()

def mud_spots(cr, a, spots):
    if a <= 0.01: return
    for x, y, r in spots:
        cr.arc(x, y, r, 0, 2 * math.pi); cr.set_source_rgba(*MUD, a); cr.fill()
        cr.arc(x + r * 0.6, y + r * 0.9, r * 0.35, 0, 2 * math.pi); cr.set_source_rgba(*MUD, a); cr.fill()

PIG_MUD = [(-90, -260, 30), (70, -300, 22), (-40, -60, 40), (90, -100, 34), (30, -200, 18), (-120, -130, 24)]
PUP_MUD = []


def item(cr, kind, t):
    if kind == 'soap':
        rrect(cr, -95, -60, 190, 120, 40); fs(cr, hexc('#FF9EC7'))
        rrect(cr, -70, -40, 140, 30, 15); cr.set_source_rgba(1, 1, 1, 0.4); cr.fill()
        for x, y, r in ((60, -80, 26), (95, -110, 16), (20, -100, 14)):
            cr.arc(x, y, r, 0, 2 * math.pi); fs(cr, hexc('#E8F7FF'), 5)
    elif kind == 'brush':
        cr.save(); cr.rotate(-0.6)
        rrect(cr, -140, -18, 200, 36, 18); fs(cr, hexc('#3FB4FF'))
        rrect(cr, 50, -26, 90, 52, 14); fs(cr, hexc('#FFFFFF'))
        for k in range(5): cr.move_to(60 + k * 17, -26); cr.line_to(60 + k * 17, -60); stroke_dev(cr, hexc('#9AD7FF'), 9)
        rrect(cr, 52, -68, 86, 26, 12); fs(cr, hexc('#E8F7FF'), 5)
        cr.restore()
    elif kind == 'towel':
        cr.save(); cr.rotate(0.1)
        rrect(cr, -110, -90, 220, 180, 26); fs(cr, hexc('#FFC93C'))
        for y in (-50, 50): cr.rectangle(-110, y - 10, 220, 20); cr.set_source_rgb(*hexc('#FF9A1F')); cr.fill()
        rrect(cr, -110, -90, 220, 180, 26); stroke_dev(cr, OUT, 7)
        for x in range(-100, 110, 22): cr.move_to(x, 90); cr.line_to(x, 110); stroke_dev(cr, hexc('#FF9A1F'), 6)
        cr.restore()

def card(cr, x, y, s, kind, t, glow_a=0.0, dim=0.0):
    if s <= 0.01: return
    cr.push_group(); cr.save(); cr.translate(x, y); cr.scale(s, s)
    if glow_a > 0: glow(cr, 0, 0, 220, (1, 0.9, 0.3), glow_a)
    rrect(cr, -135, -135, 270, 270, 40); fs(cr, (1, 1, 1))
    cr.scale(0.85, 0.85)
    if kind: item(cr, kind, t)
    cr.restore(); cr.pop_group_to_source(); cr.paint_with_alpha(1 - 0.6 * dim)

def bathroom(cr, t):
    cr.set_source_rgb(*hexc('#DDF3FF')); cr.paint()
    for y in range(300, 1200, 90):
        for x in range(0, W, 90):
            rrect(cr, x + 4, y + 4, 82, 82, 10); cr.set_source_rgb(*hexc('#C6EAFF' if ((x + y) // 90) % 2 else '#E9F7FF')); cr.fill()
    cr.rectangle(0, 1180, W, H - 1180); cr.set_source_rgb(*hexc('#FFE3B8')); cr.fill()
    cr.move_to(0, 1180); cr.line_to(W, 1180); stroke_dev(cr, OUT, 6)
    for k in range(6): cr.move_to(k * 200, 1180); cr.line_to(k * 200 - 120, H); stroke_dev(cr, hexc('#F2C98F'), 4)
    # bath mat
    ellipse(cr, 540, 1150, 330, 60); fs(cr, hexc('#9FE0B0'))

def bubbles_fx(cr, x, y, t0, t1, t):
    if not (t0 <= t < t1 + 0.6): return
    a = 1 - smooth(t1, t1 + 0.6, t)
    for k in range(16):
        ang = k * 2.4; rr = 140 + 60 * math.sin(k * 1.7)
        bx = x + rr * math.cos(ang) + 20 * math.sin(t * 3 + k); by = y + rr * 0.9 * math.sin(ang) - 30 * ((t - t0) * 0.5 + k / 16) % 1 * 0
        r = 28 + 14 * math.sin(k * 3.1)
        cr.arc(bx, by, r * smooth(t0, t0 + 0.4, t), 0, 2 * math.pi); cr.set_source_rgba(1, 1, 1, 0.75 * a); cr.fill_preserve(); stroke_dev(cr, hexc('#9AD7FF'), 4, a)

def drips(cr, x, y, a, t):
    if a <= 0.01: return
    for k in range(7):
        dx = x + (-270, -215, -160, 160, 215, 270, 0)[k]; dy = y - 260 + ((t * 1.2 + k * 0.3) % 1) * 200 + (0 if k < 6 else -120)
        cr.move_to(dx, dy - 18); cr.curve_to(dx + 12, dy, dx + 10, dy + 14, dx, dy + 14); cr.curve_to(dx - 10, dy + 14, dx - 12, dy, dx, dy - 18)
        cr.set_source_rgba(*hexc('#4FB3FF'), a); cr.fill()


def frame(cr, t):
    m = TL['marks']
    te = 0.0 if t >= m['loop'] else t
    bathroom(cr, t)
    twist = te >= m['tw']
    ri = 0
    for i in range(3):
        if te >= m[f's{i}']: ri = i
    if not twist:
        r = ROUNDS[ri]; s0 = m[f's{ri}']; rv = m[f'r{ri}']; x0 = m[f'x{ri}']; cl = m[f'clean{ri}']
        pin = ease_out_back(clamp((te - s0) / 0.45), 1.6) * (1 - smooth(x0, x0 + 0.35, te))
        clean = smooth(cl + 0.3, cl + 1.3, te)
        scrub = 1 if cl <= te < cl + 1.3 else 0
        wig = 0.04 * math.sin(te * 30) * scrub
        happy = clean > 0.8
        if pin > 0.01:
            cr.save(); cr.translate(AX, AY + 300); cr.rotate(wig); cr.scale(pin, pin)
            if r['k'] == 'pig':
                cr.save(); cr.translate(0, 0); cr.scale(1.15, 1.15); a_pig(cr, te, 0, happy); mud_spots(cr, 1 - clean, PIG_MUD); cr.restore()
            elif r['k'] == 'hippo':
                cr.save(); cr.translate(0, -130); cr.scale(1.15, 1.15); hippo(cr, te, clean); cr.restore()
            else:
                cr.save(); cr.translate(0, -230); cr.scale(1.0 + 0.08 * clean, 1.0 + 0.08 * clean)
                if clean > 0.6:
                    for k in range(14):
                        a = k * 2 * math.pi / 14; cr.arc(200 * math.cos(a), 10 + 190 * math.sin(a), 38, 0, 2 * math.pi); cr.set_source_rgb(*hexc('#F2C48D')); cr.fill()
                puppy(cr, te, 0, happy); cr.restore()
            cr.restore()
            if r['k'] == 'puppy': drips(cr, AX, AY + 120, (1 - clean) * pin, te)
        if r['k'] == 'pig': bubbles_fx(cr, AX, AY + 120, cl, cl + 1.2, te)
        # correct item scrubbing on the animal
        for j, kind in enumerate(r['items']):
            correct = j == r['ans']
            a = ease_out_back(clamp((te - s0 - 0.3 - j * 0.12) / 0.4), 1.6) * (1 - smooth(x0, x0 + 0.35, te))
            gl = 0.8 * burst(rv, rv + 0.6, te) if correct else 0
            dim = smooth(rv, rv + 0.3, te) if not correct else 0
            card(cr, CARD_X[j], CARD_Y, a, None if (correct and rv + 0.2 <= te < m[f'clean{ri}'] + 1.7) else kind, te, gl, dim)
            if correct and te >= rv + 0.2:
                u = ease_io(clamp((te - rv - 0.2) / max(0.3, cl - rv - 0.2)))
                tx = AX + 60 * math.sin(te * 16) * scrub; ty = AY + 130 + 40 * math.cos(te * 16) * scrub
                if te >= cl + 1.3: u2 = smooth(cl + 1.3, cl + 1.7, te)
                else: u2 = 0
                ix = lerp(CARD_X[j], tx, u); iy = lerp(CARD_Y, ty, u) - 200 * math.sin(math.pi * u)
                ix = lerp(ix, CARD_X[j], u2); iy = lerp(iy, CARD_Y, u2)
                if te < cl + 1.7:
                    cr.save(); cr.translate(ix, iy); cr.scale(0.8, 0.8); item(cr, kind, te); cr.restore()
        if te >= cl + 1.3: sparkles(cr, AX, AY + 80, cl + 1.3, te, 9, 230, 340)
    else:
        # puddle and the friends watching
        tw = m['tw']
        pa = ease_out_back(clamp((te - tw) / 0.5), 1.4)
        cr.save(); cr.translate(540, 1100); cr.scale(pa, pa)
        cr.move_to(-260, 0); cr.curve_to(-280, -60, -120, -90, 0, -70); cr.curve_to(150, -95, 290, -50, 260, 10); cr.curve_to(240, 70, -220, 75, -260, 0); cr.close_path()
        fs(cr, MUD); ellipse(cr, -60, -30, 90, 18); cr.set_source_rgba(1, 1, 1, 0.25); cr.fill()
        cr.restore()
        for k, (fx, sc) in enumerate(((200, 0.55), (880, 0.55))):
            cr.save(); cr.translate(fx, 980); cr.scale(sc * pa, sc * pa)
            if k == 0: a_pig(cr, te, 0, True)
            else: cr.translate(0, -230); hippo(cr, te, 1.0)
            cr.restore()
        sp = m['splat']
        if te >= sp:
            for k in range(14):
                u = (te - sp) / 0.9
                if u < 1:
                    a = math.pi * (0.1 + 0.8 * k / 13)
                    x = 540 + math.cos(a) * 520 * u * (1 if k % 2 else -1); y = 1080 - math.sin(a) * 650 * u + 900 * u * u
                    cr.arc(x, y, 22 - 8 * u, 0, 2 * math.pi); fs(cr, MUD, 4)
    # chickpea
    st = chick_talk(base_st(), te, TL); h = 0; sx = sy = 1; look = (0.6, -0.8)
    cx, cby, csc = 170, 1820, 0.72
    for i in range(3):
        if m[f'c{i}'] <= te < m[f'r{i}']: look = (0.5 + 0.3 * math.sin(te * 2), -0.9)
        if m[f'clean{i}'] + 1.3 <= te < m[f'clean{i}'] + 2.2:
            h, sx, sy, air = hop_seq(te, m[f'clean{i}'] + 1.3, 2, 0.45, 50); st.update(happy=1, wing=[0.3 + 0.8 * air] * 2)
    muddy = 0.0
    if twist:
        jp, sp = m['jump'], m['splat']
        if te < jp: cx, cby = 170, 1820
        elif te < sp:
            u = (te - jp) / (sp - jp); cx = lerp(170, 540, u); cby = lerp(1820, 1120, u) - 450 * math.sin(math.pi * u); st.update(happy=1, wing=[1, 1])
        else:
            cx, cby = 540, 1120; muddy = 1.0
            sq = burst(sp, sp + 0.4, te); sx = 1 + 0.25 * sq; sy = 1 - 0.25 * sq
            st.update(happy=1, wing=[0.6 + 0.4 * math.sin(te * 9)] * 2)
            if te < sp + 1.2: st['happy'] = 0; st['mood'] = 0.0
        csc = 0.72 if te < jp else 0.9
    if not (twist and te >= m['splat']): shadow_at(cr, cx, cby + 3, 100)
    chick(cr, cx, cby, h, csc, st, te, look, sx, sy, acc=None,
          extra=(lambda cr_, t_: mud_spots(cr_, 1.0, [(-90, -330, 40), (60, -290, 32), (110, -190, 36), (-70, -170, 28), (0, -60, 48), (-120, -70, 26), (40, -360, 24), (-130, -250, 22), (80, -90, 30)])) if muddy else None)
    for i, r in enumerate(ROUNDS):
        count_bubble(cr, m[f'c{i}'], te, "Say it!", y=470)
        word_pop(cr, r['word'], 540, 480, 130, r['col'], m[f'r{i}'] + 0.4, m[f'x{i}'] + 0.2, te)
    word_pop(cr, "SPLAT!", 540, 560, 180, '#8B5A2B', m['splat'], m['again'] + 0.3, te, 0.1)
    draw_text(cr, "Clean Up Time!", 250, 120, t, -1)
    loop_fade(cr, TL, t)

if __name__ == '__main__': episode_main(build, F)
