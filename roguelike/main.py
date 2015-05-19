import os
import roguelike.libtcod as libtcod
from roguelike import settings

libtcod.console_set_custom_font(
    os.path.join(settings.FONT_DIR, 'arial10x10.png'),
    libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD
)
libtcod.console_init_root(settings.screen['width'], settings.screen['height'],
                          title='Roguelike', fullscreen=False)

while not libtcod.console_is_window_closed():
    key = libtcod.console_check_for_keypress()
    exited = key.vk == libtcod.KEY_ESCAPE
    if exited:
        break
    libtcod.console_set_default_foreground(0, libtcod.white)
    libtcod.console_put_char(0, 1, 1, '@', libtcod.BKGND_NONE)
    libtcod.console_flush()
