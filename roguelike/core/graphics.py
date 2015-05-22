import libtcod


class Graphics(object):
    def __init__(self, w, h):
        self.t = libtcod
        self.con = self.t.console_new(w, h)

    def put_char(self, x, y, char, flag=None):
        self.t.console_put_char(self.con, x, y, char, flag=flag or self.t.BKGND_DEFAULT)

    def flush(self):
        self.t.console_flush()

    def init_root(self, w, h, title, fullscreen=False, renderer=None):
        self.t.console_init_root(w, h, title, fullscreen,
                                 renderer=renderer or self.t.RENDERER_SDL)

    def is_window_closed(self):
        return self.t.console_is_window_closed()

    def set_default_foreground(self, colour):
        self.t.console_set_default_foreground(self.con, colour)

    def blit(self, x, y, w, h, dst, xdst, ydst, ffade=1.0, bfade=1.0):
        self.t.console_blit(self.con, x, y, w, h, dst, xdst, ydst, ffade, bfade)
