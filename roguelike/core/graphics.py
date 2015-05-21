import libtcod


class Graphics(object):
    def __init__(self):
        self.t = libtcod

    def put_char(self, x, y, char):
        self.t.console_put_char(0, x, y, char, self.t.BKGND_NONE)

    def flush(self):
        self.t.console_flush()

    def init_root(self, w, h, title, fullscreen=False, renderer=None):
        self.t.console_init_root(w, h, title, fullscreen,
                                 renderer=renderer or self.t.RENDERER_SDL)

    def set_custom_font(self, font_file, flags=None, nb_char_horiz=0, nb_char_vertic=0):
        self.t.console_set_custom_font(
            font_file,
            flags=flags or self.t.FONT_LAYOUT_ASCII_INCOL,
            nb_char_horiz=nb_char_horiz,
            nb_char_vertic=nb_char_vertic
        )

    def is_window_closed(self):
        return self.t.console_is_window_closed()

    def set_default_foreground(self, console, colour):
        self.t.console_set_default_foreground(console, colour)
