import os

import yaml

from core.entity import Entity, Component
from core.graphics import Graphics
from core.npc import NPC
from core.player import Player


class GameInput(Component):
    def update(self, keys, entity):
        key = keys.check_for_keypress(keys.KEY_RELEASED)
        entity.exited = key.vk == keys.KEY_ESCAPE


class Game(Entity):
    def __init__(self, keys, font, colour, settings):
        self.keys = keys
        self.font = font
        self.colour = colour
        self.settings = settings

        self._input = GameInput()
        self.exited = False
        self.graphics = Graphics(**self.settings.SCREEN)
        self.consts = self.get_consts()
        self.entities = self.init_entities()

    def init_entities(self):
        npc_graphics = self.graphics
        npc = NPC(self.consts['npc'])

        player_graphics = self.graphics
        player = Player(self.consts['player'])

        return [{'key': 'player', 'obj': player, 'gfx': player_graphics},
                {'key': 'npc', 'obj': npc, 'gfx': npc_graphics}]

    def get_consts(self):
        consts_list = ['player', 'npc']
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
            try:
                entity['obj'].input(self.keys)
            except AttributeError:
                pass

    def render(self):
        for entity in self.entities:
            entity['gfx'].set_default_foreground(
                getattr(self.colour, self.consts[entity['key']]['colour'])
            )

            entity['obj'].render(entity['gfx'])
            entity['gfx'].blit(x=0, y=0,
                               w=self.settings.SCREEN['w'],
                               h=self.settings.SCREEN['h'],
                               dst=0,
                               xdst=0, ydst=0)
        self.graphics.flush()
        for entity in self.entities:
            entity['obj'].post_blit(entity['gfx'])
