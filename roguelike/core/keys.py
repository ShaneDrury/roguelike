from core.mixin import PassthroughMixin


class Keys(PassthroughMixin):
    def __init__(self):
        super(Keys, self).__init__()
        self.prefix = "KEY_"
        self.key = None
        self.checking = True

    def wait_for_keypress(self, flush):
        return self.t.console_wait_for_keypress(flush)

    def check_for_keypress(self, flags=None):
        if self.checking:
            self.key = self.t.console_check_for_keypress(flags or self.KEY_RELEASED)
            self.checking = False
        return self.key

    def flush(self):
        self.checking = True

    def is_key_pressed(self, key):
        return self.t.console_is_key_pressed(key)

    def set_keyboard_repeat(self, initial_delay, interval):
        self.t.console_set_keyboard_repeat(initial_delay, interval)

    def disable_keyboard_repeat(self):
        self.t.console_disable_keyboard_repeat()
