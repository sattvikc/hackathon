import logging
from threading import Thread
from queue import Queue

from ..engine.runner import InlineRunner
from .scheduler import Scheduler


class Server(Thread):
    def __init__(self):
        super(Server, self).__init__(name='Server')
        self.logger = logging.getLogger('workflow.Server')
        self.cmd_queue = Queue()
        self.instances = []
        self.scheduler = Scheduler()

    def submit(self, workflow, properties={}):
        self.cmd_queue.put(('submit', (workflow, properties)))

    def submit_exec(self, workflow, properties):
        instance = InlineRunner(server=self, workflow=workflow, properties=properties)
        instance.prepare()
        instance.validate()
        instance.start()
        self.instances.append(instance)

    def get_scheduler(self):
        return self.scheduler

    def exit(self):
        self.cmd_queue.put(('exit', None))

    def run(self):
        while True:
            cmd, data = self.cmd_queue.get()
            if cmd == 'exit':
                self.logger.info('[exit] command received.')
                break
            elif cmd == 'submit':
                workflow, properties = data
                self.logger.info('[submit] operation, workflow [%s]' % workflow['workflow']['name'])
                self.submit_exec(workflow, properties)

        self.logger.info('Waiting for instances to complete...')
        for instance in self.instances:
            instance.join()

        self.logger.info('Server execution completed.')
