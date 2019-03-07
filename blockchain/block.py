import json
from time import time
import hashlib
import binascii
from datetime import datetime

class Block:
    def __init__(self, transactions, previous_block_hash):
        self.timestamp = time()
        self.transactions = transactions
        self.previous_block = previous_block_hash

        current = datetime.now().strftime("%Y/%m/%d/ %H:%M:%S")
        print(current)

        json_block = json.dumps(self.to_dict(include_nonce=False), sort_keys=True)
        print('json_block :', json_block)
        self.nonce = self._compute_nonce_for_pow(json_block)

        current2 = datetime.now().strftime("%Y/%m/%d/ %H:%M:%S")
        print(current2)

    def to_dict(self, include_nonce= True):
        d = {
            "timestamp" : self.timestamp,
            "transactions": list(map(json.dumps, self.transactions)),
            "previous_block": self.previous_block,
        }
        return d

        if include_nonce:
            d['nonce'] = self.nonce
        return d

    def _compute_nonce_for_pow(self, message, difficulty=5):
        # difficultyの数字を増やせば増やすほど、末尾で揃えなければならない桁数が増える。
        i = 0
        suffix = '0' * difficulty
        while True:
            nonce = str(i) # 総当たり的に数字を増やして試す
            digest = binascii.hexlify(self._get_double_sha256((message + nonce).encode('utf-8'))).decode('ascii')
            if digest.endswith(suffix):
                return nonce
            i += 1

    def _get_double_sha256(self, message):
        return hashlib.sha256(hashlib.sha256(message).digest()).digest()

class GenesisBlock(Block):
    """
    前方にブロックを持たせないブロックチェーンの始原となるブロック。
    transactionにセットしているのは
    「{"message":"this_is_simple_bitcoin_genesis_block"}」をSHA256でハッシュしたもの。深い意味はない
    """
    def __init__(self):
        super().__init__(transactions="AD9B477B42B22CDF18B1335603D", previous_block_hash=None)

    def to_dict(self, include_nonce=True):
        d = {
            "transactions": self.transactions,
            "genesis_block": True,
        }
        return d

        if include_nonce:
            d['nonce'] = self.nonce
        return d