import copy


class Monitor(object):
    def __init__(self):
        self.data = {}

    def update(self, key, value):
        key = key.split('.')
        if len(key) == 1:
            self.data.update({key: value})
        else:
            d = self.data
            for k in key[:-1]:
                d = d.setdefault(k, {})
            d.update({key[-1]: value})

    def get(self):
        return copy.deepcopy(self.data)
