from ....base import Task
from ..utils import create_ssh_client


class RemoteFileUploadTask(Task):
    ID = 'builtin.remote.file.upload'
    NAME = 'RemoteFileUpload'
    DESCRIPTION = 'Uploads file from local machine to remote machine.'
    INPUTS = [
        ('username', 'Login username'),
        ('password', 'Login password'),
        ('host', 'Remote SSH Hostname'),
        ('port', 'Remote SSH Port, default=22'),
        ('localPath', 'Local file path to upload'),
        ('remotePath', 'Remote file path to save')
    ]
    OUTPUTS = []

    def run(self):
        local_path = self.get_input('localPath')
        remote_path = self.get_input('remotePath')

        client = create_ssh_client(self.inputs)
        ftp = client.open_sftp()
        ftp.put(local_path, remote_path)
        ftp.close()
        client.close()


class RemoteFileDownloadTask(Task):
    ID = 'builtin.remote.file.download'
    NAME = 'RemoteFileDownload'
    DESCRIPTION = 'Downloads file from remote machine to local machine.'
    INPUTS = [
        ('username', 'Login username'),
        ('password', 'Login password'),
        ('host', 'Remote SSH Hostname'),
        ('port', 'Remote SSH Port, default=22'),
        ('localPath', 'Local file path to save'),
        ('remotePath', 'Remote file path to download')
    ]
    OUTPUTS = []

    def run(self):
        local_path = self.get_input('localPath')
        remote_path = self.get_input('remotePath')

        client = create_ssh_client(self.inputs)
        ftp = client.open_sftp()
        ftp.get(remote_path, local_path)
        ftp.close()
        client.close()
