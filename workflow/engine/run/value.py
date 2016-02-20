class Value(object):
    def get_value(self):
        return None


class PropertyValue(Value):
    def __init__(self, key, properties={}):
        self.key = key
        self.properties = properties

    def get_value(self):
        return self.properties.get(self.key, None)


class TaskOutputValue(Value):
    def __init__(self, task, output):
        self.task = task
        self.output = output

    def get_value(self):
        return self.task.get_output(self.output)
