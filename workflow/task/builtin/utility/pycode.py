from ...base import Task


class PythonCodeTask(Task):
    ID = 'builtin.utility.pycode'
    NAME = 'PythonCode'
    DESCRIPTION = 'Executes a python code.'
    INPUTS = [
        ('code', 'Python code'),
    ]
    OUTPUTS = []

    def run(self):
        code = self.inputs.pop('code')
        l = {}
        g = {}
        g.update(self.inputs)
        exec(code, g, l)
        self.outputs.update(l)
