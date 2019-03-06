import json

# 独自に拡張したENHANCEDメッセージの処理や生成を担当する
class MyProtocolMessageHandler(object):
    def __init__(self):
        print('mpmh __init__')
        print('Initializing MyProtocolMessageHandler...')

    def handle_message(self, msg):
        #とりあえず何も決まってないので受け取ったメッセージをコンソールに出力するだけ
        print('mpmh handle_meaage')
        msg = json.loads(msg)
        print('MyProtocolMessageHandler received ', msg)
        return