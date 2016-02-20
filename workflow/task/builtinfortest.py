from .base import Task
import random


class DummyTask(Task):
    ID = 'builtin.dummy'

    def run(self):
        print('I am a dummy task. I do nothing!')


class RandomFailTask(Task):
    ID = 'builtin.random'

    def run(self):
        if random.random() < 0.5:
            raise Exception('Random Error!')


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
