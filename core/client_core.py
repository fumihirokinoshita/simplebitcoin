import socket

from p2p.connection_manager_4edge import ConnectionManager4Edge

STATE_INIT = 0
STATE_ACTIVE = 1
STATE_SHUTTING_DOWN = 2

class ClientCore:
    def __init__(self, my_port=50082, core_host=None, core_port=None):
        print('cc __init__')
        self.client_state = STATE_INIT
        print('Initializing server ...')
        self.my_ip = self.__get_myip()
        print('Server IP address is set to ... ', self.my_ip)
        self.my_port = my_port
        self.cm = ConnectionManager4Edge(self.my_ip, my_port, core_host, core_port)

    def start(self):
        print('cc start')
        self.client_state = STATE_ACTIVE
        self.cm.start()
        self.cm.connect_to_core_node()

    def shutdown(self):
        print('cc shutdown')
        self.client_state = STATE_SHUTTING_DOWN
        print('Shutdown edge node ...')
        self.cm.connection_close()

    def get_my_current_state(self):
        print('cc get_my_current_start')
        return self.client_state

    def __get_myip(self):
        print('cc __get_myip')
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]