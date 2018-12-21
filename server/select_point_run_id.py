#!/usr/bin/python3
# -*-coding:utf-8-*-
"""
@author:lhj
@time:2018/12/21
"""
import json
import awfy


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
    ls = [(1, 22, 1545406994), (1, 24, 1545407181)]
    for i in ls:
        main(*i)
