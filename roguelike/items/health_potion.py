from functools import partial
from core.item import Item, log


class HealthPotion(Item):
    def use(self, player, turn):
        log.debug("Using {}".format(self))
        turn.add_action('ITEM', partial(self._use, player), player=True)

    def _use(self, player):
        player.hp += 10
