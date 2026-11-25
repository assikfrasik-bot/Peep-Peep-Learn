"""Counting Sheep — night meadow, sheep jump the fence. Round 1 counted aloud, round 2 kids count alone. Twist: woolly snail, Chickpea falls asleep."""
import sys; sys.path.insert(0, '/home/claude/kit')
from common import *

F = '/home/claude/ep17'
FX, FY = 540, 1390          # fence centre, ground line
FS = 1.35
WORDS = ['One', 'Two', 'Three', 'Four', 'Five']


def build():
    s = Script(F); t = 0.1
    t = s.say(t, 'hook', "Chickpea can't sleep. Let's count sheep!", 0.9) + 0.2
    j1 = []
    for k in range(3):
        j1.append(t); s.mark(f'j1_{k}', t)
        s.say(t + 0.55, f'n{k}', WORDS[k] + '...', 0.85)
        t += 1.45
    t += 0.3
    t = s.say(t, 'q1', "How many sheep jumped?", 0.9) + 0.1
    s.mark('c1', t); t += 3.0; s.mark('r1', t)
    t = s.say(t + 0.1, 'a1', "Three! Three sheep!", 0.9) + 0.3
    s.mark('more', t)
    t = s.say(t, 'more', "More sheep! Count them!", 0.9) + 0.25
    for k in range(5):
        s.mark(f'j2_{k}', t); t += 1.0
    t += 0.4
    t = s.say(t, 'q2', "How many sheep this time?", 0.9) + 0.1
    s.mark('c2', t); t += 3.0; s.mark('r2', t)
    t = s.say(t + 0.1, 'a2', "Five! Five sheep!", 0.9) + 0.3
    s.mark('snail', t)
    t = s.say(t, 'one', "And one more... very slow sheep.", 0.88) + 0.4
    s.mark('yawn', t)
    t = s.say(t, 'yawn', "Yaaawn... good night...", 0.85, True) + 0.3
    s.mark('sleep', t)
    t = s.say(t + 0.4, 'shh', "Shh... good night, Chickpea.", 0.85) + 0.5
    s.mark('again', t); t = s.say(t, 'again', "Again?", 0.95, True) + 0.25
    s.mark('loop', t); t += 0.9
    tl = s.save(t); m = tl['marks']; mx = Mix(tl['dur'])
    mx.music_loop(0, tl['dur'], 92, [([60, 64, 67], 36), ([57, 60, 64], 45), ([53, 57, 60], 41), ([55, 59, 62], 43)],
                  [[72, None, 76, None, 79, None, 76, None], [74, None, 72, None, 71, None, 67, None]], 'soft', 1.0)
    for k in range(3): mx.add('sfx', m[f'j1_{k}'] + 0.35, boing(), 0.2); mx.add('sfx', m[f'j1_{k}'] + 0.55, bell(mtof(72 + [0, 4, 7][k]), 1.0), 0.15)
    for k in range(5): mx.add('sfx', m[f'j2_{k}'] + 0.35, boing(), 0.2)
    for c in ('c1', 'c2'): countdown_ticks(mx, m[c], 0.25)
    mx.add('sfx', m['r1'], ding(), 0.18); mx.add('sfx', m['r2'], ding(), 0.18); mx.add('sfx', m['r2'] + 0.2, chime_up(), 0.2)
    mx.add('sfx', m['sleep'] + 0.3, chime_up(), 0.12)
    mx.add('sfx', m['again'] + 0.2, jingle(), 0.16)
    mx.voices(F, tl['events'])
    mx.write(F + '/audio.wav', quiet=[(m['c1'], m['r1']), (m['c2'], m['r2'])]); return tl


TL = json.load(open(F + '/timeline.json')) if os.path.exists(F + '/timeline.json') else None
rr = random.Random(17)
STARS = [(rr.uniform(20, 1060), rr.uniform(330, 1150), rr.uniform(6, 16), rr.uniform(0, 6.28)) for _ in range(45)]
SLOT1 = [(760, 1500), (870, 1500), (980, 1500)]
SLOT2 = [(740, 1490), (850, 1490), (960, 1490), (795, 1600), (905, 1600)]


def wool(cr, cx, cy, rx, ry, n=10, col=(1, 1, 1)):
    pts = [(cx + rx * math.cos(2 * math.pi * k / n), cy + ry * math.sin(2 * math.pi * k / n)) for k in range(n)]
    for x, y in pts: cr.arc(x, y, rx * 0.42, 0, 2 * math.pi); cr.new_sub_path()
    cr.arc(cx, cy, min(rx, ry), 0, 2 * math.pi)
    stroke_dev(cr, OUT, 10)
    for x, y in pts: cr.arc(x, y, rx * 0.42, 0, 2 * math.pi); cr.new_sub_path()
    cr.arc(cx, cy, min(rx, ry), 0, 2 * math.pi); cr.set_source_rgb(*col); cr.fill()

def sheep(cr, x, y, sc, t, legs=0.0, face_dir=1, happy=False, col=(1, 1, 1)):
    G_ = hexc('#4E4866')
    cr.save(); cr.translate(x, y); cr.scale(sc * face_dir, sc)
    for k, lx in enumerate((-55, -20, 25, 60)):
        sw = legs * (1 if k % 2 else -1)
        cr.move_to(lx, -40); cr.line_to(lx + sw * 18, 0); stroke_dev(cr, OUT, 20); cr.move_to(lx, -40); cr.line_to(lx + sw * 18, 0); stroke_dev(cr, G_, 12)
    wool(cr, 0, -95, 105, 58, 10, col)
    cr.save(); cr.translate(110, -125)
    for sx in (-1, 1):
        cr.save(); cr.translate(sx * 40, -10); cr.rotate(sx * -0.5); ellipse(cr, 0, 0, 28, 13); fs(cr, G_); cr.restore()
    ellipse(cr, 0, 10, 48, 58); fs(cr, G_)
    wool(cr, 0, -48, 40, 18, 6, col)
    for sx in (-1, 1):
        if happy: cr.arc(sx * 17, 4, 8, math.pi * 1.1, math.pi * 1.9); stroke_dev(cr, (1, 1, 1), 4)
        else:
            cr.arc(sx * 17, 0, 9, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()
            cr.arc(sx * 17 + 2, 1, 5, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill()
    cr.arc(0, 28, 9, 0.15 * math.pi, 0.85 * math.pi); stroke_dev(cr, (1, 1, 1), 4)
    cr.restore()
    cr.restore()


def jump_pos(u):
    """u 0..1 over the jump: from left approach to landing right of fence"""
    x = lerp(FX - 420, FX + 300, u)
    y = FY - 360 * math.sin(math.pi * clamp((u - 0.25) / 0.6)) if 0.25 < u < 0.85 else FY
    return x, y


def sheep_state(t0, slot, t, end):
    """t0 start of jump; slot (x,y) to rest; end: time they walk away"""
    u = (t - t0)
    if u < -0.6: return None
    if u < 0: x, y = lerp(-250, FX - 420, (u + 0.6) / 0.6), FY; return x, y, 0.6 * math.sin(t * 14), 1
    if u < 0.9: x, y = jump_pos(u / 0.9); return x, y, 0.0 if 0.25 < u / 0.9 < 0.85 else 0.6 * math.sin(t * 14), 1
    v = u - 0.9
    return FX + 300 + v * 650, FY, 0.6 * math.sin(t * 14), 1


def scenery(cr, t):
    g = cairo.LinearGradient(0, 0, 0, 1400); g.add_color_stop_rgb(0, *hexc('#1B1F5E')); g.add_color_stop_rgb(1, *hexc('#4B4FA8'))
    cr.set_source(g); cr.paint()
    for x, y, r, ph in STARS:
        a = 0.5 + 0.5 * math.sin(t * 2 + ph)
        star(cr, x, y, r); cr.set_source_rgba(1, 0.95, 0.6, 0.4 + 0.6 * a); cr.fill()
    # moon with face
    cx, cy = 840, 470
    glow(cr, cx, cy, 230, (1, 0.95, 0.7), 0.25)
    cr.arc(cx, cy, 120, 0, 2 * math.pi); fs(cr, hexc('#FFF1A8'))
    for x, y, r in ((-40, -50, 18), (45, 40, 14), (-55, 50, 10)):
        cr.arc(cx + x, cy + y, r, 0, 2 * math.pi); cr.set_source_rgba(0.9, 0.8, 0.4, 0.5); cr.fill()
    for sx in (-1, 1): cr.arc(cx + sx * 38, cy - 5, 13, math.pi * 0.1, math.pi * 0.9); stroke_dev(cr, OUT, 6)
    cr.arc(cx, cy + 30, 20, 0.2 * math.pi, 0.8 * math.pi); stroke_dev(cr, OUT, 5)
    hills(cr, 1250, '#2E6B4F', 50)
    ground(cr, FY - 10, '#3E8F5A', '#2A6A44')

def fence(cr):
    cr.save(); cr.translate(FX, FY); cr.scale(FS, FS); cr.translate(-FX, -FY)
    for dx in (-110, 0, 110):
        cr.move_to(FX + dx - 22, FY + 10); cr.line_to(FX + dx - 22, FY - 165); cr.line_to(FX + dx, FY - 190); cr.line_to(FX + dx + 22, FY - 165); cr.line_to(FX + dx + 22, FY + 10); cr.close_path()
        fs(cr, hexc('#E9D8B8'))
    for y in (FY - 130, FY - 60):
        rrect(cr, FX - 165, y, 330, 30, 10); fs(cr, hexc('#D9C29A'))
    cr.restore()

def bed(cr, t):
    rrect(cr, 20, 1720, 440, 170, 46); fs(cr, hexc('#7D6BFF'))
    for k in range(6): cr.arc(70 + k * 70, 1770, 11, 0, 2 * math.pi); cr.set_source_rgba(1, 1, 1, 0.5); cr.fill()
    ellipse(cr, 120, 1660, 120, 60); fs(cr, (1, 1, 1))

def mask(cr, t):
    cr.save(); cr.translate(0, -300)
    rrect(cr, -95, -25, 190, 50, 24); fs(cr, hexc('#A66CFF'))
    for x in (-45, 45): star5(cr, x, 0, 14); cr.set_source_rgb(*hexc('#FFE27A')); cr.fill()
    cr.restore()

def sleepy_eyes(amt):
    def f(cr, t):
        if amt <= 0: return
        for s in (-1, 1):
            cr.arc(s * 40, -22, 22, 0, 2 * math.pi); cr.set_source_rgba(*YEL, amt); cr.fill()
            cr.arc(s * 40, -30, 18, math.pi * 0.15, math.pi * 0.85); stroke_dev(cr, OUT, 7, amt)
        mask(cr, t)
    return f


def frame(cr, t):
    m = TL['marks']
    te = 0.0 if t >= m['loop'] else t
    scenery(cr, t)
    fence(cr)
    # sheep, round 1 and 2
    for k in range(3):
        stt = sheep_state(m[f'j1_{k}'], SLOT1[k], te, m['more'])
        if stt:
            x, y, lg, d = stt
            if x < 1300: sheep(cr, x, y, 0.95, te, lg, 1, happy=m['r1'] <= te)
    for k in range(5):
        stt = sheep_state(m[f'j2_{k}'], SLOT2[k], te, m['snail'] + 0.6)
        if stt:
            x, y, lg, d = stt
            col = (1, 1, 1) if k != 3 else hexc('#FFE3F0')
            if x < 1300: sheep(cr, x, y, 0.95, te, lg, 1, happy=m['r2'] <= te, col=col)
    # slow woolly snail
    if te >= m['snail']:
        u = te - m['snail']
        x = lerp(-150, FX - 330, clamp(u / 6.0))
        cr.save(); cr.translate(x, FY); cr.scale(-1.7, 1.7); draw_snail(cr, 0, 0, t)
        wool(cr, 10, -85, 40, 22, 7); cr.restore()
    # bed + chick
    bed(cr, t)
    sleep_amt = smooth(m['yawn'] + 0.8, m['sleep'] + 0.3, te) * (1 - smooth(m['again'] - 0.1, m['again'] + 0.2, te))
    st = chick_talk(base_st(), te, TL)
    look = (0.6, -0.3)
    for k in range(3):
        if m[f'j1_{k}'] <= te < m[f'j1_{k}'] + 1.0: look = (clamp((jump_pos(clamp((te - m[f'j1_{k}']) / 0.9))[0] - 300) / 500, -1, 1), -0.6)
    for k in range(5):
        if m[f'j2_{k}'] <= te < m[f'j2_{k}'] + 1.0: look = (clamp((jump_pos(clamp((te - m[f'j2_{k}']) / 0.9))[0] - 300) / 500, -1, 1), -0.6)
    if m['r1'] <= te < m['r1'] + 0.9 or m['r2'] <= te < m['r2'] + 0.9: st.update(happy=1, wing=[0.9, 0.9])
    if m['yawn'] <= te < m['yawn'] + 1.0: st['beak'] = 0.8 * math.sin(math.pi * clamp(te - m['yawn'])); st['happy'] = 1
    tilt = -0.25 * sleep_amt
    chick(cr, 240, 1760, 0, 0.86, st, te, look, rot=tilt, extra=sleepy_eyes(sleep_amt) if sleep_amt > 0 else mask)
    if sleep_amt > 0.5:
        for k in range(3):
            ph = (te * 0.5 + k / 3) % 1
            big_word(cr, 'z', 380 + ph * 140 + k * 10, 1420 - ph * 280, 60 + 30 * k, (1, 1, 1), 1.0, 0.2, math.sin(math.pi * ph) * sleep_amt)
    # numbers
    for k in range(3):
        word_pop(cr, str(k + 1), 540, 600, 200, '#FFD93B', m[f'j1_{k}'] + 0.5, m[f'j1_{k}'] + 1.3, te)
    for k in range(3):
        a = smooth(m[f'j1_{k}'] + 0.5, m[f'j1_{k}'] + 0.7, te) * (1 - smooth(m['more'] - 0.2, m['more'] + 0.2, te))
        if a > 0:
            cr.push_group(); sheep(cr, 540 + (k - 1) * 170 - 20, 780, 0.36, te, 0, 1, True); cr.pop_group_to_source(); cr.paint_with_alpha(a)
    for k in range(5):
        a = smooth(m[f'j2_{k}'] + 0.5, m[f'j2_{k}'] + 0.7, te) * (1 - smooth(m['snail'] - 0.2, m['snail'] + 0.2, te))
        if a > 0:
            col = (1, 1, 1) if k != 3 else hexc('#FFE3F0')
            cr.push_group(); sheep(cr, 540 + (k - 2) * 160 - 20, 780, 0.32, te, 0, 1, True, col); cr.pop_group_to_source(); cr.paint_with_alpha(a)
    word_pop(cr, "3", 540, 640, 240, '#FFD93B', m['r1'], m['more'], te)
    word_pop(cr, "5", 540, 640, 240, '#FFD93B', m['r2'], m['snail'] + 0.3, te)
    count_bubble(cr, m['c1'], te, y=420); count_bubble(cr, m['c2'], te, y=420)
    draw_text(cr, "Counting Sheep", 250, 130, t, -1)
    loop_fade(cr, TL, t)

if __name__ == '__main__': episode_main(build, F)
