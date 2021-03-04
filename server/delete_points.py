#!/usr/bin/python
import json
import os
import sys


if __name__ == '__main__':
    TEMP = sys.argv[1]
    if os.path.isdir(TEMP):
        file_list = os.listdir(TEMP)
        file_list.sort()

        print file_list
        for file_name in file_list:
            path = os.path.join(TEMP, file_name)
            cmd = 'python delete_points.py ' + path
            if os.system(cmd):
                break
    else:
        import replace_all
        machine_id = TEMP.split('-')[2]
        mode_id = TEMP.split('-')[3].split('.')[0]
        print TEMP, machine_id, mode_id
        if not mode_id.isdigit():
            mode_id = None
        with open(TEMP) as f:
            data = f.read()
        point_ls = json.loads(data)
        replace_all.delete_all(point_ls, machine_id, mode_id)


