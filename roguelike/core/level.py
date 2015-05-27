from __future__ import division

from collections import OrderedDict
import logging
import random

from core.entity import Component, EntityCollection, Point
from core.mapping import Map
from core.npc import NPC
from core.player import Player


log = logging.getLogger('rogue.mapping')


class MonsterGenerator(Component):
    @staticmethod
    def update(map_, player, graphics, consts, level):
        level_consts = consts['level'][level]
        monsters = consts['monsters']
        num_monsters_const = level_consts['num_monsters']
        num_monsters = int(random.gauss(num_monsters_const['avg'],
                                        num_monsters_const['std']))
        allowed_monsters = level_consts['allowed_monsters']
        population = [k for k, v in allowed_monsters.iteritems()
                      for _ in range(v['weight'])]
        entities = {}
        for n in range(num_monsters):
            p = random.choice(population)
            npc = NPC(monsters[p])
            npc_room = map_.rooms[random.randint(1, len(map_.rooms)-1)]
            while True:
                npcx = random.randint(npc_room.x1, npc_room.x2+1)
                npcy = random.randint(npc_room.y1, npc_room.y2+1)
                npc.pos = Point(npcx, npcy)

                for k, entity in entities.iteritems():
                    if entity.obj == npc:
                        continue
                    if npc.pos == entity.obj.pos:
                        log.debug("Collision {}".format(k))
                        break
                else:
                    entity_key = "{}_{}".format(p, random.randint(0, 1e8))
                    log.debug("Added {}".format(entity_key))
                    entities[entity_key] = EntityCollection(npc, graphics)
                    break
        return entities


class Level(Component):
    def __init__(self):
        self.monster_generator = MonsterGenerator()
        self.level = 1

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
        monster_entities = self.monster_generator.update(map_, player, world.graphics,
                                                         consts, self.level)
        entities.update(monster_entities)
        return entities
