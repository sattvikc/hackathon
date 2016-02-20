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
