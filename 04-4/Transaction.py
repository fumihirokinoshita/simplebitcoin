class Transaction:
    """
    持っていないこいんを誰かに簡単に送金できてしまってはまったく意味がないので
    過去のトランザクションにて自分を宛先とsちえ送金されたコインの総計を超える
    送金以来を作ることができないよう、inputsとoutputsのペアによって管理する
    """
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs