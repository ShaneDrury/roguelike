import logging
import os

from fysom import Fysom
import yaml

from core.colour import Colour
from core.entity import Component, EntityPack, priorities
from core.font import Font
from core.graphics import Graphics
from core.inventory import Inventory
from core.keys import Keys
from core.level import Level
from core.message import Message
from core.panel import Panel
from core.player import Player
from core.turn import Turn


log = logging.getLogger('rogue')
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
ch.setLevel(logging.DEBUG)
log.addHandler(ch)


class GameInput(Component):
    @staticmethod
    def update(keys, game, turn, entities):
        if keys.key == 'QUIT':
            game.exited = True
            return
        for ent in entities.values():
            obj = ent.obj
            if hasattr(obj, 'input'):
                obj.input(keys, game, turn)


class InventoryInput(Component):
    @staticmethod
    def update(keys, game, turn, entities):
        if keys.key == 'QUIT':
            game.fsm.close_inventory()
            return
        ent = entities['inventory']
        obj = ent.obj
        if hasattr(obj, 'input'):
            obj.input(keys, game, turn)


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

        self.consts = self.load_consts()
        self.key_consts = self.get_keys()
        self._input = {'game': GameInput(),
                       'inventory': InventoryInput()}
        self.exited = False
        self.colour = Colour()
        self.graphics = Graphics(self.colour, **self.settings.SCREEN)
        self.key_pressed = False
        self.current_depth = 1

        message_width = self.settings.SCREEN['w'] - self.consts['panel']['bar']['w'] - 2
        message_height = self.consts['panel']['rect']['h'] - 1
        self.message = Message(message_width, message_height)
        self.message.add('Welcome to Roguelike', 'white')
        self.turn = Turn(self.consts['actions'])
        self.levels = [Level(n, self.turn, self.message) for n in range(1, 3)]
        self.level_handler = self.levels[0]
        self.keys = {k: Keys(v) for k, v in self.key_consts.iteritems()}
        self.panel = Panel(self.consts['panel'], self)
        self.panel_graphics = Graphics(self.colour,
                                       w=self.settings.SCREEN['w'],
                                       h=self.consts['panel']['rect']['h'])
        self.entities = {}
        self.inventory = None
        self.player = None
        self.render_params = None
        self.init_entities()

    def init_entities(self):
        player_graphics = self.graphics
        player = Player(self.consts['player'], self.message)
        inventory_graphics = Graphics(self.graphics.colour,
                                      w=self.consts['inventory']['rect']['w'],
                                      h=self.consts['inventory']['rect']['h'])
        self.entities['player'] = EntityPack(player, player_graphics)
        self.inventory = Inventory(self.fsm, player, self.turn, self.consts['inventory'])
        self.player = self.entities['player'].obj
        level_entities = self.level_handler.gen_level_entities(self.inventory,
                                                               self.graphics,
                                                               self.consts)
        self.entities.update(level_entities)
        self.player.pos = self.entities['map'].obj.rooms[0].center
        self.entities['panel'] = EntityPack(self.panel, self.panel_graphics)
        self.entities['inventory'] = EntityPack(self.inventory, inventory_graphics)
        self.render_params = self.init_render_params()
        self.fov.recompute(self.player.pos.x, self.player.pos.y)

    @property
    def fov(self):
        return self.level_handler.fov

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

    def load_consts(self):
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
                if hasattr(entity.obj, 'update'):
                    entity.obj.update()
        self.entities = {k: v for k, v in self.entities.iteritems()
                         if getattr(v.obj, 'alive', True)}

    @property
    def state(self):
        return self.fsm.current

    def input(self):
        # TODO: Add update_render state on different tick
        self._input[self.state].update(
            self.keys[self.state], self, self.turn, self.entities
        )

    def render(self):
        keys = self.entities.keys()
        for p in priorities:
            pkeys = [k for k in keys if k.startswith(p)]
            for k in pkeys:
                ent = self.entities[k]
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
            if hasattr(target, 'collide'):
                if entity.pos == target.pos:  # Hit entity
                    if target.blocking:
                        log.debug("{} overlapping {} {} prev={}".
                                  format(entity, target, entity.pos, prev))
                        entity.pos = prev
                    target.collide(entity)
