from core.entity import Entity
from core.player import SimpleRender


class NPCRender(SimpleRender):
    pass


class NPC(Entity):
    def __init__(self, consts):
        super(NPC, self).__init__()
        self.x = 25
        self.y = 0
        self._render = NPCRender()
        self.consts = consts
        self.char = consts['char']

    def post_render(self, graphics):
        self._render.post_render(graphics, self)
