from django.contrib import admin

from .models import *


@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    pass


@admin.register(WorkflowRun)
class WorkflowRunAdmin(admin.ModelAdmin):
    pass
