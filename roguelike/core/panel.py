from core.entity import Entity, Component


class EntityRender(Component):
    def update(self, consts, graphics, **kwargs):
        self.render_bar(1, 1, consts['bar']['w'], 'HP', 10, 20,
                        graphics.colour.light_red, graphics.colour.darker_red, graphics)
        self._blit(graphics, **kwargs)

    @staticmethod
    def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color,
                   graphics):
        bar_width = int(float(value) / maximum * total_width)
        graphics.set_default_background(back_color)
        graphics.rect(x, y, total_width, 1, False, graphics.background.BKGND_SCREEN)
        graphics.set_default_background(bar_color)
        if bar_width > 0:
            graphics.rect(x, y, bar_width, 1, False, graphics.background.BKGND_SCREEN)
        graphics.set_default_foreground(graphics.colour.white)
        graphics.print_ex(x + total_width / 2, y, graphics.background.BKGND_NONE,
                          graphics.CENTER,
                          name + ': ' + str(value) + '/' + str(maximum))

    @staticmethod
    def _blit(graphics, x, y, w, h, dst, xdst, ydst):
        graphics.blit(x, y, w, h, dst, xdst, ydst)


class Panel(Entity):
    def __init__(self, consts):
        super(Panel, self).__init__()
        self.consts = consts
        self._render = EntityRender()

    def render(self, graphics, fov, **kwargs):
        self._render.update(self.consts, graphics, **kwargs)
