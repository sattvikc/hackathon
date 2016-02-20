from workflow.task.builtin.remote.exec.command import RemoteCommandExecTask

VM_SETTINGS = {
    'host': '192.168.99.100',
    'port': 2020,
    'directory': '/root',
    'filename': 'test.txt',
    'contents': 'Hello World!\n',
    'username': 'root',
    'password': 'root',
}


def test_remote_exec_command():
    task = RemoteCommandExecTask()
    task.inputs.update(VM_SETTINGS)
    task.inputs.update({
        'command': 'whoami',
    })

    task.run()
    assert('root' in task.get_output('stdout'))
