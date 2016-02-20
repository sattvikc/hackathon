from threading import Lock


class Context(object):
    def __init__(self):
        self.lock = Lock()
        self.data = {}

    def set(self, key, value):
        with self.lock:
            self.data[key] = value

    def get(self, key):
        with self.lock:
            return self.data.get(key, None)
