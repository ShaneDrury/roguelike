import logging
from core.entity import Entity, Point, Component
from core.player import SimpleRender


log = logging.getLogger('rogue.npc')

class NPCRender(SimpleRender):
    pass

class NPCInput(Component):
    def update(self, keys, entity, world):
        if world.fov.is_in_fov(entity.pos.x, entity.pos.y):
            log.debug("Is in FOV")


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
            log.debug("{} hit {}".format(entity.id, self.id))

    def input(self, keys, world):
        self._input.update(keys, self, world)
