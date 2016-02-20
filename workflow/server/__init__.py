import logging
from threading import Thread
from queue import Queue

from ..engine.runner import InlineRunner
from .scheduler import Scheduler
from ..engine.compiler import Compiler


class WorkflowServer(Thread):
    def __init__(self):
        super(WorkflowServer, self).__init__(name='WorkflowServer')
        self.logger = logging.getLogger('workflow.Server')
        self.cmd_queue = Queue()
        self.instances = []
        self.scheduler = Scheduler()

    def submit(self, workflow, properties={}):
        self.cmd_queue.put(('submit', (workflow, properties)))

    def submit_exec(self, workflow, properties):
        workflow_instance = Compiler.compile(definition=workflow, properties=properties)
        instance = InlineRunner(server=self, workflow_instance=workflow_instance)
        instance.prepare()
        instance.validate()
        instance.start()
        self.instances.append(instance)

    def get_scheduler(self):
        return self.scheduler

    def finish(self):
        self.cmd_queue.put(('finish', None))
        self.join()

    def init(self):
        pass

    def run(self):
        self.init()
        while True:
            cmd, data = self.cmd_queue.get()
            if cmd == 'finish':
                self.logger.info('[finish] command received.')
                break
            elif cmd == 'submit':
                workflow, properties = data
                self.logger.info('[submit] operation, workflow [%s]' % workflow['workflow']['name'])
                self.submit_exec(workflow, properties)

        self.logger.info('Waiting for instances to complete...')
        for instance in self.instances:
            instance.join()

        self.logger.info('Server execution completed.')
