from core.entity import Point


class Rect(object):
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.w = w
        self.h = h
        self.x2 = x + w
        self.y2 = y + h

    def intersect(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

    @property
    def center(self):
        return Point(self.x1 + int(self.w / 2), self.y1 + int(self.h / 2))
