from .value import Value


class TaskInstance(object):
    def __init__(self):
        self.name = None
        self.task = None
        self.dependencies = []
        self.exception = None
        self.inputs = {}
        self.outputs = {}
        self.state = 'CREATED'

    def set_input(self, key, value):
        self.inputs[key] = value

    def get_input(self, key):
        return self.inputs.get(key, None)

    def set_output(self, key, value):
        self.outputs[key] = value

    def get_output(self, key):
        return self.outputs.get(key, None)

    def set_name(self, name):
        self.name = name

    def set_task(self, task):
        self.task = task

    def add_dependency(self, task):
        self.dependencies.append(task)

    def resolve_dict(self, value):
        result = {}
        for key, val in value.items():
            if isinstance(val, dict):
                result.update({key: self.resolve_dict(val)})
            elif isinstance(val, Value):
                val = val.get_value()
                result.update({key: val})
            else:
                result.update({key: val})
        return result

    def resolve_inputs(self):
        self.inputs = self.resolve_dict(self.inputs)
        self.task.inputs.update(self.inputs)

    def run(self):
        try:
            self.state = 'RUNNING'
            self.task.run()
            for k in self.outputs:
                self.outputs[k] = self.task.outputs[k]
            self.state = 'SUCCESSFUL'
        except Exception as e:
            self.exception = str(e)
            self.state = 'FAILURE'

    def is_ready(self):
        ready = True
        for task in self.dependencies:
            if not (task.is_complete() and task.is_successful()):
                ready = False
        return ready

    def is_complete(self):
        return self.state == 'SUCCESSFUL' or self.state == 'FAIULRE'

    def is_successful(self):
        return self.state == 'SUCCESSFUL'

    def is_failure(self):
        return self.state == 'FAILURE'

    def __str__(self):
        return 'TaskInstance<%s>' % self.name

    def __repr__(self):
        return 'TaskInstance<%s>' % self.name
