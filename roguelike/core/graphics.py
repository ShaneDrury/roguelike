from roguelike import libtcod


class Graphics(object):
    def __init__(self):
        self.tcod = libtcod

    def put_char(self, x, y, char):
        self.tcod.console_put_char(0, x, y, char, libtcod.BKGND_NONE)

    def flush(self):
        self.tcod.console_flush()

    def init_root(self, w, h, title, fullscreen=False, renderer=None):
        self.tcod.console_init_root(w, h, title, fullscreen,
                                    renderer=renderer or self.tcod.RENDERER_SDL)

    def set_custom_font(self, font_file, flags=None, nb_char_horiz=0, nb_char_vertic=0):
        self.tcod.console_set_custom_font(
            font_file,
            flags=flags or self.tcod.FONT_LAYOUT_ASCII_INCOL, nb_char_horiz=0,
            nb_char_vertic=0
        )
