import logging
import random

from core.entity import Entity, Component
from core.render import SimpleRender


log = logging.getLogger('rogue.item')


class ItemRender(Component):
    def update(self, graphics, fov, entity, **kwargs):
        pass


class Item(Entity):
    def __init__(self, name, consts, inventory, turn, message):
        super(Item, self).__init__()
        self.name = name
        self.turn = turn
        self.key = "{}_{}".format(self.name, random.randint(0, 1e8))
        self.inventory = inventory
        self.consts = consts
        self.char = consts['char']
        self.colour = consts['colour']
        self.message = message
        self._render = SimpleRender()
        self.picked_up = False
        self.alive = True
        self.blocking = False

    def render(self, graphics, fov, **kwargs):
        self._render.update(graphics, fov, self, **kwargs)

    def update(self):
        if self.picked_up:
            self.alive = False

    def use(self, player, turn):
        self.inventory.remove(self)

    def collide(self, entity):
        if entity.is_player:
            self.turn.add_action('PICKUP', self._pickup, player=True)
        else:
            pass

    def _pickup(self):
        if self.inventory.add(self):
            self.picked_up = True
            self.message.add("Picked up {}".format(self), 'white')
