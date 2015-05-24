import logging
from math import sqrt, ceil, copysign
from core.entity import Entity, Point, Component
from core.player import SimpleRender


log = logging.getLogger('rogue.npc')


class NPCRender(SimpleRender):
    pass


class NPCInput(Component):
    @staticmethod
    def update(keys, entity, world):
        if world.fov.is_in_fov(entity.pos.x, entity.pos.y):
            # Move towards player
            player = world.entities['player'].obj.pos
            x, y = player
            prev = entity.pos
            nx, ny = prev
            dx = x - nx
            dy = y - ny
            if not(dx == 0 and dy == 0):
                distance = sqrt(dx * dx + dy * dy)
                mx = int(copysign(ceil(abs(dx / distance)), dx))
                my = int(copysign(ceil(abs(dy / distance)), dy))
                if not (mx == 0 and my == 0):
                    entity.pos = Point(nx + mx, ny + my)
                    world.resolve_collision(entity, prev)


class NPC(Entity):
    def __init__(self, consts):
        super(NPC, self).__init__()
        self.pos = Point(55, 23)
        self._render = NPCRender()
        self._input = NPCInput()
        self.consts = consts
        self.char = consts['char']
        self.hp = consts['hp']
        self.alive = True

    def collide(self, entity):
        if entity.is_player:
            self.hp -= 1
            log.debug("{} hit {}".format(entity, self))

    def input(self, keys, world):
        self._input.update(keys, self, world)
