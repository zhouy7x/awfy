#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
@author:zy
@time:2020/10/20
"""
import os
import sys
import benchmarks
import utils

Benchmarks = {
    'speedometer2': benchmarks.Speedometer2(),
    'webxprt3': benchmarks.WebXPRT3(),
    'webxprt4': benchmarks.WebXPRT4(),
    'jetstream2': benchmarks.JetStream2(),
}


def test(name, shell, target_os, env=os.environ.copy(), args=None):
    """
    remote test benchmark, return test result in dict
    """
    bench = Benchmarks[name]
    if target_os == 'win64':
        BenchmarkPath = 'c:/work/awfy/benchmarks'
        with utils.chdir(os.path.join(BenchmarkPath, bench.folder)):
            print os.getcwd()
            data = bench.win_benchmark(shell=shell, env=env, args=args)
    else:
        BenchmarkPath = '/home/user/work/awfy/benchmarks'
        with utils.chdir(os.path.join(BenchmarkPath, bench.folder)):
            print os.getcwd()
            data = bench.benchmark(shell=shell, env=env, args=args)
    return data


if __name__ == '__main__':
    name = sys.argv[1]
    shell = sys.argv[2]
    target_os = sys.argv[3]
    args = sys.argv[4:]
    test(name, shell, target_os, args=args)
