from core.background import Background
import libtcod


class Graphics(object):
    LEFT = 0
    RIGHT = 1
    CENTER = 2

    def __init__(self, colour, w, h):
        self.t = libtcod
        self.con = self.t.console_new(w, h)
        self.background = Background()
        self.colour = colour

    def put_char(self, x, y, char, flag=None):
        self.t.console_put_char(self.con, x, y, char, flag=flag or self.t.BKGND_DEFAULT)

    def flush(self):
        self.t.console_flush()

    def clear(self):
        self.t.console_clear(self.con)

    def init_root(self, w, h, title, fullscreen=False, renderer=None):
        self.t.console_init_root(w, h, title, fullscreen,
                                 renderer=renderer or self.t.RENDERER_SDL)

    def is_window_closed(self):
        return self.t.console_is_window_closed()

    def set_default_foreground(self, colour):
        if isinstance(colour, basestring):
            colour = getattr(self.colour, colour)
        self.t.console_set_default_foreground(self.con, colour)

    def set_default_background(self, col):
        self.t.console_set_default_background(self.con, col)

    def rect(self, x, y, w, h, clr, flag=None):
        self.t.console_rect(self.con, x, y, w, h, clr,
                            flag or self.background.BKGND_DEFAULT)

    def print_ex(self, x, y, flag, alignment, fmt):
        self.t.console_print_ex(self.con, x, y, flag, alignment, fmt)

    def blit(self, x, y, w, h, dst, xdst, ydst, ffade=1.0, bfade=1.0):
        self.t.console_blit(self.con, x, y, w, h, dst, xdst, ydst, ffade, bfade)

    def set_char_background(self, x, y, col, flag=None):
        self.t.console_set_char_background(self.con, x, y, col, flag or self.t.BKGND_SET)
