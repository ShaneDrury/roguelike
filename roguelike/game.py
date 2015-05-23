import os

import yaml
from core.colour import Colour

from core.entity import Component
from core.font import Font
from core.graphics import Graphics
from core.keys import Keys
from core.mapping import Map
from core.npc import NPC
from core.player import Player


class GameInput(Component):
    def update(self, keys, game):
        key = keys.check_for_keypress(keys.KEY_RELEASED)
        game.exited = key.vk == keys.KEY_ESCAPE


class Game(object):
    def __init__(self, settings):
        self.keys = Keys()
        self.font = Font()
        self.settings = settings

        self._input = GameInput()
        self.exited = False
        self.colour = Colour()
        self.graphics = Graphics(self.colour, **self.settings.SCREEN)
        self.consts = self.get_consts()
        self.entities = self.init_entities()

    def init_entities(self):
        npc_graphics = self.graphics
        player_graphics = self.graphics
        map_graphics = self.graphics

        npc = NPC(self.consts['npc'])
        player = Player(self.consts['player'])
        map_ = Map(self.consts['map'])

        # TODO: Make it key-value pairs of name and namedtuple

        return [{'key': 'player', 'obj': player, 'gfx': player_graphics},
                {'key': 'npc', 'obj': npc, 'gfx': npc_graphics},
                {'key': 'map', 'obj': map_, 'gfx': map_graphics}]

    def get_consts(self):
        consts_list = ['player', 'npc', 'map']
        consts = {}
        for c in consts_list:
            with open(os.path.join(self.settings.VARS_FOLDER, c + '.yml'), 'r') as f:
                consts[c] = yaml.load(f)
        return consts

    def main(self):
        self.font.set_custom_font(
            os.path.join(self.settings.FONT_DIR, 'arial10x10.png'),
            self.font.FONT_TYPE_GREYSCALE | self.font.FONT_LAYOUT_TCOD
        )
        self.graphics.init_root(title='Roguelike', fullscreen=False,
                                **self.settings.SCREEN)

        while not self.exited:
            self.input()
            self.render()
            self.keys.flush()

    def input(self):
        self._input.update(self.keys, self)
        for entity in self.entities:
            obj = entity['obj']
            if hasattr(obj, 'input'):
                obj.input(self.keys, self)

    def render(self):
        render_params = {
            'player': {'x': 0, 'y': 0, 'w': 0, 'h': 0, 'dst': 0, 'xdst': 0, 'ydst': 0},
        }
        render_params['npc'] = render_params['player']
        for entity in self.entities:
            extra = render_params.get(entity['key'], {})
            entity['obj'].render(entity['gfx'], **extra)
        self.graphics.flush()
        for entity in self.entities:
            try:
                entity['obj'].post_render(entity['gfx'])
            except AttributeError:
                pass

    def resolve_collision(self, entity, prev):
        for other in self.entities:
            target = other['obj']
            if target is entity:
                continue
            if other['key'] == 'map':
                x, y = entity.pos
                if target.tiles[x][y].blocked:
                    entity.pos = prev
                continue
            try:
                if entity.pos == target.pos:
                    entity.pos = prev
            except AttributeError:
                pass
