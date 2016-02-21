from django.db import models
from jsonfield import JSONField
import copy
import json


class Workflow(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    definition = JSONField()

    def __str__(self):
        return self.name

    def definition_json(self):
        temp = copy.deepcopy(self.definition)
        tasks = temp.get('tasks', [])
        for task in tasks:
            if 'ui' in task:
                del task['ui']
        return json.dumps(temp, sort_keys=True, indent=4)


class WorkflowRun(models.Model):
    workflow = models.ForeignKey(Workflow)
    run_id = models.CharField(max_length=50)
    properties = JSONField(default={})

    status = JSONField(blank=True)

    def __str__(self):
        return self.workflow.name + '.' + self.run_id

    def properties_json(self):
        return json.dumps(self.properties, sort_keys=True, indent=4)
