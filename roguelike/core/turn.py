from collections import namedtuple

Action = namedtuple('Action', ['tick', 'callback', 'player'])


class Turn(object):
    def __init__(self, consts):
        self.consts = consts
        self.base_multiplier = consts['COST_MULTIPLIER']
        self.actions = []
        self.blocking = False

    def add_action(self, name, callback, player, multiplier=1):
        tick = self.base_multiplier * self.consts[name]['cost'] * multiplier
        self.actions.append(Action(tick, callback, player))

    def take_player_action(self):
        """
        If there are any player actions, tick forward
        """
        for action in self.actions:
            if action.player:
                self.tick()
                self.take_actions()
                self.blocking = True
                break
        else:
            self.blocking = False

    @property
    def available_actions(self):
        return [action for action in self.actions if action.tick == 0]

    def tick(self):
        todo = []
        for action in self.actions:
            action = Action(action.tick - 1, action.callback, action.player)
            todo.append(action)
        self.actions = todo

    def take_actions(self):
        for action in self.available_actions:
            action.callback()
        self.actions = [a for a in self.actions if a.tick > 0]
