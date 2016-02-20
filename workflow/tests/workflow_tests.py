import workflow.task.builtin.registry
from workflow.engine.compiler import Compiler
from workflow.engine.runner import InlineRunner

import yaml

WORKFLOW1 = yaml.load("""workflow:
  name: "SampleWorkflow"
  tasks:
    - name: task01
      def: "builtin.dummy"
      dependencies:
        - task02
    - name: task02
      def: "builtin.dummy"
      dependencies:
        - task03
    - name: task03
      def: "builtin.dummy"
""")


def run_workflow(wf_def, properties={}):
    workflow_instance = Compiler.compile(definition=wf_def, properties=properties)
    instance = InlineRunner(server=None, workflow_instance=workflow_instance)
    instance.prepare()
    instance.validate()
    instance.start()
    instance.join()


def test_basic_workflow():
    run_workflow(WORKFLOW1)
