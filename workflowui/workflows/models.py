from django.db import models
from jsonfield import JSONField


class Workflow(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    definition = JSONField()

    def __str__(self):
        return self.name


class WorkflowRun(models.Model):
    workflow = models.ForeignKey(Workflow)
    run_id = models.CharField(max_length=50)
    properties = JSONField(default={})

    status = JSONField(blank=True)

    def __str__(self):
        return self.workflow.name + '.' + self.run_id
