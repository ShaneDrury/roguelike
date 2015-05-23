from roguelike.core.entity import Entity, Component


class SimpleRender(Component):
    def update(self, graphics, entity, **kwargs):
        self._set_colour(graphics, entity)
        graphics.put_char(entity.x, entity.y, entity.char)
        self._blit(graphics, **kwargs)

    def _set_colour(self, graphics, entity):
        graphics.set_default_foreground(
            getattr(graphics.colour, entity.consts.get('colour', 'white'))
        )

    def _blit(self, graphics, x, y, w, h, dst, xdst, ydst):
        graphics.blit(x, y, w, h, dst, xdst, ydst)

    def post_render(self, graphics, entity):
        graphics.put_char(entity.x, entity.y, ' ')


class PlayerInput(Component):
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
        super(Player, self).__init__()
        self._render = SimpleRender()
        self._input = PlayerInput()
        self.x = 0
        self.y = 0
        self.consts = consts
        self.char = consts['char']

    def post_render(self, graphics):
        self._render.post_render(graphics, self)

    def input(self, keys):
        self._input.update(keys, self)
