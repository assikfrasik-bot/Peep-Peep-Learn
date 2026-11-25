import cairo, math, random
from anim import *
W2, H2 = 2048, 1152
SAFE = (406, 407, 1641, 745)  # x0,y0,x1,y1
surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2, H2); cr = cairo.Context(surf)
rr = random.Random(11)

def hill(f, col_top, col_bot, y0):
    cr.move_to(0, H2)
    for x in range(0, W2 + 21, 16): cr.line_to(x, f(x))
    cr.line_to(W2, H2); cr.close_path()
    g = cairo.LinearGradient(0, y0, 0, H2); g.add_color_stop_rgb(0, *hexc(col_top)); g.add_color_stop_rgb(1, *hexc(col_bot))
    cr.set_source(g); cr.fill()

def tree(x, y, s, col):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.rectangle(-16, -120, 32, 120); fs(cr, hexc('#9B6B43'))
    blobs = [(-55, -150, 62), (55, -150, 62), (0, -205, 72), (0, -140, 60)]
    for bx, by, r in blobs: cr.arc(bx, by, r, 0, 2*math.pi); cr.new_sub_path()
    stroke_dev(cr, OUT, 12)
    for bx, by, r in blobs: cr.arc(bx, by, r, 0, 2*math.pi); cr.new_sub_path()
    cr.set_source_rgb(*hexc(col)); cr.fill()
    for bx, by, r in ((-30, -215, 18), (40, -170, 14), (-60, -150, 12)):
        cr.arc(bx, by, r, 0, 2*math.pi); cr.set_source_rgba(1, 1, 1, 0.25); cr.fill()
    for ax, ay in ((-40, -130), (35, -200), (20, -120)):
        cr.arc(ax, ay, 11, 0, 2*math.pi); fs(cr, hexc('#FF5A5F'), 4)
    cr.restore()

def balloon(x, y, col, s=1.0):
    cr.save(); cr.translate(x, y); cr.scale(s, s)
    cr.move_to(0, 70); cr.curve_to(-20, 120, 20, 160, -5, 230); stroke_dev(cr, OUT, 3)
    ellipse(cr, 0, 0, 55, 68); fs(cr, hexc(col))
    cr.move_to(-8, 66); cr.line_to(8, 66); cr.line_to(0, 80); cr.close_path(); fs(cr, hexc(col), 4)
    ellipse(cr, -20, -25, 12, 20); cr.set_source_rgba(1, 1, 1, 0.5); cr.fill()
    cr.restore()

def block(x, y, sz, col, letter):
    d = sz * 0.28
    cr.move_to(x, y - sz); cr.line_to(x + d, y - sz - d); cr.line_to(x + sz + d, y - sz - d); cr.line_to(x + sz, y - sz); cr.close_path()
    fs(cr, mixc(hexc(col), (1, 1, 1), 0.35))
    cr.move_to(x + sz, y); cr.line_to(x + sz, y - sz); cr.line_to(x + sz + d, y - sz - d); cr.line_to(x + sz + d, y - d); cr.close_path()
    fs(cr, mixc(hexc(col), (0, 0, 0), 0.2))
    cr.rectangle(x, y - sz, sz, sz); fs(cr, hexc(col))
    cr.rectangle(x + 10, y - sz + 10, sz - 20, sz - 20); stroke_dev(cr, (1, 1, 1), 4, 0.7)
    cr.select_font_face("Nunito ExtraLight"); cr.set_font_size(sz * 0.72)
    e = cr.text_extents(letter)
    cr.move_to(x + sz/2 - e.width/2 - e.x_bearing, y - sz/2 - e.height/2 - e.y_bearing); cr.text_path(letter)
    cr.set_source_rgb(1, 1, 1); cr.fill_preserve(); stroke_dev(cr, OUT, 4)

def title(text, cx, cy, size, maxw, cols, outline=18):
    cr.select_font_face("Nunito ExtraLight"); cr.set_font_size(size)
    advs = [cr.text_extents(ch).x_advance for ch in text]; tot = sum(advs)
    k = min(1, maxw / tot); cr.set_font_size(size * k); advs = [a * k for a in advs]; tot *= k
    x = cx - tot / 2; paths = []
    ci = 0
    for i, ch in enumerate(text):
        if ch != ' ':
            cr.save(); cr.translate(x + advs[i]/2, cy + 10*math.sin(i*0.9)); cr.rotate(0.05*math.sin(i*1.7))
            cr.move_to(-advs[i]/2, size*k*0.36); cr.text_path(ch); cr.restore()
            paths.append((cr.copy_path(), cols[ci % len(cols)])); cr.new_path(); ci += 1
        x += advs[i]
    for p, c in paths:  # shadow
        cr.save(); cr.translate(6, 10); cr.append_path(p); cr.restore()
    stroke_dev(cr, (0.15, 0.1, 0.3), outline + 6, 0.35)
    for p, c in paths: cr.append_path(p)
    stroke_dev(cr, hexc('#3B2A6B'), outline)
    for p, c in paths:
        cr.append_path(p); cr.set_source_rgb(*c); cr.fill()
        cr.save(); cr.append_path(p); cr.clip()
        cr.rectangle(0, cy - size*k*0.5, W2, size*k*0.22); cr.set_source_rgba(1, 1, 1, 0.28); cr.fill()
        cr.restore()

# ---- sky
g = cairo.LinearGradient(0, 0, 0, 900)
g.add_color_stop_rgb(0, *hexc('#3FB4FF')); g.add_color_stop_rgb(0.6, *hexc('#8ADCFF')); g.add_color_stop_rgb(1, *hexc('#D8F6FF'))
cr.set_source(g); cr.paint()
# soft rays from sun
cr.save(); cr.translate(230, 190)
for i in range(18):
    a = i * 2*math.pi/18
    cr.move_to(0, 0); cr.arc(0, 0, 2400, a, a + math.pi/36); cr.close_path()
cr.set_source_rgba(1, 1, 1, 0.08); cr.fill(); cr.restore()
# rainbow
for i, c in enumerate(['#FF5A5F', '#FF9F1C', '#FFE14D', '#3ECF8E', '#2EA7FF', '#A66CFF']):
    cr.arc(1024, 1250, 980 - i*52, math.pi, 2*math.pi); stroke_dev(cr, hexc(c), 54, 0.55, cairo.LINE_CAP_BUTT)
# sun
cr.save(); cr.translate(-640, -80); cr.scale(1.0, 1.0); draw_sun(cr, 0.3); cr.restore()
# clouds
for x, y, s in ((560, 170, 0.75), (1380, 120, 0.6), (1830, 300, 0.8), (90, 470, 0.55), (1990, 560, 0.5), (980, 300, 0.45)):
    draw_cloud(cr, x, y, s, (1, 1, 1), outline=False)
# balloons (decor, outside safe)
balloon(1880, 150, '#FF5A5F', 0.95); balloon(1975, 230, '#FFB400', 0.8); balloon(1790, 260, '#2EA7FF', 0.75)
# hills
hill(lambda x: 700 - 90*math.sin(math.pi*x/W2*1.6 + 0.3), '#A6E58A', '#7FCF63', 600)
for x, s, c in ((120, 1.0, '#4CB944'), (300, 0.75, '#5DC85A'), (1760, 0.8, '#4CB944'), (1950, 1.05, '#5DC85A')):
    tree(x, 690 - 90*math.sin(math.pi*x/W2*1.6 + 0.3) + 40, s, c)
fy = lambda x: 770 - 22*math.sin(2*math.pi*x/W2*1.2 + 1.2)
hill(fy, '#62C64C', '#3E9E3A', 740)
for x in range(-10, W2 + 10, 12):
    y = fy(x) + 4; h = rr.uniform(26, 50); sw = rr.uniform(-6, 6)
    cr.move_to(x - 7, y); cr.line_to(x + sw, y - h); cr.line_to(x + 7, y); cr.close_path()
cr.set_source_rgb(*hexc('#4DB23C')); cr.fill()
fcols = ['#FF5A5F', '#FFFFFF', '#A66CFF', '#FFB400', '#FF7EB6', '#2EA7FF']
for i, x in enumerate(list(range(40, 380, 70)) + list(range(1690, 2040, 70)) + [700, 1360]):
    draw_flower(cr, x, fy(x) + 50 + (i % 3) * 25, 0.9 + 0.1*(i % 2), hexc(fcols[i % 6]), 0, i * 1.3)
for i, x in enumerate(range(80, 2000, 160)):
    draw_flower(cr, x + rr.uniform(-30, 30), rr.uniform(960, 1130), rr.uniform(0.9, 1.25), hexc(fcols[(i+2) % 6]), 0, i * 0.9)

# ---- safe-zone content
# chickpea left
st = dict(x=0, h=0, sx=1, sy=1, rot=0, phase='chick', crack=0, hatch=1, mood=0,
          wing=[0.4, 1.3], beak=0.8, happy=0, shiver=0, by=0)
cr.save(); cr.translate(535, 742); cr.scale(0.84, 0.84)
draw_body(cr, 0, -215, 1.0, st, 1.0, (0.5, -0.15)); shell_part(cr, top=False)
cr.restore()
# blocks right
block(1405, 742, 92, '#FF5A5F', 'A'); block(1500, 742, 92, '#2EA7FF', 'B'); block(1452, 650, 92, '#3ECF8E', 'C')
draw_bfly(cr, 1545, 515, 0.05, 0.3, 0.8)
for x, y, r in ((700, 450, 20), (1330, 440, 16), (1610, 690, 14), (460, 440, 14)):
    star(cr, x, y, r); cr.set_source_rgb(1, 1, 0.85); cr.fill()
# title + tagline
title("Chickpea & Friends", 1025, 530, 150, 740, TITLE_COLS)
cr.select_font_face("Nunito ExtraLight"); cr.set_font_size(44)
tag = "Colors, Numbers, ABC & Fun!"
e = cr.text_extents(tag); pw, ph = e.x_advance + 70, 74
px, py = 1025 - pw/2, 640
cr.new_sub_path(); r = ph/2
cr.arc(px + r, py + r, r, math.pi/2, 3*math.pi/2); cr.arc(px + pw - r, py + r, r, -math.pi/2, math.pi/2); cr.close_path()
fs(cr, (1, 1, 1), 6, hexc('#3B2A6B'))
cr.move_to(1025 - e.x_advance/2, py + ph/2 + 15); cr.set_source_rgb(*hexc('#3B2A6B')); cr.show_text(tag)
surf.write_to_png('chickpea_banner.png')
