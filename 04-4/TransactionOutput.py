class TransactionOutput:
    """
    トランザクションの中でOutput（送金相手と送る金額）を管理する
    """
    def __init__(self, recipient_address, value):
        self.recipient = recipient_address
        self.value = value