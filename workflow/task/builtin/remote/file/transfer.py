from ....base import Task
from ..utils import create_ssh_client


class RemoteFileUploadTask(Task):
    ID = 'builtin.remote.file.upload'

    def run(self):
        local_path = self.get_input('localPath')
        remote_path = self.get_input('remotePath')

        client = create_ssh_client(self.inputs)
        ftp = client.open_sftp()
        ftp.put(local_path, remote_path)
        ftp.close()
        client.close()


class RemoteFileDownloadTask(Task):
    ID = 'builtin.remote.file.upload'

    def run(self):
        local_path = self.get_input('localPath')
        remote_path = self.get_input('remotePath')

        client = create_ssh_client(self.inputs)
        ftp = client.open_sftp()
        ftp.get(remote_path, local_path)
        ftp.close()
        client.close()
