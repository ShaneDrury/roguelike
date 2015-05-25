from collections import OrderedDict
import logging
import os

import yaml

from core.colour import Colour
from core.entity import Component, EntityCollection
from core.font import Font
from core.fov import FOV
from core.graphics import Graphics
from core.keys import Keys
from core.mapping import Map
from core.npc import NPC
from core.player import Player


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
    @staticmethod
    def update(keys, game):
        game.key_pressed = False
        key = keys.check_for_keypress(keys.KEY_RELEASED)
        if key:
            game.key_pressed = True
        game.exited = key == 'QUIT'


class Game(object):
    def __init__(self, settings):
        self.font = Font()
        self.settings = settings

        self.consts = self.get_consts()
        self._input = GameInput()
        self.exited = False
        self.colour = Colour()
        self.graphics = Graphics(self.colour, **self.settings.SCREEN)
        self.key_pressed = False

        self.keys = Keys(self.consts['keys'])
        self.entities = self.init_entities()
        self.fov = FOV(self.entities['map'].obj.tiles)
        player = self.entities['player'].obj
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
            self.update()
            self.input()
            self.keys.flush()

    def init_entities(self):
        npc_graphics = self.graphics
        player_graphics = self.graphics
        map_graphics = self.graphics

        npc = NPC(self.consts['npc'])
        player = Player(self.consts['player'])
        map_ = Map(self.consts['map'])

        return OrderedDict([
            ('player', EntityCollection(player, player_graphics)),
            ('npc', EntityCollection(npc, npc_graphics)),
            ('map', EntityCollection(map_, map_graphics)),
        ])

    def get_consts(self):
        consts_list = ['player', 'npc', 'map', 'keys']
        consts = {}
        for c in consts_list:
            with open(os.path.join(self.settings.VARS_FOLDER, c + '.yml'), 'r') as f:
                consts[c] = yaml.load(f)
        return consts

    def update(self):
        if self.key_pressed:
            for entity in self.entities.values():
                update = getattr(entity.obj, 'update', noop)
                update()
        self.entities = OrderedDict([
            (k, v) for k, v in self.entities.iteritems() if getattr(v.obj, 'alive', True)
        ])

    def input(self):
        # TODO: Add update_render state on different tick
        self._input.update(self.keys, self)
        if self.key_pressed:
            for ent in self.entities.values():
                obj = ent.obj
                input_ = getattr(obj, 'input', noop)
                input_(self.keys, self)

    def render(self):
        render_params = {
            'player': {'x': 0, 'y': 0, 'w': 0, 'h': 0, 'dst': 0, 'xdst': 0, 'ydst': 0},
        }
        render_params['npc'] = render_params['player']
        for k, ent in self.entities.items():
            extra = render_params.get(k, {})
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
            if entity.pos == target.pos and target.blocking:  # Hit entity
                log.debug("{} overlapping {} {} prev={}".
                          format(entity, target, entity.pos, prev))
                entity.pos = prev
                target.collide(entity)
