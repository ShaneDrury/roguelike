import os
from core.entity import Entity, Component


class GameInput(Component):
    def update(self, keys, entity):
        key = keys.check_for_keypress(keys.KEY_RELEASED)
        entity.exited = key.vk == keys.KEY_ESCAPE


class Game(Entity):
    def __init__(self, graphics, keys, player, font, colour, settings):
        self._input = GameInput()
        self.exited = False

        self.graphics = graphics
        self.keys = keys
        self.player = player
        self.font = font
        self.colour = colour
        self.settings = settings

    def main(self):
        self.graphics.set_custom_font(
            os.path.join(self.settings.FONT_DIR, 'arial10x10.png'),
            self.font.FONT_TYPE_GREYSCALE | self.font.FONT_LAYOUT_TCOD
        )
        self.graphics.init_root(title='Roguelike', fullscreen=False,
                                **self.settings.SCREEN)
        self.graphics.set_default_foreground(0, self.colour.white)
        while not self.exited:
            self.input()
            self.render()
            self.keys.flush()

    def input(self):
        self._input.update(self.keys, self)
        self.player.input(self.keys)

    def render(self):
        self.player.render(self.graphics)
