from fysom import Fysom
from core.entity import Entity, Component


class InventoryInput(Component):
    def __init__(self):
        self.keys_dict = {
            'INVENTORY': self.toggle_inventory
        }

    def update(self, keys, world, entity, fsm, state):
        key = keys.check_for_keypress(keys.KEY_PRESSED)
        func = self.keys_dict.get(key)
        if func:
            func(fsm, state)

    @staticmethod
    def toggle_inventory(fsm, state):
        if state == 'closed':
            fsm.open()
        else:
            fsm.close()


class InventoryRender(Component):
    def update(self, graphics, fov, entity, **kwargs):
        if entity.fsm.current == 'opened':
            print("OPEN")


class Inventory(Entity):
    def __init__(self):
        super(Inventory, self).__init__()
        self._render = InventoryRender()
        self._input = InventoryInput()
        self.blocked_input = True
        self.fsm = Fysom({
            'initial': 'closed',
            'events': [
                {'name': 'open', 'src': 'closed', 'dst': 'opened'},
                {'name': 'close', 'src': 'opened', 'dst': 'closed'}
            ]
        })

    def input(self, keys, world, turn):
        self._input.update(keys, world, self, self.fsm, self.fsm.current)
