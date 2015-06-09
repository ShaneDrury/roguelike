from __future__ import division

from collections import OrderedDict
import logging
import random

from core.entity import Component, EntityCollection, Point, Entity
from core.fov import FOV
from core.graphics import Graphics
from core.inventory import Inventory
from core.mapping import Map
from core.npc import NPC
from core.player import Player
from core.render import SimpleRender
from items import get_item

log = logging.getLogger('rogue.mapping')


def place_in_random_room(entity, entities, rooms):
    """
    Sets entity.pos to be in a random place in a random room
    """
    room = rooms[random.randint(1, len(rooms)-1)]
    while True:
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)
        entity.pos = Point(x, y)
        for k, other in entities.iteritems():
            if other.obj == entity:
                continue
            if entity.pos == other.obj.pos:
                log.debug("Collision {}".format(k))
                break
        else:
            break


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
            place_in_random_room(npc, entities, map_.rooms)
            entity_key = "{}_{}".format(p, random.randint(0, 1e8))
            log.debug("Added {}".format(entity_key))
            entities[entity_key] = EntityCollection(npc, graphics)
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
            place_in_random_room(item, entities, map_.rooms)
            entity_key = "{}_{}".format(p, random.randint(0, 1e8))
            log.debug("Added {}".format(entity_key))
            entities[entity_key] = EntityCollection(item, graphics)
        return entities


class Stairs(Entity):
    def __init__(self, direction, consts):
        super(Stairs, self).__init__()
        self.blocking = False
        self.consts = consts
        self._render = SimpleRender()
        self.pos = None
        self.direction = direction
        self.char = consts[self.direction]['char']


class StairsGenerator(Component):
    def __init__(self, message):
        self.message = message

    def update(self, map_, graphics, consts):
        stairs = Stairs('down', consts['map']['stairs'])
        place_in_random_room(stairs, {}, map_.rooms)
        return {'stairs': EntityCollection(stairs, graphics)}


class Level(Component):
    def __init__(self, depth, turn, message):
        self.message = message
        self.turn = turn
        self.monster_generator = MonsterGenerator(self.message)
        self.item_generator = ItemGenerator(self.turn, self.message)
        self.stairs_generator = StairsGenerator(self.message)
        self.depth = depth
        self.fov = None

    def init_entities(self, fsm, message, graphics, turn, consts):
        player_graphics = graphics
        player = Player(consts['player'], message)

        entities = OrderedDict()
        inventory = Inventory(fsm, player, turn, consts['inventory'])
        inventory_graphics = Graphics(graphics.colour,
                                      w=consts['inventory']['rect']['w'],
                                      h=consts['inventory']['rect']['h'])
        entities['player'] = EntityCollection(player, player_graphics)
        entities['inventory'] = EntityCollection(inventory, inventory_graphics)
        return entities

    def gen_level_entities(self, inventory, graphics, consts):
        map_ = Map(consts['map'])
        map_graphics = graphics
        entities = OrderedDict()
        monster_entities = self.monster_generator.update(map_, graphics,
                                                         consts, self.depth)
        item_entities = self.item_generator.update(map_, graphics,
                                                   consts, self.depth,
                                                   inventory)
        stairs = self.stairs_generator.update(map_, graphics, consts)
        entities.update(stairs)
        entities.update(item_entities)
        entities.update(monster_entities)
        entities['map'] = EntityCollection(map_, map_graphics)
        self.fov = FOV(map_.tiles)
        return entities
