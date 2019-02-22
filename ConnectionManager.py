from message_manager import MessageManager

PING_INTERVAL = 1800 # 30分


class ConnectionManager:
    def __init__(self):

        # 待受を開始する際に呼び出される (ServerCore向け)
        def start(self):

        # ユーザが指定した既知のCoreノードへの接続（ServerCore向け）
        def join_network(self):

        # 指定されたノードに対してメッセージを送信する
        def send_msg(self):

        # Coreノードリストに登録されているすべてのノードに対して
        # 同じメッセージをブロードキャストする
        def send_msg_to_all_peer(self):

        # 終了前の処理としてソケットを閉じる（ServerCore向け）
        def connection_close(self):

        # 受信したメッセージを確認して、内容に応じた処理を行う。クラスの外からは利用しない想定
        def __handle_message(self):

        # 新たに接続されたCoreノードをリストに追加する。クラスの外からは利用しない想定
        def __add_peer(self):

        # 離脱したCoreノードをリストから削除する。クラスの外からは利用しない想定
        def __remove_peer(self):

        # 接続されているCoreノードすべての接続状況確認を行う。クラスの外からは利用しない想定
        def __check_peers_connection(self):