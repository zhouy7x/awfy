import os
import sys
import socket
import subprocess
import thread
import signal
import time

# executable path
ChromiumShell = "/home/user/work/repos/chromium/src/out/Release/content_shell"
# lock for running chromium
ALock = thread.allocate_lock()

Chromiump = None
# lock the Chromiump variable
Lockv = thread.allocate_lock()

# timeout for one turn
Timeout = 20

# last start time
StartTime = 0


# use to handle time out
def TimeoutHandler(elapsedTime):
    global Chromiump, Lockv, ALock

    Lockv.acquire()
    if Chromiump:
        print "Timeout Stop after running", elapsedTime, "s"
        Chromiump.kill()
        Chromiump = None
        # ALock.release()
        # use a new lock
        ALock = thread.allocate_lock()
    Lockv.release()


# start chromium socket server
def StartChromiumServer(port=50005):
    HOST = ''

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, port))
    s.listen(3)

    print "ChromiumServer start at port:", port

    print "Chromium timeout:", Timeout, "s"

    while True:
        conn, addr = s.accept()
        print 'Connected by', addr
        thread.start_new_thread(ClientThreadHandle, (conn, addr))

    s.close()


# handle connected client
def ClientThreadHandle(conn, addr):
    global Chromiump, StartTime, ALock

    while True:
        data = conn.recv(1024)
        if not data:
            break

        print 'From:', addr
        print 'Recv:', data

        args = data.split(";");
        if args[0] == "start":
            print "start request"
            run_cmd = [ChromiumShell] + args[1:]

            elapsedTime = time.time() - StartTime
            if elapsedTime > Timeout:
                TimeoutHandler(elapsedTime)

            # one chromium at a time
            ALock.acquire()
            # start chromium
            Lockv.acquire()
            Chromiump = subprocess.Popen(run_cmd, env=os.environ.copy())
            StartTime = time.time()
            Lockv.release()
        elif args[0] == "end":
            print "end request"
            # if chromium is running, kill it and release the lock
            Lockv.acquire()
            if Chromiump:
                Chromiump.kill()
                Chromiump = None
                ALock.release()
            Lockv.release()

    conn.close()
    print "Disconnected by", addr


if __name__ == "__main__":
    StartChromiumServer()
