from message_manager import MessageManager

PING_INTERVAL = 1800 # 30分


class ConnectionManager:
    def __init__(self):
        print('Initializing ConnectionManager...')
        self.host = host
        self.port = my_port
        self.core_node_set = set()
        self.__add_peer((host, my_port))
        self.mm = MessageManager()

    # 待受を開始する際に呼び出される (ServerCore向け)
    def start(self):

    def __wait_for_access(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(0)

        executor = ThreadPoolExecutor(max_workers=10)

        while True:

            print('Waiting for the connection ...')
            soc, addr = self.socket.accept()
            print('Connected by .. ', addr)
            data_sum = ''

            params = (soc, addr, data_sum)
            executor.submit(self.__handle_message, params)

    # ユーザが指定した既知のCoreノードへの接続（ServerCore向け）
    def join_network(self):

    # 指定されたノードに対してメッセージを送信する
    def send_msg(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((peer))
            s.sendall(msg.encode('utf-8'))
            s.close()
        except OSError:
            print('Connection failed for peer : ', peer)
            self.__remove_peer(peer)

    # Coreノードリストに登録されているすべてのノードに対して
    # 同じメッセージをブロードキャストする
    def send_msg_to_all_peer(self):
        print('send_msg_to_all_peer was called! ')
        for peer in self.core_node_set:
            if peer != (self.host, self.port):
                print('message will be sent to ...', peer)
                self.send_msg(peer, msg)

    # 終了前の処理としてソケットを閉じる（ServerCore向け）
    def connection_close(self):

    # 受信したメッセージを確認して、内容に応じた処理を行う。クラスの外からは利用しない想定
    def __handle_message(self, params):

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
            if cmd == MSG_ADD:
                print('ADD nod request was received!!')
                self.__add_peer((addr[0], peer_port))
                if(addr[0], peer_port) == (self.host, self.port):
                    return
                else:
                    cl = pickle.dumps(self.core_node_set, 0).decode()
                    msg = self.mm.build(MSG_CORE_LIST, self.port, cl)
                    self.send_msg_to_all_peer(msg)
            elif cmd == MSG_REMOVE:
                print('REMOVE request was received!! from', addr[0], peer_port)
                self.__remove_peer((addr[0], peer_port))
                cl = pickle.dumps(self.core_node_set, 0).decode()
                msg = self.mm.build(MSG_CORE_LIST, self.port, cl)
                self.send_msg_to_all_peer(msg)
            elif cmd == MSG_PING:
                # 特にやることがない
                return
            elif cmd == MSG_REQUEST_CORE_LIST:
                print('List fore Core nodes was requested!!')
                cl = pickle.dumps(self.core_node_set, 0).decode()
                msg = self.mm.build(MSG_CORE_LIST, self.port, cl)
                self.send_msg((addr[0], peer_port), cmd)
            else:
                print('received unknown command', cmd)
                return
        elif status == ('ok', OK_WITH_PAYLOAD):
            if cmd == MSG_CORE_LIST:
                # TODO: 受信したリストをただ上書きしてしまうのは
                # 本来セキュリティ的によろしくない。
                # 信頼できるノードの鍵とかをセットSとく必要があるかも
                # この辺りの議論は第6章にて補足予定
                print('Refresh the core node list...')
                new_core_set = pickle.loads(payload.encode('utf-8'))
                print('latest core node list:', new_core_set)
                self.core_node_set = new_core_set
            else:
                print('received unknown command', cmd)
                return
        else:
            print('Unexpected status', status)


        # 新たに接続されたCoreノードをリストに追加する。クラスの外からは利用しない想定
        def __add_peer(self):
            print('Adding peer: ', peer)
            self.core_node_set.add((peer))

        # 離脱したCoreノードをリストから削除する。クラスの外からは利用しない想定
        def __remove_peer(self):
            if peer in self.core_node_set:
                print('Removing peer:', peer)
                self.core_node_set.remove(peer)
                print('Current Core list: ', self.core_node_set)

        # 接続されているCoreノードすべての接続状況確認を行う。クラスの外からは利用しない想定
        def __check_peers_connection(self):
            """
            接続されているCoreノードすべての接続状況確認を行う。クラスの外からは利用しない想定
            この確認処理は定期的に実行sれる
            """
            print('check_peers_connection was called')
            changed = False
            dead_c_node_set = list(filter(lambda p: not self.__is_alive(p), self.core_node_set))
            if dead_c_node_set:
                changed = True
                print('Removing ', dead_c_node_set)
                self.core_node_set = self.core_node_set - set(dead_c_node_set)

            print('current core node list:', self.core_node_list)
            # 変更があったとだけブロードキャストで通知する
            if changed:
                cl = pickle.dumps(self.core_node_set, 0).decode()
                msg = self.mm.build(MSG_CORE_LIST, self.port, cl)
                self.send_msg_to_all_peer(msg)

            self.ping_timer = threading.Timer(PING_INTERVAL, SELF.__check_peers_connection)
            self.ping_timer.start()

        def __is_alive(self, target):
            """
            有効ノード確認メッセージの送信

            param:
                target : 有効ノード確認メッセージの送り先となるノードの接続情報
                        （IPアドレスとポート番号）
            """
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((target))
                msg_type = MSG_TYPE
                msg = self.mm.build(msg_type)
                s.sendall(msg.encode('utf-8'))
                s.close()
                return True
            except OSError:
                return False