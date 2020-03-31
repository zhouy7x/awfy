#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author:lhj
@time:2019/01/21
"""
import os
import time

# commit = "34570c6ca91033824e621f1d9733da6612a1fd90"
# commit = "489d2a1888e4d00a780ed7d99d33cc3514082602"
commit = "a62c96a"
if __name__ == '__main__':
    repo_path = "/repos/v8"
    os.chdir(repo_path)
    while True:
        cmd = "git log --oneline"
        data = os.popen(cmd)
        res = data.readline()
        # print(type(res))
        print(res)
        if commit in res:
            print('find current commit.')
            while True:
                print('sleep 1 min.')
                time.sleep(60)
                data = os.popen(cmd)
                res = data.readline()
                if commit not in res:
                    cmd2 = "python /home/user/work/awfy/driver/all_kill.py v8"
                    if not os.system(cmd2):
                        print("kill successed.")
                        break
                    else:
                        print('kill failed.')

            break

        time.sleep(5 * 60)
