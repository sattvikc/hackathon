from ....base import Task
from ..utils import create_ssh_client


class RemoteFileCreateTask(Task):
    ID = 'builtin.remote.file.create'
    NAME = 'RemoteFileCreate'
    DESCRIPTION = 'Create file on a remote machine.'
    INPUTS = [
        ('username', 'Login username'),
        ('password', 'Login password'),
        ('host', 'Remote SSH Hostname'),
        ('port', 'Remote SSH Port, default=22'),
        ('directory', 'Remote machine directory for the file'),
        ('filename', 'File name of the file to be created'),
        ('contents', 'File contents'),
    ]
    OUTPUTS = []

    def run(self):
        directory = self.get_input('directory')
        filename = self.get_input('filename')
        contents = self.get_input('contents')

        client = create_ssh_client(self.inputs)

        stdin, stdout, stderr = client.exec_command("cd %s; cat > %s" % (directory, filename))
        stdin.write(contents)
        stdin.flush()
        stdin.close()
        client.close()
