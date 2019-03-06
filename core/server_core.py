import socket

from p2p.connection_manager import ConnectionManager

STATE_INIT = 0
STATE_STANDBY = 1
STATE_CONNECTED_TO_NETWORK = 2
STATE_SHUTTING_DOWN = 3


class ServerCore:
    def __init__(self, my_port=50082, core_node_host=None, core_node_port=None):
        print('sc def __init__')
        self.server_state = STATE_INIT
        print('Initializing server...')
        self.my_ip = self.__get_myip()
        print('Server IP address is set to ... ', self.my_ip)
        self.my_port = my_port
        self.cm = ConnectionManager(self.my_ip, self.my_port)
        self.core_node_host = core_node_host
        self.core_node_port = core_node_port

    def start(self):
        print('sc def start')
        self.server_state = STATE_STANDBY
        self.cm.start()

    def join_network(self):
        print('sc def join_network')
        # ここの条件分岐は昨日していなかった。
        if self.core_node_host is not None:
            self.server_state = STATE_CONNECTED_TO_NETWORK
            self.cm.join_network(self.core_node_host, self.core_node_port)
        else:
            print('This sever is running as Genesis Core Node...')

    def shutdown(self):
        print('sc def shutdown')
        self.server_state = STATE_SHUTTING_DOWN
        print('Shutdown server...')
        self.cm.connection_close()

    def get_my_current_state(self):
        print('sc def get_my_current_state')
        return self.server_state

    def __handle_message(self, msg, peer=None):
        print('sc __handle_message')
        if peer != None:
            # MSG_REQUEST_FULL_CHAIN
            print('Send our latest blockchain for reply to : ', peer)
        else:
            if msg[2] == MSG_NEW_TRANSACTION:
                # TODO: 新規transactionを登録する処理を呼び出す
                pass
            elif msg[2] == MSG_NEW_BLOCK:
                # TODO: 新規ブロックを検証する処理を呼び出す
            elif msg[2] == RSP_FULL_CHAIN:
                # TODO: ブロックチェーン送信要求に応じて返却されたブロックチェーンを検証する処理を呼び出す
                pass
            elif msg[2] == MSG_HENHANCED:
                # P2P Networkを単なるトランスポートして使っているアプリケーションが独自拡張したメッセージはここで処理する。
                # SimpleBitcoinとしてはこの種別は使わない
                self.mpmh.handle_message(msg[4])
                pass

    def __get_myip(self):
        print('sc def __get_myip')
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]