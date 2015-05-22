from roguelike.core.entity import Entity, Component


class SimpleRender(Component):
    def update(self, graphics, entity):
        graphics.put_char(entity.x, entity.y, entity.char)

    def post_blit(self, graphics, entity):
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
        self._render = SimpleRender()
        self._input = PlayerInput()
        self.x = 0
        self.y = 0
        self.char = consts['char']

    def render(self, graphics):
        self._render.update(graphics, self)

    def post_blit(self, graphics):
        self._render.post_blit(graphics, self)

    def input(self, keys):
        self._input.update(keys, self)
