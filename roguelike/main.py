from core.colour import Colour
from core.font import Font
from core.keys import Keys
from game import Game
import settings

def main():
    keys = Keys()
    font = Font()
    colour = Colour()
    game = Game(keys, font, colour, settings)
    game.main()

if __name__ == '__main__':
    main()
