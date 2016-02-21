from django.shortcuts import render, redirect
from django.http import HttpResponse

from workflow.client import WorkflowClient

from .models import Workflow, WorkflowRun


ENDPOINT = 'http://localhost:12120/api/1.0'
CLIENT = WorkflowClient(ENDPOINT)


def new(request):
    name = request.POST.get('name')
    desc = request.POST.get('description', '')
    defn = request.POST.get('workflow')
    wf = Workflow()
    wf.name = name
    wf.description = desc
    wf.definition = defn
    wf.save()


def save(request, pk):
    name = request.POST.get('name')
    desc = request.POST.get('description', '')
    defn = request.POST.get('workflow')
    wf = Workflow.objects.get(pk=pk)
    wf.name = name
    wf.description = desc
    wf.definition = defn
    wf.save()


def submit(request, pk):
    wf = Workflow.objects.get(pk=pk)
    wf_def = wf.definition
    properties = request.POST.get('properties', {})

    result = CLIENT.submit(wf_def, properties)
    run_id = result.get('runId')

    wf_run = WorkflowRun()
    wf_run.workflow = wf
    wf_run.run_id = run_id
    wf_run.properties = properties
    wf_run.save()
    return redirect('workflow:monitor', pk=wf_run.pk)


def monitor(request, pk):
    wf_run = WorkflowRun.objects.get(pk=pk)
    if not wf_run.status['workflow']['state'] == 'COMPLETED':
        status = CLIENT.status(wf_run.run_id)
        wf_run.status = status
        wf_run.save()
    else:
        status = wf_run.status
    return render(request, 'workflows/monitor.html', {
            'workflow': wf_run.workflow,
            'run_id': wf_run.run_id,
            'status': status,
        })
