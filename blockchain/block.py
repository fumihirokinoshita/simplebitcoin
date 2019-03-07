import json
from time import time

class Block:
    def __init__(self, transactions, previous_block_hash):
        self.timestamp = time()
        self.transactions = transactions
        self.previous_block = previous_block_hash

    def to_dict(self):
        d = {
            "timestamp" : self.timestamp,
            "transactions": list(map(json.dumps, self.transactions)),
            "previous_block": self.previous_block,
        }
        return d

class GenesisBlock(Block):
    """
    前方にブロックを持たせないブロックチェーンの始原となるブロック。
    transactionにセットしているのは
    「{"message":"this_is_simple_bitcoin_genesis_block"}」をSHA256でハッシュしたもの。深い意味はない
    """
    def __init__(self):
        super().__init__(transactions="AD9B477B42B22CDF18B1335603D", previous_block_hash=None)

    def to_dict(self):
        d = {
            "transactions": self.transactions,
            "genesis_block": True,
        }
        return d