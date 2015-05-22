from core.mixin import PassthroughMixin


class Font(PassthroughMixin):
    def __init__(self):
        super(Font, self).__init__()
        self.prefix = "FONT_"

    def set_custom_font(self, font_file, flags=None, nb_char_horiz=0, nb_char_vertic=0):
        self.t.console_set_custom_font(
            font_file,
            flags=flags or self.FONT_LAYOUT_ASCII_INCOL,
            nb_char_horiz=nb_char_horiz,
            nb_char_vertic=nb_char_vertic
        )
