import libtcod


class FOV(object):
    def __init__(self, tiles):
        self.t = libtcod
        self.fov_map = self.init_map(tiles)
        self.algo_dict = {
            'BASIC': self.t.FOV_BASIC,
            'DIAMOND': self.t.FOV_DIAMOND,
            'SHADOW': self.t.FOV_SHADOW
        }
        self.algorithm = self.algo_dict['BASIC']
        self.light_walls = True
        self.torch_radius = 100

    def init_map(self, tiles):
        fov_map = self.t.map_new(len(tiles), len(tiles[0]))
        for x, row in enumerate(tiles):
            for y, tile in enumerate(row):
                self.t.map_set_properties(fov_map,
                                          x, y,
                                          not tile.block_sight,
                                          not tile.blocked)
        return fov_map

    def recompute(self, x, y):
        self.t.map_compute_fov(self.fov_map, x, y,
                               self.torch_radius, self.light_walls, self.algorithm)

    def is_in_fov(self, x, y):
        return self.t.map_is_in_fov(self.fov_map, x, y)
