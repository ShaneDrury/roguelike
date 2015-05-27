import logging
import random
from core.entity import Entity, Component
from core.rect import Rect


log = logging.getLogger('rogue.mapping')


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
        for room in entity.rooms:
            x, y = room.center
            graphics.put_char(x, y, 'X')
            graphics.blit(x, y, 0, 0, 0, 0, 0)

        # TODO: Maybe pass some of this on to the Tile
        # Can do FSM stuff to simplify it
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
        self.rooms = []
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
        room_num_params = self.consts['room_num']
        room_num = int(random.gauss(room_num_params['avg'], room_num_params['std']))
        log.debug("Num rooms: {}".format(room_num))
        room_size_params = self.consts['room_size']

        for n in range(room_num):
            while True:
                w = int(random.gauss(room_size_params['avg'],
                                     room_size_params['std']))
                h = int(random.gauss(room_size_params['avg'],
                                     room_size_params['std']))
                x = random.randint(1, self.consts['rect']['w'] - w - 1)
                y = random.randint(1, self.consts['rect']['h'] - h - 1)
                room = Rect(x, y, w, h)
                for r in self.rooms:
                    if room.intersect(r, border=1):
                        break
                else:
                    self.rooms.append(room)
                    log.debug("Room {}: ({}, {}, {}, {})".format(n+1, x, y, w, h))
                    break

        for n, room in enumerate(self.rooms):
            self._carve_room(room, tiles)
            # TODO: Can make this a rolling window
            if n != 0:
                (prev_x, prev_y) = self.rooms[n-1].center
                if random.randint(0, 1):
                    self._carve_h_tunnel(prev_x, room.center.x, prev_y, tiles)
                    self._carve_v_tunnel(prev_y, room.center.y, room.center.x, tiles)
                else:
                    self._carve_v_tunnel(prev_y, room.center.y, prev_x, tiles)
                    self._carve_h_tunnel(prev_x, room.center.x, room.center.y, tiles)
        return tiles

    def _carve_h_tunnel(self, x1, x2, y, tiles):
        self._carve_room(Rect(min(x1, x2), y, abs(x2 - x1) + 1, 1), tiles)

    def _carve_v_tunnel(self, y1, y2, x, tiles):
        self._carve_room(Rect(x, min(y1, y2), 1, abs(y2 - y1) + 1), tiles)

    @staticmethod
    def _carve_room(room, tiles):
        for x in range(room.x1, room.x2):
            for y in range(room.y1, room.y2):
                tiles[x][y].blocked = False
                tiles[x][y].block_sight = False
