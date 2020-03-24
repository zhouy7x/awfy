#!/usr/bin/python
import re
import os
import sys

import benchmarks
import utils

# wasm = benchmarks.Wasm()
# shell = '/repos/v8/out.gn/1/x64.release/d8'
# env = None
# args = None
# print(os.getcwd())

# wasm.benchmark(shell, env, args)

wx = benchmarks.WebXPRT3()
os.chdir('/home/user/work/awfy/benchmarks/webxprt3')
ret = wx.benchmark(shell="/home/user/work/repos/chrome/arm/chromium/src/out/arm/chrome",
             env=os.environ.copy(),
                   args=None)
print ret