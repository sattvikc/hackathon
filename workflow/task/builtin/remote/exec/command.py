from ....base import Task
from ..utils import create_ssh_client


class RemoteCommandExecTask(Task):
    ID = 'builtin.remote.exec.command'

    def run(self):
        command = self.get_input('command')

        client = create_ssh_client(self.inputs)

        stdin, stdout, stderr = client.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()
        stdout = stdout.read()
        stderr = stderr.read()
        self.set_output('stdout', stdout.decode('utf-8'))
        self.set_output('stderr', stderr.decode('utf-8'))
        self.set_output('exit_status', exit_status)
        client.close()
