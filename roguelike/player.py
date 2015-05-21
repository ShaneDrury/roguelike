from roguelike.core.entity import Entity, Component


class PlayerRender(Component):
    def update(self, graphics, entity):
        graphics.put_char(entity.x, entity.y, entity.char)
        graphics.flush()
        graphics.put_char(entity.x, entity.y, ' ')


class PlayerInput(Component):
    def __init__(self):
        self.checking = True

    def update(self, keys, entity):
        key = keys.check_for_keypress(keys.KEY_PRESSED)
        if key.vk == keys.KEY_RIGHT:
            entity.x += 1
        elif key.vk == keys.KEY_LEFT:
            entity.x -= 1
        elif key.vk == keys.KEY_UP:
            entity.y -= 1
        elif key.vk == keys.KEY_DOWN:
            entity.y += 1


class Player(Entity):
    def __init__(self, consts):
        self._render = PlayerRender()
        self._input = PlayerInput()
        self.x = 0
        self.y = 0
        self.char = consts['player_char']

    def render(self, graphics):
        self._render.update(graphics, self)

    def input(self, keys):
        self._input.update(keys, self)
