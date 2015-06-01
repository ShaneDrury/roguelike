from core.entity import Entity, Component


class InventoryInput(Component):
    def __init__(self):
        self.keys_dict = {
            'INVENTORY': self.toggle_inventory
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


class InventoryRender(Component):
    def update(self, graphics, fov, entity, **kwargs):
        pass


class Inventory(Entity):
    def __init__(self):
        super(Inventory, self).__init__()
        self._render = InventoryRender()
        self._input = InventoryInput()
        self.blocked_input = True

    def input(self, keys, world, turn):
        self._input.update(keys, world, self)
