from core.mixin import PassthroughMixin


class Font(PassthroughMixin):
    def __init__(self):
        super(Font, self).__init__()
        self.prefix = "FONT_"
