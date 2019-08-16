#!/usr/bin/python
import re
import os
import benchmarks
import utils

# wasm = benchmarks.Wasm()
# shell = '/repos/v8/out.gn/1/x64.release/d8'
# env = None
# args = None
# print(os.getcwd())

# wasm.benchmark(shell, env, args)

tests = []
with open('log2.txt') as f:
    output = f.read()
subcases = re.findall(r'(\w+)\n[\w\W]+?\n\[INFO\] Normalized time: (\d+\.\d+)\n', output)
print subcases, len(subcases)
for subcase in subcases:
    name = subcase[0]
    score = utils.myround(subcase[1])
    tests.append({'name': name, 'time': score})
    print(score + '     - ' + name)
# ls = [float(x['time']) for x in tests]
# t = reduce(lambda i, j: i * j, ls)
# print ls
# print t
# print type(t)
# total = pow(t, 1.0/len(tests))
total = pow(reduce(lambda i, j: i * j, [float(x['time']) for x in tests]), 1.0 / len(tests))
# print total
name = '__total__'
score = utils.myround(total)
tests.append({'name': name, 'time': score})
print(score + '     - ' + name)
# a = round(float(score), 4)
# print a, type(a)
