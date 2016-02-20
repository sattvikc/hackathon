from ....base import Task

import paramiko


class RemoteFileCreateTask(Task):
    ID = 'builtin.remote.file.create'

    def run(self):
        host = self.get_input('host')
        port = self.get_input('port', 22)
        username = self.get_input('username')
        password = self.get_input('password')
        directory = self.get_input('directory')
        filename = self.get_input('filename')
        contents = self.get_input('contents')
        treat_as_known = self.get_input('treatAsKnown', True)

        client = paramiko.SSHClient()
        if treat_as_known:
            client.set_missing_host_key_policy(
                paramiko.AutoAddPolicy())

        client.connect(host, port, username, password)
        stdin, stdout, stderr = client.exec_command("cd %s; cat > %s" % (directory, filename))
        stdin.write(contents)
        stdin.flush()
        stdin.close()
        client.close()
