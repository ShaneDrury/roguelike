from roguelike.core.entity import Entity, Component, Point


class SimpleRender(Component):
    def update(self, graphics, entity, **kwargs):
        self._set_colour(graphics, entity)
        x, y = entity.pos
        graphics.put_char(x, y, entity.char)
        self._blit(graphics, **kwargs)

    @staticmethod
    def _set_colour(graphics, entity):
        graphics.set_default_foreground(
            getattr(graphics.colour, entity.consts.get('colour', 'white'))
        )

    @staticmethod
    def _blit(graphics, x, y, w, h, dst, xdst, ydst):
        graphics.blit(x, y, w, h, dst, xdst, ydst)

    @staticmethod
    def post_render(graphics, entity):
        x, y = entity.pos
        graphics.put_char(x, y, ' ')


class PlayerInput(Component):
    def __init__(self):
        self.keys_dict = {
            'RIGHT': Point(1, 0),
            'LEFT': Point(-1, 0),
            'UP': Point(0, -1),
            'DOWN': Point(0, 1),
            'UP_LEFT': Point(-1, -1),
            'UP_RIGHT': Point(1, -1),
            'DOWN_RIGHT': Point(1, 1),
            'DOWN_LEFT': Point(-1, 1)
        }

    def update(self, keys, entity, world):
        key = keys.check_for_keypress(keys.KEY_PRESSED)
        prev = entity.pos
        x, y = entity.pos
        diff = self.keys_dict.get(key, None)
        if diff:
            entity.pos = Point(x + diff.x, y + diff.y)
            world.resolve_collision(entity, prev)


class Player(Entity):
    def __init__(self, consts):
        super(Player, self).__init__()
        self._render = SimpleRender()
        self._input = PlayerInput()
        self.pos = Point(25, 23)
        self.consts = consts
        self.char = consts['char']

    def post_render(self, graphics):
        self._render.post_render(graphics, self)

    def input(self, keys, world):
        self._input.update(keys, self, world)
