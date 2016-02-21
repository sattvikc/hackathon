import json
import requests
import yaml


class DictObj(object):
    def __init__(self, obj={}):
        for k, v in obj.items():
            if isinstance(v, dict):
                setattr(self, k, DictObj(v))
            else:
                setattr(self, k, v)


class WorkflowClient(object):
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def workflow_submit(self, workflow, properties={}):
        workflow = json.dumps(workflow)
        properties = json.dumps(properties)

        url = self.endpoint + '/workflow/submit'
        result = requests.put(url, data={
            'workflow': workflow,
            'properties': properties,
        })
        return json.loads(result.content.decode('utf-8'))

    def workflow_status(self, run_id):
        url = self.endpoint + '/workflow/status/' + run_id
        result = requests.get(url)
        return json.loads(result.content.decode('utf-8'))

    def server_task_types(self):
        url = self.endpoint + '/server/task-types'
        result = requests.get(url)
        return json.loads(result.content.decode('utf-8'))

    def server_task_type_meta(self, key):
        url = self.endpoint + '/server/task-type-meta/' + key
        result = requests.get(url)
        return json.loads(result.content.decode('utf-8'))
