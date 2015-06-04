from __future__ import division

from collections import OrderedDict
import logging
import random

from core.entity import Component, EntityCollection, Point
from core.graphics import Graphics
from core.inventory import Inventory
from core.mapping import Map
from core.npc import NPC
from core.player import Player
from items import get_item

log = logging.getLogger('rogue.mapping')


class MonsterGenerator(Component):
    def __init__(self, message):
        self.message = message

    def update(self, map_, graphics, consts, level):
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
            npc = NPC(p, monsters[p], self.message)
            npc_room = map_.rooms[random.randint(1, len(map_.rooms)-1)]
            while True:
                npcx = random.randint(npc_room.x1, npc_room.x2)
                npcy = random.randint(npc_room.y1, npc_room.y2)
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


class ItemGenerator(Component):
    def __init__(self, turn, message):
        self.turn = turn
        self.message = message

    def update(self, map_, graphics, consts, level, inventory):
        level_consts = consts['level'][level]
        items = consts['items']
        num_items_const = level_consts['num_items']
        num_items = int(random.gauss(num_items_const['avg'],
                                     num_items_const['std']))
        allowed_items = level_consts['allowed_items']
        population = [k for k, v in allowed_items.iteritems()
                      for _ in range(v['weight'])]
        entities = {}
        for n in range(num_items):
            p = random.choice(population)
            item_cls = get_item(p)
            item = item_cls(p, items[p], inventory, self.turn, self.message)
            item_room = map_.rooms[random.randint(1, len(map_.rooms)-1)]
            while True:
                itemx = random.randint(item_room.x1, item_room.x2)
                itemy = random.randint(item_room.y1, item_room.y2)
                item.pos = Point(itemx, itemy)
                for k, entity in entities.iteritems():
                    if entity.obj == item:
                        continue
                    if item.pos == entity.obj.pos:
                        log.debug("Collision {}".format(k))
                        break
                else:
                    entity_key = "{}_{}".format(p, random.randint(0, 1e8))
                    log.debug("Added {}".format(entity_key))
                    entities[entity_key] = EntityCollection(item, graphics)
                    break
        return entities


class Level(Component):
    def __init__(self, turn, message):
        self.message = message
        self.turn = turn
        self.monster_generator = MonsterGenerator(self.message)
        self.item_generator = ItemGenerator(self.turn, self.message)
        self.level = 1

    def init_entities(self, world, consts):
        player_graphics = world.graphics
        map_graphics = world.graphics

        player = Player(consts['player'], world.message)
        map_ = Map(consts['map'])
        player.pos = map_.rooms[0].center

        entities = OrderedDict([
            ('map', EntityCollection(map_, map_graphics)),
            ('player', EntityCollection(player, player_graphics)),
        ])

        inventory = Inventory(world.fsm, player, world.turn, consts['inventory'])
        inventory_graphics = Graphics(world.colour,
                                      w=consts['inventory']['rect']['w'],
                                      h=consts['inventory']['rect']['h'])
        monster_entities = self.monster_generator.update(map_, world.graphics,
                                                         consts, self.level)
        item_entities = self.item_generator.update(map_, world.graphics,
                                                   consts, self.level,
                                                   inventory)
        entities.update(item_entities)
        entities.update(monster_entities)
        entities['inventory'] = EntityCollection(inventory, inventory_graphics)
        return entities
