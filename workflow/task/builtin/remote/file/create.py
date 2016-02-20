from ....base import Task
from ..utils import create_ssh_client


class RemoteFileCreateTask(Task):
    ID = 'builtin.remote.file.create'

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
