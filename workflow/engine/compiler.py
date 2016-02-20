from .run.task import TaskInstance
from .run.workflow import WorkflowInstance
from ..task.base import Task


class Compiler(object):
    @classmethod
    def compile(cls, workflow):
        wi = WorkflowInstance()
        workflow = workflow['workflow']
        wi.set_name(workflow.get('name'))

        for task_def in workflow.get('tasks'):
            name = task_def.get('name')
            ti = TaskInstance()
            ti.set_name(name)
            task = Task.create_from_def(task_def)
            ti.set_task(task)

            ti.inputs.update(task_def.get('inputs', {}))
            for output in task_def.get('outputs', []):
                ti.outputs.update({output: None})
            wi.add_task(ti)

        wi.compute_dependencies()
        return wi
