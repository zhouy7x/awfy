#!/usr/bin/python3
# -*-coding:utf-8-*-
"""
@author:lhj
@time:2018/12/21
"""
import json
import awfy
import argparse


help = """
Manual to the script of %s, you need:
   - A machine id:

        --machine=1
    
   - A mode id:
   
        --mode=34
        
   - A number of start stamp:
     
        --startstamp=1555082061
        
   - A number of stop stamp:
     
        --stopstamp=1555082062
        
     (default is: none, means till the end.)
   - A command in terminal, you can use simple name for each config("-m" for "--machine", 
     "-o" for "--mode", "-st" for "--startstamp", "-sp" for "--stopstamp"):

        python select_point_run_id.py -m 1 -o 10 -st 1555082061 -sp 1555082062


Examples:

      python select_point_run_id.py -m 1 -o 10 -st 1555082061
      python select_point_run_id.py --machine=1 --mode=10 --startstamp=1555082061 --stopstamp=1555082062

""" % __file__
parser = argparse.ArgumentParser(description='------')
parser.usage = help
parser.add_argument('-m', '--machine', type=int, required=True, help="machine id")
parser.add_argument('-o', '--mode', type=int, default=None, help="mode id, default is None")
parser.add_argument('-st', '--startstamp', type=int, required=True, help="start stamp number")
parser.add_argument('-sp', '--stopstamp', type=int, default=None, help="stop stamp number, default is None")

args = parser.parse_args()
machine = args.machine
mode = args.mode
start_stamp = args.startstamp
stop_stamp = args.stopstamp


def write_to_file(data, a1, a2):
    with open('run-id-%s-%s.txt' % (a1, a2), 'w') as f:
        f.write(json.dumps(data))


def main(machine_id, mode_id, startstamp, stopstamp):

    tmp_ls = []
    query = """
    SELECT STRAIGHT_JOIN *          
              FROM awfy_run r    
                    JOIN awfy_build b ON r.id = b.run_id       
              WHERE  r.machine = %s 
    """
    tmp_ls.append(machine_id)
    if mode_id:
        query += " AND b.mode_id=%s "
        tmp_ls.append(mode_id)
    if startstamp:
        query += " AND r.stamp >= %s "
        tmp_ls.append(startstamp)
    if stopstamp:
        query += " AND r.stamp <= %s "
        tmp_ls.append(stopstamp)
    query += " ORDER BY r.stamp DESC; "
    print query
    c = awfy.db.cursor()
    lines = c.execute(query, tmp_ls)
    print (lines)
    a = c.fetchall()
    # print a
    run_id_ls = []
    for i in a:
        run_id_ls.append(i[0])

    print (run_id_ls)

    write_to_file(run_id_ls, machine_id, mode_id)


if __name__ == '__main__':
    main(machine, mode, start_stamp, stop_stamp)
