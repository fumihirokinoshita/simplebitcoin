from distutils.version import StrictVersion
import json

PROTOCOL_NAME = 'simple-bitcoin_protocl'
MY_VERSION = '0.1.0'

MSG_ADD = 0
MSG_REMOVE = 1
MSG_CORE_LEST = 2
MSG_REQUEST_CORE_LIST = 3
MSG_PING = 4
MSG_ADD_AS_EDGE = 5
MSG_REMOVE_EDGE = 6

ERR_PROTOCOL_UNMATCH = 0
ERR_VERSION_UMMATCH = 1
OK_WITH_PAYLOAD = 2
OK_WTHOUT_PYLOAD = 3


class MessageManager:
    def __init__(self):
        print('Initializing MessageManager...')

    def build(self, msg_type, payload=None):

        message = {
            'protocol': PROTOCOL_NAME,
            'version': MY_VERSION,
            'msg_type': msg_type,
        }

        if payload is not None:
            message['payload'] = payload

        return json.dumps(message)

    def parse(self, msg):

        msg = json.loads(msg)
        msg_ver = StrictVersion(msg['version'])

        cmd = msg['msg_type']
        payload = msg['payload']

        if msg['protocol'] != PROTOCOL_NAME:
            return ('error', ERR_PROTOCOL_UNMATCH, None, None)
        elif msg_ver > StrictVersion(MY_VERSION):
            return ('error', ERR_VERSION_UMMATCH, None, None)
        elif cmd == MSG_CORE_LEST:
            return ('ok', OK_WITH_PAYLOAD, cmd, payload)
        else:
            return ('ok', OK_WTHOUT_PYLOAD, cmd, None)