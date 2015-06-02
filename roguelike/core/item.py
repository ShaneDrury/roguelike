import logging
import random
from fysom import Fysom
from core.entity import Entity, Component
from core.render import SimpleRender


log = logging.getLogger('rogue.item')


class ItemRender(Component):
    def update(self, graphics, fov, entity, **kwargs):
        pass


class Item(Entity):
    def __init__(self, name, consts):
        super(Item, self).__init__()
        self.name = name
        self.key = "{}_{}".format(self.name, random.randint(0, 1e8))
        self.consts = consts
        self.char = consts['char']
        self.colour = consts['colour']
        self._render = {
            'on_ground': SimpleRender(),
            'inventory': ItemRender()
        }
        self.fsm = Fysom({
            'initial': 'on_ground',
            'events': [
                {'name': 'pickup', 'src': 'on_ground', 'dst': 'inventory'},
                {'name': 'drop', 'src': 'inventory', 'dst': 'on_ground'}
            ]
        })

    def render(self, graphics, fov, **kwargs):
        self._render[self.fsm.current].update(graphics, fov, self, **kwargs)

    def use(self, player):
        log.debug("Using {}".format(self))
