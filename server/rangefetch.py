# remove test scores

import awfy
import time
import datetime


def fetch_test_scores(machine_id, suite_version_id, mode_id,
                      finish_stamp=(0, "UNIX_TIMESTAMP()"),
                      test_stamp=(0, "UNIX_TIMESTAMP()")):
    '''
    query = "DELETE s FROM awfy_score s                                             \
             JOIN awfy_build b ON s.build_id = b.id                                 \
             JOIN awfy_run r ON b.run_id = r.id                                     \
             WHERE s.suite_version_id = %s                                          \
             AND r.finish_stamp >= "+str(finish_stamp[0])+"                         \
             AND r.finish_stamp <= "+str(finish_stamp[1])+"                         \
             AND r.stamp >= "+str(test_stamp[0])+"                                  \
             AND r.stamp <= "+str(test_stamp[1])

    c = awfy.db.cursor()
    c.execute(query, [suite_version_id])
    print (str(c.rowcount) + " rows from awfy_score deleted.")
    '''

    query = "SELECT b.cset, d.score, t.name FROM awfy_breakdown d                \
             JOIN awfy_suite_test t ON d.suite_test_id = t.id                       \
             JOIN awfy_build b ON d.build_id = b.id                                 \
             JOIN awfy_run r ON b.run_id = r.id                                     \
             WHERE r.machine = %s                                                   \
             AND t.suite_version_id = %s                                            \
             AND b.mode_id = %s                                                     \
             AND r.finish_stamp >= " + str(finish_stamp[0]) + "                         \
             AND r.finish_stamp <= " + str(finish_stamp[1]) + "                         \
             AND r.stamp >= " + str(test_stamp[0]) + "                                  \
             AND r.stamp <= " + str(test_stamp[1]) + "                                  \
             ORDER BY t.name, r.stamp"

    c = awfy.db.cursor()
    c.execute(query, [machine_id, suite_version_id, mode_id])
    rows = c.fetchall()

    print(str(c.rowcount) + " rows")

    for row in rows:
        print(str(row[2]) + "-" + str(row[0]) + ": " + str(row[1]));


if __name__ == '__main__':
    machine_id = 2
    suite_version_id = 9

    sdt = datetime.datetime(2015, 8, 19)
    start_stamp = int(time.mktime(sdt.timetuple()))

    edt = datetime.datetime(2015, 11, 21)
    end_stamp = int(time.mktime(edt.timetuple()))

    mode_id = 25

    fetch_test_scores(machine_id, suite_version_id, mode_id, test_stamp=(start_stamp, end_stamp))

# ls | grep -v "metadata" | grep "JerrySunspiderPerf-" | xargs rm
