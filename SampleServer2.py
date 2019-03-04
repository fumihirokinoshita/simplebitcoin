import signal

from core.server_core import ServerCore

my_p2p_server = None


def signal_handler(signal, frame):
    print('ss2 signal_handler')
    shutdown_server()


def shutdown_server():
    print('ss2 shutdown_server')
    global my_p2p_server
    my_p2p_server.shutdown()


def main():
    print('ss2 main')
    signal.signal(signal.SIGINT, signal_handler)
    global my_p2p_server
    my_p2p_server = ServerCore(50090, '192.168.10.104', 50082)
    my_p2p_server.start()
    my_p2p_server.join_network()


if __name__ == '__main__':
    main()
