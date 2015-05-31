from core.entity import Component


class SimpleRender(Component):
    def update(self, graphics, fov, entity, **kwargs):
        x, y = entity.pos
        if fov.is_in_fov(x, y):
            self._set_colour(graphics, entity)
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
