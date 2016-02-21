from .monitor import Monitor
from .run.context import Context

from datetime import datetime

import logging
import uuid


class RunnerBase(object):
    def __init__(self, server, workflow_instance, run_id=str(uuid.uuid4())):
        super(RunnerBase, self).__init__()
        self.server = server
        self.context = Context()

        self.instance = None
        self.logger = logging.getLogger('engine.%s' % self.__class__.__name__)
        self.monitor = Monitor()
        self.run_id = run_id
        self.workflow_instance = workflow_instance
        self.workflow_name = workflow_instance.name

        self.set_default_context_values()

    def get_run_id(self):
        return self.run_id

    def set_default_context_values(self):
        self.context.set('run.id', self.run_id)

    def prepare(self):
        self.monitor.update('workflow.state', 'PREPARING')
        self.workflow_instance.set_context(self.context)
        self.workflow_instance.prepare_inputs(self)
        self.monitor.update('workflow.state', 'PREPARED')
        for task in self.workflow_instance.tasks:
            self.monitor.update('tasks.' + task.name + '.state', 'NOTREADY')

    def validate(self):
        pass


class InlineRunner(RunnerBase):
    def run(self):
        self.completed = False
        self.logger.info('Starting workflow run.')
        self.monitor.update('workflow.state', 'RUNNING')
        self.monitor.update('workflow.execution.start_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
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
                    self.monitor.update('tasks.' + task.name + '.state', 'READY')

            # Execute the ready queue
            for task in ready_queue:
                task.resolve_inputs()
                for i in range(3):
                    self.logger.info('Task [%s] execution started (Attempt %d).' % (task.name, i+1))
                    self.monitor.update('tasks.' + task.name + '.state', 'RUNNING')
                    self.monitor.update('tasks.' + task.name + '.input.values', task.inputs)
                    task.run()
                    if task.is_successful():
                        self.logger.info('Task [%s] execution completed successfully.' % task.name)
                        self.monitor.update('tasks.' + task.name + '.state', 'SUCCESSFUL')
                        self.monitor.update('tasks.' + task.name + '.output.values', task.outputs)
                        break
                    else:
                        self.logger.info('Task [%s] execution failed.' % task.name)
                        self.monitor.update('tasks.' + task.name + '.state', 'FAILURE')

            if len(ready_queue) == 0:
                # Deadlock or no more executable tasks
                self.logger.warn('No tasks are ready for execution!')
                for task in task_queue:
                    task.status = 'SKIPPED'
                    self.logger.warn('Task [%s] execution was skipped.' % task.name)
                    self.monitor.update('tasks.' + task.name + '.state', 'SKIPPED')
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
        self.monitor.update('workflow.state', 'COMPLETED')
        self.monitor.update('workflow.execution.end_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        self.completed = True

    def __str__(self):
        return 'InlineRunner<%s,%s>' % (self.workflow_name, self.run_id)

    def __repr__(self):
        return 'InlineRunner<%s,%s>' % (self.workflow_name, self.run_id)

    def get_status(self):
        return self.monitor.get()

    def is_complete(self):
        return self.completed
