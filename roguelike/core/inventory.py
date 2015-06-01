from functools import partial
from core.entity import Entity, Component
from core.panel import BarRender


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


class InventoryRender(Component):
    def __init__(self):
        self.bar_render = BarRender()

    def update(self, graphics, **kwargs):
        player_hp = 10
        player_max_hp = 20
        bar_x = 30
        self.pre_render(graphics)
        self.bar_render.bar(1, 1, bar_x, 'HP', player_hp, player_max_hp,
                            graphics.colour.light_red, graphics.colour.darker_red,
                            graphics)
        self._blit(graphics, **kwargs)

    @staticmethod
    def pre_render(graphics):
        graphics.set_default_background(graphics.colour.black)
        graphics.clear()

    @staticmethod
    def _blit(graphics, x, y, w, h, dst, xdst, ydst):
        graphics.blit(x, y, w, h, dst, xdst, ydst)


class Inventory(Entity):
    def __init__(self, fsm):
        super(Inventory, self).__init__()
        self._render = InventoryRender()
        self._input = InventoryInput()
        self.fsm = fsm

    def input(self, keys, world, turn):
        self._input.update(keys, world, self)

    def render(self, graphics, fov, **kwargs):
        if self.fsm.current == 'inventory':
            self._render.update(graphics, **kwargs)
