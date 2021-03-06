import string

from core.entity import Entity, Component


class InventoryInput(Component):
    def update(self, keys, fsm, entity):
        key = keys.check_for_keypress(keys.KEY_PRESSED)
        if key == 'INVENTORY':
            self.toggle_inventory(fsm)
        else:
            self.handle_keys(fsm, key, entity)

    @staticmethod
    def toggle_inventory(fsm):
        if fsm.current == 'game':
            fsm.open_inventory()
        elif fsm.current == 'inventory':
            fsm.close_inventory()

    @staticmethod
    def handle_keys(fsm, key, entity):
        if fsm.current == 'inventory':
            entity.use_item(key)


class InventoryItemRender(Component):
    def render(self, graphics, x, y, item, alpha_index):
        msg = "{})   {} {}".format(alpha_index, item.char, item.name)
        # TODO: Make the string colourful
        # colour = item.colour
        colour = 'white'
        graphics.set_default_foreground(colour)
        graphics.print_ex(x, y, graphics.background.BKGND_NONE, graphics.LEFT, msg)


class InventoryRender(Component):
    def __init__(self):
        self.inventory_item = InventoryItemRender()

    def update(self, graphics, rect, inventory, **kwargs):
        self.pre_render(graphics, graphics.colour.desaturated_blue)
        graphics.rect(0, 0, rect['w'], rect['h'],
                      False, graphics.background.BKGND_SCREEN)
        sorted_keys = sorted(inventory.keys())
        for y, k in enumerate(sorted_keys):
            self.inventory_item.render(graphics, 0, y, inventory[k], k)
        self._blit(graphics, **kwargs)

    @staticmethod
    def pre_render(graphics, colour):
        graphics.set_default_background(colour)
        graphics.clear()

    @staticmethod
    def _blit(graphics, x, y, w, h, dst, xdst, ydst):
        graphics.blit(x, y, w, h, dst, xdst, ydst)


class Inventory(Entity):
    def __init__(self, fsm, player, turn, consts):
        super(Inventory, self).__init__()
        self._render = InventoryRender()
        self._input = InventoryInput()
        self.fsm = fsm
        self.player = player
        self.rect = consts['rect']
        self.items = {}
        self.turn = turn

    def add(self, item):
        available_letters = [s for s in string.ascii_lowercase if s not in self.items]
        try:
            letter = available_letters[0]
        except IndexError:
            return False
        self.items[letter] = item
        return True

    def remove(self, item):
        for k, v in self.items.iteritems():
            if v == item:
                del self.items[k]
                break
        else:
            raise KeyError("No such item {}".format(item))

    def input(self, keys, world, turn):
        self._input.update(keys, world.fsm, self)

    def render(self, graphics, fov, **kwargs):
        if self.fsm.current == 'inventory':
            self._render.update(graphics, self.rect, self.items, **kwargs)

    def use_item(self, key):
        item = self.items.get(key)
        if item:
            item.use(self.player, self.turn)
            self.fsm.close_inventory()
