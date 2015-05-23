from core.entity import Entity, Component


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
        self.tiles = [[Tile() for _ in range(self.rect['h'])]
                      for _ in range(self.rect['w'])]

        self.tiles[30][22].blocked = True
        self.tiles[30][22].block_sight = True
        self.tiles[50][22].blocked = True
        self.tiles[50][22].block_sight = True

        self.colour_wall = self.consts['wall']['bg_colour']
        self.colour_ground = self.consts['ground']
