from ....base import Task

import paramiko


class RemoteFileUploadTask(Task):
    ID = 'builtin.remote.file.upload'

    def run(self):
        host = self.get_input('host')
        port = self.get_input('port', 22)
        username = self.get_input('username')
        password = self.get_input('password')
        local_path = self.get_input('localPath')
        remote_path = self.get_input('remotePath')
        treat_as_known = self.get_input('treatAsKnown', True)

        client = paramiko.SSHClient()
        if treat_as_known:
            client.set_missing_host_key_policy(
                paramiko.AutoAddPolicy())

        client.connect(host, port, username, password)
        ftp = client.open_sftp()
        ftp.put(local_path, remote_path)
        ftp.close()
        client.close()


class RemoteFileDownloadTask(Task):
    ID = 'builtin.remote.file.upload'

    def run(self):
        host = self.get_input('host')
        port = self.get_input('port', 22)
        username = self.get_input('username')
        password = self.get_input('password')
        local_path = self.get_input('localPath')
        remote_path = self.get_input('remotePath')
        treat_as_known = self.get_input('treatAsKnown', True)

        client = paramiko.SSHClient()
        if treat_as_known:
            client.set_missing_host_key_policy(
                paramiko.AutoAddPolicy())

        client.connect(host, port, username, password)
        ftp = client.open_sftp()
        ftp.get(remote_path, local_path)
        ftp.close()
        client.close()
