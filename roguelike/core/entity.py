from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])

EntityPack = namedtuple('EntityPack', ['obj', 'gfx'])

priorities = ['stairs', 'player', 'item_', 'monster_', 'map', 'panel', 'inventory']


class Entity(object):
    def __init__(self):
        self._input = None
        self._render = None
        self.blocking = True

    def __str__(self):
        return "{}-{}".format(self.__class__.__name__, id(self))

    def render(self, graphics, fov, **kwargs):
        self._render.update(graphics, fov, self, **kwargs)


class Component(object):
    pass
