import threading


class EdgeNodeList:
    def __init__(self):
        print('enl def __init__')
        self.lock = threading.Lock()
        self.list = set()
    
    def add(self, edge):
        print('enl def add')
        """
        Edgeノードをリストに追加する。
        """
        with self.lock:
            print('Adding edge: ', edge)
            self.list.add((edge))
            print('Current Edge List: ', self.list)

    def remove(self, edge):
        print('enl def remove')
        """
        離脱したと判断されるEdgeノードをリストから削除する。
        """
        with self.lock:
            if edge in self.list:
                print('Removing edge: ', edge)
                self.list.remove(edge)
                print('Current Edge List: ', self.list)

    def get_list(self):
        print('enl def get_list')
        """
        現在接続状態にあるEdgeノードの一覧を返却する。
        """
        return self.list