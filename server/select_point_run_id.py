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
   
        -mode=34
        
   - A number of stamp:
     
        -stamp=1555082061
     
   - A command in terminal, you can use simple name for each config("-m" for "--machine", "-o" for "--mode", "-s" for 
     "--stamp"):

        python select_point_run_id.py -m 1 -o 10 -s 1555082061


Examples:

      python select_point_run_id.py -m 1 -o 10 -s 1555082061
      python select_point_run_id.py -machine=1 -mode=10 -stamp=1555082061

""" % __file__
parser = argparse.ArgumentParser(description='------')
parser.usage = help
parser.add_argument('-m', '--machine', type=int, required=True, help="machine id")
parser.add_argument('-o', '--mode', type=int, required=True, help="mode id")
parser.add_argument('-s', '--stamp', type=int, required=True, help="stamp number")

args = parser.parse_args()
machine = args.machine
mode = args.mode
stamp = args.stamp


def write_to_file(data, a1, a2):
    with open('run-id-%s-%s.txt' % (a1, a2), 'w') as f:
        f.write(json.dumps(data))


def main(machine_id, mode_id, start_stamp):
    query = """
    SELECT STRAIGHT_JOIN *          
          FROM awfy_run r    
                JOIN awfy_build b ON r.id = b.run_id       
          WHERE  r.machine = %s 
                and b.mode_id=%s
                and r.stamp >= %s  
          ORDER BY r.stamp DESC;
    """
    c = awfy.db.cursor()
    lines = c.execute(query, [machine_id, mode_id, start_stamp])
    print (lines)
    a = c.fetchall()
    # print a
    run_id_ls = []
    for i in a:
        run_id_ls.append(i[0])

    print (run_id_ls)

    write_to_file(run_id_ls, machine_id, mode_id)


if __name__ == '__main__':
    main(machine, mode, stamp)
