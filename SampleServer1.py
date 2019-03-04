import signal
from time import sleep

from core.server_core import ServerCore

my_p2p_server = None


def signal_handler(signal, frame):
    print('ss1 signal_handler')
    shutdown_server()


def shutdown_server():
    print('ss1 shutdown_server')
    global my_p2p_server
    my_p2p_server.shutdown()


def main():
    print('ss1 main')
    signal.signal(signal.SIGINT, signal_handler)
    global my_p2p_server
    # 始原のCoreノードとして起動する
    my_p2p_server = ServerCore(50082)
    my_p2p_server.start()


if __name__ == '__main__':
    main()