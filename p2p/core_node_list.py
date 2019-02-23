import threading

class CoreNodeList:
    def __init__(self):
        print('cnl def __init__')
        self.lock = threading.Lock()
        self.list = set()

    def add(self, peer):
        print('cnl def add')
        """
        Coreノードをリストに追加する。
        """
        with self.lock:
            print('Adding peer: ', peer)
            self.list.add((peer))
            print('Current Core List:', self.list)

    def remove(self, peer):
        print('cnl def remove')
        """
        離脱したと判断されるCoreノードをリストから削除する。
        """
        with self.lock:
            if peer in self.list:
                print('Removing peer: ', peer)
                self.list.remove(peer)
                print('Current Core list: ', self.list)

    def overwrite(self, new_list):
        print('cnl def overwrite')
        """
        複数のpeerの接続状況確認を行ったあとで一括での上書き処理をしたいような場合はこちら
        """
        with self.lock:
            print('core node list will be going to overwrite')
            self.list = new_list
            print('Current Core list: ', self.list)
      
    def get_list(self):
        print('cnl def get_list')
        """
        現在接続状態にあるPeerの一覧を返却する
        """
        return self.list

    def get_c_node_info(self):
        return list(self.list)[0]

