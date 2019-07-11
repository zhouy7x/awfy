#!/usr/bin/python
import os
import time
from sys import argv

d8_path = argv[1]
start = time.time()
cmd = 'bash run-wasm.sh %s' % d8_path
print(cmd)
os.system(cmd)
print('Running for ',time.time()-start,'s.')
