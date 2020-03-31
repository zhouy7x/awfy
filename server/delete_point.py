#!/usr/bin/python
import replace_all
import json
import sys

# FILE = 'run-id-1-22.txt'
FILE = sys.argv[1]
machine_id = FILE.split('-')[2]
print FILE, machine_id

with open(FILE) as f:
    data = f.read()
point_ls = json.loads(data)
replace_all.delete_all(point_ls, machine_id)

# point_ls = [167572]
# machine_id = 9
# replace_all.delete_all(point_ls, machine_id)
