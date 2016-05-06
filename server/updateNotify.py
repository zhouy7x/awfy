# vim: set ts=4 sw=4 tw=99 et:
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import sys
import awfy
import data
import time
import util
import os.path
import datetime
import condenser, json
from profiler import Profiler
from builder import Builder

def export(name, j):
    path = os.path.join(awfy.path, name)
    if os.path.exists(path):
        os.remove(path)
    with open(path, 'w') as fp:
        util.json_dump(j, fp)
    print('Exported: ' + name)

def load_metadata(prefix):
    try:
        with open(os.path.join(awfy.path, 'metadata-' + prefix + '.json'), 'r') as fp:
            cache = util.json_load(fp)
    except:
        cache = { 'last_stamp': 0 }

    return cache

def save_metadata(prefix, data):
    with open(os.path.join(awfy.path, 'metadata-' + prefix + '.json'), 'w') as fp:
        util.json_dump(data, fp)

def delete_metadata(prefix, data):
    name = os.path.join(awfy.path, 'metadata-' + prefix + '.json')
    if os.path.exists(name):
        os.remove(name)

def fetch_test_scores(machine_id, suite_id, name,
                      finish_stamp = (0,"UNIX_TIMESTAMP()"),
                      test_stamp = (0, "UNIX_TIMESTAMP()")):
    query = "SELECT STRAIGHT_JOIN r.id, r.stamp, b.cset, s.score, b.mode_id, v.id   \
             FROM awfy_run r                                                        \
             JOIN awfy_build b ON r.id = b.run_id                                   \
             JOIN awfy_breakdown s ON s.build_id = b.id                             \
             JOIN awfy_suite_test t ON s.suite_test_id = t.id                       \
             JOIN awfy_suite_version v ON v.id = t.suite_version_id                 \
             WHERE v.suite_id = %s                                                  \
             AND t.name = %s                                                        \
             AND r.status > 0                                                       \
             AND r.machine = %s                                                     \
             AND r.finish_stamp >= "+str(finish_stamp[0])+"                         \
             AND r.finish_stamp <= "+str(finish_stamp[1])+"                         \
             AND r.stamp >= "+str(test_stamp[0])+"                                  \
             AND r.stamp <= "+str(test_stamp[1])+"                                  \
             ORDER BY r.stamp ASC                                                   \
             "
    c = awfy.db.cursor()
    c.execute(query, [suite_id, name, machine_id])
    return c.fetchall()

def fetch_suite_scores(machine_id, suite_id,
                       finish_stamp = (0,"UNIX_TIMESTAMP()"),
                       test_stamp = (0, "UNIX_TIMESTAMP()")):
    query = "SELECT STRAIGHT_JOIN r.id, r.stamp, b.cset, s.score, b.mode_id, v.id   \
             FROM awfy_run r                                                        \
             JOIN awfy_build b ON r.id = b.run_id                                   \
             JOIN awfy_score s ON s.build_id = b.id                                 \
             JOIN awfy_suite_version v ON v.id = s.suite_version_id                 \
             WHERE v.suite_id = %s                                                  \
             AND r.status > 0                                                       \
             AND r.machine = %s                                                     \
             AND r.finish_stamp >= "+str(finish_stamp[0])+"                         \
             AND r.finish_stamp <= "+str(finish_stamp[1])+"                         \
             AND r.stamp >= "+str(test_stamp[0])+"                                  \
             AND r.stamp <= "+str(test_stamp[1])+"                                  \
             ORDER BY r.stamp ASC                                                   \
             "
    c = awfy.db.cursor()
    c.execute(query, [suite_id, machine_id])
    return c.fetchall()

def delete_cache(prefix):
    os.remove(os.path.join(awfy.path, prefix + '.json'))

def open_cache(suite, prefix):
    try:
        with open(os.path.join(awfy.path, prefix + '.json')) as fp:
            cache = util.json_load(fp)
            return cache['graph']
    except:
        return { 'timelist': [],
                 'lines': [],
                 'direction': suite.direction
               }

def save_cache(prefix, cache):
    j = { 'graph': cache,
          'version': awfy.version
        }
    with open(os.path.join(awfy.path, prefix + '.json'), 'w') as fp:
        util.json_dump(j, fp)

def update_cache(cx, suite, prefix, when, rows):
    # Sort everything into separate modes.
    modes = { }
    for row in rows:
        modeid = int(row[4])
        if not modeid in cx.modemap:
            continue

        if modeid in modes:
            line = modes[modeid]
        else:
            line = []
            modes[modeid] = line

        line.append(row)

    # Build our actual datasets.
    lines = [ ]
    builder = Builder()
    for modeid in modes:
        rows = modes[modeid]
        points = []
        for row in rows:
            score = float(row[3])
            if score:
                cset = row[2]
            else:
                cset = None
            builder.addPoint(points,
                             int(row[1]),
                             cset,
                             None,
                             score,
                             row[5])
        line = { 'modeid': modeid,
                 'data': points
               }
        lines.append(line)
    builder.prune()
    builder.finish(lines)

    # Open the old cache.
    cache = open_cache(suite, prefix)

    # Build a reverse mode mapping for the cache.
    cache_modes = { }
    for i, oldline in enumerate(cache['lines']):
        cache_modes[int(oldline['modeid'])] = oldline

    # Updating fails if there are items before the last time in the cache.
    if len(cache['timelist']) and len(builder.timelist):
        last_time = cache['timelist'][-1]
        i = 0
        while i < len(builder.timelist) and builder.timelist[i] < last_time:
            return False
        if i:
            builder.timelist = builder.timelist[i:]
            for line in lines:
                line['data'] = line['data'][i:]


    # For any of our lines that are not in the cache, prepend null points so
    # the line width matches the existing lines.
    for line in lines:
        if line['modeid'] in cache_modes:
            continue

        data = { 'data': [None] * len(cache['timelist']),
                 'modeid': line['modeid']
               }
        cache['lines'].append(data)
        cache_modes[line['modeid']] = data

    # Now we can merge our data into the existing graph.
    for line in lines:
        oldline = cache_modes[line['modeid']]
        oldline['data'].extend(line['data'])

    # For any lines which are in the cache, but not in our pulled data, extend
    # them to have null datapoints for our timelist.
    for oldline in cache['lines']:
        modeid = int(oldline['modeid'])
        if modeid in modes:
            continue
        oldline['data'].extend([None] * len(builder.timelist))

    # Finally we can extend the cache timelist.
    cache['timelist'].extend(builder.timelist)

    # Sanity check.
    for line in cache['lines']:
        if len(line['data']) != len(cache['timelist']):
            print(str(len(line['data'])) + ' != ' + str(len(cache['timelist'])))
            raise Exception('computed datapoints wrong')

    # Now save the results.
    save_cache(prefix, cache)
    return True

def renew_cache(cx, machine, suite, prefix, when, last_stamp, fetch):
    delete_cache(prefix + '-' + str(when[0]) + '-' + str(when[1]));

    # Delete corresponding condensed graph
    before, after = prefix.split("raw", 1)
    delete_cache(before + "condensed" + after + '-' + str(when[0]) + '-' + str(when[1]));

    dt = datetime.datetime(year=when[0], month=when[1], day=1)
    start_stamp = int(time.mktime(dt.timetuple()))

    next_month = when[1] + 1
    next_year = when[0]
    if next_month == 13:
        next_month = 1
        next_year += 1
    dt = datetime.datetime(year=next_year, month=next_month, day=1)
    stop_stamp = int(time.mktime(dt.timetuple())) - 1
    if last_stamp < stop_stamp:
        stop_stamp = last_stamp

    # Querying all information from this month.
    sys.stdout.write('Querying ' + prefix + '... ')
    sys.stdout.flush()
    with Profiler() as p:
        rows = fetch(machine, test_stamp=(start_stamp,stop_stamp))
        diff = p.time()
    new_rows = len(rows)
    print('found ' + str(new_rows) + ' rows in ' + diff)

    name = prefix + '-' + str(when[0]) + '-' + str(when[1])
    update_cache(cx, suite, name, when, rows) 

def perform_update(cx, machine, suite, prefix, fetch):
    # Fetch the actual data.
    metadata = load_metadata(prefix)
    last_stamp = metadata['last_stamp']
    current_stamp = int(time.time())

    sys.stdout.write('Querying ' + prefix + '... ')
    sys.stdout.flush()
    with Profiler() as p:
        rows = fetch(machine, finish_stamp=(last_stamp+1, current_stamp))
        diff = p.time()
    new_rows = len(rows)
    print('found ' + str(new_rows) + ' new rows in ' + diff)

    # Break everything into months.
    year = 0
    month = 0
    current = []
    months = []
    for row in rows:
        stamp = int(row[1])
        t = time.gmtime(stamp)
        if t.tm_year != year or t.tm_mon != month:
            if year and len(current):
                months.append(((year, month), current))
            current = []
            year = t.tm_year
            month = t.tm_mon

        current.append(row)

    if len(current):
        months.append(((year, month), current))

    for when, data in months:
        name = prefix + '-' + str(when[0]) + '-' + str(when[1])

        sys.stdout.write('Updating cache for ' + name + '...')
        sys.stdout.flush()
        with Profiler() as p:
            if not update_cache(cx, suite, name, when, data):
                renew_cache(cx, machine, suite, prefix, when, last_stamp, fetch)
            diff = p.time()
        print('took ' + diff)

    metadata['last_stamp'] = current_stamp
    save_metadata(prefix, metadata)

    return new_rows
# Done

def update(cx, machine, suite):
    def fetch_aggregate(machine, finish_stamp = (0,"UNIX_TIMESTAMP()"),
                                 test_stamp = (0, "UNIX_TIMESTAMP()")):
        return fetch_suite_scores(machine.id, suite.id, finish_stamp, test_stamp)

    prefix = ""
    if suite.visible == 2:
        prefix = "auth-"

    prefix += 'raw-' + suite.name + '-' + str(machine.id)
    new_rows = perform_update(cx, machine, suite, prefix, fetch_aggregate)

    # This is a little cheeky, but as an optimization we don't bother querying
    # subtests if we didn't find new rows.
    if not new_rows:
        return

    for test_name in suite.tests:
        def fetch_test(machine, finish_stamp = (0,"UNIX_TIMESTAMP()"),
                                test_stamp = (0, "UNIX_TIMESTAMP()")):
            return fetch_test_scores(machine.id, suite.id, test_name, finish_stamp, test_stamp)

        prefix = ""
        if suite.visible == 2:
            prefix = "auth-"

        prefix += 'bk-raw-' + suite.name + '-' + test_name + '-' + str(machine.id)
        perform_update(cx, machine, suite, prefix, fetch_test)

def export_master(cx):
    j = { "version": awfy.version,
          "modes": cx.exportModes(),
          "vendors": cx.exportVendors(),
          "machines": cx.exportMachines(),
          "suites": cx.exportSuites(),
          "suiteversions" : cx.exportSuiteVersions()
        }

    text = "var AWFYMaster = " + json.dumps(j) + ";\n"

    path = os.path.join(awfy.path, 'master.js')
    if os.path.exists(path):
        os.remove(path)
    with open(path, 'w') as fp:
        fp.write(text)

def update_all(cx):
    for machine in cx.machines:
        # Don't try to update machines that we're no longer tracking.
        if machine.active == 2:
            continue

        for benchmark in cx.benchmarks:
            update(cx, machine, benchmark)

def main(argv):
    sys.stdout.write('Computing master properties... ')
    sys.stdout.flush()
    with Profiler() as p:
        cx = data.Context()
        diff = p.time()
    print('took ' + diff)

    update_all(cx)
    condenser.condense_all(cx)
    export_master(cx)

if __name__ == '__main__':
    main(sys.argv[1:])

