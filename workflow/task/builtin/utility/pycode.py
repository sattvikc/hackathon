from ...base import Task


class PythonCodeTask(Task):
    ID = 'builtin.utility.pycode'

    def run(self):
        code = self.inputs.pop('code')
        l = {}
        g = {}
        g.update(self.inputs)
        exec(code, g, l)
        self.outputs.update(l)
