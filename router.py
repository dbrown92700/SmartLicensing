from netmiko import ConnectHandler, SCPConn


class Router:
    def __init__(self, host, username, password, port=22, device_type='cisco_ios'):

        # device_type 'cisco_ios' works with Cisco CLI

        try:
            self.connection = ConnectHandler(device_type=device_type, host=host, username=username, password=password,
                                             port=port)
            self.status = 'Connected'
            self.error = 'None'
        except Exception as e:
            self.status = 'Failed'
            self.error = e.args[0]

    def send_command(self, command, expect=None):
        if expect is None:
            return self.connection.send_command(command)
        else:
            return self.connection.send_command(command_string=command, expect_string=expect)

    def send_file(self, local_file: str, remote_file: str):
        scpconn = SCPConn(self.connection)
        scpconn.establish_scp_conn()
        scpconn.scp_put_file(local_file, remote_file)
        scpconn.close()

    def get_file(self, local_file: str, remote_file: str):
        scpconn = SCPConn(self.connection)
        scpconn.establish_scp_conn()
        scpconn.scp_get_file(remote_file, local_file)
        scpconn.close()

    def disconnect(self):
        self.connection.disconnect()
        self.status = 'Disconnected'
