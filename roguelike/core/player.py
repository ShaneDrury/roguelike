from functools import partial
import logging

from core.render import SimpleRender
from roguelike.core.entity import Entity, Component, Point

log = logging.getLogger('rogue.player')


class PlayerInput(Component):
    def __init__(self):
        self.keys_dict = {
            'RIGHT': Point(1, 0),
            'LEFT': Point(-1, 0),
            'UP': Point(0, -1),
            'DOWN': Point(0, 1),
            'UP_LEFT': Point(-1, -1),
            'UP_RIGHT': Point(1, -1),
            'DOWN_RIGHT': Point(1, 1),
            'DOWN_LEFT': Point(-1, 1),
            'WAIT': Point(0, 0)
        }

    def update(self, keys, entity, world, turn):
        key = keys.check_for_keypress(keys.KEY_PRESSED)
        prev = entity.pos
        x, y = entity.pos
        diff = self.keys_dict.get(key, None)
        if diff:
            callback = partial(self.move, world, entity, diff, x, y, prev)
            turn.add_action('MOVE', callback, player=True)

    @staticmethod
    def move(world, entity, diff, x, y, prev):
        entity.pos = Point(x + diff.x, y + diff.y)
        world.resolve_collision(entity, prev)
        world.fov.recompute(entity.pos.x, entity.pos.y)


class Player(Entity):
    def __init__(self, consts, message):
        super(Player, self).__init__()
        self._render = SimpleRender()
        self._input = PlayerInput()
        self.message = message
        self.pos = Point(25, 20)
        self.consts = consts
        self.char = consts['char']
        self.is_player = True
        self.hp = 20
        self.max_hp = 20
        self.attack = consts['attack']

    def input(self, keys, world, turn):
        self._input.update(keys, self, world, turn)

    def collide(self, entity):
        self.hp -= entity.attack
        self.message.add("{} hit Player for {}".format(entity.name, entity.attack),
                         'lightest_red')
