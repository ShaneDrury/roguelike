from functools import partial
import logging
from math import sqrt, ceil, copysign
from fysom import Fysom
from core.entity import Entity, Point, Component
from core.render import SimpleRender

log = logging.getLogger('rogue.npc')


class NPCRender(SimpleRender):
    pass


class HuntingInput(Component):
    def update(self, entity, world, turn):
        if world.fov.is_in_fov(entity.pos.x, entity.pos.y):
            callback = partial(self.move, world, entity)
            turn.add_action('MOVE', callback, player=False)

    @staticmethod
    def move(world, entity):
        # TODO: Make this an actual path finder
        # Move towards player
        px, py = world.entities['player'].obj.pos
        prev = entity.pos
        nx, ny = prev
        dx = px - nx
        dy = py - ny
        if not(dx == 0 and dy == 0):
            distance = sqrt(dx * dx + dy * dy)
            mx = int(copysign(ceil(abs(dx / distance)), dx))
            my = int(copysign(ceil(abs(dy / distance)), dy))
            if not (mx == 0 and my == 0):
                entity.pos = Point(nx + mx, ny + my)
                world.resolve_collision(entity, prev)


class SleepingInput(Component):
    @staticmethod
    def update(keys, entity, world, turn):
        pass


class NPCUpdate(Component):
    @staticmethod
    def update(fsm, state, entity):
        if entity.hp <= 0:
            log.debug("KILLED")
            entity.alive = False


class NPC(Entity):
    def __init__(self, name, consts, message):
        super(NPC, self).__init__()
        self.name = name.capitalize()
        self.message = message
        self.pos = None
        self._render = NPCRender()
        self._update = NPCUpdate()
        self._input = {
            'hunting': HuntingInput(),
            'sleeping': SleepingInput()
        }
        self.consts = consts
        self.char = consts['char']
        self.hp = consts['hp']
        self.attack = consts['attack']
        self.alive = True
        self.is_player = False
        self.fsm = Fysom({
            'initial': 'hunting',
            'events': [
                {'name': 'wake', 'src': 'sleeping', 'dst': 'wandering'},
                {'name': 'sleep', 'src': 'wandering', 'dst': 'sleeping'},
                {'name': 'alert', 'src': ['wandering', 'sleeping'], 'dst': 'hunting'},
                {'name': 'calm', 'src': 'hunting', 'dst': 'wandering'},
            ]
        })

    def update(self):
        self._update.update(self.fsm, self.fsm.current, self)

    def collide(self, entity):
        if entity.is_player:
            self.hp -= entity.attack
            self.message.add("Player hit {} for {}".format(self.name, entity.attack),
                             'lightest_violet')
            log.debug("{} hit {} - {}".format(entity, self, self.hp))

    def input(self, keys, world, turn):
        self._input[self.fsm.current].update(self, world, turn)
