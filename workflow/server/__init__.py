from .scheduler import Scheduler
from ..engine.compiler import Compiler
from ..engine.runner import InlineRunner
from ..task.base import Task

from threading import Thread
from queue import Queue

import logging
import uuid


class WorkflowServer(Thread):
    def __init__(self):
        super(WorkflowServer, self).__init__(name='WorkflowServer')
        self.logger = logging.getLogger(__name__)
        self.cmd_queue = Queue()
        self.instances = []
        self.instances_dict = {}
        self.scheduler = Scheduler()

    def get_task_types(self):
        return sorted(list(Task.get_keys()))

    def get_task_meta(self, key):
        cls = Task.get_class(key)
        if cls is None:
            return None
        return {
            'key': cls.ID,
            'name': cls.NAME,
            'description': cls.DESCRIPTION,
            'inputs': cls.INPUTS,
            'outputs': cls.OUTPUTS,
        }

    def submit(self, workflow, properties={}):
        run_id = str(uuid.uuid4())
        self.cmd_queue.put(('submit', (workflow, properties, run_id)))
        return run_id

    def submit_exec(self, workflow, properties, run_id):
        workflow_instance = Compiler.compile(definition=workflow, properties=properties)
        run_instance = InlineRunner(server=self, workflow_instance=workflow_instance, run_id=run_id)
        run_instance.prepare()
        run_instance.validate()
        self.instances.append(run_instance)
        self.instances_dict.update({run_id: run_instance})
        run_instance.run()

    def get_status(self, run_id):
        inst = self.instances_dict.get(run_id)
        return inst.get_status()

    def get_scheduler(self):
        return self.scheduler

    def finish(self):
        self.cmd_queue.put(('finish', None))

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
                workflow, properties, run_id = data
                self.logger.info('[submit] operation, workflow [%s]' % workflow['workflow']['name'])
                self.submit_exec(workflow, properties, run_id)

        self.logger.info('Waiting for instances to complete...')

        self.logger.info('Server execution completed.')
