import copy
import logging
import uuid

from threading import Thread

from .compiler import Compiler
from .run.context import Context


class RunnerBase(Thread):
    def __init__(self, server, workflow_instance):
        self.server = server
        run_id = str(uuid.uuid4())
        super(RunnerBase, self).__init__(name='Runner[%s]' % str(uuid.uuid4()))

        self.context = Context()
        self.instance = None
        self.logger = logging.getLogger('engine.%s' % self.__class__.__name__)
        self.run_id = run_id
        self.status = {}
        self.workflow_instance = workflow_instance
        self.workflow_name = workflow_instance.name

        self.set_default_context_values()

    def get_run_id(self):
        return self.run_id

    def set_default_context_values(self):
        self.context.set('run.id', self.run_id)

    def prepare(self):
        self.status.update({'state': 'PREPARING'})
        self.workflow_instance.set_context(self.context)
        self.workflow_instance.prepare_inputs(self)
        self.status.update({'state': 'PREPARED'})
        self.status.update({'tasks': {}})
        for task in self.workflow_instance.tasks:
            self.status['tasks'].setdefault(task.name, {}).update({'state': 'NOTREADY'})

    def validate(self):
        pass


class InlineRunner(RunnerBase):
    def run(self):
        self.logger.info('Starting workflow run.')
        self.status.update({'state': 'RUNNING'})
        task_queue = []
        ready_queue = []
        success_queue = []
        failure_queue = []
        skipped_queue = []

        for task in self.workflow_instance.tasks:
            task_queue.append(task)

        while len(task_queue) > 0:
            for task in task_queue:
                if task.is_ready():
                    task_queue.remove(task)
                    ready_queue.append(task)
                    self.status['tasks'].setdefault(task.name, {}).update({'state': 'READY'})

            # Execute the ready queue
            for task in ready_queue:
                task.resolve_inputs()
                for i in range(3):
                    self.logger.info('Task [%s] execution started (Attempt %d).' % (task.name, i+1))
                    self.status['tasks'].setdefault(task.name, {}).update({'state': 'RUNNING'})
                    task.run()
                    if task.is_successful():
                        self.logger.info('Task [%s] execution completed successfully.' % task.name)
                        self.status['tasks'].setdefault(task.name, {}).update({'state': 'SUCCESSFUL'})
                        break
                    else:
                        self.logger.info('Task [%s] execution failed.' % task.name)
                        self.status['tasks'].setdefault(task.name, {}).update({'state': 'FAILURE'})

            if len(ready_queue) == 0:
                # Deadlock or no more executable tasks
                self.logger.warn('No tasks are ready for execution!')
                for task in task_queue:
                    task.status = 'SKIPPED'
                    self.logger.warn('Task [%s] execution was skipped.' % task.name)
                    self.status['tasks'].setdefault(task.name, {}).update({'state': 'SKIPPED'})
                    skipped_queue.append(task)
                task_queue.clear()
                break

            for task in ready_queue:
                ready_queue.remove(task)
                if task.is_successful():
                    success_queue.append(task)
                elif task.is_failure():
                    failure_queue.append(task)

        if len(skipped_queue) == 0 and len(failure_queue) == 0:
            self.logger.info('All tasks executed successfully!')
        self.logger.info('Completed workflow run.')
        self.status.update({'state': 'COMPLETE'})

    def __str__(self):
        return 'InlineRunner<%s,%s>' % (self.workflow_name, self.run_id)

    def __repr__(self):
        return 'InlineRunner<%s,%s>' % (self.workflow_name, self.run_id)

    def get_status(self):
        return copy.deepcopy(self.status)
