import os

import yaml
from core.colour import Colour

from core.entity import Component, EntityCollection
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

        return {'player': EntityCollection(player, player_graphics),
                'npc': EntityCollection(npc, npc_graphics),
                'map': EntityCollection(map_, map_graphics)}

    def get_consts(self):
        consts_list = ['player', 'npc', 'map']
        consts = {}
        for c in consts_list:
            with open(os.path.join(self.settings.VARS_FOLDER, c + '.yml'), 'r') as f:
                consts[c] = yaml.load(f)
        return consts

    def main(self):
        self.font.set_custom_font(
            os.path.join(self.settings.FONT_DIR, 'arial12x12.png'),
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
        for k, ent in self.entities.iteritems():
            obj = ent.obj
            if hasattr(obj, 'input'):
                obj.input(self.keys, self)

    def render(self):
        render_params = {
            'player': {'x': 0, 'y': 0, 'w': 0, 'h': 0, 'dst': 0, 'xdst': 0, 'ydst': 0},
        }
        render_params['npc'] = render_params['player']
        for k, ent in self.entities.iteritems():
            extra = render_params.get(k, {})
            ent.obj.render(ent.gfx, **extra)
        self.graphics.flush()
        for k, ent in self.entities.iteritems():
            try:
                ent.obj.post_render(ent.gfx)
            except AttributeError:
                pass

    def resolve_collision(self, entity, prev):
        for k, other in self.entities.iteritems():
            target = other.obj
            if target is entity:
                continue
            if k == 'map':
                x, y = entity.pos
                if target.tiles[x][y].blocked:
                    entity.pos = prev
                continue
            try:
                if entity.pos == target.pos and target.blocking:
                    entity.pos = prev
            except AttributeError:
                pass
