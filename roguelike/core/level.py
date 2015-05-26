from collections import OrderedDict
import random
from core.entity import Component, EntityCollection
from core.mapping import Map
from core.npc import NPC
from core.player import Player


class MonsterGenerator(Component):
    @staticmethod
    def update(map_, player, entities, graphics, consts):
        npc = NPC(consts['rat'])
        npc_room = random.randint(1, len(map_.rooms)-1)
        npc.pos = map_.rooms[npc_room].center
        entities['rat'] = EntityCollection(npc, graphics)
        return entities


class Level(Component):
    def __init__(self):
        self.monster_generator = MonsterGenerator()

    def init_entities(self, world, consts):
        player_graphics = world.graphics
        map_graphics = world.graphics

        player = Player(consts['player'])
        map_ = Map(consts['map'])
        player.pos = map_.rooms[0].center

        entities = OrderedDict([
            ('map', EntityCollection(map_, map_graphics)),
            ('player', EntityCollection(player, player_graphics)),
        ])
        entities = self.monster_generator.update(map_, player, entities, world.graphics,
                                                 consts['monsters'])
        return entities
