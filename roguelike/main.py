import yaml

from core.colour import Colour
from core.font import Font
from core.graphics import Graphics
from core.keys import Keys
from game import Game
from player import Player
import settings

def main():
    with open(settings.VARS_FILE, 'r') as f:
        consts = yaml.load(f)
    graphics = Graphics()
    keys = Keys()
    player = Player(consts)
    font = Font()
    colour = Colour()
    game = Game(graphics, keys, player, font, colour, settings)
    game.main()

if __name__ == '__main__':
    main()
