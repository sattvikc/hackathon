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
