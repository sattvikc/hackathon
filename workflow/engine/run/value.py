class Value(object):
    def get_value(self):
        return None


class PropertyValue(Value):
    def __init__(self, key):
        self.key = key


class TaskOutputValue(Value):
    def __init__(self, task, output):
        self.task = task
        self.output = output

    def get_value(self):
        return self.task.get_output(self.output)
