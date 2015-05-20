import os

import yaml

from roguelike import libtcod
from roguelike import settings
from roguelike.core.graphics import Graphics
from roguelike.player import Player

with open(settings.VARS_FILE, 'r') as f:
    consts = yaml.load(f)

graphics = Graphics()
graphics.set_custom_font(
    os.path.join(settings.FONT_DIR, 'arial10x10.png'),
    libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD
)
graphics.init_root(title='Roguelike', fullscreen=False, **settings.SCREEN)
player = Player()

while not libtcod.console_is_window_closed():
    key = libtcod.console_check_for_keypress()
    exited = key.vk == libtcod.KEY_ESCAPE
    if exited:
        break
    libtcod.console_set_default_foreground(0, libtcod.white)
    player.render(graphics)
    graphics.flush()
