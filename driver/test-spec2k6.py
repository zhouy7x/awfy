#!/usr/bin/python
import re
import os
import benchmarks
import utils

wasm = benchmarks.Spec2k6()
shell = '/repos/v8/out.gn/1/x64.release/d8'
env = None
args = None
print(os.getcwd())

# wasm.benchmark(shell, env, args)

tests = []
# output = """
# gemm\n[INFO] Running 5 times /home/user/work/repos/v8/out.gn/6/arm.release/d8...\n[INFO] Maximal variance authorized on 3 average runs: 5%...\n/home/user/work/repos/v8/out.gn/6/arm.release/d8 ./gemm.js\n[INFO] Maximal deviation from arithmetic mean of 3 average runs: 0.07500%\n[INFO] Normalized time: 12.37866666\ngemver\n[INFO] Running 5 times /home/user/work/repos/v8/out.gn/6/arm.release/d8...\n[INFO] Maximal variance authorized on 3 average runs: 5%...\n/home/user/work/repos/v8/out.gn/6/arm.release/d8 ./gemver.js\n[INFO] Maximal deviation from arithmetic mean of 3 average runs: 1.82900%\n[INFO] Normalized time: 0.16400000\ngesummv\n[INFO] Running 5 times /home/user/work/repos/v8/out.gn/6/arm.release/d8...\n[INFO] Maximal variance authorized on 3 average runs: 5%...\n/home/user/work/repos/v8/out.gn/6/arm.release/d8 ./gesummv.js\n [INFO] Maximal deviation from arithmetic mean of 3 average runs: 0%\n[INFO] Normalized time: 0.02600000\nsymm\n[INFO] Running 5 times /home/user/work/repos/v8/out.gn/6/arm.release/d8...\n[INFO] Maximal variance authorized on 3 average runs: 5%...\n/home/user/work/repos/v8/out.gn/6/arm.release/d8 ./symm.js\n[INFO] Maximal deviation from arithmetic mean of 3 average runs: 0.35800%\n[INFO] Normalized time: 18.98200000\nsyr2k\n[INFO] Running 5 times /home/user/work/repos/v8/out.gn/6/arm.release/d8...\n[INFO] Maximal variance authorized on 3 average runs: 5%...\n/home/user/work/repos/v8/out.gn/6/arm.release/d8 ./syr2k.js\n[INFO] Maximal deviation from arithmetic mean of 3 average runs: 0.45200%\n[INFO] Normalized time: 24.75600000\nsyrk\n[INFO] Running 5 times /home/user/work/repos/v8/out.gn/6/arm.release/d8...\n[INFO] Maximal variance authorized on 3 average runs: 5%...\n/home/user/work/repos/v8/out.gn/6/arm.release/d8 ./syrk.js\n[INFO] Maximal deviation from arithmetic mean of 3 average runs: 0.29900%\n[INFO] Normalized time: 11.92233333\ntrmm\n[INFO] Running 5 times /home/user/work/repos/v8/out.gn/6/arm.release/d8...\n[INFO] Maximal variance authorized on 3 average runs: 5%...\n/home/user/work/repos/v8/out.gn/6/arm.release/d8 ./trmm.js\n[INFO] Maximal deviation from arithmetic mean of 3 average runs: 0.08600%\n[INFO] Normalized time: 13.47133333\n2mm\n[INFO] Running 5 times /home/user/work/repos/v8/out.gn/6/arm.release/d8...\n[INFO] Maximal variance authorized on 3 average runs: 5%...\n/home/user/work/repos/v8/out.gn/6/arm.release/d8 ./2mm.js\n[INFO] Maximal deviation from arithmetic mean of 3 average runs: 0.05000%\n[INFO] Normalized time: 25.80400000\n3mm\n[INFO] Running 5 times /home/user/work/repos/v8/out.gn/6/arm.release/d8...\n[INFO] Maximal variance authorized on 3 average runs: 5%...\n/home/user/work/repos/v8/out.gn/6/arm.release/d8 ./3mm.js\n[INFO] Maximal deviation from arithmetic mean of 3 average runs: 0.88500%\n[INFO] Normalized time: 45.09066666\natax\n[INFO] Running 5 times /home/user/work/repos/v8/out.gn/6/arm.release/d8...\n[INFO] Maximal variance authorized on 3 average runs: 5%...\n/home/user/work/repos/v8/out.gn/6/arm.release/d8 ./atax.js\n[INFO] Maximal deviation from arithmetic mean of 3 average runs: 1.56200%\n[INFO] Normalized time: 0.06400000\nbicg\n[INFO] Running 5 times /home/user/work/repos/v8/out.gn/6/arm.release/d8...\n[INFO] Maximal variance authorized on 3 average runs: 5%...\n/home/user/work/repos/v8/out.gn/6/arm.release/d8 ./bicg.js\n[INFO] Maximal deviation from arithmetic mean of 3 average runs: 1.01500%\n[INFO] Normalized time: 0.06566666\ndoitgen\n[INFO] Running 5 times /home/user/work/repos/v8/out.gn/6/arm.release/d8...\n[INFO] Maximal variance authorized on 3 average runs: 5%...\n/home/user/work/repos/v8/out.gn/6/arm.release/d8 ./doitgen.js\n[INFO] Maximal deviation from arithmetic mean of 3 average runs: 0.13400%\n[INFO] Normalized time: 4.20833333\n
# """
with open('log.txt') as f:
    output = f.read()

tests = []

regular_string = r'=== Result of \d+\.(\w+) ===\nAverage compile time: +(\d+\.\d+)\nTotal execution time: +(\d+\.\d+)'
print regular_string
subcases = re.findall(regular_string, output)
print subcases
for i in subcases:
    name1 = i[0] + '-compilation'
    name2 = i[0] + '-execution'
    score1 = utils.myround(i[1])
    score2 = utils.myround(i[2])
    tests.append({'name': name1, 'time': score1})
    tests.append({'name': name2, 'time': score2})
    print(score1 + '     - ' + name1)
    print(score2 + '     - ' + name2)

total = re.search(r'=== Final Result ===\nScore: *(\d+\.\d+)', output)
name = '__total__'
score = utils.myround(total.group(1))
tests.append({'name': name, 'time': score})
print(score + '     - ' + name)



# print len(subcases)
# for i in subcases:
#     p = []
#     data = i[1].splitlines()
#     q = re.findall(r'compile: *(\d+\.\d*)\n[\w\W]+?\nmean: *(\d+\.\d*)', i[1])
#     # print q
#     compilation_time, execution_time = utils.get_result_of_spec2k6(q)
#     # print compilation_time
#     # print execution_time
#     name1 = i[0] + '_compilation_time'
#     name2 = i[0] + '_execution_time'
#     # score = utils.myround(subcase[1], 2)
#     tests.append({'name': name1, 'time': compilation_time})
#     tests.append({'name': name2, 'time': execution_time})
#     print(compilation_time + '     - ' + name1)
#     print(execution_time + '     - ' + name2)
# # Todo: need a __total__ score.
# total = pow(reduce(lambda i, j: i * j, [float(x['time']) for x in tests]), 1.0 / len(tests))
# name = '__total__'
# score = utils.myround(total, 2)
# tests.append({'name': name, 'time': score})
# print(score + '     - ' + name)

