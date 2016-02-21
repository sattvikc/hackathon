from ....base import Task
from ..utils import create_ssh_client

import os
import uuid


class RemoteScriptExecTask(Task):
    ID = 'builtin.remote.exec.command'
    NAME = 'RemoteScriptExec'
    DESCRIPTION = 'Execute a script on remote machine.'
    INPUTS = [
        ('username', 'Login username'),
        ('password', 'Login password'),
        ('host', 'Remote SSH Hostname'),
        ('port', 'Remote SSH Port, default=22'),
        ('script', 'Script to be executed'),
        ('workDir', 'Directory where the script would be created.'),
    ]
    OUTPUTS = [
        ('stdout', 'Output stream'),
        ('stderr', 'Error stream'),
        ('exit_status', 'Exit status'),
    ]

    def run(self):
        script = self.get_input('script')
        work_dir = self.get_input('workDir', '/tmp')

        client = create_ssh_client(self.inputs)
        fpath = work_dir
        fname = str(uuid.uuid4())

        # Create and copy the script
        fd = open(fname, 'w')
        fd.write(script)
        fd.close()
        ftp = client.open_sftp()
        ftp.put(fname, os.path.join(fpath, fname))
        ftp.close()
        os.remove(fname)

        # Make it executable
        sin, sout, serr = client.exec_command('chmod +x %s' % os.path.join(fpath, fname))
        sout.channel.recv_exit_status()

        # Run the script
        stdin, stdout, stderr = client.exec_command(os.path.join(fpath, fname))
        exit_status = stdout.channel.recv_exit_status()
        stdout = stdout.read()
        stderr = stderr.read()
        self.set_output('stdout', stdout.decode('utf-8'))
        self.set_output('stderr', stderr.decode('utf-8'))
        self.set_output('exit_status', exit_status)

        # Delete the script
        sin, sout, serr = client.exec_command('rm %s' % os.path.join(fpath, fname))
        sout.channel.recv_exit_status()

        client.close()
