class TransactionInput:
    """
    トランザクションの中でInputに格納するUTXOを指定する
    """
    def __init__(self, transaction, output_index):
        self.transaction = transaction
        self.output_index = output_index

    def to_dict(self):
        d = {
            'transaction': self.transaction,
            'output_index': self.output_index
        }
        return d

class TransactionOutput:
    """
    トランザクションのなkでOutput（送金相手と送る金額）を管理する
    """
    def __init__(self, recipient_address, value):
        self.recipient = recipient_address
        self.value = value

    def to_dict(self):
        d = {
            'recipient_address': self.recipient,
            'value': self.value
        }
        return d

class Transaction:
    """
    持っていないコインを誰かに簡単に送金できてしまってはまったく意味がないので、
    過去のトランザクションにて自分を宛先として送金されたコインの統計を
    超える送金依頼を作ることができないよう、inputs と outputs のペアによって管理する
    """
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs

    def to_dict(self):
        d = {
            'inputs': list(map(TransactionInput.to_dict, self.inputs)),
            'outputs': list(map(TransactionOutput.to_dict, self.outputs)),
        }

        return d

    def is_enough_inputs(self, fee):
        total_in = sum(i.transaction['inputs'][i.output_index]['value'] for i in self.inputs)
        total_out = sum(int(o.value) for o in self.outputs) + int(fee)
        delta = total_in - total_out
        if delta >= 0:
            return True
        else:
            return False

class CoinbaseTransaction(Transaction):
    """
    Coinbase Transacitonは例外的にInputが存在しない。
    """
    def __init__(self, recipient_address, value=30):
        self.inputs = []
        self.outputs = [TransactionOutput(recipient_address, value)]

    def to_dict(self):
        return super().to_dict()