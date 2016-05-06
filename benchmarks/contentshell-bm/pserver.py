import socket

def getMyName():
    name = socket.gethostname()
    return name + '.sh.intel.com'

def getTestDataBySocket(port=50007, timeout=None):
    HOST = ''

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, port))
    s.listen(1)

    if timeout:
        s.settimeout(timeout)
    conn, addr = s.accept()
    print 'Connected by', addr

    res = ''
    while True:
        data = conn.recv(1024)
        res = res + data
        if not data:
            break
    conn.close()

    return res
