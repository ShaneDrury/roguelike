# A simple disjoint set ADT which uses path compression on finds
# to speed things up


class DisjointSet:
    size = 0

    def __init__(self):
        self.__items = {}

    def union(self, root1, root2):
        if self.__items[root2] < self.__items[root1]:
            self.__items[root1] = root2
        else:
            if self.__items[root1] == self.__items[root2]:
                self.__items[root1] -= 1

            self.__items[root2] = root1

    def find(self, x):
        try:
            while self.__items[x] > 0:
                x = self.__items[x]

        except KeyError:
            self.__items[x] = -1

        return x

    def split_sets(self):
        sets = {}
        for j in self.__items.keys():
            root = self.find(j)

            if root > 0:
                if root in sets:
                    list_ = sets[root]
                    list_.append(j)

                    sets[root] = list_
                else:
                    sets[root] = [j]

        return sets

    def dump(self):
        print self.__items
