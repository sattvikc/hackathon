from bottle import Bottle, run, response

from workflow.server.endpoints.api_v_1_0 import api_v10_app
from workflow.server import WorkflowServer

import workflow.task.builtin.registry

import logging


if __name__ == '__main__':
    wf_server = WorkflowServer()
    wf_server.start()
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)-8s %(asctime)s    %(name)-32s %(message)s'
    )
    app = Bottle()

    @app.route('/')
    def home():
        response.content_type = 'text/plain'
        return "Bang Hack Workflow server!"

    app.mount('/api/1.0/', api_v10_app(wf_server))
    run(app, host='localhost', port=12120)
