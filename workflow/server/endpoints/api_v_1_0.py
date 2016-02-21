from bottle import Bottle, request, response

import json


def api_v10_app(wf_server):
    app = Bottle()

    @app.route('/')
    def root():
        response.content_type = 'application/json'
        return json.dumps({
            'name': 'Workflow server',
            'version': '1.0'
        }, sort_keys=True)

    @app.route('/workflow/submit', method='PUT')
    def workflow_submit():
        workflow = json.loads(request.forms.get('workflow'))
        properties = json.loads(request.forms.get('properties', '{}'))

        run_id = wf_server.submit(workflow, properties)
        response.content_type = 'application/json'
        return json.dumps({
            'runId': run_id,
        }, sort_keys=True)

    @app.route('/workflow/status/<run_id>')
    def workflow_status(run_id):
        response.content_type = 'application/json'
        return json.dumps(wf_server.get_status(run_id), sort_keys=True)

    @app.route('/server/task-types')
    def server_task_types():
        response.content_type = 'application/json'
        return json.dumps(wf_server.get_task_types(), sort_keys=True)

    @app.route('/server/task-type-meta/<key>')
    def server_task_type_meta(key):
        response.content_type = 'application/json'
        return json.dumps(wf_server.get_task_meta(key), sort_keys=True)

    return app
