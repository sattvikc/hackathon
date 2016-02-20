from .base import Task
import time


class DummyTask(Task):
    ID = 'builtin.dummy'

    def run(self):
        print('I am a dummy task. I do nothing!')
        time.sleep(2)
        print('Wasted 2 seconds.')
