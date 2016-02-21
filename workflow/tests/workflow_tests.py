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

WORKFLOW2 = yaml.load("""workflow:
  name: "SampleWorkflow2"
  tasks:
    - name: task01
      def: "builtin.utility.pycode"
      inputs:
        code: "x = 100"
      outputs:
        - x
    - name: task02
      def: "builtin.utility.pycode"
      inputs:
        code: "y = x * 2"
        x:
          src: taskout
          key: "task01.x"
      outputs:
        - y
      dependencies:
        - task01
""")

WORKFLOW3 = yaml.load("""workflow:
  name: "SampleWorkflow3"
  tasks:
    - name: task01
      def: "builtin.utility.pycode"
      inputs:
        code: "x = val"
        val:
          src: properties
          key: "input.value"
      outputs:
        - x
    - name: task02
      def: "builtin.utility.pycode"
      inputs:
        code: "y = x * 2"
        x:
          src: taskout
          key: "task01.x"
      outputs:
        - y
      dependencies:
        - task01
""")


def run_workflow(wf_def, properties={}):
    workflow_instance = Compiler.compile(definition=wf_def, properties=properties)
    instance = InlineRunner(server=None, workflow_instance=workflow_instance)
    instance.prepare()
    instance.validate()
    instance.run()
    return workflow_instance


def test_basic_workflow():
    wi = run_workflow(WORKFLOW1)


def test_task_out_data():
    wi = run_workflow(WORKFLOW2)
    task02 = wi.get_task('task02')
    assert (task02.get_output('y') == 200)


def test_property_resolution():
    wi = run_workflow(WORKFLOW3, {'input.value': 100})
    task02 = wi.get_task('task02')
    assert (task02.get_output('y') == 200)
