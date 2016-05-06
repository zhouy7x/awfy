import os
import pserver
import subprocess
import socket
import chromiumclient

def webscore(shell, env, args, url, timeout=600):
        full_args = []
        if args:
            full_args.extend(args)
        full_args.append('--no-sandbox')
        full_args.append(url)

        # use chromium client to start contentshell on slave machine
        chromiumclient.startChromium(args=full_args)

        try:
            data = pserver.getTestDataBySocket(timeout=timeout)
        except socket.timeout:
            print "CONTENT SHELL TEST TIME OUT!"
            data = ''
        finally:
            #phttpserver.kill()
            #pcontentshell.kill()
            chromiumclient.stopChromium()

        return data


shell = '/home/user/work/awfy/repos/chromium/src/out/Release/content_shell'
env = os.environ.copy()
args = None
url = 'http://commit.sh.intel.com/dom-2.1.html'
timeout = 300

print "Data:", webscore(shell, env, args, url, timeout)
