#!/usr/bin/python
import os


cmd = 'cd driver ; find . -name "dostuff*"'
ret = os.popen(cmd).read().splitlines()
print ret
ret = map(lambda x: x.replace('./', ''), ret)
print ret

replaced = map(lambda x: x.replace('-', '_'), ret)
print replaced

extra = map(lambda x: '-'.join(x.split('-')[:-1])+'-\%s.py', ret)
print extra

extra_replaced = map(lambda x: x.replace('-', '_'), extra)
print extra_replaced

for i in range(len(ret)):
    cmd1 = 'python replace_host.py '+ret[i]+' '+replaced[i]
    print cmd1
    os.system(cmd1)
    cmd2 = 'python replace_host.py '+extra[i]+' '+extra_replaced[i]
    print cmd2
    os.system(cmd2)

for i in range(len(ret)):
    cmd = 'cd driver ; mv '+ret[i]+' '+replaced[i]
    print cmd
    os.system(cmd)

