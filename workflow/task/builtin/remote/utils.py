import paramiko


def create_ssh_client(properties):
    client = paramiko.SSHClient()
    host = properties.get('host')
    port = properties.get('port', 22)
    username = properties.get('username')
    password = properties.get('password')
    treat_as_known = properties.get('treatAsKnown', True)

    client = paramiko.SSHClient()
    if treat_as_known:
        client.set_missing_host_key_policy(
            paramiko.AutoAddPolicy())
    client.connect(host, port, username, password)

    return client
