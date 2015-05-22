from core.entity import Entity
from core.player import SimpleRender


class NPCRender(SimpleRender):
    pass

class NPC(Entity):
    def __init__(self, consts):
        self.x = 50
        self.y = 0
        self._render = NPCRender()
        self.char = consts['char']

    def render(self, graphics):
        self._render.update(graphics, self)

    def post_blit(self, graphics):
        self._render.post_blit(graphics, self)
