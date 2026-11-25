"""Hot or Cold? — kitchen, stove vs fridge. Twist: ice cream melts next to the stove."""
import sys; sys.path.insert(0, '/home/claude/kit')
from common import *

F = '/home/claude/ep19'
IX, IY = 540, 700
STOVE = (230, 1150)       # pot top centre / place for hot things
FRIDGE_SLOTS = [(850, 1080), (850, 1290)]
STOVE_SLOTS = [(200, 1080), (330, 1080)]
ROUNDS = [dict(k='soup', hot=True, q="Soup! Is it hot, or cold?", a="Hot! The soup is hot!"),
          dict(k='ice', hot=False, q="Ice cubes! Hot, or cold?", a="Cold! Brrr! Ice is cold!"),
          dict(k='cocoa', hot=True, q="Cocoa! Hot, or cold?", a="Hot! Careful, it's hot!"),
          dict(k='pop', hot=False, q="An ice pop! Hot, or cold?", a="Cold! Nice and cold!")]


def build():
    s = Script(F); t = 0.1
    for i, r in enumerate(ROUNDS):
        s.mark(f's{i}', 0.0 if i == 0 else t)
        t = s.say(t + (0.3 if i else 0), f'q{i}', r['q']) + 0.1
        s.mark(f'c{i}', t); t += 3.0; s.mark(f'r{i}', t)
        t = s.say(t + 0.05, f'a{i}', r['a']) + 0.1
        s.mark(f'm{i}', t); t += 0.8
    s.mark('ice', t)
    t = s.say(t, 'yum', "Yum! Ice cream!", 1.0, True) + 0.2
    s.mark('near', t); t += 0.6
    t = s.say(t, 'melt', "Oh no! It's melting!", 1.0, True) + 0.1
    t = s.say(t, 'why', "Hot things make cold things melt!") + 0.15
    t = s.say(t, 'sticky', "Hee hee! Sticky!", 1.0, True) + 0.25
    s.mark('again', t); t = s.say(t, 'again', "Again?", 1.0, True) + 0.25
    s.mark('loop', t); t += 0.9
    tl = s.save(t); m = tl['marks']; mx = Mix(tl['dur'])
    mx.music_loop(0, tl['dur'], 114, [([60, 64, 67], 36), ([57, 60, 64], 45), ([62, 65, 69], 38), ([67, 71, 74], 43)],
                  [[76, None, 74, None, 72, None, 74, None], [76, None, 79, None, 76, None, None, None]], 'bouncy', 0.8)
    for i, r in enumerate(ROUNDS):
        mx.add('sfx', m[f's{i}'] + (0.05 if i else 0.0), pop(300, 800, 0.12), 0.3)
        countdown_ticks(mx, m[f'c{i}'])
        if r['hot']:
            mx.add('sfx', m[f'r{i}'], bp(rng.standard_normal(int(0.9 * SR)), 1500, 6000) * np.exp(-tt(0.9) / 0.4), 0.25)
            mx.add('sfx', m[f'r{i}'] + 0.1, slide_whistle(400, 1300, 0.5), 0.15)
        else:
            mx.add('sfx', m[f'r{i}'], chime_up(), 0.3)
            mx.add('sfx', m[f'r{i}'] + 0.1, slide_whistle(1300, 500, 0.5), 0.12)
        mx.add('sfx', m[f'm{i}'], whoosh(0.5), 0.25); mx.add('sfx', m[f'm{i}'] + 0.5, pop(600, 200, 0.15), 0.3)
    mx.add('sfx', m['ice'], chime_up(), 0.25)
    mx.add('sfx', m['near'] + 0.4, slide_whistle(900, 250, 1.4), 0.15)
    mx.add('sfx', m['near'] + 1.5, pop(500, 120, 0.2), 0.35)
    mx.add('sfx', m['again'] + 0.2, jingle(), 0.22)
    mx.voices(F, tl['events'])
    mx.write(F + '/audio.wav', quiet=[(m[f'c{i}'], m[f'r{i}']) for i in range(4)]); return tl


TL = json.load(open(F + '/timeline.json')) if os.path.exists(F + '/timeline.json') else None


# ---------------- items (~240 wide, origin centre) ----------------
def steam(cr, x, y, t, a=1.0, n=3, sp=50):
    for k in range(n):
        ph = (t * 0.7 + k / n) % 1
        cr.move_to(x + (k - (n - 1) / 2) * sp, y)
        for j in range(1, 8):
            cr.line_to(x + (k - (n - 1) / 2) * sp + 14 * math.sin(j * 0.9 + t * 3 + k), y - j * 18 - ph * 40)
        stroke_dev(cr, (1, 1, 1), 9, a * (1 - ph) * 0.85)

def it_soup(cr, t):
    steam(cr, 0, -70, t)
    cr.move_to(-130, -40); cr.curve_to(-125, 90, 125, 90, 130, -40); cr.close_path(); fs(cr, hexc('#FF8A5B'))
    ellipse(cr, 0, -40, 130, 32); fs(cr, hexc('#FFB347'))
    for x, y in ((-50, -45), (20, -35), (60, -48)): cr.arc(x, y, 10, 0, 2 * math.pi); fs(cr, hexc('#3ECF5E'), 4)
    face(cr, 0, 25, 0.8)

def it_ice(cr, t):
    for dx, dy, rot in ((-65, 15, -0.15), (65, -5, 0.12)):
        cr.save(); cr.translate(dx, dy); cr.rotate(rot)
        rrect(cr, -70, -70, 140, 140, 22); cr.set_source_rgba(0.75, 0.93, 1, 0.95); cr.fill_preserve(); stroke_dev(cr, OUT, 7)
        cr.move_to(-45, -50); cr.line_to(-10, -50); stroke_dev(cr, (1, 1, 1), 9, 0.9)
        face(cr, 0, 10, 0.6); cr.restore()
    for k in range(4):
        star(cr, -120 + k * 80, -100 + 20 * math.sin(t * 3 + k), 14); cr.set_source_rgba(1, 1, 1, 0.8 + 0.2 * math.sin(t * 5 + k)); cr.fill()

def it_cocoa(cr, t):
    steam(cr, -10, -110, t, 1.0, 2, 60)
    cr.arc(110, -10, 42, -1.4, 1.4); stroke_dev(cr, OUT, 26); cr.arc(110, -10, 42, -1.4, 1.4); stroke_dev(cr, hexc('#FF5FA2'), 14)
    rrect(cr, -110, -100, 220, 200, 34); fs(cr, hexc('#FF5FA2'))
    ellipse(cr, 0, -100, 110, 26); fs(cr, hexc('#8A5A2E'))
    for x in (-40, 10, 50): rrect(cr, x - 20, -122, 40, 34, 10); fs(cr, (1, 1, 1), 4)
    face(cr, 0, 10, 0.85)

def it_pop(cr, t):
    rrect(cr, -18, 80, 36, 110, 14); fs(cr, hexc('#E9B97A'))
    cr.move_to(-80, 100); cr.line_to(-80, -90); cr.curve_to(-80, -170, 80, -170, 80, -90); cr.line_to(80, 100); cr.close_path()
    p = cr.copy_path(); fs(cr, hexc('#FF7EB6'))
    cr.save(); cr.append_path(p); cr.clip(); cr.rectangle(-90, -40, 180, 50); cr.set_source_rgb(*hexc('#FFE14D')); cr.fill()
    cr.rectangle(-90, 10, 180, 45); cr.set_source_rgb(*hexc('#7FD0FF')); cr.fill(); cr.restore()
    cr.append_path(p); stroke_dev(cr, OUT, 7)
    ellipse(cr, -45, -100, 12, 30); cr.set_source_rgba(1, 1, 1, 0.5); cr.fill()
    face(cr, 0, -80, 0.7)

ITEMS = dict(soup=it_soup, ice=it_ice, cocoa=it_cocoa, pop=it_pop)


def cone(cr, melt, t):
    """ice cream cone held; melt 0..1"""
    cr.move_to(-55, 0); cr.line_to(0, 170); cr.line_to(55, 0); cr.close_path(); fs(cr, hexc('#E9B05A'))
    for k in range(-2, 3): cr.move_to(-50 + k * 8, 10 + abs(k) * 4); cr.line_to(k * 20 + 30, 120); stroke_dev(cr, hexc('#C98E3A'), 3)
    sy = 1 - 0.45 * melt
    cr.save(); cr.scale(1 + 0.15 * melt, sy)
    cr.arc(0, -55, 70, 0, 2 * math.pi); fs(cr, hexc('#FFB3D1'))
    cr.restore()
    if melt > 0:
        for k, (dx, ln) in enumerate(((-45, 90), (5, 140), (40, 70))):
            l = ln * melt
            cr.move_to(dx - 12, 0); cr.line_to(dx - 12, l); cr.arc(dx, l, 12, math.pi, 0); cr.line_to(dx + 12, 0); cr.close_path(); fs(cr, hexc('#FFB3D1'), 5)
    if melt < 0.6:
        for sx in (-1, 1): cr.arc(sx * 22, -60 * sy, 7, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill()
        cr.arc(0, -42 * sy, 10, 0.15 * math.pi, 0.85 * math.pi); stroke_dev(cr, OUT, 4)
    else:
        for sx in (-1, 1): cr.move_to(sx * 22 - 8, -58 * sy); cr.line_to(sx * 22 + 8, -52 * sy); stroke_dev(cr, OUT, 4)
        cr.arc(0, -25 * sy, 10, 1.15 * math.pi, 1.85 * math.pi); stroke_dev(cr, OUT, 4)


# ---------------- kitchen ----------------
def kitchen(cr, t):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *hexc('#FFF4DC')); g.add_color_stop_rgb(1, *hexc('#FFE7C2'))
    cr.set_source(g); cr.paint()
    for y in range(330, 960, 90):
        for x in range(0, W, 90):
            rrect(cr, x + 4, y + 4, 82, 82, 10); cr.set_source_rgba(1, 1, 1, 0.45); cr.fill()
    # stove (left)
    rrect(cr, 30, 1130, 420, 450, 24); fs(cr, hexc('#E9EEF5'))
    rrect(cr, 70, 1300, 340, 220, 18); fs(cr, hexc('#3C3F4A'))
    rrect(cr, 95, 1325, 290, 170, 12); cr.set_source_rgba(1, 0.55, 0.2, 0.35 + 0.1 * math.sin(t * 6)); cr.fill()
    for x in (110, 240, 370): cr.arc(x, 1215, 18, 0, 2 * math.pi); fs(cr, hexc('#FF5A5F'), 5)
    for x in (165, 315):
        ellipse(cr, x, 1132, 70, 14); fs(cr, hexc('#3C3F4A'), 5)
        for k in range(5):
            ph = (t * 1.5 + k / 5 + x) % 1
            cr.move_to(x - 40 + k * 20, 1125); cr.line_to(x - 40 + k * 20, 1110 - 12 * math.sin(math.pi * ph)); stroke_dev(cr, hexc('#FF8A1F'), 6, 0.8)
    # fridge (right)
    rrect(cr, 650, 820, 400, 760, 40); fs(cr, hexc('#D7F1FF'))
    rrect(cr, 680, 860, 340, 560, 26); fs(cr, hexc('#F2FBFF'))
    for y in (1190, 1400): cr.move_to(690, y); cr.line_to(1010, y); stroke_dev(cr, hexc('#9DD7F5'), 8)
    rrect(cr, 680, 1440, 340, 110, 20); fs(cr, hexc('#BFE6FA'))
    rrect(cr, 980, 1460, 18, 70, 8); fs(cr, hexc('#9DB2C4'), 4)
    for k in range(9):
        x = 700 + (k * 53) % 300; y = 880 + (k * 97) % 520
        star(cr, x, y, 10 + 4 * math.sin(t * 3 + k)); cr.set_source_rgba(0.6, 0.85, 1, 0.8); cr.fill()
    # floor
    cr.rectangle(0, 1580, W, H - 1580); cr.set_source_rgb(*hexc('#9ED3B0')); cr.fill()
    for x in range(0, W, 110):
        for y in range(1580, H, 110):
            if ((x + y) // 110) % 2: cr.rectangle(x, y, 110, 110); cr.set_source_rgba(1, 1, 1, 0.35); cr.fill()
    cr.move_to(0, 1580); cr.line_to(W, 1580); stroke_dev(cr, OUT, 6)


def thermo(cr, x, y, hot, p, s=1.0):
    if p <= 0.01: return
    cr.save(); cr.translate(x, y); cr.scale(s * ease_out_back(min(1, p * 2)), s * ease_out_back(min(1, p * 2)))
    rrect(cr, -26, -170, 52, 220, 26); fs(cr, (1, 1, 1))
    cr.arc(0, 70, 46, 0, 2 * math.pi); fs(cr, hexc('#FF3B3B' if hot else '#2EA7FF'))
    lvl = lerp(-20, -150, clamp(p)) if hot else lerp(-120, 30, clamp(p))
    rrect(cr, -12, lvl, 24, 80 - lvl, 12); cr.set_source_rgb(*hexc('#FF3B3B' if hot else '#2EA7FF')); cr.fill()
    for k in range(5): cr.move_to(14, -140 + k * 32); cr.line_to(24, -140 + k * 32); stroke_dev(cr, OUT, 4)
    cr.restore()


def frame(cr, t):
    m = TL['marks']
    te = 0.0 if t >= m['loop'] else t
    kitchen(cr, t)
    hot_n = 0; cold_n = 0
    for i, r in enumerate(ROUNDS):
        s0, r0, mv = m[f's{i}'], m[f'r{i}'], m[f'm{i}']
        slot = None
        if r['hot']: slot = STOVE_SLOTS[hot_n]; hot_n += 1
        else: slot = FRIDGE_SLOTS[cold_n]; cold_n += 1
        if te < s0 and i: continue
        if te < mv:
            app = ease_out_back((te - s0) / 0.5) if i else 1.0
            if app <= 0.01: continue
            wob = 0
            if te >= r0: wob = (0.06 * math.sin(te * 40) * burst(r0, r0 + 0.6, te)) if not r['hot'] else 0.0
            cr.save(); cr.translate(IX, IY + 15 * math.sin(te * 2.3)); cr.rotate(wob); cr.scale(1.3 * app, 1.3 * app)
            if te >= r0 and r['hot']: glow(cr, 0, 0, 220, (1, 0.5, 0.2), 0.5 * burst(r0, r0 + 1.2, te))
            if te >= r0 and not r['hot']: glow(cr, 0, 0, 220, (0.6, 0.85, 1), 0.6 * burst(r0, r0 + 1.2, te))
            ITEMS[r['k']](cr, te); cr.restore()
            thermo(cr, IX + 300, IY + 20, r['hot'], smooth(r0, r0 + 0.8, te), 0.9)
        else:
            u = smooth(mv, mv + 0.6, te)
            x = lerp(IX, slot[0], u); y = lerp(IY, slot[1], u) - 120 * math.sin(math.pi * u); sc = lerp(1.3, 0.5, u)
            cr.save(); cr.translate(x, y); cr.scale(sc, sc); ITEMS[r['k']](cr, te); cr.restore()
        word_pop(cr, 'HOT!' if r['hot'] else 'COLD!', 540, 470, 170, '#FF4D4D' if r['hot'] else '#2EA7FF', r0, mv + 0.2, te)
        count_bubble(cr, m[f'c{i}'], te, y=420)
    # chick with chef hat, twist with ice cream
    st = chick_talk(base_st(), te, TL); look = (0.0, -0.8); h = 0; sx = sy = 1
    cx = 540
    for i, r in enumerate(ROUNDS):
        if m[f'c{i}'] <= te < m[f'r{i}']: look = (0.6 * math.sin(te * 2), -0.9)
        if m[f'r{i}'] <= te < m[f'r{i}'] + 0.9:
            h, sx, sy, air = hop_seq(te, m[f'r{i}'], 2, 0.45, 50); st.update(happy=1, wing=[0.3 + 0.8 * air] * 2)
            if not r['hot']: st['mood'] = 0.0
        if m[f'm{i}'] <= te < m[f'm{i}'] + 0.6: look = (-0.9 if r['hot'] else 0.9, -0.5)
    melt = 0.0; holding = te >= m['ice']
    if holding:
        walk = smooth(m['near'], m['near'] + 0.6, te)
        cx = lerp(540, 430, walk)
        melt = smooth(m['near'] + 0.5, m['near'] + 2.2, te)
        st['wing'][0] = 1.0
        look = (-0.6, -0.2) if melt < 0.3 else (0.3, -0.6)
        if te < m['near']: st['happy'] = 1
        if melt > 0.3: st['mood'] = 0.0
    shadow_at(cr, cx, 1803, 105)
    def ex(c, tt_):
        if holding:
            c.save(); c.translate(-175, -330); c.rotate(-0.15); c.scale(1.35, 1.35); cone(c, melt, tt_); c.restore()
            if melt > 0.5:
                for k in range(3):
                    c.arc(-120 + k * 40, -360 + 10 * k, 16 * min(1, (melt - 0.5) * 3), 0, 2 * math.pi); fs(c, hexc('#FFB3D1'), 4)
    chick(cr, cx, 1800, h, 0.8, st, te, look, sx, sy, acc='chef', extra=ex)
    if holding and melt > 0.1:
        for k in range(4):
            ph = ((te - m['near']) * 1.1 + k / 4) % 1
            cr.arc(cx - 175 * 0.8 + 10 * k - 10, 1530 + ph * 250, 10, 0, 2 * math.pi); fs(cr, hexc('#FFB3D1'), 4, alpha=(1 - ph) * melt)
    word_pop(cr, "Yum!", 540, 470, 160, '#FF5FA2', m['ice'] + 0.1, m['near'] + 0.3, te)
    word_pop(cr, "Melting!", 540, 470, 160, '#FF9A1F', m['near'] + 1.0, m['again'] + 0.3, te)
    draw_text(cr, "Hot or Cold?", 250, 140, t, -1)
    loop_fade(cr, TL, t)

if __name__ == '__main__': episode_main(build, F)
