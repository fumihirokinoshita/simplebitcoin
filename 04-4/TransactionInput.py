class TransactionInput:
    """
    トランザクションの中でInputに格納するUTXOを指定する
    """
    def __init__(self, transaction, output_index):
        self.transaction = transaction
        self.output_index = output_index