import os

from core.entity import Entity, Component
from core.graphics import Graphics


class GameInput(Component):
    def update(self, keys, entity):
        key = keys.check_for_keypress(keys.KEY_RELEASED)
        entity.exited = key.vk == keys.KEY_ESCAPE


class Game(Entity):
    def __init__(self, keys, player, font, colour, settings):
        self.keys = keys
        self.player = player
        self.font = font
        self.colour = colour
        self.settings = settings

        self._input = GameInput()
        self.exited = False
        self.graphics = Graphics(**self.settings.SCREEN)
        self.player_graphics = Graphics(**self.settings.SCREEN)

    def main(self):
        self.font.set_custom_font(
            os.path.join(self.settings.FONT_DIR, 'arial10x10.png'),
            self.font.FONT_TYPE_GREYSCALE | self.font.FONT_LAYOUT_TCOD
        )
        self.graphics.init_root(title='Roguelike', fullscreen=False,
                                **self.settings.SCREEN)
        self.player_graphics.set_default_foreground(self.colour.white)
        while not self.exited:
            self.input()
            self.render()
            self.keys.flush()

    def input(self):
        self._input.update(self.keys, self)
        self.player.input(self.keys)

    def render(self):
        self.player.render(self.player_graphics)
        self.player_graphics.flush()
        self.player_graphics.blit(x=0, y=0,
                                  w=self.settings.SCREEN['w'],
                                  h=self.settings.SCREEN['h'],
                                  dst=0,
                                  xdst=0, ydst=0)
        self.player.post_blit(self.player_graphics)

        # TODO: We have to blit just before the flush, but the Player can't do it
        # since they should have no control over where they render to.
        # The Game object does that. The player can render to player_graphics and
        # we can then tell it to
