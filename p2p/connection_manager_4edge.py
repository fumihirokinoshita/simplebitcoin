import socket
import threading
import pickle
import codecs
from concurrent.futures import ThreadPoolExecutor

from .core_node_list import CoreNodeList
from .message_manager import (
    MessageManager,
    MSG_CORE_LIST,
    MSG_PING,
    MSG_ADD_AS_EDGE,
    ERR_PROTOCOL_UNMATCH,
    ERR_VERSION_UNMATCH,
    OK_WITH_PAYLOAD,
    OK_WITHOUT_PAYLOAD,
)

# 動作確認用の値。本来は30分(1800)くらいが良いのでは
PING_INTERVAL = 10


class ConnectionManager4Edge(object):
    def __init__(self, host, my_port, my_core_host, my_core_port, callback):
        print('4 def __init__')
        print('Initializing ConnectionManager4Edge...')
        self.host = host
        self.port = my_port
        self.my_core_host = my_core_host
        self.my_core_port = my_core_port
        self.core_node_set = CoreNodeList()
        self.mm = MessageManager()

        self.callback = callback

    def start(self):
        print('4 def start')
        """
        最初の待受を開始する際に呼び出される（ClientCore向け）
        """
        t = threading.Thread(target=self.__wait_for_access)
        t.start()

        self.ping_timer = threading.Timer(PING_INTERVAL, self.__send_ping)
        self.ping_timer.start()

    def connect_to_core_node(self):
        print('4 def connect_to_core_node')
        """
        ユーザが指定した既知のCoreノードへの接続（ClientCore向け）
        """
        self.__connect_to_P2PNW(self.my_core_host, self.my_core_port)

    def get_message_text(self, msg_type, payload = None):
        msgtxt = self.mm.build(msg_type, self.port, payload)
        print('generated_msg:', msgtxt)
        return msgtxt

    def send_msg(self, peer, msg):
        print('4 def send_msg')
        """
        指定されたノードに対してメッセージを送信する
        """
        print('Sending... ', msg)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((peer))
            s.sendall(msg.encode('utf-8'))
            s.close()
        except:
            print('Connection failed for peer : ', peer)
            self.core_node_set.remove(peer)
            print('Tring to connect into P2P network...')
            current_core_list = self.core_node_set.get_list()
            # 接続エラー時には他のCoreノードに移住する
            if len(current_core_list) != 0:
                new_core = self.core_node_set.get_c_node_info()
                self.my_core_host = new_core[0]
                self.my_core_port = new_core[1]
                self.connect_to_core_node()
                self.send_msg((new_core[0], new_core[1]), msg)
            else:
                print('No core node found in our list...')
                self.ping_timer.cancel()

    def connection_close(self):
        print('4 def connection_close')
        """
        終了前の処理としてソケットを閉じる
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        self.socket.close()
        s.close()
        self.ping_timer.cancel()

    def __connect_to_P2PNW(self, host, port):
        print('4 def __connect_to_P2PNW')
        """
        指定したCoreノードへ接続要求メッセージを送信する
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        msg = self.mm.build(MSG_ADD_AS_EDGE, self.port)
        print(msg)
        s.sendall(msg.encode('utf-8'))
        s.close()

    def __wait_for_access(self):
        print('4 def __wait_for_access')
        """
        Serverソケットを開いて待受状態に移行する
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(0)

        executor = ThreadPoolExecutor(max_workers=10)

        while True:

            print('Waiting for the connection ...')
            soc, addr = self.socket.accept()
            print('Connected by ...', addr)
            data_sum = ''

            params = (soc, addr, data_sum)
            executor.submit(self.__handle_message, params)

    def __handle_message(self, params):
        print('4 def __handle_message')
        """
        受信したメッセージを確認して、内容に応じた処理を行う。
        クラスの外からは利用しない想定
        """

        soc, addr, data_sum = params
        
        while True:
            data = soc.recv(1024)
            data_sum = data_sum + data.decode('utf-8')

            if not data:
                break

        if not data_sum:
            return

        result, reason, cmd, peer_port, payload = self.mm.parse(data_sum)
        print(result, reason, cmd, peer_port, payload)
        status = (result, reason)

        if status == ('error', ERR_PROTOCOL_UNMATCH):
            print('Error: Protocol name is not matched')
            return
        elif status == ('error', ERR_VERSION_UNMATCH):
            print('Error: Protocol version is not matched')
            return
        elif status == ('ok', OK_WITHOUT_PAYLOAD):
            if cmd == MSG_PING:
                pass
            else:
                # 接続情報以外のメッセージしかEdgeノードで処理することは想定していない
                print('Edge node does not have functions for this message!')
        elif status == ('ok', OK_WITH_PAYLOAD):
            if cmd == MSG_CORE_LIST:
                # Coreノードに依頼してCoreノードのリストを受け取る口だけはある
                print('Referesh the core node list...')
                new_core_set = pickle.loads(payload.encode('utf8'))
                print('latest core node list: ', new_core_set)
            else:
                self.callback((result, reason, cmd, peer_port, payload))
        else:
            print('Unexpected status', status)

    def __send_ping(self):
        print('4 def __send_ping')
        """
        生存確認メッセージの送信処理実体。中で確認処理は定期的に実行し続けられる
        """
        peer = (self.my_core_host, self.my_core_port)

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((peer))
            msg = self.mm.build(MSG_PING)
            s.sendall(msg.encode('utf-8'))
            s.close()
        except:
            print('Connection failed for peer : ', peer)
            self.core_node_set.remove(peer)
            print('Tring to connect into P2P network...')
            current_core_list = self.core_node_set.get_list()
            # 接続エラー時には他のCoreノードに移住する
            if len(current_core_list) != 0:
                new_core = self.core_node_set.get_c_node_info()
                self.my_core_host = new_core[0]
                self.my_core_port = new_core[1]
                self.connect_to_core_node()
            else:
                print('No core node found in our list...')
                self.ping_timer.cancel()
        
        self.ping_timer = threading.Timer(PING_INTERVAL, self.__send_ping)
        self.ping_timer.start()