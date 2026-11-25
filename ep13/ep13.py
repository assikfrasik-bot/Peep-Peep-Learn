"""Who Says Moo? — farm barn, animal sounds from behind the doors. Twist: 'Peep peep!' is Chickpea's baby brother."""
import sys; sys.path.insert(0, '/home/claude/kit')
from common import *

F = '/home/claude/ep13'
DX, DY, DW, DH = 540, 1250, 430, 470          # doorway centre / size
ROUNDS = [dict(k='cow', snd="Moooo!", q="Who says moo?", a="A cow! The cow says moo!", w='COW!', c='#2EA7FF', sp=0.9),
          dict(k='duck', snd="Quack, quack!", q="Who says quack?", a="A duck! The duck says quack!", w='DUCK!', c='#FF9A1F', sp=1.05),
          dict(k='pig', snd="Oink, oink!", q="Who says oink?", a="A pig! The pig says oink!", w='PIG!', c='#FF5FA2', sp=1.0),
          dict(k='sheep', snd="Baaaa!", q="Who says baa?", a="A sheep! The sheep says baa!", w='SHEEP!', c='#A15CFF', sp=0.9)]


def build():
    s = Script(F); t = 0.1
    t = s.say(t, 'hook', "Who's in the barn? Listen!") + 0.15
    for i, r in enumerate(ROUNDS):
        s.mark(f's{i}', t)
        t = s.say(t, f'snd{i}', r['snd'], r['sp'], False, 'am_puck') + 0.15
        t = s.say(t, f'q{i}', r['q']) + 0.1
        s.mark(f'c{i}', t); t += 3.0; s.mark(f'r{i}', t)
        t = s.say(t + 0.35, f'a{i}', r['a']) + 0.15
        s.mark(f'x{i}', t); t += 0.6
    s.mark('s4', t)
    t = s.say(t, 'peep', "Peep, peep!", 1.15, True) + 0.1
    t = s.say(t, 'q4', "Who says peep?") + 0.35
    s.mark('r4', t)
    t = s.say(t + 0.5, 'bro', "My little brother!", 1.0, True) + 0.1
    s.mark('all', t)
    t = s.say(t + 0.2, 'everyone', "Everybody's here!") + 0.2
    t = s.say(t, 'laugh', "Hee hee!", 1.0, True) + 0.2
    s.mark('again', t); t = s.say(t, 'again', "Again?", 1.0, True) + 0.25
    s.mark('loop', t); t += 0.9
    tl = s.save(t); m = tl['marks']; mx = Mix(tl['dur'])
    mx.music_loop(0, tl['dur'], 120, [([60, 64, 67], 36), ([65, 69, 72], 41), ([67, 71, 74], 43), ([60, 64, 67], 36)],
                  [[72, 74, 76, None, 79, None, 76, None], [77, None, 76, None, 74, None, None, None]], 'bouncy', 0.8)
    for i in range(4):
        countdown_ticks(mx, m[f'c{i}'])
        mx.add('sfx', m[f'r{i}'], flick(), 0.4); mx.add('sfx', m[f'r{i}'] + 0.05, whoosh(0.5), 0.3)
        mx.add('sfx', m[f'r{i}'] + 0.35, pop(300, 900, 0.14), 0.4); mx.add('sfx', m[f'r{i}'] + 0.45, ding(), 0.18)
        mx.add('sfx', m[f'x{i}'], whoosh(0.4), 0.2); mx.add('sfx', m[f'x{i}'] + 0.4, kick(), 0.25)
    mx.add('sfx', m['r4'], whoosh(0.5), 0.3); mx.add('sfx', m['r4'] + 0.3, chirp(), 0.3); mx.add('sfx', m['r4'] + 0.4, tada(72), 0.2)
    mx.add('sfx', m['all'], boing(), 0.25); mx.add('sfx', m['all'] + 0.2, tada(76), 0.15)
    mx.add('sfx', m['again'] + 0.2, jingle(), 0.22)
    mx.voices(F, tl['events'])
    mx.write(F + '/audio.wav', quiet=[(m[f'c{i}'], m[f'r{i}']) for i in range(4)]); return tl


TL = json.load(open(F + '/timeline.json')) if os.path.exists(F + '/timeline.json') else None
rr = random.Random(13)
FLW = [(rr.uniform(30, 1050), rr.uniform(1700, 1880), rr.choice(['#FF5A5F', '#FFFFFF', '#A66CFF', '#FFB400', '#FF7EB6']), rr.uniform(0.7, 1.0)) for _ in range(9)]


# ---------------- animals (local origin = feet/centre-bottom of visible part, ~360 tall) ----------------
def eyes(cr, x, y, sp, s=1.0, happy=False):
    for sx in (-1, 1):
        if happy:
            cr.arc(x + sx * sp, y + 6 * s, 14 * s, math.pi * 1.1, math.pi * 1.9); stroke_dev(cr, OUT, 6)
        else:
            cr.arc(x + sx * sp, y, 15 * s, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill()
            cr.arc(x + sx * sp - 4 * s, y - 5 * s, 5 * s, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()

def cheeks(cr, x, y, sp, s=1.0):
    for sx in (-1, 1):
        ellipse(cr, x + sx * sp, y, 18 * s, 11 * s); cr.set_source_rgba(1, 0.45, 0.55, 0.5); cr.fill()

def a_cow(cr, t, talk=0, happy=False):
    W_ = hexc('#FFFFFF'); P = hexc('#FFB3C1')
    ellipse(cr, 0, -90, 170, 120); fs(cr, W_)
    for x, y, rx, ry in ((-90, -110, 50, 38), (80, -60, 42, 30)):
        cr.save(); ellipse(cr, 0, -90, 167, 117); cr.clip(); ellipse(cr, x, y, rx, ry); cr.set_source_rgb(*OUT); cr.fill(); cr.restore()
    for sx in (-1, 1):
        cr.save(); cr.translate(sx * 120, -330); cr.rotate(sx * 0.5); ellipse(cr, 0, 0, 16, 40); fs(cr, hexc('#F2E3C6')); cr.restore()
        cr.save(); cr.translate(sx * 150, -270); cr.rotate(sx * -0.4); ellipse(cr, 0, 0, 52, 26); fs(cr, W_); ellipse(cr, 0, 0, 30, 13); cr.set_source_rgb(*P); cr.fill(); cr.restore()
    ellipse(cr, 0, -250, 125, 105); fs(cr, W_)
    cr.save(); ellipse(cr, 0, -250, 122, 102); cr.clip(); ellipse(cr, 70, -310, 50, 40); cr.set_source_rgb(*OUT); cr.fill(); cr.restore()
    eyes(cr, 0, -265, 48, 1.0, happy)
    ellipse(cr, 0, -180, 92, 52 + 10 * talk); fs(cr, P)
    for sx in (-1, 1): ellipse(cr, sx * 32, -190, 11, 15); cr.set_source_rgb(*hexc('#C9707F')); cr.fill()
    if talk > 0.1: ellipse(cr, 0, -158, 34, 14 * talk + 2); cr.set_source_rgb(0.7, 0.2, 0.3); cr.fill()
    cheeks(cr, 0, -225, 88)

def a_duck(cr, t, talk=0, happy=False):
    W_ = (1, 1, 1); O = hexc('#FF9A1F')
    ellipse(cr, 0, -80, 140, 95); fs(cr, W_)
    cr.save(); cr.translate(-60, -95); cr.rotate(-0.3); ellipse(cr, 0, 0, 70, 38); fs(cr, hexc('#F0F2F5')); cr.restore()
    cr.arc(30, -250, 90, 0, 2 * math.pi); fs(cr, W_)
    ellipse(cr, 30, -150, 60, 30); cr.set_source_rgb(1, 1, 1); cr.fill()
    cr.move_to(10, -340); cr.curve_to(0, -380, 40, -390, 30, -345); fs(cr, W_, 5)
    eyes(cr, 30, -270, 36, 0.9, happy)
    o = 18 * talk
    ellipse(cr, 30, -215 - o / 2, 62, 20); fs(cr, O, 5)
    ellipse(cr, 30, -195 + o / 2, 55, 17); fs(cr, O, 5)
    cheeks(cr, 30, -228, 64, 0.9)

def a_pig(cr, t, talk=0, happy=False):
    Pk = hexc('#FFA8C5'); Pd = hexc('#FF8AB0')
    ellipse(cr, 0, -85, 165, 110); fs(cr, Pk)
    for sx in (-1, 1):
        cr.move_to(sx * 50, -330); cr.line_to(sx * 120, -390); cr.line_to(sx * 115, -300); cr.close_path(); fs(cr, Pd)
    cr.arc(0, -250, 118, 0, 2 * math.pi); fs(cr, Pk)
    eyes(cr, 0, -285, 45, 1.0, happy)
    ellipse(cr, 0, -215, 62, 44 + 6 * talk); fs(cr, Pd)
    for sx in (-1, 1): ellipse(cr, sx * 20, -215, 10, 15); cr.set_source_rgb(*hexc('#C9577F')); cr.fill()
    if talk > 0.1: ellipse(cr, 0, -160, 30, 10 * talk + 2); cr.set_source_rgb(0.7, 0.2, 0.3); cr.fill()
    else: cr.arc(0, -175, 22, 0.2 * math.pi, 0.8 * math.pi); stroke_dev(cr, OUT, 5)
    cheeks(cr, 0, -235, 85)

def wool(cr, cx, cy, rx, ry, n=10):
    pts = [(cx + rx * math.cos(2 * math.pi * k / n), cy + ry * math.sin(2 * math.pi * k / n)) for k in range(n)]
    for x, y in pts: cr.arc(x, y, rx * 0.42, 0, 2 * math.pi); cr.new_sub_path()
    cr.arc(cx, cy, min(rx, ry), 0, 2 * math.pi)
    stroke_dev(cr, OUT, 12)
    for x, y in pts: cr.arc(x, y, rx * 0.42, 0, 2 * math.pi); cr.new_sub_path()
    cr.arc(cx, cy, min(rx, ry), 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()

def a_sheep(cr, t, talk=0, happy=False):
    wool(cr, 0, -100, 150, 80)
    G_ = hexc('#5A5470')
    for sx in (-1, 1):
        cr.save(); cr.translate(sx * 105, -260); cr.rotate(sx * -0.5); ellipse(cr, 0, 0, 45, 22); fs(cr, G_); cr.restore()
    ellipse(cr, 0, -240, 85, 105); fs(cr, G_)
    wool(cr, 0, -335, 70, 30, 7)
    for sx in (-1, 1):
        if happy: cr.arc(sx * 32, -250, 13, math.pi * 1.1, math.pi * 1.9); stroke_dev(cr, (1, 1, 1), 6)
        else:
            cr.arc(sx * 32, -255, 17, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()
            cr.arc(sx * 32, -253, 10, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill()
            cr.arc(sx * 32 - 3, -257, 3.5, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()
    ellipse(cr, 0, -175, 28 + 8 * talk, 8 + 14 * talk); cr.set_source_rgb(*hexc('#2A2638')); cr.fill()
    cheeks(cr, 0, -205, 55, 0.9)

ANIM = dict(cow=a_cow, duck=a_duck, pig=a_pig, sheep=a_sheep)


def baby(cr, x, by, sc, t, talk):
    st = dict(wing=[0.6 + 0.4 * math.sin(t * 9), 0.6 + 0.4 * math.sin(t * 9 + 1)], beak=talk, happy=1 if talk < 0.05 else 0, mood=0)
    chick(cr, x, by, 0, sc, st, t, (0.0, 0.1))


# ---------------- barn ----------------
def scenery(cr, t):
    sky(cr, '#61C4FF', '#EAF9FF', 1300)
    small_sun(cr, t, 900, 380, 0.55)
    clouds(cr, t, ((200, 360, 0.45), (900, 620, 0.35), (520, 700, 0.3)), 10)
    hills(cr, 1200, '#A6E58A', 50)
    for x, s in ((60, 0.8), (1020, 0.75)): tree(cr, x, 1230, s, '#4CB944')
    # fence
    for x in range(-20, 1100, 70):
        if 140 < x < 940: continue
        rrect(cr, x, 1290, 26, 150, 8); fs(cr, (1, 1, 1))
    for y in (1320, 1380):
        for x0, x1 in ((-30, 160), (920, 1110)):
            rrect(cr, x0, y, x1 - x0, 20, 8); fs(cr, (1, 1, 1))
    ground(cr, 1470, '#7CD35F', '#4AAE42')
    # path
    cr.move_to(DX - DW / 2 + 20, 1480); cr.line_to(DX + DW / 2 - 20, 1480); cr.line_to(DX + 330, H); cr.line_to(DX - 330, H); cr.close_path()
    cr.set_source_rgb(*hexc('#E8C890')); cr.fill()

def barn_body(cr, t):
    R = hexc('#E8473F'); Rd = hexc('#B8322D')
    cr.move_to(150, 820); cr.line_to(540, 600); cr.line_to(930, 820); cr.line_to(930, 1485); cr.line_to(150, 1485); cr.close_path(); fs(cr, R)
    cr.save(); cr.move_to(150, 820); cr.line_to(540, 600); cr.line_to(930, 820); cr.line_to(930, 1485); cr.line_to(150, 1485); cr.close_path(); cr.clip()
    for x in range(170, 930, 48): cr.move_to(x, 600); cr.line_to(x, 1490); stroke_dev(cr, Rd, 4, 0.6)
    cr.restore()
    cr.move_to(110, 840); cr.line_to(540, 585); cr.line_to(970, 840); stroke_dev(cr, OUT, 52)
    cr.move_to(110, 840); cr.line_to(540, 585); cr.line_to(970, 840); stroke_dev(cr, hexc('#FFFFFF'), 36)
    # hayloft window
    cr.arc(540, 860, 92, 0, 2 * math.pi); fs(cr, hexc('#5A2E22'), 7)
    cr.arc(540, 860, 92, 0, 2 * math.pi); stroke_dev(cr, (1, 1, 1), 12)
    for k in range(7):
        cr.move_to(470 + k * 22, 905); cr.line_to(480 + k * 22, 935 - (k % 3) * 8); stroke_dev(cr, hexc('#F2C14E'), 6)
    # doorway frame
    rrect(cr, DX - DW / 2 - 22, DY - DH / 2 - 22, DW + 44, DH + 40, 10); fs(cr, (1, 1, 1))

def doorway_inside(cr):
    cr.rectangle(DX - DW / 2, DY - DH / 2, DW, DH); cr.set_source_rgb(*hexc('#4A261D')); cr.fill()
    for k in range(9):
        x = DX - DW / 2 + 20 + k * 47
        cr.move_to(x, DY + DH / 2); cr.line_to(x + 15, DY + DH / 2 - 60 - (k % 3) * 15); stroke_dev(cr, hexc('#E3B54A'), 7)

def door_panel(cr, side, openu, shake):
    """side -1 left (hinge at left edge), +1 right"""
    R = hexc('#D93B35'); w = DW / 2
    hx = DX + side * DW / 2
    sc = math.cos(openu * math.pi * 0.47)
    cr.save(); cr.translate(hx + shake, DY); cr.scale(-side * sc, 1); cr.translate(0, -DH / 2)
    cr.rectangle(0, 0, w, DH); fs(cr, R if sc > 0.15 else mixc(R, (0, 0, 0), 0.25))
    cr.rectangle(14, 14, w - 28, DH - 28); stroke_dev(cr, (1, 1, 1), 10)
    cr.move_to(14, 14); cr.line_to(w - 14, DH - 14); cr.move_to(w - 14, 14); cr.line_to(14, DH - 14); stroke_dev(cr, (1, 1, 1), 10)
    cr.restore()

def sound_rings(cr, t0, t1, t):
    if not (t0 <= t < t1): return
    for k in range(3):
        ph = ((t - t0) * 1.4 + k / 3) % 1
        a = (1 - ph) * smooth(t0, t0 + 0.2, t) * (1 - smooth(t1 - 0.2, t1, t))
        for side in (-1, 1):
            r = 110 + ph * 160
            cr.arc(540, 860, r, -0.5 + (math.pi if side < 0 else 0), 0.5 + (math.pi if side < 0 else 0))
            stroke_dev(cr, (1, 1, 1), 10, a)
    for k in range(3):
        ph = ((t - t0) * 0.8 + k / 3) % 1
        x = 540 + (k - 1) * 170 + 30 * math.sin(t * 3 + k); y = 760 - ph * 220
        a = math.sin(math.pi * ph) * smooth(t0, t0 + 0.2, t) * (1 - smooth(t1 - 0.2, t1, t))
        cr.push_group()
        ellipse(cr, x, y, 22, 17); cr.set_source_rgb(*DARK); cr.fill()
        cr.move_to(x + 18, y); cr.line_to(x + 18, y - 70); cr.line_to(x + 45, y - 55); stroke_dev(cr, DARK, 8)
        cr.pop_group_to_source(); cr.paint_with_alpha(a)


def frame(cr, t):
    m = TL['marks']
    te = 0.0 if t >= m['loop'] else t
    scenery(cr, t)
    barn_body(cr, t)
    # which phase
    ri = -1
    for i in range(5):
        if te >= m[f's{i}']: ri = i
    openu = 0.0; anim = None; talk = 0; happy = False
    if 0 <= ri < 4:
        r0 = m[f'r{ri}']; x0 = m[f'x{ri}']
        openu = smooth(r0, r0 + 0.45, te) * (1 - smooth(x0, x0 + 0.4, te))
        anim = ROUNDS[ri]['k']
        for e in TL['events']:
            if e['name'] in (f'a{ri}',) and e['t'] <= te < e['t'] + e['dur']: happy = True
        talk = 0.0
    if ri == 4 or te >= m['r4']:
        openu = smooth(m['r4'], m['r4'] + 0.45, te)
    doorway_inside(cr)
    # animal inside
    if anim and openu > 0.02:
        r0 = m[f'r{ri}']; x0 = m[f'x{ri}']
        e = ease_out_back((te - r0 - 0.15) / 0.5) * (1 - smooth(x0 - 0.05, x0 + 0.35, te))
        talk = 0.5 * abs(math.sin(te * 12)) if any(ev['name'] == f'a{ri}' and ev['t'] <= te < ev['t'] + 0.6 for ev in TL['events']) else 0
        bounce = 10 * math.sin(te * 5)
        cr.save(); cr.rectangle(DX - DW / 2, DY - DH / 2, DW, DH); cr.clip()
        cr.translate(DX, DY + DH / 2 + 40 + (1 - e) * 380 - abs(bounce)); cr.scale(0.98, 0.98)
        ANIM[anim](cr, te, talk, happy=e > 0.9 and talk == 0)
        cr.restore()
    if te >= m['r4']:
        e = ease_out_back((te - m['r4'] - 0.15) / 0.5)
        cr.save(); cr.rectangle(DX - DW / 2, DY - DH / 2, DW, DH); cr.clip()
        talk_b = 0.5 * abs(math.sin(te * 16)) if te < m['r4'] + 0.5 else 0
        h = abs(math.sin(te * 6)) * 30
        baby(cr, DX, DY + DH / 2 - 10 + (1 - e) * 300 - h, 0.56, te, talk_b)
        cr.restore()
    # doors
    shake = 0
    for i in range(5):
        k = f'snd{i}' if i < 4 else 'peep'
        for ev in TL['events']:
            if ev['name'] == k and ev['t'] <= te < ev['t'] + ev['dur']: shake = 7 * math.sin(te * 60)
    if te < m['s0']: shake = 0
    for side in (-1, 1): door_panel(cr, side, openu, shake * (1 if side < 0 else -1))
    # finale: everyone pops out
    if te >= m['all']:
        u = te - m['all']
        peeks = [('cow', 540, 952, 0.42, 0.0), ('pig', 905, 1500, 0.55, 0.15), ('sheep', 115, 1320, 0.5, 0.3), ('duck', 540, 625, 0.5, 0.45)]
        for k, x, y, sc, d in peeks:
            e = ease_out_back((u - d) / 0.5)
            if e <= 0: continue
            cr.save(); cr.translate(x, y - abs(math.sin(te * 5 + d * 6)) * 14 * e); cr.scale(sc * e, sc * e)
            if k == 'cow':
                cr.save(); cr.restore()
            ANIM[k](cr, te, 0, happy=True); cr.restore()
    # sound cue
    for i in range(4):
        ev = [e for e in TL['events'] if e['name'] == f'snd{i}'][0]
        sound_rings(cr, ev['t'], ev['t'] + ev['dur'] + 0.2, te)
    ev = [e for e in TL['events'] if e['name'] == 'peep'][0]
    sound_rings(cr, ev['t'], ev['t'] + ev['dur'] + 0.2, te)
    if te < m['s0'] + 0.01:
        pass
    # chickpea in straw hat, front-left
    st = chick_talk(base_st(), te, TL); look = (0.7, -0.4); h = 0; sx = sy = 1
    for i in range(4):
        if m[f'r{i}'] <= te < m[f'r{i}'] + 0.9:
            h, sx, sy, air = hop_seq(te, m[f'r{i}'] + 0.3, 2, 0.45, 55); st.update(happy=1, wing=[0.3 + 0.9 * air, 0.3 + 0.9 * air])
        if m[f'c{i}'] <= te < m[f'r{i}']: st['wing'] = [0.0, 0.9]; look = (0.8, -0.5)
    if m['r4'] <= te < m['again']:
        st['happy'] = 1; st['wing'] = [1.0 + 0.3 * math.sin(te * 8), 1.0 + 0.3 * math.sin(te * 8 + 1)]
        if m['all'] <= te: h, sx, sy, air = hop_seq(te, m['all'], 3, 0.45, 50)
    for i, (x, y, c, s) in enumerate(FLW):
        if 300 < x < 780 or x < 330: continue
        draw_flower(cr, x, y, s, hexc(c), t, i)
    shadow_at(cr, 170, 1745, 90)
    chick(cr, 170, 1742, h, 0.72, st, te, look, sx, sy, acc='straw')
    # UI
    for i, r in enumerate(ROUNDS):
        count_bubble(cr, m[f'c{i}'], te)
        word_pop(cr, r['w'], 540, 470, 150, r['c'], m[f'r{i}'] + 0.3, m[f'x{i}'], te)
    word_pop(cr, "Peep peep!", 540, 470, 140, '#FFB400', m['r4'] + 0.3, m['all'] - 0.1, te)
    word_pop(cr, "Hooray!", 600, 1610, 150, '#3ECF5E', m['all'] + 0.2, m['again'] + 0.4, te)
    draw_text(cr, "Who Says Moo?", 250, 135, t, -1)
    loop_fade(cr, TL, t)

if __name__ == '__main__': episode_main(build, F)
