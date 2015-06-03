from collections import OrderedDict
import logging
import os
from fysom import Fysom

import yaml

from core.colour import Colour
from core.entity import Component, EntityCollection
from core.font import Font
from core.fov import FOV
from core.graphics import Graphics
from core.inventory import Inventory
from core.keys import Keys
from core.level import Level
from core.message import Message
from core.panel import Panel
from core.turn import Turn
from items.health_potion import HealthPotion

log = logging.getLogger('rogue')
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
ch.setLevel(logging.DEBUG)
log.addHandler(ch)


def noop(*args, **kwargs):
    pass


class GameInput(Component):
    def update(self, keys, game, turn, entities):
        self.system_keys(keys, game)
        for ent in entities.values():
            obj = ent.obj
            input_ = getattr(obj, 'input', noop)
            input_(keys, game, turn)

    @staticmethod
    def system_keys(keys, game):
        key = keys.check_for_keypress(keys.KEY_RELEASED)
        if key == 'QUIT':
            game.exited = key == 'QUIT'


class InventoryInput(Component):
    def update(self, keys, game, turn, entities):
        self.system_keys(keys, game)
        ent = entities['inventory']
        obj = ent.obj
        input_ = getattr(obj, 'input', noop)
        input_(keys, game, turn)

    @staticmethod
    def system_keys(keys, game):
        key = keys.check_for_keypress(keys.KEY_RELEASED)
        if key == 'QUIT':
            game.fsm.close_inventory()


class Game(object):
    def __init__(self, settings):
        self.font = Font()
        self.settings = settings

        self.fsm = Fysom({
            'initial': 'game',
            'events': [
                {'name': 'open_inventory', 'src': 'game', 'dst': 'inventory'},
                {'name': 'close_inventory', 'src': 'inventory', 'dst': 'game'},
            ]
        })

        self.consts = self.get_consts()
        self.key_consts = self.get_keys()
        self._input = {'game': GameInput(),
                       'inventory': InventoryInput()}
        self.exited = False
        self.colour = Colour()
        self.graphics = Graphics(self.colour, **self.settings.SCREEN)
        self.key_pressed = False

        message_width = self.settings.SCREEN['w'] - self.consts['panel']['bar']['w'] - 2
        message_height = self.consts['panel']['rect']['h'] - 1
        self.message = Message(message_width, message_height)
        self.message.add('Welcome to Roguelike', 'white')

        self.level_handler = Level(self.message)
        self.keys = {k: Keys(v) for k, v in self.key_consts.iteritems()}
        self.panel = Panel(self.consts['panel'], self)
        self.panel_graphics = Graphics(self.colour,
                                       w=self.settings.SCREEN['w'],
                                       h=self.consts['panel']['rect']['h'])
        self.entities = self.level_handler.init_entities(self, self.consts)
        self.entities['panel'] = EntityCollection(self.panel, self.panel_graphics)
        self.render_params = self.init_render_params()
        self.fov = FOV(self.entities['map'].obj.tiles)
        player = self.entities['player'].obj
        self.turn = Turn(self.consts['actions'])
        self.inventory_graphics = Graphics(self.colour,
                                           w=self.consts['inventory']['rect']['w'],
                                           h=self.consts['inventory']['rect']['h'])
        self.inventory = Inventory(self.fsm, player, self.turn, self.consts['inventory'])
        self.entities['inventory'] = EntityCollection(self.inventory,
                                                      self.inventory_graphics)
        item_entities = [HealthPotion('potion', self.consts['items']['potion'])]
        for ent in item_entities:
            ent.fsm.pickup()
            self.entities[ent.key] = EntityCollection(ent, self.graphics)
            self.inventory.add(ent)
        self.fov.recompute(player.pos.x, player.pos.y)

    def main(self):
        self.font.set_custom_font(
            os.path.join(self.settings.FONT_DIR, 'arial12x12.png'),
            self.font.FONT_TYPE_GREYSCALE | self.font.FONT_LAYOUT_TCOD
        )
        self.graphics.init_root(title='Roguelike', fullscreen=False,
                                **self.settings.SCREEN)

        while not self.exited:
            self.render()  # TODO: put this after keys
            self.turn.blocking = True
            while self.turn.blocking:
                self.turn.take_player_action()
                self.update()
            self.get_keypress()
            if self.key_pressed:
                self.input()
            for keys in self.keys.values():
                keys.flush()

    def get_keypress(self):
        self.key_pressed = False
        key = self.keys[self.state].check_for_keypress(
            self.keys[self.state].KEY_RELEASED
        )
        if key:
            self.key_pressed = True

    def init_render_params(self):
        panel_height = self.consts['panel']['rect']['h']
        screen_width = self.settings.SCREEN['w']
        screen_height = self.settings.SCREEN['h']
        panel_y = screen_height - panel_height
        inventory_y = 3
        inventory_width = 10
        render_params = {
            'map': {},
            'player': {'x': 0, 'y': 0, 'w': 0, 'h': 0, 'dst': 0, 'xdst': 0, 'ydst': 0},
            'panel': {'x': 0, 'y': 0, 'w': 0, 'h': panel_height, 'dst': 0,
                      'xdst': 0, 'ydst': panel_y},
            'inventory': {'x': 0, 'y': 0, 'w': 0, 'h': 0, 'dst': 0,
                          'xdst': screen_width / 2 - inventory_width / 2,
                          'ydst': inventory_y},
        }
        for k, entity in self.entities.iteritems():
            if k in render_params.keys():
                continue
            render_params[k] = render_params['player']
        return render_params

    def get_consts(self):
        consts_list = ['player', 'monsters', 'map', 'level', 'panel', 'items',
                       'actions', 'inventory']
        consts = {}
        for c in consts_list:
            with open(os.path.join(self.settings.VARS_FOLDER, c + '.yml'), 'r') as f:
                consts[c] = yaml.load(f)
        return consts

    def get_keys(self):
        keys_list = ['player', 'inventory', 'game']
        all_consts = {}
        for c in keys_list:
            with open(os.path.join(self.settings.VARS_FOLDER, 'keys',
                                   c + '.yml'), 'r') as f:
                all_consts[c] = yaml.load(f)
        merged_consts = {
            'game': self.merge_dicts(all_consts['game'],
                                     all_consts['player']),
            'inventory': all_consts['inventory'],
        }
        return merged_consts

    @staticmethod
    def merge_dicts(d1, d2):
        updated = d1.copy()
        updated.update(d2)
        return updated

    def update(self):
        if self.key_pressed:
            for entity in self.entities.values():
                update = getattr(entity.obj, 'update', noop)
                update()
        self.entities = OrderedDict([
            (k, v) for k, v in self.entities.iteritems()
            if getattr(v.obj, 'alive', True)
        ])

    @property
    def state(self):
        return self.fsm.current

    def input(self):
        # TODO: Add update_render state on different tick
        self._input[self.state].update(
            self.keys[self.state], self, self.turn, self.entities
        )

    def render(self):
        for k, ent in self.entities.items():
            extra = self.render_params.get(k, {})
            ent.obj.render(ent.gfx, self.fov, **extra)
        self.graphics.flush()

    def resolve_collision(self, entity, prev):
        for k, other in self.entities.items():
            target = other.obj
            if target is entity:
                continue
            if k == 'map':  # Hit wall
                x, y = entity.pos
                if target.tiles[x][y].blocked:
                    entity.pos = prev
                continue
            if hasattr(target, 'pos'):
                if entity.pos == target.pos and target.blocking:  # Hit entity
                    log.debug("{} overlapping {} {} prev={}".
                              format(entity, target, entity.pos, prev))
                    entity.pos = prev
                    target.collide(entity)
