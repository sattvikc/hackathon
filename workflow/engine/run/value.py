class Value(object):
    pass


class PropertyValue(Value):
    def __init__(self, key):
        self.key = key


class TaskOutputValue(Value):
    def __init__(self, task, output):
        self.task = task
        self.output = output
