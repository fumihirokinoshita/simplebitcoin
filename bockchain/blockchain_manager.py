import threading

class BlockchainManager:
    def __init__(self):
        print('Initializing BlockchainManager...')
        self.chain = []
        self.lock = threading.Lock()

    def set_new_block(self, block):
        with self.lock:
            self.chain.append(block)

    def _get_double_sha256(self, message):
        return hashlib.sha256(hashlib.sha256(message).dijest()).dijest()

    def get_hash(self, block):
        block_string = json.dumps(block, sort_keys=True)
        return binascii.hexlify(self._get_double_sha256((block_string).encode('utf-8'))).decode('ascii')