from random import randrange
from disjoint import DisjointSet

PERM_WALL = 0
WALL = 1
FLOOR = 2


class CaveFactory:
    def __init__(self, w, h, initial_open=0.40):
        """
        >>> caf = CaveFactory(80, 45, 0.41)
        >>> caf.gen_map()
        >>> caf.print_grid()
        """
        self.height = h
        self.width = w
        self.area = h * w
        self.map = []
        self.ds = DisjointSet()
        self.up_loc = 0
        self.center_pt = (int(self.height / 2), int(self.width / 2))
        self._gen_initial_map(initial_open)

    def print_grid(self):
        for r in range(0, self.height):
            for c in range(0, self.width):
                if self.map[r][c] in (WALL, PERM_WALL):
                    print '#',
                else:
                    print '.',
            print

    def gen_map(self):
        for r in range(1, self.height - 1):
            for c in range(1, self.width - 1):
                wall_count = self._adj_wall_count(r, c)

                if self.map[r][c] == FLOOR:
                    if wall_count > 5:
                        self.map[r][c] = WALL
                elif wall_count < 4:
                    self.map[r][c] = FLOOR

        self._join_rooms()

        return self.map

    # make all border squares walls
    # This could be moved to a superclass
    def _set_border(self):
        for j in range(0, self.height):
            self.map[j][0] = PERM_WALL
            self.map[j][self.width - 1] = PERM_WALL

        for j in range(0, self.width):
            self.map[0][j] = PERM_WALL
            self.map[self.height - 1][j] = PERM_WALL

    def _gen_initial_map(self, initial_open):
        for r in range(0, self.height):
            row = []
            for c in range(0, self.width):
                row.append(WALL)
            self.map.append(row)

        open_count = int(self.area * initial_open)
        self._set_border()

        while open_count > 0:
            rand_r = randrange(1, self.height - 1)
            rand_c = randrange(1, self.width - 1)

            if self.map[rand_r][rand_c] == WALL:
                self.map[rand_r][rand_c] = FLOOR
                open_count -= 1

    def _adj_wall_count(self, sr, sc):
        count = 0

        for r in (-1, 0, 1):
            for c in (-1, 0, 1):
                if self.map[(sr + r)][sc + c] != FLOOR and not (r == 0 and c == 0):
                    count += 1

        return count

    def _join_rooms(self):
        # divide the square into equivalence classes
        for r in range(1, self.height - 1):
            for c in range(1, self.width - 1):
                if self.map[r][c] == FLOOR:
                    self._union_adj_sqr(r, c)

        all_caves = self.ds.split_sets()

        for cave in all_caves.keys():
            self._join_points(all_caves[cave][0])

    def _join_points(self, pt1):
        while True:
            direction = self._get_tunnel_dir(pt1, self.center_pt)
            move = randrange(0, 3)

            if move == 0:
                next_pt = (pt1[0] + direction[0], pt1[1])
            elif move == 1:
                next_pt = (pt1[0], pt1[1] + direction[1])
            else:
                next_pt = (pt1[0] + direction[0], pt1[1] + direction[1])

            if self._stop_drawing(pt1, next_pt, self.center_pt):
                return

            root1 = self.ds.find(next_pt)
            root2 = self.ds.find(pt1)

            if root1 != root2:
                self.ds.union(root1, root2)

            self.map[next_pt[0]][next_pt[1]] = FLOOR

            pt1 = next_pt

    def _stop_drawing(self, pt, npt, cpt):
        if self.ds.find(npt) == self.ds.find(cpt):
            return 1
        if self.ds.find(pt) != self.ds.find(npt) \
                and self.map[npt[0]][npt[1]] == FLOOR:
            return 1
        else:
            return 0

    @staticmethod
    def _get_tunnel_dir(pt1, pt2):
        if pt1[0] < pt2[0]:
            h_dir = +1
        elif pt1[0] > pt2[0]:
            h_dir = -1
        else:
            h_dir = 0

        if pt1[1] < pt2[1]:
            v_dir = +1
        elif pt1[1] > pt2[1]:
            v_dir = -1
        else:
            v_dir = 0

        return h_dir, v_dir

    def _union_adj_sqr(self, sr, sc):
        loc = (sr, sc)

        for r in (-1, 0):
            for c in (-1, 0):
                nloc = (sr + r, sc + c)

                if self.map[nloc[0]][nloc[1]] == FLOOR:
                    root1 = self.ds.find(loc)
                    root2 = self.ds.find(nloc)

                    if root1 != root2:
                        self.ds.union(root1, root2)
