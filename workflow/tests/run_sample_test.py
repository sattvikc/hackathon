import logging
import os
import yaml
import json

from workflow.server import Server
import workflow.task.builtin


logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)-8s %(asctime)s    %(name)-48s %(message)s'
)

f = os.path.join(os.path.dirname(__file__), 'sample_workflow.yaml')
workflow_def = yaml.load(open(f))

properties = {
    "hello.world": "Hello world!",
}


ws = Server()
ws.start()
ws.submit(workflow_def, properties)
ws.exit()
