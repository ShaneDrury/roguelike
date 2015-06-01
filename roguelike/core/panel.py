from core.entity import Entity, Component


class BarRender(Component):
    @staticmethod
    def bar(x, y, total_width, name, value, maximum, bar_color, back_color, graphics):
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


class MessageRender(Component):
    # TODO: Probably move this to Message as its component
    @staticmethod
    def render_all(messages, graphics, x):
        for y, (line, colour) in enumerate(messages, start=1):
            graphics.set_default_foreground(colour)
            graphics.print_ex(x, y, graphics.background.BKGND_NONE, graphics.LEFT, line)


class PanelRender(Component):
    def __init__(self):
        self.bar_render = BarRender()
        self.msg_render = MessageRender()

    def update(self, consts, graphics, world, **kwargs):
        player_hp = world.entities['player'].obj.hp
        player_max_hp = world.entities['player'].obj.max_hp
        bar_x = consts['bar']['w']
        msg_x = bar_x + 2
        self.pre_render(graphics)
        self.bar_render.bar(1, 1, bar_x, 'HP', player_hp, player_max_hp,
                            graphics.colour.light_red, graphics.colour.darker_red,
                            graphics)
        self.msg_render.render_all(world.message.messages, graphics, msg_x)
        self._blit(graphics, **kwargs)

    @staticmethod
    def pre_render(graphics):
        graphics.set_default_background(graphics.colour.black)
        graphics.clear()

    @staticmethod
    def _blit(graphics, x, y, w, h, dst, xdst, ydst):
        graphics.blit(x, y, w, h, dst, xdst, ydst)


class Panel(Entity):
    def __init__(self, consts, world):
        super(Panel, self).__init__()
        self.consts = consts
        self.world = world
        self._render = PanelRender()

    def render(self, graphics, fov, **kwargs):
        self._render.update(self.consts, graphics, self.world, **kwargs)
