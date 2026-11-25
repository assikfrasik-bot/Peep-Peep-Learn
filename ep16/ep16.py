"""What Should I Wear? — weather in the window, pick the right item. Twist: silly weather, Chickpea wears everything."""
import sys; sys.path.insert(0, '/home/claude/kit')
from common import *

F = '/home/claude/ep16'
WX, WY, WW, WH = 140, 470, 800, 640           # window
CARDS = [(280, 1330), (800, 1330)]
ROUNDS = [dict(w='sunny', q="It's sunny and hot! What should Chickpea wear?", opts=['glasses', 'beanie'], ans=0,
               a="Sunglasses! Cool!", word='SUNNY', c='#FFB400'),
          dict(w='rainy', q="It's raining! What does Chickpea need?", opts=['ball', 'umbrella'], ans=1,
               a="An umbrella! Nice and dry!", word='RAINY', c='#2EA7FF'),
          dict(w='snowy', q="Brrr, it's snowing! What should Chickpea wear?", opts=['beanie', 'swimring'], ans=0,
               a="A warm hat and scarf!", word='SNOWY', c='#7FB8FF')]


def build():
    s = Script(F); t = 0.1
    for i, r in enumerate(ROUNDS):
        s.mark(f's{i}', 0.0 if i == 0 else t)
        t = s.say(t + (0.3 if i else 0), f'q{i}', r['q']) + 0.1
        s.mark(f'c{i}', t); t += 3.0; s.mark(f'r{i}', t)
        t = s.say(t + 0.35, f'a{i}', r['a']) + 0.3
        s.mark(f'x{i}', t); t += 0.4
    s.mark('crazy', t)
    t = s.say(t + 0.2, 'crazy', "Whoa! Sun, rain AND snow?") + 0.2
    s.mark('all', t)
    t = s.say(t, 'all', "I'll wear everything!", 1.0, True) + 0.25
    t = s.say(t, 'rainbow', "Silly weather makes a rainbow!") + 0.15
    t = s.say(t, 'laugh', "Hee hee!", 1.0, True) + 0.2
    s.mark('again', t); t = s.say(t, 'again', "Again?", 1.0, True) + 0.25
    s.mark('loop', t); t += 0.9
    tl = s.save(t); m = tl['marks']; mx = Mix(tl['dur'])
    mx.music_loop(0, tl['dur'], 110, [([60, 64, 67], 36), ([65, 69, 72], 41), ([57, 60, 64], 45), ([67, 71, 74], 43)],
                  [[79, None, 76, None, 72, None, 76, None], [77, None, 74, None, 71, None, None, None]], 'bouncy', 0.8)
    for i in range(3):
        if i: mx.add('sfx', m[f's{i}'], whoosh(0.6), 0.3)
        countdown_ticks(mx, m[f'c{i}'])
        mx.add('sfx', m[f'r{i}'], ding(), 0.2); mx.add('sfx', m[f'r{i}'] + 0.2, slide_whistle(500, 1400, 0.4), 0.15)
        mx.add('sfx', m[f'r{i}'] + 0.6, pop(300, 1000, 0.13), 0.35)
    for k in range(3): mx.add('sfx', m['crazy'] + k * 0.15, whoosh(0.4), 0.2)
    mx.add('sfx', m['all'], chime_up(), 0.3); mx.add('sfx', m['all'] + 1.2, tada(72), 0.2)
    mx.add('sfx', m['again'] + 0.2, jingle(), 0.22)
    mx.voices(F, tl['events'])
    mx.write(F + '/audio.wav', quiet=[(m[f'c{i}'], m[f'r{i}']) for i in range(3)]); return tl


TL = json.load(open(F + '/timeline.json')) if os.path.exists(F + '/timeline.json') else None
rr = random.Random(16)
RAIN = [(rr.uniform(0, 1), rr.uniform(0, 1), rr.uniform(0.8, 1.2)) for _ in range(60)]
SNOW = [(rr.uniform(0, 1), rr.uniform(0, 1), rr.uniform(6, 14), rr.uniform(0, 6.28)) for _ in range(50)]


# ---------------- items (local, ~260 wide) ----------------
def it_glasses(cr, t, s=1.0):
    cr.save(); cr.scale(s, s)
    for sx in (-1, 1):
        rrect(cr, sx * 70 - 60, -45, 120, 85, 32); fs(cr, hexc('#2B2B3A'), 7)
        cr.move_to(sx * 70 - 35, -25); cr.line_to(sx * 70 - 5, -25); stroke_dev(cr, (1, 1, 1), 6, 0.7)
    cr.move_to(-12, -15); cr.curve_to(-5, -30, 5, -30, 12, -15); stroke_dev(cr, OUT, 9)
    cr.restore()

def it_beanie(cr, t, s=1.0):
    cr.save(); cr.scale(s, s)
    cr.move_to(-110, 30); cr.curve_to(-110, -120, 110, -120, 110, 30); cr.close_path(); fs(cr, hexc('#FF5A5F'))
    for x in (-60, -20, 20, 60):
        cr.move_to(x, -70); cr.line_to(x, 20); stroke_dev(cr, hexc('#E03E45'), 5)
    rrect(cr, -120, 10, 240, 50, 22); fs(cr, (1, 1, 1))
    cr.arc(0, -105, 32, 0, 2 * math.pi); fs(cr, (1, 1, 1))
    cr.restore()

def it_scarf(cr, t, s=1.0):
    cr.save(); cr.scale(s, s)
    rrect(cr, -110, -30, 220, 50, 22); fs(cr, hexc('#3ECF5E'))
    rrect(cr, 40, -10, 50, 120, 18); fs(cr, hexc('#3ECF5E'))
    for y in (55, 80): cr.move_to(42, y); cr.line_to(88, y); stroke_dev(cr, (1, 1, 1), 6)
    cr.restore()

def it_umbrella(cr, t, s=1.0):
    cr.save(); cr.scale(s, s)
    cr.move_to(0, -10); cr.line_to(0, 140); cr.arc_negative(-22, 140, 22, 0, math.pi); stroke_dev(cr, OUT, 14)
    cr.move_to(0, -10); cr.line_to(0, 140); cr.arc_negative(-22, 140, 22, 0, math.pi); stroke_dev(cr, hexc('#8A5D39'), 7)
    cr.move_to(-150, -10)
    for k in range(4): cr.curve_to(-150 + k * 75 + 20, -40, -150 + k * 75 + 55, -40, -150 + (k + 1) * 75, -10)
    cr.curve_to(150, -120, -150, -120, -150, -10); cr.close_path()
    p = cr.copy_path(); fs(cr, hexc('#A15CFF'))
    cr.save(); cr.append_path(p); cr.clip()
    for k in (-1, 1): cr.move_to(0, -95); cr.curve_to(k * 40, -70, k * 70, -40, k * 75, -10); stroke_dev(cr, hexc('#7D3BE0'), 5)
    cr.restore()
    cr.arc(0, -98, 9, 0, 2 * math.pi); fs(cr, hexc('#FFD93B'), 4)
    cr.restore()

def it_ball(cr, t, s=1.0):
    cr.save(); cr.scale(s, s)
    cr.arc(0, 0, 110, 0, 2 * math.pi); fs(cr, (1, 1, 1))
    for k, c in enumerate(['#FF4D4D', '#FFD21F', '#2EA7FF']):
        cr.save(); cr.arc(0, 0, 107, 0, 2 * math.pi); cr.clip()
        cr.move_to(0, 0); cr.arc(0, 0, 120, k * 2.09 - 0.5, k * 2.09 + 0.55); cr.close_path(); cr.set_source_rgb(*hexc(c)); cr.fill(); cr.restore()
    cr.arc(0, 0, 110, 0, 2 * math.pi); stroke_dev(cr, OUT, 6)
    ellipse(cr, -40, -50, 22, 14); cr.set_source_rgba(1, 1, 1, 0.6); cr.fill()
    cr.restore()

def it_swimring(cr, t, s=1.0):
    cr.save(); cr.scale(s, s)
    cr.arc(0, 0, 115, 0, 2 * math.pi); cr.arc_negative(0, 0, 55, 2 * math.pi, 0); cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    cr.set_source_rgb(*hexc('#FF7EB6')); cr.fill_preserve(); cr.set_fill_rule(cairo.FILL_RULE_WINDING); stroke_dev(cr, OUT, 6)
    for k in range(4):
        cr.save(); cr.rotate(k * math.pi / 2 + 0.4)
        cr.move_to(58, -20); cr.line_to(112, -28); cr.line_to(112, 28); cr.line_to(58, 20); cr.close_path(); cr.set_source_rgb(1, 1, 1); cr.fill(); cr.restore()
    cr.arc(0, 0, 115, 0, 2 * math.pi); stroke_dev(cr, OUT, 6); cr.arc(0, 0, 55, 0, 2 * math.pi); stroke_dev(cr, OUT, 6)
    cr.restore()

def it_beanie_scarf(cr, t, s=1.0):
    cr.save(); cr.translate(0, -40); it_beanie(cr, t, 0.75 * s); cr.restore()
    cr.save(); cr.translate(0, 90); it_scarf(cr, t, 0.75 * s); cr.restore()

ITEMS = dict(glasses=it_glasses, beanie=it_beanie_scarf, umbrella=it_umbrella, ball=it_ball, swimring=it_swimring)


# ---------------- wearing (body space) ----------------
def wear_beanie(cr, t):
    cr.save(); cr.translate(0, -320); it_beanie(cr, t, 0.78); cr.restore()

def wear_scarf(cr, t):
    cr.save(); cr.translate(0, -172)
    cr.move_to(-112, -20); cr.curve_to(-60, 10, 60, 10, 112, -20); cr.line_to(108, 22); cr.curve_to(60, 50, -60, 50, -108, 22); cr.close_path()
    fs(cr, hexc('#3ECF5E'))
    rrect(cr, 50, 10, 46, 110, 16); fs(cr, hexc('#3ECF5E'))
    for y in (70, 92): cr.move_to(52, y); cr.line_to(94, y); stroke_dev(cr, (1, 1, 1), 5)
    cr.restore()

def wear_umbrella(cr, t):
    cr.save(); cr.translate(150, -380); cr.rotate(0.1 + 0.03 * math.sin(t * 2)); it_umbrella(cr, t, 1.15); cr.restore()


# ---------------- room & window ----------------
def room(cr, t):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, *hexc('#CFEFFF')); g.add_color_stop_rgb(1, *hexc('#E9F7FF'))
    cr.set_source(g); cr.paint()
    for x in range(0, W, 90):
        cr.rectangle(x, 0, 45, 1560); cr.set_source_rgba(1, 1, 1, 0.35); cr.fill()
    cr.rectangle(0, 1560, W, H - 1560); cr.set_source_rgb(*hexc('#E3B47A')); cr.fill()
    for x in range(-200, W, 160): cr.move_to(x, 1560); cr.line_to(x + 260, H); stroke_dev(cr, hexc('#C9965A'), 4, 0.6)
    cr.move_to(0, 1560); cr.line_to(W, 1560); stroke_dev(cr, OUT, 6)
    ellipse(cr, 540, 1800, 380, 70); fs(cr, hexc('#FF9EBB'), 6)
    ellipse(cr, 540, 1800, 300, 50); stroke_dev(cr, (1, 1, 1), 5, 0.6)

def weather_view(cr, kind, t, a=1.0):
    if a <= 0: return
    cr.push_group()
    if kind == 'sunny':
        g = cairo.LinearGradient(0, WY, 0, WY + WH); g.add_color_stop_rgb(0, *hexc('#3FB4FF')); g.add_color_stop_rgb(1, *hexc('#BFEBFF')); cr.set_source(g); cr.paint()
        cr.save(); cr.translate(WX + 560 - 870 * 0.8, WY + 200 - 270 * 0.8); cr.scale(0.8, 0.8); draw_sun(cr, t); cr.restore()
        hills(cr, WY + WH - 120, '#7CD35F', 30)
    elif kind == 'rainy':
        g = cairo.LinearGradient(0, WY, 0, WY + WH); g.add_color_stop_rgb(0, *hexc('#7D8CA3')); g.add_color_stop_rgb(1, *hexc('#B9C4D3')); cr.set_source(g); cr.paint()
        hills(cr, WY + WH - 120, '#5FA35A', 30)
        for x0, y0, sp in RAIN:
            x = WX + x0 * WW; y = WY + ((y0 + t * 1.3 * sp) % 1) * WH
            cr.move_to(x, y); cr.line_to(x - 12, y + 40); stroke_dev(cr, hexc('#E6F4FF'), 5)
        for x, y, s in ((WX + 220, WY + 130, 0.55), (WX + 560, WY + 170, 0.6)):
            draw_cloud(cr, x + 20 * math.sin(t * 0.6), y, s, hexc('#9AA6B8'), True, 0.0)
    elif kind == 'snowy':
        g = cairo.LinearGradient(0, WY, 0, WY + WH); g.add_color_stop_rgb(0, *hexc('#9FC3E6')); g.add_color_stop_rgb(1, *hexc('#E8F3FF')); cr.set_source(g); cr.paint()
        hills(cr, WY + WH - 140, '#FFFFFF', 30)
        for k, x in enumerate((WX + 160, WX + 600)):
            cr.move_to(x, WY + WH - 120); cr.line_to(x - 60, WY + WH - 40); cr.line_to(x + 60, WY + WH - 40); cr.close_path(); fs(cr, hexc('#2E8B57'))
        for x0, y0, r, ph in SNOW:
            x = WX + x0 * WW + 18 * math.sin(t * 1.5 + ph); y = WY + ((y0 + t * 0.18) % 1) * WH
            cr.arc(x, y, r, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()
    elif kind == 'crazy':
        g = cairo.LinearGradient(0, WY, 0, WY + WH); g.add_color_stop_rgb(0, *hexc('#5DBBFF')); g.add_color_stop_rgb(1, *hexc('#DDF3FF')); cr.set_source(g); cr.paint()
        cx, cy = WX + WW / 2, WY + WH + 60
        for k, c in enumerate(['#FF4D4D', '#FF9A1F', '#FFD93B', '#3ECF5E', '#2EA7FF', '#A15CFF']):
            cr.arc(cx, cy, 470 - k * 34, math.pi, 2 * math.pi); stroke_dev(cr, hexc(c), 34)
        cr.save(); cr.translate(WX + 120 - 870 * 0.55, WY + 140 - 270 * 0.55); cr.scale(0.55, 0.55); draw_sun(cr, t); cr.restore()
        draw_cloud(cr, WX + 600, WY + 140, 0.5, hexc('#9AA6B8'), True, 0)
        for x0, y0, sp in RAIN[:25]:
            x = WX + 450 + x0 * 300; y = WY + 200 + ((y0 + t * 1.3 * sp) % 1) * (WH - 200)
            cr.move_to(x, y); cr.line_to(x - 10, y + 34); stroke_dev(cr, hexc('#E6F4FF'), 5)
        for x0, y0, r, ph in SNOW[:25]:
            x = WX + x0 * WW + 18 * math.sin(t * 1.5 + ph); y = WY + ((y0 + t * 0.18) % 1) * WH
            cr.arc(x, y, r, 0, 2 * math.pi); cr.set_source_rgb(1, 1, 1); cr.fill()
    cr.pop_group_to_source(); cr.paint_with_alpha(a)

def window(cr, t, kinds):
    cr.save(); rrect(cr, WX, WY, WW, WH, 40); cr.clip()
    for k, a in kinds: weather_view(cr, k, t, a)
    cr.restore()
    rrect(cr, WX, WY, WW, WH, 40); stroke_dev(cr, OUT, 34); rrect(cr, WX, WY, WW, WH, 40); stroke_dev(cr, (1, 1, 1), 22)
    cr.move_to(WX + WW / 2, WY); cr.line_to(WX + WW / 2, WY + WH); cr.move_to(WX, WY + WH / 2); cr.line_to(WX + WW, WY + WH / 2)
    stroke_dev(cr, OUT, 26); cr.move_to(WX + WW / 2, WY); cr.line_to(WX + WW / 2, WY + WH); cr.move_to(WX, WY + WH / 2); cr.line_to(WX + WW, WY + WH / 2)
    stroke_dev(cr, (1, 1, 1), 14)
    rrect(cr, WX - 40, WY + WH - 10, WW + 80, 40, 14); fs(cr, (1, 1, 1))
    # curtains
    for side in (-1, 1):
        x = WX - 70 if side < 0 else WX + WW + 70
        cr.move_to(x - 70 * side * -1, WY - 60); cr.curve_to(x + side * 10, WY + 200, x - side * 40, WY + 420, x, WY + WH + 60)
        cr.line_to(x + side * 70, WY + WH + 60); cr.line_to(x + side * 70, WY - 60); cr.close_path(); fs(cr, hexc('#FF8CC0'))
    rrect(cr, WX - 120, WY - 80, WW + 240, 36, 18); fs(cr, hexc('#C88A55'))


def card(cr, x, y, item, t, glow_a=0.0, dim=0.0, shake=0.0, s=1.0):
    if s <= 0.01: return
    cr.save(); cr.translate(x + shake, y); cr.scale(s, s)
    if glow_a > 0: glow(cr, 0, 0, 260, (1, 0.95, 0.5), glow_a)
    cr.push_group()
    rrect(cr, -170, -170, 340, 340, 50); fs(cr, (1, 1, 1), 7)
    rrect(cr, -154, -154, 308, 308, 40); stroke_dev(cr, hexc('#FFD93B'), 7, 0.8)
    cr.save(); cr.scale(0.95, 0.95); ITEMS[item](cr, t); cr.restore()
    cr.pop_group_to_source(); cr.paint_with_alpha(1 - dim)
    cr.restore()


def frame(cr, t):
    m = TL['marks']
    te = 0.0 if t >= m['loop'] else t
    room(cr, t)
    ri = 0
    for i in range(3):
        if te >= m[f's{i}']: ri = i
    kinds = []
    if te < m['crazy']:
        for i, r in enumerate(ROUNDS):
            a = smooth(m[f's{i}'], m[f's{i}'] + 0.6, te) if i else 1.0
            if i < 2: a *= 1 - smooth(m[f's{i + 1}'], m[f's{i + 1}'] + 0.6, te)
            if a > 0: kinds.append((r['w'], a))
    else:
        kinds = [('snowy', 1 - smooth(m['crazy'], m['crazy'] + 0.6, te)), ('crazy', smooth(m['crazy'], m['crazy'] + 0.6, te))]
    window(cr, t, kinds)
    # weather word on the window sill
    for i, r in enumerate(ROUNDS):
        word_pop(cr, r['word'], 540, WY + WH - 80, 120, r['c'], m[f's{i}'] + (0.3 if i else 0.2), m[f'x{i}'], te)
    # cards
    if te < m['crazy']:
        r = ROUNDS[ri]
        app = ease_out_back((te - m[f's{ri}'] - 0.2) / 0.5) if ri else ease_out_back((te + 0.3) / 0.5)
        leave = smooth(m[f'x{ri}'], m[f'x{ri}'] + 0.35, te)
        for j, (x, y) in enumerate(CARDS):
            isans = j == r['ans']; rv = smooth(m[f'r{ri}'], m[f'r{ri}'] + 0.3, te)
            if isans:
                fly = smooth(m[f'r{ri}'] + 0.45, m[f'r{ri}'] + 0.9, te)
                if fly < 1:
                    card(cr, lerp(x, 540, fly), lerp(y, 1500, fly), r['opts'][j], te, 0.55 * rv * (1 - fly), 0, 0, app * (1 - leave) * (1 - 0.6 * fly))
            else:
                sh = 14 * math.sin(te * 40) * burst(m[f'r{ri}'], m[f'r{ri}'] + 0.4, te)
                card(cr, x, y, r['opts'][j], te, 0, 0.65 * rv, sh, app * (1 - leave))
    # chickpea wearing things
    accs = []; extra = []
    if te >= m['r0'] + 0.85: accs.append('glasses')
    if m['r1'] + 0.85 <= te: extra.append(wear_umbrella)
    if m['r2'] + 0.85 <= te: extra.append(wear_scarf); extra.append(wear_beanie)
    if m['x0'] <= te < m['all'] and 'glasses' in accs: accs.remove('glasses')
    if m['x1'] <= te < m['all'] and wear_umbrella in extra: extra.remove(wear_umbrella)
    if te >= m['all']:
        accs = ['glasses']; extra = [wear_umbrella, wear_scarf, wear_beanie]
    st = chick_talk(base_st(), te, TL); look = (0.0, -0.5); h = 0; sx = sy = 1
    for i in range(3):
        if m[f'c{i}'] <= te < m[f'r{i}']: look = (math.sin(te * 2.2), 0.6)
        if m[f'r{i}'] + 0.85 <= te < m[f'r{i}'] + 1.75:
            h, sx, sy, air = hop_seq(te, m[f'r{i}'] + 0.85, 2, 0.45, 55); st.update(happy=1, wing=[0.3 + 0.8 * air] * 2)
    if m['crazy'] <= te < m['all']: st['mood'] = 0.0; look = (0.0, -0.9)
    if te >= m['all']:
        st['happy'] = 1
        if te < m['all'] + 0.9: h, sx, sy, air = hop_seq(te, m['all'], 2, 0.45, 60)
    shadow_at(cr, 540, 1803, 110)
    def ex(c, tt_):
        for f in extra: f(c, tt_)
    chick(cr, 540, 1800, h, 0.8, st, te, look, sx, sy, acc=accs, extra=ex)
    for i in range(3):
        sparkles(cr, 540, 1550, m[f'r{i}'] + 0.85, te)
    sparkles(cr, 540, 1550, m['all'], te, 9)
    for i in range(3): count_bubble(cr, m[f'c{i}'], te, "Point to it!", y=420, w=560)
    word_pop(cr, "Silly!", 540, WY + WH - 80, 140, '#A15CFF', m['all'] + 0.6, m['again'] + 0.3, te)
    draw_text(cr, "What Should I Wear?", 250, 120, t, -1)
    loop_fade(cr, TL, t)

if __name__ == '__main__': episode_main(build, F)
