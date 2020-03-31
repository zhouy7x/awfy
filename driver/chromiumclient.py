import socket

HOST = "127.0.0.1"
PORT = 50005


def startChromium(host=HOST, port=PORT, args=[]):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    msg = 'start';
    for arg in args:
        msg += ';' + arg;

    s.sendall(msg)

    s.close()


def stopChromium(host=HOST, port=PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    s.sendall('end')

    s.close()
