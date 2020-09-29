#!/usr/bin/python
import re
import os
import socket
import sys

import benchmarks
import utils

# wasm = benchmarks.Wasm()
# shell = '/repos/v8/out.gn/1/x64.release/d8'
# env = None
# args = None
# print(os.getcwd())

# wasm.benchmark(shell, env, args)
src = "d:\src\chromium\src"
# src = "d:"
reger = re.match(r"^(\w):(.*)$", src)
if reger:
    tmp = reger.groups()
    print tmp
    src = "/cygdrive/" + tmp[0] + tmp[1]
    src = src.replace('\\', '/')

    print src
#
# host = "10.239.61.100"
# port = 8781
# #port = 8790
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((host, port))
# hello = s.recv(1024)
# print hello
# print 'over'
source = r"chromium\src"
cpu = 'x64'
shell = os.path.join('out', cpu, 'Chrome-bin', 'chrome.exe')
# shell = r"d:\src\chromium\src\out\x64\Chrome-bin\chrome.exe"
print shell
shell = os.path.join(r"c:\work\repos\win64-chrome\x64", source, shell)
print shell
