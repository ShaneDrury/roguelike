from core.font import Font
from core.keys import Keys
from game import Game
import settings


def main():
    keys = Keys()
    font = Font()
    game = Game(keys, font, settings)
    game.main()

if __name__ == '__main__':
    main()
