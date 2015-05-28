import libtcod


class Colour(object):
    def __init__(self):
        self.t = libtcod

    def lerp(self, c1, c2, a):
        return self.t.color_lerp(c1, c2, a)

    def set_hsv(self, c, h, s, v):
        self.t.color_set_hsv(c, h, s, v)

    def get_hsv(self, c):
        return self.t.color_get_hsv(c)

    def scale_hsv(self, c, scoef, vcoef):
        self.t.color_scale_HSV(c, scoef, vcoef)

    def gen_map(self, colors, indexes):
        return self.t.color_gen_map(colors, indexes)

    def __getattr__(self, item):
        if item in self.allowed:
            return getattr(self.t, item)
        else:
            raise AttributeError("No such colour {}".format(item))

    allowed = ["black",
               "darkest_grey",
               "darker_grey",
               "dark_grey",
               "grey",
               "light_grey",
               "lighter_grey",
               "lightest_grey",
               "darkest_gray",
               "darker_gray",
               "dark_gray",
               "gray",
               "light_gray",
               "lighter_gray",
               "lightest_gray",
               "white",
               "darkest_sepia",
               "darker_sepia",
               "dark_sepia",
               "sepia",
               "light_sepia",
               "lighter_sepia",
               "lightest_sepia",
               "red",
               "flame",
               "orange",
               "amber",
               "yellow",
               "lime",
               "chartreuse",
               "green",
               "sea",
               "turquoise",
               "cyan",
               "sky",
               "azure",
               "blue",
               "han",
               "violet",
               "purple",
               "fuchsia",
               "magenta",
               "pink",
               "crimson",
               "dark_red",
               "dark_flame",
               "dark_orange",
               "dark_amber",
               "dark_yellow",
               "dark_lime",
               "dark_chartreuse",
               "dark_green",
               "dark_sea",
               "dark_turquoise",
               "dark_cyan",
               "dark_sky",
               "dark_azure",
               "dark_blue",
               "dark_han",
               "dark_violet",
               "dark_purple",
               "dark_fuchsia",
               "dark_magenta",
               "dark_pink",
               "dark_crimson",
               "darker_red",
               "darker_flame",
               "darker_orange",
               "darker_amber",
               "darker_yellow",
               "darker_lime",
               "darker_chartreuse",
               "darker_green",
               "darker_sea",
               "darker_turquoise",
               "darker_cyan",
               "darker_sky",
               "darker_azure",
               "darker_blue",
               "darker_han",
               "darker_violet",
               "darker_purple",
               "darker_fuchsia",
               "darker_magenta",
               "darker_pink",
               "darker_crimson",
               "darkest_red",
               "darkest_flame",
               "darkest_orange",
               "darkest_amber",
               "darkest_yellow",
               "darkest_lime",
               "darkest_chartreuse",
               "darkest_green",
               "darkest_sea",
               "darkest_turquoise",
               "darkest_cyan",
               "darkest_sky",
               "darkest_azure",
               "darkest_blue",
               "darkest_han",
               "darkest_violet",
               "darkest_purple",
               "darkest_fuchsia",
               "darkest_magenta",
               "darkest_pink",
               "darkest_crimson",
               "light_red",
               "light_flame",
               "light_orange",
               "light_amber",
               "light_yellow",
               "light_lime",
               "light_chartreuse",
               "light_green",
               "light_sea",
               "light_turquoise",
               "light_cyan",
               "light_sky",
               "light_azure",
               "light_blue",
               "light_han",
               "light_violet",
               "light_purple",
               "light_fuchsia",
               "light_magenta",
               "light_pink",
               "light_crimson",
               "lighter_red",
               "lighter_flame",
               "lighter_orange",
               "lighter_amber",
               "lighter_yellow",
               "lighter_lime",
               "lighter_chartreuse",
               "lighter_green",
               "lighter_sea",
               "lighter_turquoise",
               "lighter_cyan",
               "lighter_sky",
               "lighter_azure",
               "lighter_blue",
               "lighter_han",
               "lighter_violet",
               "lighter_purple",
               "lighter_fuchsia",
               "lighter_magenta",
               "lighter_pink",
               "lighter_crimson",
               "lightest_red",
               "lightest_flame",
               "lightest_orange",
               "lightest_amber",
               "lightest_yellow",
               "lightest_lime",
               "lightest_chartreuse",
               "lightest_green",
               "lightest_sea",
               "lightest_turquoise",
               "lightest_cyan",
               "lightest_sky",
               "lightest_azure",
               "lightest_blue",
               "lightest_han",
               "lightest_violet",
               "lightest_purple",
               "lightest_fuchsia",
               "lightest_magenta",
               "lightest_pink",
               "lightest_crimson",
               "desaturated_red",
               "desaturated_flame",
               "desaturated_orange",
               "desaturated_amber",
               "desaturated_yellow",
               "desaturated_lime",
               "desaturated_chartreuse",
               "desaturated_green",
               "desaturated_sea",
               "desaturated_turquoise",
               "desaturated_cyan",
               "desaturated_sky",
               "desaturated_azure",
               "desaturated_blue",
               "desaturated_han",
               "desaturated_violet",
               "desaturated_purple",
               "desaturated_fuchsia",
               "desaturated_magenta",
               "desaturated_pink",
               "desaturated_crimson",
               "brass",
               "copper",
               "gold",
               "silver",
               "celadon",
               "peach"]
