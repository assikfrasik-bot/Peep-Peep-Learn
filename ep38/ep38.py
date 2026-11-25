"""Paint the Rainbow! — red, orange... which color comes next? Twist: Chickpea slides down the finished rainbow!"""
import sys; sys.path.insert(0, '/home/claude/kit')
from common import *

F = '/home/claude/ep38'
RCX, RCY = 540, 1250
R0, BW = 470, 56
COLS = [('red', '#FF4D4D'), ('orange', '#FF9A1F'), ('yellow', '#FFD93B'), ('green', '#3ECF5E'), ('blue', '#2EA7FF'), ('purple', '#A15CFF')]
CX3 = [420, 660, 900]
CY3 = 1540
ROUNDS = [dict(band=2, opts=[3, 2, 4], ans=1), dict(band=4, opts=[4, 0, 2], ans=0), dict(band=5, opts=[1, 3, 5], ans=2)]


def build():
    s = Script(F); t = 0.1
    s.mark('b0', 0.15); s.mark('b1', 0.9)
    t = s.say(t, 'hook', "Let's paint a rainbow! Red... orange...") + 0.1
    for i, r in enumerate(ROUNDS):
        if i == 1:
            s.mark('b3', t); t = s.say(t, 'green', "Green!", 1.0, True) + 0.3
        s.mark(f's{i}', t)
        t = s.say(t, f'q{i}', "What color comes next?") + 0.05
        s.mark(f'c{i}', t); t += 3.0; s.mark(f'r{i}', t)
        t = s.say(t + 0.4, f'a{i}', COLS[r['band']][0].capitalize() + "!") + 0.1
        s.mark(f'b{r["band"]}', t - 0.5)
        s.mark(f'x{i}', t + 0.3); t += 0.6
    t = s.say(t, 'done', "We made a rainbow!") + 0.1
    s.mark('tw', t)
    t = s.say(t, 'slide', "Rainbow slide! Wheee!", 1.0, True) + 0.05
    s.mark('land', t + 0.6); t += 1.0
    t = s.say(t, 'soft', "So soft! Hee hee!", 1.0, True) + 0.25
    s.mark('again', t); t = s.say(t, 'again', "Again?", 1.0, True) + 0.25
    s.mark('loop', t); t += 0.9
    tl = s.save(t); m = tl['marks']; mx = Mix(tl['dur'])
    mx.music_loop(0, tl['dur'], 108, [([60, 64, 67], 36), ([65, 69, 72], 41), ([57, 60, 64], 45), ([67, 71, 74], 43)],
                  [[72, None, 74, None, 76, None, 77, None], [79, None, 81, None, 84, None, None, None]], 'soft', 0.75)
    for k in range(6): mx.add('sfx', m[f'b{k}'], bell(mtof(72 + [0, 2, 4, 5, 7, 9][k]), 0.9), 0.3)
    for i in range(3):
        mx.add('sfx', m[f's{i}'] + 0.1, pop(300, 900, 0.12), 0.2)
        countdown_ticks(mx, m[f'c{i}'])
        mx.add('sfx', m[f'r{i}'], ding(), 0.2); mx.add('sfx', m[f'r{i}'] + 0.15, whoosh(0.5), 0.12)
    mx.add('sfx', m['tw'] + 0.3, slide_whistle(1400, 500, 1.6), 0.2)
    mx.add('sfx', m['land'], boing(), 0.3); mx.add('sfx', m['land'] + 0.2, tada(72), 0.15)
    mx.add('sfx', m['again'] + 0.2, jingle(), 0.22)
    mx.voices(F, tl['events'])
    mx.write(F + '/audio.wav', quiet=[(m[f'c{i}'], m[f'r{i}']) for i in range(3)]); return tl


TL = json.load(open(F + '/timeline.json')) if os.path.exists(F + '/timeline.json') else None


def band(cr, k, p):
    if p <= 0.01: return
    r = R0 - k * BW
    a0 = math.pi; a1 = math.pi + math.pi * p
    cr.arc(RCX, RCY, r, a0, a1); stroke_dev(cr, OUT, BW + 8, cap=cairo.LINE_CAP_BUTT)
    cr.arc(RCX, RCY, r, a0, a1); stroke_dev(cr, hexc(COLS[k][1]), BW - 4, cap=cairo.LINE_CAP_BUTT)
    cr.arc(RCX, RCY, r - BW * 0.25, a0, a1); stroke_dev(cr, (1, 1, 1), 5, 0.25, cap=cairo.LINE_CAP_BUTT)

def bucket(cr, x, y, col, s, name, glow_a=0.0, dim=0.0):
    if s <= 0.01: return
    cr.push_group(); cr.save(); cr.translate(x, y); cr.scale(s, s)
    if glow_a > 0: glow(cr, 0, -40, 200, hexc(col), glow_a)
    cr.arc(0, -120, 95, math.pi * 1.05, math.pi * 1.95); stroke_dev(cr, OUT, 8)
    cr.move_to(-110, -100); cr.line_to(110, -100); cr.line_to(90, 60); cr.line_to(-90, 60); cr.close_path(); fs(cr, hexc('#E8EEF5'))
    ellipse(cr, 0, -100, 110, 26); fs(cr, hexc(col))
    cr.move_to(-60, -100); cr.curve_to(-60, -40, -30, -40, -30, -70); cr.curve_to(-30, -100, -60, -100, -60, -100); cr.close_path(); cr.set_source_rgb(*hexc(col)); cr.fill()
    cr.restore()
    big_word(cr, name.upper(), x, y + 10 * s, 40 * s, hexc(col), 1.0)
    cr.pop_group_to_source(); cr.paint_with_alpha(1 - 0.6 * dim)

def cloud_big(cr, x, y, s, t):
    draw_cloud(cr, x, y, s, (1, 1, 1), True, 1.0)


def frame(cr, t):
    m = TL['marks']
    te = 0.0 if t >= m['loop'] else t
    sky(cr, '#8FD8FF', '#F2FBFF', 1450)
    clouds(cr, t, ((830, 420, 0.4), (200, 520, 0.34)))
    small_sun(cr, t, 940, 600, 0.45)
    hills(cr, 1320, '#A6E58A', 50); ground(cr, 1380)
    # clouds at the rainbow's feet
    for x in (RCX - R0 + 2.5 * BW, RCX + R0 - 2.5 * BW):
        draw_cloud(cr, x, RCY + 30, 0.9, (1, 1, 1), True, 0.0)
    # bands drawn so far
    for k in range(6):
        mk = f'b{k}'
        if mk in m and te >= m[mk]: band(cr, k, ease_io(clamp((te - m[mk]) / 0.7)))
    # mark the next band slot
    for i, r in enumerate(ROUNDS):
        if m[f's{i}'] <= te < m[f'b{r["band"]}']:
            rr = R0 - r['band'] * BW
            cr.set_dash([18, 14]); cr.arc(RCX, RCY, rr, math.pi, 2 * math.pi); stroke_dev(cr, OUT, 5, 0.5); cr.set_dash([])
            big_word(cr, "?", RCX, RCY - rr - 6, 70, hexc('#A15CFF'), 1.0, 0.1 * math.sin(te * 3))
    # buckets
    ri = None
    for i in range(3):
        if m[f's{i}'] <= te < m[f'x{i}'] + 0.4: ri = i
    if ri is not None:
        r = ROUNDS[ri]; rv = m[f'r{ri}']; x0 = m[f'x{ri}']
        for j, ci in enumerate(r['opts']):
            a = ease_out_back(clamp((te - m[f's{ri}'] - j * 0.1) / 0.4), 1.6) * (1 - smooth(x0, x0 + 0.35, te))
            correct = j == r['ans']
            bucket(cr, CX3[j], CY3, COLS[ci][1], a * (1 + 0.1 * burst(rv, rv + 0.5, te) * correct), COLS[ci][0],
                   0.7 * burst(rv, rv + 0.8, te) * correct, smooth(rv, rv + 0.3, te) * (not correct))
        # paint splash flying up to the rainbow
        bk = m[f'b{r["band"]}']
        if rv + 0.1 <= te < bk + 0.2:
            u = ease_io(clamp((te - rv - 0.1) / (bk - rv - 0.1)))
            rr = R0 - r['band'] * BW
            x = lerp(CX3[r['ans']], RCX - rr, u); y = lerp(CY3 - 100, RCY, u) - 300 * math.sin(math.pi * u)
            cr.arc(x, y, 30, 0, 2 * math.pi); fs(cr, hexc(COLS[r['band']][1]))
        if te >= bk: sparkles(cr, RCX, RCY - (R0 - r['band'] * BW), bk, te, 8, 120, 220)
    # chickpea
    st = chick_talk(base_st(), te, TL); h = 0; sx = sy = 1; look = (0.6, -0.9); rot = 0
    cx, cby, sc = 160, 1820, 0.72
    for i in range(3):
        if m[f'c{i}'] <= te < m[f'r{i}']: look = (0.5 + 0.3 * math.sin(te * 2), -0.8)
        if m[f'r{i}'] + 0.4 <= te < m[f'r{i}'] + 1.3:
            h, sx, sy, air = hop_seq(te, m[f'r{i}'] + 0.4, 2, 0.45, 50); st.update(happy=1, wing=[0.3 + 0.8 * air] * 2)
    if te >= m['tw']:
        tw, ld = m['tw'], m['land']
        u0 = ease_io(clamp((te - tw) / 0.5))
        if te < tw + 0.5:
            cx = lerp(160, RCX - R0 + 20, u0); cby = lerp(1820, RCY - 30, u0) - 250 * math.sin(math.pi * u0); sc = lerp(0.72, 0.5, u0)
        elif te < ld:
            u = clamp((te - tw - 0.5) / (ld - tw - 0.5)); a = math.pi + math.pi * (u ** 1.3)
            rr = R0 + 25
            cx = RCX + rr * math.cos(a); cby = RCY + rr * math.sin(a) - 10; sc = 0.5; rot = 0.7 * (a - 1.5 * math.pi)
            st.update(happy=1, wing=[1.0, 1.0])
        else:
            uu = clamp((te - ld) / 0.4)
            cx = RCX + R0 - 2.5 * BW; cby = RCY + 10 + 30 * (1 - uu); sc = 0.55
            sq = burst(ld, ld + 0.4, te); sx = 1 + 0.2 * sq; sy = 1 - 0.2 * sq
            st.update(happy=1, wing=[0.6 + 0.4 * math.sin(te * 9)] * 2)
        if te >= ld: confetti(cr, ld, te, RCX + R0 - 2.5 * BW, RCY - 200, 500)
    if te < m['tw']: shadow_at(cr, cx, cby + 3, 100)
    chick(cr, cx, cby, h, sc, st, te, look, sx, sy, acc='beret', rot=rot)
    for i, r in enumerate(ROUNDS):
        count_bubble(cr, m[f'c{i}'], te, "Say it!", y=470)
        cn, ch = COLS[r['band']]
        word_pop(cr, cn.capitalize() + "!", 540, 480, 130, ch, m[f'r{i}'] + 0.4, m[f'x{i}'] + 0.3, te)
    word_pop(cr, "Wheee!", 540, 480, 150, '#FF5FA2', m['tw'] + 0.5, m['again'] + 0.3, te, 0.1)
    draw_text(cr, "Paint the Rainbow!", 250, 112, t, -1)
    loop_fade(cr, TL, t)

if __name__ == '__main__': episode_main(build, F)
