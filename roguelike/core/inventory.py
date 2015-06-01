from functools import partial
from core.entity import Entity, Component


class InventoryInput(Component):
    def __init__(self):
        self.keys_dict = {
            'INVENTORY': self.toggle_inventory,
            'UP': partial(self.handle_keys, key='UP'),
            'DOWN': partial(self.handle_keys, key='DOWN')
        }

    def update(self, keys, world, entity):
        key = keys.check_for_keypress(keys.KEY_PRESSED)
        func = self.keys_dict.get(key)
        if func:
            func(world)

    def toggle_inventory(self, world):
        if world.fsm.current == 'game':
            world.fsm.open_inventory()
        elif world.fsm.current == 'inventory':
            world.fsm.close_inventory()

    def handle_keys(self, world, key):
        if world.fsm.current == 'inventory':
            print(key)


class InventoryItemRender(Component):
    def render(self, graphics, x, y, item):
        msg = "{} {}".format(item.char, item.name)
        colour = item.colour
        graphics.set_default_foreground(colour)
        graphics.print_ex(x, y, graphics.background.BKGND_NONE, graphics.LEFT, msg)


class InventoryRender(Component):
    def __init__(self):
        self.inventory_item = InventoryItemRender()

    def update(self, graphics, rect, inventory, **kwargs):
        self.pre_render(graphics, graphics.colour.desaturated_blue)
        graphics.rect(0, 0, rect['w'], rect['h'], False, graphics.background.BKGND_SCREEN)
        for y, item in enumerate(inventory):
            self.inventory_item.render(graphics, 0, y, item)
        self._blit(graphics, **kwargs)

    @staticmethod
    def pre_render(graphics, colour):
        graphics.set_default_background(colour)
        graphics.clear()

    @staticmethod
    def _blit(graphics, x, y, w, h, dst, xdst, ydst):
        graphics.blit(x, y, w, h, dst, xdst, ydst)


class Inventory(Entity):
    def __init__(self, fsm, player, consts):
        super(Inventory, self).__init__()
        self._render = InventoryRender()
        self._input = InventoryInput()
        self.fsm = fsm
        self.player = player
        self.rect = consts['rect']

    def input(self, keys, world, turn):
        self._input.update(keys, world, self)

    def render(self, graphics, fov, **kwargs):
        if self.fsm.current == 'inventory':
            self._render.update(graphics, self.rect, self.player.inventory, **kwargs)
