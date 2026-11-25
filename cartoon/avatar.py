import cairo, math
from anim import *
S = 800
surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, S, S); cr = cairo.Context(surf)
cx, cy = S/2, S/2
# sunburst background
cr.set_source_rgb(*hexc('#4FC3FF')); cr.paint()
cr.save(); cr.translate(cx, cy*0.95)
for i in range(16):
    a = i * 2*math.pi/16
    cr.move_to(0, 0); cr.arc(0, 0, 900, a, a + math.pi/16); cr.close_path()
cr.set_source_rgb(*hexc('#7DD8FF')); cr.fill()
g = cairo.RadialGradient(0, 0, 0, 0, 0, 420)
g.add_color_stop_rgba(0, 1, 1, 0.85, 0.85); g.add_color_stop_rgba(1, 1, 1, 0.85, 0)
cr.set_source(g); cr.arc(0, 0, 420, 0, 2*math.pi); cr.fill()
cr.restore()
# hill
cr.move_to(0, S)
for x in range(0, S+21, 20): cr.line_to(x, 640 - 30*math.sin(math.pi*x/S))
cr.line_to(S, S); cr.close_path(); cr.set_source_rgb(*hexc('#5FC44A')); cr.fill()
# chick
st = dict(x=0, h=0, sx=1, sy=1, rot=0, phase='chick', crack=0, hatch=1, mood=0,
          wing=[0.9, 0.9], beak=0.75, happy=0, shiver=0, by=0)
cr.save(); cr.translate(cx, 690); cr.scale(1.55, 1.55)
draw_body(cr, 0, -215, 1.0, st, 1.0, (0.15, -0.1))
shell_part(cr, top=False)
cr.restore()
draw_bfly(cr, 610, 215, 0.06, 0.3, 0.8)
for (x, y, r) in ((130, 170, 26), (690, 400, 18), (95, 420, 16)):
    star(cr, x, y, r); cr.set_source_rgb(1, 1, 0.9); cr.fill()
surf.write_to_png('chickpea_avatar.png')
