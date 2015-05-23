from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])

EntityCollection = namedtuple('EntityCollection', ['obj', 'gfx'])


class Entity(object):
    def __init__(self):
        self._input = None
        self._render = None
        self.blocking = True

    def render(self, graphics, fov, **kwargs):
        self._render.update(graphics, fov, self, **kwargs)


class Component(object):
    pass
