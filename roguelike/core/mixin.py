import libtcod


class PassthroughMixin(object):
    def __init__(self):
        self.t = libtcod
        self.prefix = None

    def __getattr__(self, item):
        if item.startswith(self.prefix):
            if hasattr(self.t, item):
                return getattr(self.t, item)
            elif hasattr(self, item):
                return getattr(self, item)
            else:
                raise AttributeError(item)
