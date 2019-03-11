#!/usr/bin/python
import replace_all
import json

# FILE = 'run-id-1-22.txt'
#FILE = 'run-id-1-24.txt'
#machine_id = 1

#with open(FILE) as f:
#    data = f.read()
#point_ls = json.loads(data)
#replace_all.delete_all(point_ls, machine_id)

point_ls = [167572]
machine_id = 9
replace_all.delete_all(point_ls, machine_id)
