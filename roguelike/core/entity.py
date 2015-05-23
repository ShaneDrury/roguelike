from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])


class Entity(object):
    def __init__(self):
        self._input = None
        self._render = None

    def render(self, graphics, **kwargs):
        self._render.update(graphics, self, **kwargs)


class Component(object):
    pass
