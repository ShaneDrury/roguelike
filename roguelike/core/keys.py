from core.mixin import PassthroughMixin


class Keys(PassthroughMixin):
    def __init__(self, keys_dict):
        super(Keys, self).__init__()
        self.prefix = "KEY_"
        self._cached_key = None
        self.checking = True
        self.keys_dict = keys_dict

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
