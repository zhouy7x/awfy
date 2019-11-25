#!/usr/bin/python
import re
import os
import benchmarks
import utils

spk = benchmarks.Spec2k6()
poly = benchmarks.Polybench()
env = {
    "LD_LIBRARY_PATH": "/home/user/work/repos/jsc/base/webkit/WebKitBuild/Release/lib:/home/user/jsc-dependence:$LD_LIBRARY_PATH"
}
shell = "/home/user/work/repos/jsc/base/webkit/WebKitBuild/Release/bin/jsc"

spk.benchmark(shell, env, None)
poly.benchmark(shell, env, None)




