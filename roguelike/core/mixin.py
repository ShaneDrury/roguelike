import libtcod


class PassthroughMixin(object):
    def __init__(self):
        self.t = libtcod
        self.prefix = None

    def __getattr__(self, item):
        if item.startswith(self.prefix):
            try:
                return getattr(self.t, item)
            except AttributeError:
                pass
        return getattr(self, item)
