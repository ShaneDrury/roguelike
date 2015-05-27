class Background(object):
    BKGND_NONE = 0
    BKGND_SET = 1
    BKGND_MULTIPLY = 2
    BKGND_LIGHTEN = 3
    BKGND_DARKEN = 4
    BKGND_SCREEN = 5
    BKGND_COLOR_DODGE = 6
    BKGND_COLOR_BURN = 7
    BKGND_ADD = 8
    BKGND_ADDA = 9
    BKGND_BURN = 10
    BKGND_OVERLAY = 11
    BKGND_ALPH = 12
    BKGND_DEFAULT = 13

    def bkgnd_alpha(self, a):
        return self.BKGND_ALPH | (int(a * 255) << 8)

    def bkgnd_addalpha(self, a):
        return self.BKGND_ADDA | (int(a * 255) << 8)
