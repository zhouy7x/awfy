# remove test scores

import awfy
import data
import datetime
import time
import update

def remove_test_scores(machine_id, suite_version_id,
                      finish_stamp = (0,"UNIX_TIMESTAMP()"),
                      test_stamp = (0, "UNIX_TIMESTAMP()")):
    where_list = []
    qargs = []
    if machine_id > 0:
        where_list.append("r.machine = %s")
        qargs.append(machine_id)
    if suite_version_id > 0:
        where_list.append("s.suite_version_id = %s")
        qargs.append(suite_version_id)

    where_clause = " WHERE " + " and ".join(where_list)

    query = "DELETE s FROM awfy_score s                                             \
             JOIN awfy_build b ON s.build_id = b.id                                 \
             JOIN awfy_run r ON b.run_id = r.id" + where_clause + "                 \
             AND r.finish_stamp >= "+str(finish_stamp[0])+"                         \
             AND r.finish_stamp <= "+str(finish_stamp[1])+"                         \
             AND r.stamp >= "+str(test_stamp[0])+"                                  \
             AND r.stamp <= "+str(test_stamp[1])

    print query
    return;
    c = awfy.db.cursor()
    c.execute(query, qargs)
    print (str(c.rowcount) + " rows from awfy_score deleted.")

    query = "DELETE d FROM awfy_breakdown d                                         \
             JOIN awfy_suite_test t ON d.suite_test_id = t.id                       \
             JOIN awfy_build b ON d.build_id = b.id                                 \
             JOIN awfy_run r ON b.run_id = r.id" + where_clause + "                 \
             AND r.finish_stamp >= "+str(finish_stamp[0])+"                         \
             AND r.finish_stamp <= "+str(finish_stamp[1])+"                         \
             AND r.stamp >= "+str(test_stamp[0])+"                                  \
             AND r.stamp <= "+str(test_stamp[1])

    c = awfy.db.cursor()
    c.execute(query, qargs)
    print (str(c.rowcount) + " rows from awfy_breakdown deleted.")

def make_time_stamp(year, month, day):
    sdt = datetime.datetime(year, month, day)
    re = int(time.mktime(sdt.timetuple()))
    return re

def set_meta_data(cx, machine, suite, timestamp):
    prefix = ""
    if suite.visible == 2:
        prefix = "auth-"

    prefix += 'raw-' + suite.name + '-' + str(machine.id)

    metadata = update.load_metadata(prefix)
    metadata['last_stamp'] = timestamp
    update.save_metadata(prefix, metadata)

    for test_name in suite.tests:
        prefix = ""
        if suite.visible == 2:
            prefix = "auth-"

        prefix += 'bk-raw-' + suite.name + '-' + test_name + '-' + str(machine.id)
        metadata = update.load_metadata(prefix)
        metadata['last_stamp'] = timestamp
        update.save_metadata(prefix, metadata)

def set_all_metadata(timestamp):
    cx = data.Context()
    for machine in cx.machines:
        for benchmark in cx.benchmarks:
            machine_data = set_meta_data(cx, machine, benchmark, timestamp)


set_all_metadata(make_time_stamp(2016, 4, 1))
#remove_test_scores(3, 0, finish_stamp=(make_time_stamp(2016,4,5), make_time_stamp(2016,4,10)))

#ls | grep -v "metadata" | grep "JerrySunspiderPerf-" | xargs rm 

#touch -t 201603010000 timestamp
#find . -type f -not -name "*metadata*" -newer timestamp -delete

    

