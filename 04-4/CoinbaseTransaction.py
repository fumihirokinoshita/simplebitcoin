class Coinbasetransaciton(TransactionOutput):
    """
    Coinbaseトランザクションは例外的にInputが存在しない
    """
    def __init__(self, recipient_address, value=30):
        self.inputs = []
        self.outputs = [TransactionOutput(recipient_address, value)]