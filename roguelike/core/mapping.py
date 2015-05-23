from core.entity import Entity, Component
from core.rect import Rect


class TileRender(Component):
    def update(self, graphics, fov, entity):
        pass


class Tile(Entity):
    def __init__(self, blocked=False, block_sight=None):
        super(Tile, self).__init__()
        self._render = TileRender()
        self.blocked = blocked
        self.block_sight = blocked if block_sight is None else block_sight
        self.uncovered = False


class MapRender(Component):
    @staticmethod
    def update(graphics, fov, entity):
        for x, row in enumerate(entity.tiles):
            for y, tile in enumerate(row):
                wall = tile.block_sight
                if fov.is_in_fov(x, y):
                    if wall:
                        fg_colour = entity.consts['wall']['char_colour']
                        bg_colour = entity.colours['wall']['visible']
                        char = entity.consts['wall']['char']
                    else:
                        fg_colour = entity.consts['floor']['char_colour']
                        bg_colour = entity.colours['floor']['visible']
                        char = entity.consts['floor']['char']
                    graphics.set_default_foreground(
                        getattr(graphics.colour, fg_colour)
                    )
                    graphics.put_char(x, y, char)
                    tile.uncovered = True
                else:
                    if tile.uncovered:
                        if wall:
                            bg_colour = entity.colours['wall']['invisible']
                        else:
                            bg_colour = entity.colours['floor']['invisible']
                    else:
                        bg_colour = None
                if bg_colour:
                    graphics.set_char_background(
                        x, y, getattr(graphics.colour, bg_colour)
                    )


class Map(Entity):
    def __init__(self, consts):
        super(Map, self).__init__()
        self.consts = consts
        self._render = MapRender()
        self.rect = consts['rect']
        self.tiles = self._generate_map()
        self.colours = {
            'wall': {'visible': self.consts['wall']['visible_colour'],
                     'invisible': self.consts['wall']['invisible_colour']},
            'floor': {'visible': self.consts['floor']['visible_colour'],
                      'invisible': self.consts['floor']['invisible_colour']}
        }

    def _generate_map(self):
        tiles = [[Tile(blocked=True) for _ in range(self.rect['h'])]
                 for _ in range(self.rect['w'])]
        room1 = Rect(20, 15, 10, 15)
        room2 = Rect(50, 15, 10, 15)
        for room in [room1, room2]:
            self._carve_room(room, tiles)
        self._carve_room(Rect(25, 23, 30, 1), tiles)
        return tiles

    def _carve_room(self, room, tiles):
        for x in range(room.x1, room.x2):
            for y in range(room.y1, room.y2):
                tiles[x][y].blocked = False
                tiles[x][y].block_sight = False
