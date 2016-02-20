import logging
from threading import Thread
import uuid

from .compiler import Compiler
from .run.context import Context


class RunnerBase(Thread):
    def __init__(self, server, workflow, properties={}):
        self.server = server
        run_id = str(uuid.uuid4())
        super(RunnerBase, self).__init__(name='Runner[%s]' % str(uuid.uuid4()))

        self.context = Context()
        self.instance = None
        self.logger = logging.getLogger('engine.WorkflowRunner')
        self.properties = properties
        self.run_id = run_id
        self.workflow = workflow
        self.workflow_name = workflow['workflow']['name']

        self.set_default_context_values()

    def set_default_context_values(self):
        self.context.set('run.id', self.run_id)

    def prepare(self):
        self.instance = Compiler.compile(self.workflow)
        self.instance.set_context(self.context)
        self.instance.prepare_inputs()

    def validate(self):
        pass


class InlineRunner(RunnerBase):
    def run(self):
        self.logger.info('Starting workflow run.')
        task_queue = []
        ready_queue = []
        success_queue = []
        failure_queue = []
        skipped_queue = []

        for task in self.instance.tasks:
            task_queue.append(task)

        while len(task_queue) > 0:
            for task in task_queue:
                if task.is_ready():
                    task_queue.remove(task)
                    ready_queue.append(task)

            # Execute the ready queue
            for task in ready_queue:
                task.resolve_inputs()
                task.run()

            if len(ready_queue) == 0:
                # Deadlock or no more executable tasks
                for task in task_queue:
                    task.status = 'SKIPPED'
                    skipped_queue.append(task)
                task_queue.clear()
                break

            for task in ready_queue:
                ready_queue.remove(task)
                if task.is_successful():
                    success_queue.append(task)
                elif task.is_failure():
                    failure_queue.append(task)

        self.logger.info('Completed workflow run.')

    def __str__(self):
        return 'InlineRunner<%s,%s>' % (self.workflow_name, self.run_id)

    def __repr__(self):
        return 'InlineRunner<%s,%s>' % (self.workflow_name, self.run_id)
