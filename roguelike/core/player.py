from roguelike.core.entity import Entity, Component, Point


class SimpleRender(Component):
    def update(self, graphics, entity, **kwargs):
        self._set_colour(graphics, entity)
        x, y = entity.pos
        graphics.put_char(x, y, entity.char)
        self._blit(graphics, **kwargs)

    def _set_colour(self, graphics, entity):
        graphics.set_default_foreground(
            getattr(graphics.colour, entity.consts.get('colour', 'white'))
        )

    def _blit(self, graphics, x, y, w, h, dst, xdst, ydst):
        graphics.blit(x, y, w, h, dst, xdst, ydst)

    def post_render(self, graphics, entity):
        x, y = entity.pos
        graphics.put_char(x, y, ' ')


class PlayerInput(Component):
    def update(self, keys, entity, world):
        key = keys.check_for_keypress(keys.KEY_PRESSED)
        prev = entity.pos
        x, y = entity.pos
        if key.vk == keys.KEY_RIGHT:
            x += 1
        elif key.vk == keys.KEY_LEFT:
            x -= 1
        elif key.vk == keys.KEY_UP:
            y -= 1
        elif key.vk == keys.KEY_DOWN:
            y += 1
        entity.pos = Point(x, y)
        world.resolve_collision(entity, prev)


class Player(Entity):
    def __init__(self, consts):
        super(Player, self).__init__()
        self._render = SimpleRender()
        self._input = PlayerInput()
        self.pos = Point(0, 0)
        self.consts = consts
        self.char = consts['char']

    def post_render(self, graphics):
        self._render.post_render(graphics, self)

    def input(self, keys, world):
        self._input.update(keys, self, world)
