import sys, importlib, cairo
folder, module, f0, f1 = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
sys.path.insert(0, folder); sys.path.insert(0, '/home/claude/kit')
m = importlib.import_module(module)
out = sys.stdout.buffer
for n in range(f0, f1):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080, 1920); cr = cairo.Context(s)
    m.frame(cr, n / 30); s.flush(); out.write(bytes(s.get_data()))
