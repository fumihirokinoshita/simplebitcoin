from time import time

class Block:
    def __init__(self, transaction, previous_block_hash):
        self.timestamp = time()
        self.transaction = transaction
        self.previous_block = previous_block_hash