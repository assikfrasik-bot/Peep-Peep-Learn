"""Land, Sea or Sky? — Chickpea drives a car, sails a boat, flies a plane. Twist: a rocket goes all the way to space."""
import sys; sys.path.insert(0, '/home/claude/kit')
from common import *

F = '/home/claude/ep26'
SKY1, LAND1, SEA1 = 960, 1300, 1640      # zone bottoms
ZONE_Y = dict(sky=650, land=1215, sea=1500)
ROUNDS = [dict(k='car', z='land', q="Where does the car go?", a="On the land!", y="Beep beep!", word='Land!', col='#3ECF5E'),
          dict(k='boat', z='sea', q="Where does the boat go?", a="On the sea!", y="Splash, splash!", word='Sea!', col='#2EA7FF'),
          dict(k='plane', z='sky', q="Where does the plane go?", a="In the sky!", y="Wheee!", word='Sky!', col='#FF9A1F')]
CX, CY = 540, 920


def build():
    s = Script(F); t = 0.1
    t = s.say(t, 'hook', "Land, sea, or sky? Where does it go?") + 0.05
    t = s.say(t, 'vroom', "Vroom vroom!", 1.0, True) + 0.15
    for i, r in enumerate(ROUNDS):
        s.mark(f's{i}', t); t += 0.5
        t = s.say(t, f'q{i}', r['q']) + 0.05
        s.mark(f'c{i}', t); t += 3.0; s.mark(f'r{i}', t)
        t = s.say(t + 0.45, f'a{i}', r['a']) + 0.05
        t = s.say(t, f'y{i}', r['y'], 1.0, True) + 0.25
        s.mark(f'x{i}', t); t += 0.8
    s.mark('tw', t); t += 0.4
    t = s.say(t, 'rocket', "And the rocket?") + 0.1
    s.mark('launch', t); t += 0.6
    t = s.say(t, 'up', "Up, up, up... all the way to space!") + 0.1
    t = s.say(t, 'moon', "To the moon! Wheee!", 1.0, True) + 0.25
    s.mark('again', t); t = s.say(t, 'again', "Again?", 1.0, True) + 0.25
    s.mark('loop', t); t += 0.9
    tl = s.save(t); m = tl['marks']; mx = Mix(tl['dur'])
    mx.music_loop(0, tl['dur'], 120, [([60, 64, 67], 36), ([67, 71, 74], 43), ([65, 69, 72], 41), ([67, 71, 74], 43)],
                  [[79, None, 76, None, 72, None, 74, 76], [77, None, 74, None, 79, None, None, None]], 'march', 0.75)
    snd = dict(car=lambda t0: [mx.add('sfx', t0 + k * 0.25, pluck(mtof(76 - k * 4), 0.25), 0.25) for k in range(2)],
               boat=lambda t0: mx.add('sfx', t0, splash_snd(0.7), 0.4),
               plane=lambda t0: mx.add('sfx', t0, slide_whistle(400, 1400, 0.8), 0.15))
    for i, r in enumerate(ROUNDS):
        mx.add('sfx', m[f's{i}'], pop(300, 900, 0.12), 0.3)
        countdown_ticks(mx, m[f'c{i}'])
        mx.add('sfx', m[f'r{i}'], whoosh(0.5), 0.15); mx.add('sfx', m[f'r{i}'] + 0.45, ding(), 0.2)
        snd[r['k']](m[f'r{i}'] + 0.6)
    mx.add('sfx', m['tw'], pop(300, 900, 0.12), 0.3)
    mx.add('sfx', m['launch'], rumble(1.6), 0.5); mx.add('sfx', m['launch'] + 0.3, slide_whistle(200, 1600, 2.0), 0.15)
    mx.add('sfx', m['launch'] + 2.4, chime_up(), 0.25)
    mx.add('sfx', m['again'] + 0.2, jingle(), 0.22)
    mx.voices(F, tl['events'])
    mx.write(F + '/audio.wav', quiet=[(m[f'c{i}'], m[f'r{i}']) for i in range(3)]); return tl


TL = json.load(open(F + '/timeline.json')) if os.path.exists(F + '/timeline.json') else None


def rider(cr, x, by, sc, t, wave=False):
    st = base_st(); st['happy'] = 1
    if wave: st['wing'] = [0.2, 0.7 + 0.5 * math.sin(t * 10)]
    chick(cr, x, by, 0, sc, st, t, (0.4, 0), shell=False)

def car(cr, t, mv=0.0):
    bob = 4 * math.sin(t * 14) * mv
    cr.save(); cr.translate(0, bob)
    cr.move_to(-120, -110); cr.line_to(-70, -215); cr.line_to(85, -215); cr.line_to(135, -110); cr.close_path(); fs(cr, hexc('#FF4D4D'))
    cr.save(); cr.move_to(-95, -112); cr.line_to(-55, -195); cr.line_to(72, -195); cr.line_to(110, -112); cr.close_path(); cr.clip()
    cr.set_source_rgb(*hexc('#CFF1FF')); cr.paint(); rider(cr, 10, -40, 0.42, t, mv > 0.5)
    cr.restore()
    cr.move_to(-95, -112); cr.line_to(-55, -195); cr.line_to(72, -195); cr.line_to(110, -112); cr.close_path(); stroke_dev(cr, OUT, 7)
    rrect(cr, -215, -125, 430, 105, 40); fs(cr, hexc('#FF4D4D'))
    rrect(cr, -190, -95, 380, 20, 10); cr.set_source_rgba(1, 1, 1, 0.35); cr.fill()
    ellipse(cr, 195, -85, 22, 18); fs(cr, hexc('#FFE45C'), 5)
    rrect(cr, -222, -70, 30, 22, 8); fs(cr, hexc('#FF9A1F'), 5)
    cr.restore()
    for x in (-120, 125):
        cr.save(); cr.translate(x, -20); cr.rotate(t * 12 * mv)
        cr.arc(0, 0, 48, 0, 2 * math.pi); fs(cr, hexc('#3A3550')); cr.arc(0, 0, 20, 0, 2 * math.pi); fs(cr, hexc('#D0D6E0'), 5)
        cr.move_to(-20, 0); cr.line_to(20, 0); stroke_dev(cr, OUT, 4)
        cr.restore()

def boat(cr, t, mv=0.0):
    cr.save(); cr.rotate(0.05 * math.sin(t * 2.5))
    cr.move_to(0, -95); cr.line_to(0, -420); stroke_dev(cr, OUT, 16); cr.move_to(0, -95); cr.line_to(0, -420); stroke_dev(cr, hexc('#9B6B43'), 8)
    cr.move_to(12, -405); cr.curve_to(150, -330, 190, -210, 175, -130); cr.line_to(12, -130); cr.close_path(); fs(cr, (1, 1, 1))
    cr.move_to(-12, -380); cr.curve_to(-90, -300, -120, -200, -115, -140); cr.line_to(-12, -140); cr.close_path(); fs(cr, hexc('#FF5A5F'))
    cr.move_to(0, -420); cr.line_to(70, -400); cr.line_to(0, -380); cr.close_path(); fs(cr, hexc('#FFC93C'), 5)
    rider(cr, -70, -80, 0.4, t, mv > 0.5)
    cr.move_to(-240, -95); cr.line_to(240, -95); cr.curve_to(210, -20, 170, 10, 130, 15); cr.line_to(-140, 15); cr.curve_to(-180, 10, -215, -30, -240, -95); cr.close_path()
    hull = cr.copy_path(); fs(cr, hexc('#2E8BD9'))
    cr.save(); cr.append_path(hull); cr.clip(); cr.rectangle(-250, -75, 500, 22); cr.set_source_rgb(1, 1, 1); cr.fill(); cr.restore()
    cr.append_path(hull); stroke_dev(cr, OUT, 7)
    for x in (-110, 0, 110): cr.arc(x, -30, 14, 0, 2 * math.pi); fs(cr, hexc('#CFF1FF'), 5)
    cr.restore()

def plane(cr, t, mv=0.0):
    cr.save(); cr.rotate(-0.06 + 0.04 * math.sin(t * 2))
    cr.move_to(-60, -40); cr.line_to(-140, -170); cr.line_to(-80, -170); cr.line_to(40, -40); cr.close_path(); fs(cr, hexc('#2EA7FF'))
    cr.move_to(-210, -80); cr.line_to(-260, -190); cr.line_to(-210, -190); cr.line_to(-150, -80); cr.close_path(); fs(cr, hexc('#FF5A5F'))
    ellipse(cr, 0, -70, 240, 72); fs(cr, (1, 1, 1))
    cr.save(); ellipse(cr, 0, -70, 237, 69); cr.clip(); cr.rectangle(-250, -60, 500, 16); cr.set_source_rgb(*hexc('#FF5A5F')); cr.fill(); cr.restore()
    cr.save(); cr.arc(90, -120, 62, math.pi, 2 * math.pi); cr.close_path(); cr.clip(); cr.set_source_rgb(*hexc('#CFF1FF')); cr.paint(); rider(cr, 90, -95, 0.36, t, mv > 0.5); cr.restore()
    cr.arc(90, -120, 62, math.pi, 2 * math.pi); cr.close_path(); stroke_dev(cr, OUT, 7)
    for x in (-150, -90, -30): cr.arc(x, -85, 13, 0, 2 * math.pi); fs(cr, hexc('#CFF1FF'), 5)
    cr.move_to(-40, -70); cr.line_to(-120, 60); cr.line_to(-60, 60); cr.line_to(60, -70); cr.close_path(); fs(cr, hexc('#2EA7FF'))
    cr.save(); cr.translate(245, -70)
    ellipse(cr, 0, 0, 16, 22); fs(cr, hexc('#FFC93C'), 5)
    sp = math.cos(t * 40); ellipse(cr, 8, 0, 6, 80 * abs(sp) + 10); cr.set_source_rgba(0.3, 0.3, 0.35, 0.6); cr.fill()
    cr.restore()
    cr.restore()

def rocket(cr, t, fire=0.0):
    if fire > 0:
        for k, (c, w, l) in enumerate((('#FF5A1F', 75, 260), ('#FFC93C', 50, 190), ('#FFFFFF', 25, 110))):
            fl = l * fire * (1 + 0.15 * math.sin(t * 40 + k))
            cr.move_to(-w, 20); cr.curve_to(-w, 20 + fl * 0.5, -10, 20 + fl, 0, 20 + fl); cr.curve_to(10, 20 + fl, w, 20 + fl * 0.5, w, 20); cr.close_path()
            cr.set_source_rgb(*hexc(c)); cr.fill()
    for sx in (-1, 1):
        cr.move_to(sx * 80, -120); cr.line_to(sx * 160, 30); cr.line_to(sx * 70, 20); cr.close_path(); fs(cr, hexc('#FF5A5F'))
    cr.move_to(-90, 20); cr.line_to(-95, -260); cr.curve_to(-90, -400, -30, -480, 0, -510); cr.curve_to(30, -480, 90, -400, 95, -260); cr.line_to(90, 20); cr.close_path()
    body = cr.copy_path(); fs(cr, (1, 1, 1))
    cr.save(); cr.append_path(body); cr.clip()
    cr.rectangle(-100, -440, 200, 400); cr.set_source_rgba(0, 0, 0, 0); cr.fill()
    cr.move_to(-100, -400); cr.curve_to(-60, -540, 60, -540, 100, -400); cr.close_path(); cr.set_source_rgb(*hexc('#FF5A5F')); cr.fill()
    cr.rectangle(-100, -40, 200, 25); cr.set_source_rgb(*hexc('#2EA7FF')); cr.fill()
    cr.restore(); cr.append_path(body); stroke_dev(cr, OUT, 8)
    cr.save(); cr.arc(0, -250, 62, 0, 2 * math.pi); cr.clip(); cr.set_source_rgb(*hexc('#CFF1FF')); cr.paint(); rider(cr, 0, -195, 0.33, t, fire > 0.5); cr.restore()
    cr.arc(0, -250, 62, 0, 2 * math.pi); stroke_dev(cr, hexc('#9AA7B8'), 16); cr.arc(0, -250, 70, 0, 2 * math.pi); stroke_dev(cr, OUT, 6)
    rrect(cr, -22, -90, 44, 60, 14); fs(cr, hexc('#FFC93C'), 5)

VEH = dict(car=car, boat=boat, plane=plane)


def world(cr, t):
    # space above y=0 (revealed by the camera pan)
    cr.rectangle(0, -2300, W, 2300 + 400); g = cairo.LinearGradient(0, -1700, 0, 400)
    g.add_color_stop_rgb(0, *hexc('#120C2E')); g.add_color_stop_rgb(0.75, *hexc('#3B2A7A')); g.add_color_stop_rgb(1, *hexc('#6FC8FF'))
    cr.set_source(g); cr.fill()
    for k in range(40):
        x = (k * 197) % W; y = -1450 + (k * 331) % 1500
        star5(cr, x, y, 8 + (k % 4) * 4); cr.set_source_rgba(1, 0.95, 0.7, 0.5 + 0.5 * math.sin(t * 3 + k)); cr.fill()
    cr.arc(820, -1150, 150, 0, 2 * math.pi); fs(cr, hexc('#F3F1E4'))
    for x, y, r in ((770, -1190, 30), (870, -1100, 22), (800, -1080, 16)): cr.arc(x, y, r, 0, 2 * math.pi); cr.set_source_rgb(*hexc('#D9D5C3')); cr.fill()
    for sx in (-1, 1): cr.arc(820 + sx * 45, -1150, 12, 0, 2 * math.pi); cr.set_source_rgb(*OUT); cr.fill()
    cr.arc(820, -1130, 30, 0.2 * math.pi, 0.8 * math.pi); stroke_dev(cr, OUT, 6)
    cr.arc(250, -500, 70, 0, 2 * math.pi); fs(cr, hexc('#FF9A5C'))
    ellipse(cr, 250, -500, 120, 22); stroke_dev(cr, OUT, 14); ellipse(cr, 250, -500, 120, 22); stroke_dev(cr, hexc('#FFD27A'), 7)
    # sky
    g = cairo.LinearGradient(0, 300, 0, SKY1); g.add_color_stop_rgb(0, *hexc('#6FC8FF')); g.add_color_stop_rgb(1, *hexc('#D6F2FF'))
    cr.rectangle(0, 300, W, SKY1 - 300); cr.set_source(g); cr.fill()
    clouds(cr, t, ((760, 450, 0.45), (230, 700, 0.4), (980, 780, 0.3)))
    # land
    hills(cr, SKY1 + 20, '#9BE07A', 45)
    cr.rectangle(0, SKY1 + 20, W, LAND1 - SKY1 - 20); cr.set_source_rgb(*hexc('#7ACB5A')); cr.fill()
    rrect(cr, -20, 1165, W + 40, 100, 20); fs(cr, hexc('#5D5A70'))
    for k in range(9): rrect(cr, (k * 140 - (t * 60) % 140), 1208, 70, 14, 7); cr.set_source_rgb(1, 1, 1); cr.fill()
    for x in (90, 990): tree(cr, x, 1160, 0.75, '#3ECF5E')
    # sea
    cr.rectangle(0, LAND1, W, SEA1 - LAND1); g = cairo.LinearGradient(0, LAND1, 0, SEA1)
    g.add_color_stop_rgb(0, *hexc('#4FC3F7')); g.add_color_stop_rgb(1, *hexc('#1E88E5')); cr.set_source(g); cr.fill()
    for row in range(3):
        y = LAND1 + 60 + row * 100
        cr.move_to(0, y)
        for x in range(0, W + 40, 40): cr.line_to(x, y + 8 * math.sin(x / 50 + t * 2 + row))
        stroke_dev(cr, (1, 1, 1), 5, 0.5)
    cr.move_to(0, LAND1); cr.line_to(W, LAND1); stroke_dev(cr, OUT, 6)
    # sand foreground
    cr.rectangle(0, SEA1, W, 900); cr.set_source_rgb(*hexc('#FFE3A3')); cr.fill()
    cr.move_to(0, SEA1); cr.line_to(W, SEA1); stroke_dev(cr, OUT, 6)
    # sandcastle + beach ball
    cr.save(); cr.translate(860, 1830)
    for x, w_, h_ in ((-90, 60, 110), (30, 60, 110), (-40, 90, 150)):
        rrect(cr, x, -h_, w_, h_, 8); fs(cr, hexc('#F5C978'))
        for k in range(3): cr.rectangle(x + k * w_ / 3, -h_ - 18, w_ / 6, 18)
        fs(cr, hexc('#F5C978'), 5)
    cr.move_to(5, -168); cr.line_to(5, -230); stroke_dev(cr, OUT, 5); cr.move_to(5, -230); cr.line_to(50, -215); cr.line_to(5, -200); cr.close_path(); fs(cr, hexc('#FF5A5F'), 4)
    cr.restore()
    cr.save(); cr.translate(190, 1790); cr.rotate(t * 0.6)
    cr.arc(0, 0, 70, 0, 2 * math.pi); fs(cr, (1, 1, 1))
    for k, c in enumerate(('#FF5A5F', '#2EA7FF', '#FFC93C')):
        cr.move_to(0, 0); cr.arc(0, 0, 66, k * 2.094, k * 2.094 + 1.05); cr.close_path(); cr.set_source_rgb(*hexc(c)); cr.fill()
    cr.arc(0, 0, 70, 0, 2 * math.pi); stroke_dev(cr, OUT, 7)
    cr.restore()

def zone_label(cr, text, y, col, pulse):
    s = 1 + 0.25 * pulse
    cr.save(); cr.translate(960, y); cr.scale(s, s)
    rrect(cr, -95, -36, 190, 72, 36); fs(cr, (1, 1, 1))
    cr.restore()
    big_word(cr, text, 960, y + 2, 52 * s, hexc(col), 1.0)


def frame(cr, t):
    m = TL['marks']
    te = 0.0 if t >= m['loop'] else t
    twist = te >= m['tw']
    pan = 0
    if twist: pan = 1650 * ease_io(clamp((te - m['launch'] - 0.8) / 2.6))
    cr.save(); cr.translate(0, pan)
    world(cr, t)
    ri = 0
    for i in range(3):
        if te >= m[f's{i}']: ri = i
    pulses = dict(sky=0, land=0, sea=0)
    if not twist:
        r = ROUNDS[ri]; rv = m[f'r{ri}']
        pulses[r['z']] = burst(rv + 0.3, rv + 1.0, te)
    for z, lab, col in (('sky', 'SKY', '#FF9A1F'), ('land', 'LAND', '#3ECF5E'), ('sea', 'SEA', '#2EA7FF')):
        zone_label(cr, lab, {'sky': 450, 'land': 1050, 'sea': 1385}[z], col, pulses[z])
    if not twist:
        r = ROUNDS[ri]; rv = m[f'r{ri}']; x0 = m[f'x{ri}']
        pin = ease_out_back(clamp((te - m[f's{ri}']) / 0.45), 1.6)
        # spotlight disc while asking
        disc = pin * (1 - smooth(rv, rv + 0.3, te))
        if disc > 0.01:
            cr.arc(CX, CY, 290 * disc, 0, 2 * math.pi); fs(cr, (1, 1, 1)); cr.arc(CX, CY, 290 * disc, 0, 2 * math.pi); cr.set_source_rgba(1, 0.95, 0.6, 0.35); cr.fill()
        u = ease_io(clamp((te - rv) / 0.9))
        zy = ZONE_Y[r['z']]
        base_y = {'car': 130, 'boat': 90, 'plane': 100}[r['k']]
        x = CX + (te - rv - 0.9) * 260 * (1 if te > rv + 0.9 else 0) + 1300 * smooth(x0, x0 + 0.8, te) ** 2
        y = lerp(CY + base_y, zy + base_y * 0.55, u)
        sc = lerp(0.85, 0.62, u) * pin
        if r['k'] == 'boat': y += 8 * math.sin(te * 2.5)
        if r['k'] == 'plane': y += 20 * math.sin(te * 1.8) - 90 * smooth(x0, x0 + 0.8, te)
        if sc > 0.01:
            cr.save(); cr.translate(x, y); cr.scale(sc, sc); VEH[r['k']](cr, te, 1.0 if te > rv else 0.0); cr.restore()
        if r['k'] == 'boat' and te > rv + 0.9:
            for k in range(4):
                cr.arc(x - 160 - k * 50, y + 10 + 4 * math.sin(te * 6 + k), 12 - k * 2, 0, 2 * math.pi); cr.set_source_rgba(1, 1, 1, 0.8); cr.fill()
        if r['k'] == 'car' and te > rv + 0.9:
            for k in range(3):
                cr.arc(x - 160 - k * 40 - (te * 200) % 40, y - 30 - k * 8, 16 + k * 6, 0, 2 * math.pi); cr.set_source_rgba(1, 1, 1, 0.6 - k * 0.15); cr.fill()
    else:
        pin = ease_out_back(clamp((te - m['tw']) / 0.45), 1.6)
        lu = clamp((te - m['launch']) / 3.2)
        ry = CY + 260 - (lu ** 1.7) * (CY + 260 + 480)
        shake = 5 * math.sin(te * 60) * (1 if m['launch'] <= te < m['launch'] + 0.8 else 0)
        fire = smooth(m['launch'], m['launch'] + 0.3, te)
        if pin > 0.01:
            cr.save(); cr.translate(CX + shake, ry); cr.scale(0.75 * pin, 0.75 * pin); rocket(cr, te, fire); cr.restore()
        if m['launch'] <= te < m['launch'] + 2.0:
            for k in range(8):
                u = (te - m['launch']) * 1.2 - k * 0.1
                if 0 < u < 1:
                    cr.arc(CX + (k - 3.5) * 60 * (1 + u), CY + 330 + 30 * u, 40 + 60 * u, 0, 2 * math.pi); cr.set_source_rgba(1, 1, 1, 0.8 * (1 - u)); cr.fill()
    cr.restore()
    for i in range(3):
        count_bubble(cr, m[f"c{i}"], te, "Say it!", y=430, w=420)
        word_pop(cr, ROUNDS[i]['word'], 470, 450, 120, ROUNDS[i]['col'], m[f'r{i}'] + 0.4, m[f'x{i}'] + 0.4, te)
    word_pop(cr, "Space!", 540, 1500, 160, '#A15CFF', m['launch'] + 2.6, m['again'] + 0.3, te)
    if te >= m['launch'] + 3.0: sparkles(cr, 540, 700, m['launch'] + 3.0, te, 9, 250, 400)
    draw_text(cr, "Land, Sea or Sky?", 250, 115, t, -1)
    loop_fade(cr, TL, t)

if __name__ == '__main__': episode_main(build, F)
