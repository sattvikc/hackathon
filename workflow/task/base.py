import logging

from workflow.utils.patterns.registry import Register


class Task(Register):
    REGISTER_BASE = True
    LOGGER = logging.getLogger('task.Registry')

    NAME = 'UnnamedTask'
    DESCRIPTION = 'Description not available.'
    INPUTS = []
    OUTPUTS = []

    def __init__(self):
        self.inputs = {}
        self.outputs = {}
        self.context = None

    def set_context(self, context):
        self.context = context

    def set_input(self, key, value):
        self.inputs[key] = value

    def get_input(self, key, default=None):
        return self.inputs.get(key, default)

    def set_output(self, key, value):
        self.outputs[key] = value

    def get_output(self, key):
        return self.outputs.get(key, None)

    def run(self):
        pass  # To be implemented in concrete class

    @classmethod
    def create_from_def(cls, task_def):
        task_class = cls.get_class(task_def.get('def'))
        if task_class is None:
            cls.LOGGER.error('Task type [%s] not found.' % task_def.get('def'))
            raise Exception('Task type not found.')

        task = task_class()
        task.dependencies = task_def.get('dependencies', [])
        return task
