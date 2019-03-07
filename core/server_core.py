import time
import socket, threading, json
import pickle

from blockchain.blockchain_manager import BlockchainManager
from blockchain.block_builder import BlockBuilder
from transaction.transaction_pool import TransactionPool
from p2p.connection_manager import ConnectionManager
from p2p.my_protocol_message_handler import MyProtocolMessageHandler
from p2p.message_manager import(
    MSG_NEW_TRANSACTION,
    MSG_NEW_BLOCK,
    MSG_REQUEST_FULL_CHAIN,
    RSP_FULL_CHAIN,
    MSG_ENHANCED,
)

STATE_INIT = 0
STATE_STANDBY = 1
STATE_CONNECTED_TO_NETWORK = 2
STATE_SHUTTING_DOWN = 3

# TransactionPoolの確認頻度
# 動作チェックように数字小さくしてるけど、600(10分)くらいはあって良さそう
CHECK_INTERVAL = 10


class ServerCore(object):
    def __init__(self, my_port=50082, core_node_host=None, core_node_port=None):
        self.server_state = STATE_INIT
        print('Initializing server...')
        self.my_ip = self.__get_myip()
        print('Server IP address is set to ... ', self.my_ip)
        self.my_port = my_port
        self.cm = ConnectionManager(self.my_ip, self.my_port, self.__handle_message)
        self.mpmh = MyProtocolMessageHandler()
        self.core_node_host = core_node_host
        self.core_node_port = core_node_port
        
        self.bb = BlockBuilder()
        my_genesis_block = self.bb.generate_genesis_block()
        self.bm = BlockchainManager(my_genesis_block.to_dict())
        self.prev_block_hash = self.bm.get_hash(my_genesis_block.to_dict())
        self.tp = TransactionPool()

    def start(self):
        self.server_state = STATE_STANDBY
        self.cm.start()

        self.bb_timer = threading.Timer(CHECK_INTERVAL, self.__generate_block_with_tp)
        self.bb_timer.start()

    def join_network(self):
        # ここの条件分岐は機能していなかった。
        if self.core_node_host != None:
            self.server_state = STATE_CONNECTED_TO_NETWORK # 状態：親ノードへ接続中
            self.cm.join_network(self.core_node_host, self.core_node_port)
        else:
            print('This server is running as Genesis Core Node...')

    def shutdown(self):
        self.server_state = STATE_SHUTTING_DOWN # 状態：切断中
        print('Shutdown server...')
        self.cm.connection_close()

    def get_my_current_state(self):
        return self.server_state

    def get_all_chains_for_resolve_conflict(self):
        print('get_all_chains_for_resolve_conflict called')
        new_message = self.cm.get_message_text(MSG_REQUEST_FULL_CHAIN)
        self.cm.send_msg_to_all_peer(new_message)

    def __generate_block_with_tp(self):

        print('Thread for generate_block_with_tp started!')
        while self.flag_stop_block_build is not True:

            result = self.tp.get_stored_transactions()

            if result == None:
                print('Transacton Pool is empty ...')
                break
            new_tp = self.bm.remove_useless_transaction(result)
            self.tp.renew_my_transaction(new_tp)
            if len(result) == 0:
                break
            new_block = self.bb.generate_new_block(new_tp, self.prev_block_hash)
            self.bm.set_new_block(new_block.to_dict())
            self.prev_block_hash = self.bm.get_hash(new_block.to_dict())
            message_new_block = self.cm.get_message_text(MSG_NEW_BLOCK, json.dumps(new_block.to_dict()))
            self.cm.send_msg_to_all_peer(message_new_block)
            index = len(result)
            self.tp.clear_my_transactions(index)
            break

        print('Current Blockchain is ... ', self.bm.chain)
        print('Current prev_block_hash is ... ', self.prev_block_hash)
        self.flag_stop_block_build = False
        self.is_bb_running = False
        self.bb_timer = threading.Timer(CHECK_INTERVAL, self.__generate_block_with_tp)
        self.bb_timer.start()

    def __handle_message(self, msg, is_core, peer=None):
        if peer != None:
            if msg[2] == MSG_REQUEST_FULL_CHAIN:
                print('Send our latest blockchain for reply to : ', peer)
                mychain = self.bm.get_my_blockchain()
                chain_data = pickle.dumps(mychain, 0).decode()
                new_message = self.cm.get_message_text(RSP_FULL_CHAIN, chain_data)
                self.cm.send_msg(peer, new_message)
        else:
            if msg[2] == MSG_NEW_TRANSACTION:
                # 新規transactionを登録する処理を呼び出す
                new_transaction = json.loads(msg[4])
                print("received new_transaction", new_transaction)
                current_transactions = self.tp.get_stored_transactions()
                has_same = False
                if new_transaction in current_transactions:
                    print("this is already pooled transaction:", t)
                    return
                if not is_core:
                    self.tp.set_new_transaction(new_transaction)
                    new_message = self.cm.get_message_text(MSG_NEW_TRANSACTION, json.dumps(new_transaction))
                    self.cm.send_msg_to_all_peer(new_message)
                else:
                    self.tp.set_new_transaction(new_transaction)
            elif msg[2] == MSG_NEW_BLOCK:
                if not is_core:
                    print('block received from unknown')
                    return
                # 新規ブロックを検証し、正当なものであればブロックチェーンに追加する
                new_block = json.loads(msg[4])
                print('new_block: ', new_block)
                if self.bm.is_valid_chain(self.prev_block_hash, new_block):
                    # ブロック生成が行われていたら、いったん停止してあげる
                    # (threadingなのでキレイに止まらない場合あり)
                    if self.is_bb_running:
                        self.flag_stop_block_build = True
                    self.prev_block_hash = self.bm.get_hash(new_block)
                    self.bm.set_new_block(new_block)
                    new_tp = self.bm.remove_useless_transaction(result)
                    self.tp.renew_my_transaction(new_tp)
                else:
                    # ブロックとして不正ではないがVerifyにコケる婆は自分がorphanブロックを生成している可能性がある
                    sef.get_all_chains_for_resolve_conflict()
            elif msg[2] == RSP_FULL_CHAIN:
                # ブロックチェーン送信要求に応じて返却されたブロックチェーンを検証し、有効なものか検証した上で
                # 自分の持つチェーンと比較し優位な方を今後のブロックチェーンとして有効化する

                if not is_core:
                    print('blockchain received from unknown')
                    return
                new_block_chain = pickle.loads(msg[4].encode('utf8'))
                print(new_block_chain)
                result, pool_4_orphan_blocks = self.bm.resolve_conflicts(new_block_chain)
                print('blockchain received form central')
                if result is not None:
                    self.prev_block_hash = result
                    if len(pool_4_orphan_blocks) != 0:
                        # orphanブロック群の中にあった未処理扱いになる
                        # TransactionをTransactionPoolに戻す
                        new_transactions = self.bm.get_transactions_from_orphan_blocks(pool_4_orphan_blocks)

                        for t in new_transactions:
                            self.tp.set_new_transaction(t)
                else:
                    print('Received blockchain is useless...')

            elif msg[2] == MSG_ENHANCED:
                # P2P Networkを単なるトランスポートして使っているアプリケーションが独自拡張したメッセージはここで処理する。SimpleBitcoinとしてはこの種別は使わない

                self.mpmh.handle_message(msg[4])

    def __get_myip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]