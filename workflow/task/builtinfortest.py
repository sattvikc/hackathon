from .base import Task
import time


class DummyTask(Task):
    ID = 'builtin.dummy'

    def run(self):
        print('I am a dummy task. I do nothing!')
        print('Wasted 2 seconds.')
        self.set_output('dummy_out', 'Dummy output!')
        self.set_output('a', 'AAA')
        self.set_output('b', 'BBB')
        self.set_output('c', 'CCC')


class AddTask(Task):
    ID = 'builtin.add'

    def run(self):
        a = self.get_input('a')
        b = self.get_input('b')
        c = a + b
        self.set_output('c', c)


class MultiplyTask(Task):
    ID = 'builtin.multiply'

    def run(self):
        a = self.get_input('a')
        b = self.get_input('b')
        c = a * b
        self.set_output('c', c)


class PrintTask(Task):
    ID = 'builtin.print'

    def run(self):
        for k, v in self.inputs.items():
            print(k, '=', v)
