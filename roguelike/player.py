from roguelike.core.entity import Entity, Component


class PlayerRender(Component):
    def render(self, graphics):
        graphics.put_char(1, 1, '@')

class Player(Entity):
    def __init__(self):
        self._render = PlayerRender()

    def render(self, graphics):
        self._render.render(graphics)
