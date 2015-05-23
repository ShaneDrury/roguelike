from core.mixin import PassthroughMixin


class Keys(PassthroughMixin):
    def __init__(self):
        super(Keys, self).__init__()
        self.prefix = "KEY_"
        self._cached_key = None
        self.checking = True

        self.keys_dict = {
            'UP': ['k', 'KEY_UP', 'KEY_KP8'],
            'DOWN': ['j', 'KEY_DOWN', 'KEY_KP2'],
            'LEFT': ['h', 'KEY_LEFT', 'KEY_KP4'],
            'RIGHT': ['l', 'KEY_RIGHT', 'KEY_KP6'],
            'UP_LEFT': ['y', 'KEY_KP7'],
            'UP_RIGHT': ['u', 'KEY_KP9'],
            'DOWN_LEFT': ['b', 'KEY_KP1'],
            'DOWN_RIGHT': ['n', 'KEY_KP3'],
            'QUIT': ['KEY_ESCAPE']
        }

    def wait_for_keypress(self, flush):
        return self.t.console_wait_for_keypress(flush)

    def check_for_keypress(self, flags=None):
        if self.checking:
            self._cached_key = self.t.console_check_for_keypress(flags or
                                                                 self.KEY_RELEASED)
            self.checking = False
        return self._translate_raw_key(self._cached_key)

    def _translate_raw_key(self, key):
        processed_key = None
        if key.vk == self.KEY_CHAR:
            for k, v in self.keys_dict.iteritems():
                if chr(key.c) in v:
                    processed_key = k
                    break
        else:
            for k, v in self.keys_dict.iteritems():
                for button in v:
                    if button.startswith('KEY_'):
                        if getattr(self, button) == key.vk:
                            processed_key = k
                            break
        return processed_key

    def flush(self):
        self.checking = True

    def is_key_pressed(self, key):
        return self.t.console_is_key_pressed(key)

    def set_keyboard_repeat(self, initial_delay, interval):
        self.t.console_set_keyboard_repeat(initial_delay, interval)

    def disable_keyboard_repeat(self):
        self.t.console_disable_keyboard_repeat()
