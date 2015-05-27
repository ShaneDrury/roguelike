from core.entity import Entity, Component


class EntityRender(Component):
    @staticmethod
    def update():
        pass

class Panel(Entity):
    def __init__(self):
        super(Panel, self).__init__()
        self._render = EntityRender()

    def render(self, graphics, fov, **kwargs):
        self._render.update()
