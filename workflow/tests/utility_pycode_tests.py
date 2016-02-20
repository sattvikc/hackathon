from workflow.task.builtin.utility.pycode import PythonCodeTask


def test_pycode():
    task = PythonCodeTask()
    task.inputs.update({
        'code': 'print("Hello World!")\ny = x + 100\n',
        'x': 10
    })
    task.run()
    assert (110 == task.get_output('y'))
