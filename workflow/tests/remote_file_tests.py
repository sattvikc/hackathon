from workflow.task.builtin.remote.file.create import RemoteFileCreateTask
from workflow.task.builtin.remote.file.transfer import RemoteFileUploadTask, RemoteFileDownloadTask

VM_SETTINGS = {
    'host': '192.168.99.100',
    'port': 2020,
    'directory': '/root',
    'filename': 'test.txt',
    'contents': 'Hello World!\n',
    'username': 'root',
    'password': 'root',
}


def test_remote_file_create():
    task = RemoteFileCreateTask()
    task.inputs.update(VM_SETTINGS)
    task.inputs.update({
        'directory': '/home/sattvik',
        'filename': 'test.txt',
        'contents': 'Hello World!\n',
    })

    task.run()


def test_remote_file_upload():
    task = RemoteFileUploadTask()
    task.inputs.update(VM_SETTINGS)
    task.inputs.update({
        'localPath': '/Users/sattvik/test.txt',
        'remotePath': '/root/test2.txt'
    })
    task.run()


def test_remote_file_download():
    task = RemoteFileDownloadTask()
    task.inputs.update(VM_SETTINGS)
    task.inputs.update({
        'localPath': '/Users/sattvik/test3.txt',
        'remotePath': '/root/test2.txt'
    })
    task.run()
