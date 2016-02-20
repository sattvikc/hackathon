from .value import PropertyValue, TaskOutputValue


class WorkflowInstance(object):
    def __init__(self):
        self.name = ''
        self.tasks = []
        self.tasks_dict = {}
        self.dependencies = {}
        self.context = None

    def set_name(self, name):
        self.name = name

    def add_task(self, task):
        self.tasks.append(task)
        self.tasks_dict[task.name] = task

    def get_task(self, task_name):
        return self.tasks_dict.get(task_name)

    def set_context(self, context):
        self.context = context

    def compute_dependencies(self):
        for task in self.tasks:
            for dep in task.task.dependencies:
                task.add_dependency(self.tasks_dict.get(dep))

    def prepare_dict(self, value, properties={}):
        if 'src' in value:
            src = value.get('src')
            if src == 'properties':
                key = value.get('key')
                return PropertyValue(key, properties)
            elif src == 'taskout':
                task, output = value.get('key').split('.')
                return TaskOutputValue(self.tasks_dict.get(task), output)
        else:
            result = {}
            for k, v in value.items():
                if isinstance(v, dict):
                    v = self.prepare_dict(v)
                result.update({k:v})
            return result

    def prepare_inputs(self, properties={}):
        for task in self.tasks:
            for key, value in task.inputs.items():
                if isinstance(value, dict):
                    value = self.prepare_dict(value, properties)
                task.set_input(key, value)

    def __str__(self):
        return 'WorkflowInstance<%s>' % self.name

    def __repr__(self):
        return 'WorkflowInstance<%s>' % self.name
