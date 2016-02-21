from django.shortcuts import render, redirect
from django.http import HttpResponse

from workflow.client import WorkflowClient

from .models import Workflow, WorkflowRun
import json

ENDPOINT = 'http://localhost:12120/api/1.0'
CLIENT = WorkflowClient(ENDPOINT)


def wlist(request):
    wfs = Workflow.objects.all()
    return render(request, 'workflows/list.html', {
            'workflows': wfs,
        })


def new(request):
    wf = Workflow()
    wf.name = 'Untitled'
    wf.description = ''
    wf.definition = {'name': 'Untitled', 'tasks': []}
    wf.save()
    # TODO: Redirect to edit


def edit(request, pk):
    wf = Workflow.objects.get(pk=pk)
    return render(request, 'workflows/edit.html', {
            'workflow': wf,
        })


def save(request, pk):
    name = request.POST.get('name')
    desc = request.POST.get('description', '')
    defn = request.POST.get('workflow')
    wf = Workflow.objects.get(pk=pk)
    wf.name = name
    wf.description = desc
    wf.definition = json.loads(defn)
    wf.save()
    return redirect('workflow:edit', pk=wf.pk)


def execute(request, pk):
    wf = Workflow.objects.get(pk=pk)
    return render(request, 'workflows/execute.html', {
            'workflow': wf,
        })


def submit(request, pk):
    wf = Workflow.objects.get(pk=pk)
    wf_def = wf.definition

    # Pre process wf_def
    for task in wf_def['tasks']:
        inputs = task['inputs']
        task['inputs'] = {}
        for inp in inputs:
            task['inputs'][inp['name']] = inp
            inp.pop('name')

    wf_def = { 'workflow': wf_def }
    # Pre process complete

    properties = {}
    keys = request.POST.getlist('key')
    values = request.POST.getlist('value')

    for k, v in zip(keys, values):
        properties.update({k: v})

    result = CLIENT.workflow_submit(wf_def, properties)
    run_id = result.get('runId')

    wf_run = WorkflowRun()
    wf_run.workflow = wf
    wf_run.run_id = run_id
    wf_run.properties = properties
    wf_run.save()
    return redirect('workflow:monitor', pk=wf_run.pk)


def mlist(request):
    wfrs = WorkflowRun.objects.all()
    return render(request, 'workflows/run-list.html', {
            'workflow_runs': wfrs,
        })


def monitor(request, pk):
    wf_run = WorkflowRun.objects.get(pk=pk)
    if 'workflow' in wf_run.status and 'state' in wf_run.status['workflow'] and (
            wf_run.status['workflow']['state'] == 'COMPLETED'):
        status = wf_run.status
    else:
        status = CLIENT.workflow_status(wf_run.run_id)
        wf_run.status = status
        wf_run.save()
    return render(request, 'workflows/monitor.html', {
            'workflow': wf_run.workflow,
            'run_id': wf_run.run_id,
            'status': status,
        })
