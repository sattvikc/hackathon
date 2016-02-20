import logging
from threading import Thread
import uuid

from .compiler import Compiler
from .run.context import Context


class WorkflowRunner(Thread):
    def __init__(self, server, workflow, properties={}):
        self.server = server
        run_id = str(uuid.uuid4())
        super(WorkflowRunner, self).__init__(name='Runner[%s]' % str(uuid.uuid4()))
        self.logger = logging.getLogger('engine.WorkflowRunner')
        self.workflow = workflow
        self.properties = properties
        self.workflow_name = workflow['workflow']['name']
        self.run_id = run_id
        self.context = Context()
        self.instance = None
        self.set_default_context_values()

    def set_default_context_values(self):
        self.context.set('run.id', self.run_id)

    def prepare(self):
        self.instance = Compiler.compile(self.workflow)
        self.instance.set_context(self.context)
        self.instance.resolve()

    def validate(self):
        pass

    def run(self):
        self.logger.info('Starting workflow run.')
        self.instance.run(scheduler=self.server.get_scheduler())
        self.logger.info('Completed workflow run.')

    def __str__(self):
        return 'WorkflowRunner<%s,%s>' % (self.workflow_name, self.run_id)

    def __repr__(self):
        return 'WorkflowRunner<%s,%s>' % (self.workflow_name, self.run_id)
