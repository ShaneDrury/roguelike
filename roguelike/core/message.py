import textwrap


class Message(object):
    def __init__(self, w, h):
        self.messages = []
        self.w = w
        self.h = h

    def add(self, msg, colour):
        new_msg_lines = textwrap.wrap(msg, self.w)
        for line in new_msg_lines:
            if len(self.messages) == self.h:
                del self.messages[0]
            self.messages.append((line, colour))
