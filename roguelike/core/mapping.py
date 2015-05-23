from core.entity import Entity, Component
from core.rect import Rect


class TileRender(Component):
    def update(self, graphics, entity):
        pass


class Tile(Entity):
    def __init__(self, blocked=False, block_sight=None):
        super(Tile, self).__init__()
        self._render = TileRender()
        self.blocked = blocked
        self.block_sight = blocked if block_sight is None else block_sight


class MapRender(Component):
    @staticmethod
    def update(graphics, entity):
        for x, row in enumerate(entity.tiles):
            for y, tile in enumerate(row):
                colour = entity.colour_wall if tile.block_sight else entity.colour_ground
                if tile.blocked:
                    graphics.set_default_foreground(
                        getattr(graphics.colour, entity.consts['wall']['char_colour'])
                    )
                    graphics.put_char(x, y, entity.consts['wall']['char'])
                graphics.set_char_background(x, y, getattr(graphics.colour, colour))


class Map(Entity):
    def __init__(self, consts):
        super(Map, self).__init__()
        self.consts = consts
        self._render = MapRender()
        self.rect = consts['rect']
        self.tiles = self._generate_map()
        self.colour_wall = self.consts['wall']['bg_colour']
        self.colour_ground = self.consts['ground']

    def _generate_map(self):
        tiles = [[Tile(blocked=True) for _ in range(self.rect['h'])]
                 for _ in range(self.rect['w'])]
        room1 = Rect(20, 15, 10, 15)
        room2 = Rect(50, 15, 10, 15)
        rooms = [room1, room2]
        for room in rooms:
            self._carve_room(room, tiles)
        self._carve_room(Rect(25, 23, 30, 2), tiles)
        return tiles

    def _carve_room(self, room, tiles):
        for x in range(room.x1, room.x2):
            for y in range(room.y1, room.y2):
                tiles[x][y].blocked = False
                tiles[x][y].block_sight = False
