# _*_coding=utf-8_*_
import json

try:
    from server import awfy
except:
    import awfy


def get_no_score_run_id_list(run_id_list):
    query = """SELECT STRAIGHT_JOIN *   
	                  FROM awfy_run r            
                          JOIN awfy_build b ON r.id = b.run_id 
                          JOIN awfy_score sc ON sc.build_id = b.id                 

                      WHERE  r.id = %s
                        AND r.machine = %s
                      ORDER BY r.stamp ASC;
    """
    c = awfy.db.cursor()
    for run_id in run_id_list:
        c.execute(query, [run_id, machine_id])
        a = c.fetchall()
        # print(a)
        if not a:
            no_score_run_id_list.append(run_id)
            continue

    return


def get_no_score_run_id_list2(run_id_list):
    query = """SELECT STRAIGHT_JOIN *   
	                  FROM awfy_run r            
                          JOIN awfy_build b ON r.id = b.run_id 
                          JOIN awfy_score sc ON sc.build_id = b.id                 

                      WHERE  r.id = %s
                        AND r.machine = %s
                        AND b.mode_id = %s
                      ORDER BY r.stamp ASC;
    """
    c = awfy.db.cursor()
    for run_id in run_id_list:
        c.execute(query, [run_id] + machine_id.split("-"))
        a = c.fetchall()
        # print(a)
        if not a:
            no_score_run_id_list.append(run_id)
            continue

    return


def delete_all(id_list, machine_id, mode_id=None):
    """
    delete data from mysql according to the id_list.
    :param id_list:
    :return:
    """
    # awfy_breakdown
    query0 = """DELETE FROM s 
                    USING awfy_breakdown s, awfy_run r, awfy_build b
                  WHERE r.id = b.run_id 
                      AND s.build_id = b.id                      
                      AND r.id = %s 
                      AND r.machine = %s 
    """
    # awfy_score
    query1 = """DELETE FROM s 
                  USING awfy_score s, awfy_run r, awfy_build b
                  WHERE r.id = b.run_id 
                  AND s.build_id = b.id                      
                  AND r.id = %s 
                  AND r.machine = %s 
    """

    # awfy_build
    query2 = """DELETE FROM b
                  USING awfy_run r, awfy_build b
                  WHERE r.id = b.run_id 
                  AND r.id = %s 
                  AND r.machine = %s 
    """

    # awfy_run
    query3 = """DELETE FROM r
                  USING awfy_run r
                  WHERE r.id = %s 
                     AND r.machine = %s ;
    """
    if mode_id:
        query0 += " AND b.mode_id = %s "
        query1 += " AND b.mode_id = %s "
        query2 += " AND b.mode_id = %s "
    query0 += " ;"
    query1 += " ;"
    query2 += " ;"
    c = awfy.db.cursor()
    for id in id_list:
        try:
            if mode_id:
                c.execute(query0, [id, machine_id, mode_id])
                c.execute(query1, [id, machine_id, mode_id])
                c.execute(query2, [id, machine_id, mode_id])

            else:
                c.execute(query0, [id, machine_id])
                c.execute(query1, [id, machine_id])
                c.execute(query2, [id, machine_id])
                c.execute(query3, [id, machine_id])

            print('delete point commit, id=%s, machine_id=%s, mode_id=%s' % (str(id), str(machine_id), str(mode_id)))
            awfy.db.commit()
        except Exception as e:
            print(e)
            print('delete point rollback')
            awfy.db.rollback()


def delete_all2(id_list):
    """
    delete data from mysql according to the id_list.
    :param id_list:
    :return:
    """
    # awfy_breakdown
    query0 = """DELETE FROM s 
                    USING awfy_breakdown s, awfy_run r, awfy_build b
                  WHERE r.id = b.run_id 
                      AND s.build_id = b.id                      
                      AND r.id = %s 
                      AND r.machine = %s
                      AND b.mode_id = %s;
    """
    # awfy_score
    query1 = """DELETE FROM s 
                    USING awfy_score s, awfy_run r, awfy_build b
                  WHERE r.id = b.run_id 
                      AND s.build_id = b.id                      
                      AND r.id = %s 
                      AND r.machine = %s
                      AND b.mode_id = %s;
    """

    # awfy_build
    query2 = """DELETE FROM b
                    USING awfy_run r, awfy_build b
                  WHERE r.id = b.run_id 
                      AND r.id = %s  
                      AND r.machine = %s
                      AND b.mode_id = %s;

    """

    # awfy_run
    query3 = """DELETE FROM r
                    USING awfy_run r
                  WHERE r.id = %s 
                      AND r.machine = %s;
    """
    c = awfy.db.cursor()
    for id in id_list:
        try:
            c.execute(query0, [id] + machine_id.split("-"))
            c.execute(query1, [id] + machine_id.split("-"))
            c.execute(query2, [id] + machine_id.split("-"))
            c.execute(query3, [id, machine_id[0]])

            print('commit, id=%s' % str(id))
            awfy.db.commit()
        except:
            print('rollback')
            awfy.db.rollback()


def get_error_equal_id_dict(error_equal_list):
    """

    :param error_equal_list:
    :return:
    """
    i = 0
    while i < len(error_equal_list):
        val_list = []
        val_list.append(error_equal_list[i][0])
        j = i + 1
        while j < len(error_equal_list):
            if error_equal_list[i][2] == error_equal_list[j][2]:
                if error_equal_list[j][0] not in val_list:
                    val_list.append(error_equal_list[j][0])
                # print(t_list)
                j += 1
                continue
            else:
                break
        if not error_equal_id_dict.has_key(error_equal_list[i][2]):
            error_equal_id_dict[error_equal_list[i][2]] = val_list
        else:
            print('has key %s' % error_equal_list[i][2])
        i = j


def get_delete_error_equal_id_list(error_equal_id_dict):
    """

    :param error_equal_id_dict:
    :return:
    """
    query = """SELECT STRAIGHT_JOIN *      
                  FROM awfy_run r               
                    JOIN awfy_build b ON r.id = b.run_id     
                    JOIN awfy_score sc ON sc.build_id = b.id                                         
                  WHERE  r.id = %s 
                  AND  r.machine = %s;
    """
    base_lines = {
        10: 2,
        9: 1,
        8: 3,
        6: 3,
    }
    c = awfy.db.cursor()
    # right_point_id_list = []
    for k, v in error_equal_id_dict.iteritems():
        v_list = []
        for id in v:
            lines = c.execute(query, [id, machine_id])
            if lines == base_lines[machine_id]:
                v.remove(id)
                error_equal_id_list.extend(v)
                break
            else:
                v_list.append([id, lines])
                continue
        else:
            res_list = list(map(lambda x: x[0], sorted(v_list, key=lambda x: x[1], reverse=True)))[1:]
            error_equal_id_list.extend(res_list)


def get_delete_error_equal_id_list2(error_equal_id_dict):
    """

    :param error_equal_id_dict:
    :return:
    """
    query = """SELECT STRAIGHT_JOIN *      
                  FROM awfy_run r               
                    JOIN awfy_build b ON r.id = b.run_id     
                    JOIN awfy_score sc ON sc.build_id = b.id                                         
                  WHERE  r.id = %s
                    AND r.machine = %s
                    AND b.mode_id = %s;
    """
    base_lines = {
        "1-22": 3,
        "1-24": 3,
    }
    c = awfy.db.cursor()
    # right_point_id_list = []
    for k, v in error_equal_id_dict.iteritems():
        v_list = []
        for id in v:
            lines = c.execute(query, [id] + machine_id.split("-"))
            if lines == base_lines[machine_id]:
                v.remove(id)
                error_equal_id_list.extend(v)
                break
            else:
                v_list.append([id, lines])
                continue
        else:
            res_list = list(map(lambda x: x[0], sorted(v_list, key=lambda x: x[1], reverse=True)))[1:]
            error_equal_id_list.extend(res_list)


def select_points(data_list):
    """

    :param data_list:
    :return:
    """
    length = len(data_list)
    i = 0
    while i < length:
        j = i + 1
        while j < length:

            m, n = data_list[i][2], data_list[j][2]

            if m == n:
                if data_list[i] not in error_equal_list:
                    error_equal_list.append(data_list[i])
                if data_list[j] not in error_equal_list:
                    error_equal_list.append(data_list[j])

            j += 1
            #     break
        # i = j
        i += 1


if __name__ == '__main__':
    # machine_id_list = [10]
    machine_id_list = ['1-22', '1-24', 6, 8, 9, 10]

    # TODO    machine_id=9时（arm），需要删除一个错误的breakdown “port ”。

    for machine_id in machine_id_list:
        with open("data/%s.json" % str(machine_id)) as f:
            data = f.read()
            data_list = json.loads(data)
            run_id_list = map(lambda x: x[0], data_list)
            print(len(data_list))

        if isinstance(machine_id, int):
            error_list = []
            error_equal_list = []
            select_points(data_list)
            # print(error_list)
            # error_id_list = map(lambda x: x[0], error_list)   # must delete
            # print('error_id_list', error_id_list)
            # print('error_equal_list',error_equal_list)
            error_equal_id_dict = {}
            get_error_equal_id_dict(error_equal_list)
            # print('error_equal_id_dict',error_equal_id_dict)
            error_equal_id_list = []
            get_delete_error_equal_id_list(error_equal_id_dict)
            # print("machine %s's error_equal_id_list=%s"%(machine_id, str(error_equal_id_list)))                 # must delete

            no_score_run_id_list = []  # must delete
            get_no_score_run_id_list(run_id_list)
            # print("machine %s's no_score_run_id_list=%s"%(machine_id, str(no_score_run_id_list)))                 # must delete

            # get_one_score_run_id_list(run_id_list)
            # print(one_score_run_id_list)
            # print(len(one_score_run_id_list))
            all_delete_point_id_list = []
            for id in error_equal_id_list:
                if id not in all_delete_point_id_list:
                    all_delete_point_id_list.append(id)
            for id in no_score_run_id_list:
                if id not in all_delete_point_id_list:
                    all_delete_point_id_list.append(id)

            print("machine %s's all_delete_point_id=%s, %d" % (
            machine_id, all_delete_point_id_list, len(all_delete_point_id_list)))
            # delete_all(all_delete_point_id_list, machine_id)
            # delete_all([140857])
        else:
            error_list = []
            error_equal_list = []
            select_points(data_list)
            # print(error_list)
            # error_id_list = map(lambda x: x[0], error_list)   # must delete
            # print('error_id_list', error_id_list)
            # print('error_equal_list',error_equal_list)
            error_equal_id_dict = {}
            get_error_equal_id_dict(error_equal_list)
            # print('error_equal_id_dict',error_equal_id_dict)
            error_equal_id_list = []
            get_delete_error_equal_id_list2(error_equal_id_dict)
            # print("machine %s's error_equal_id_list=%s"%(machine_id, str(error_equal_id_list)))                 # must delete

            no_score_run_id_list = []  # must delete
            get_no_score_run_id_list2(run_id_list)
            # print("machine %s's no_score_run_id_list=%s"%(machine_id, str(no_score_run_id_list)))                 # must delete

            # get_one_score_run_id_list(run_id_list)
            # print(one_score_run_id_list)
            # print(len(one_score_run_id_list))
            all_delete_point_id_list = []
            for id in error_equal_id_list:
                if id not in all_delete_point_id_list:
                    all_delete_point_id_list.append(id)
            for id in no_score_run_id_list:
                if id not in all_delete_point_id_list:
                    all_delete_point_id_list.append(id)

            print("machine %s's all_delete_point_id=%s, %d" % (
            machine_id, all_delete_point_id_list, len(all_delete_point_id_list)))
            # delete_all2(all_delete_point_id_list)

            pass
