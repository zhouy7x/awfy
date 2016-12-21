# vim: set ts=4 sw=4 tw=99 et:
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import sys
import time
import util
import os.path
import datetime
import json
import argparse
import csv
import awfy

def time_to_string(timestamp):
  return time.strftime("%Y-%m-%d", time.localtime(timestamp))
def time_to_string_with_hour(timestamp):
  return time.strftime("%Y/%m/%d %H:%M", time.localtime(timestamp))

def string_to_time(time_string):
  return int(time.mktime(time.strptime(time_string, "%Y-%m-%d")))



DEFAULT_START = string_to_time("2016-09-01")
DEFAULT_END = int(time.time())
JSON_PATH = os.path.abspath("../website/crankshart_vs_turbofan.json")
CSV_PATH = "result.csv"
#1: BigCore
#6: ARM-ChromeOS(v8:octane2)
MACHINE_LIST = ['1', '6']
#22: turbofan-x64
#23: default-x64
#24: turbofan-x86
#25: default-x86
#26: turbofan-arm
#27: default-arm
MOD_LIST = ['22', '23', '24', '25', '26', '27']

#6: Octane2 Suite_version
BENCHMARK_LIST = ['6']




def execute_sql(sql):
  c = awfy.db.cursor()
  c.execute(sql)
  return c.fetchall()

def formate_array(array):
  return "(" + ",".join(array) +")"

def query_from_db(start, end):
  query = "SELECT STRAIGHT_JOIN r.id, b.id, r.stamp, r.machine, b.cset, s.score, b.mode_id \
           FROM awfy_run r                                                                \
           JOIN awfy_build b ON r.id = b.run_id                                           \
           JOIN awfy_score s ON s.build_id = b.id                                         \
           WHERE s.suite_version_id = %s                                                  \
           AND r.status > 0                                                             \
           AND r.machine in %s                                                          \
           AND r.finish_stamp >= %s                                                     \
           AND r.finish_stamp <= %s                                                     \
           AND b.mode_id in %s                                                          \
           " % (BENCHMARK_LIST[0], formate_array(MACHINE_LIST), start, end, formate_array(MOD_LIST))
  return execute_sql(query)

def get_two_mod(array):
  arm_score = 0
  default_score = 0
  for i in array:
    if i[6] % 2 == 0:
      arm_score = i
    else:
      default_score = i
  return (default_score, arm_score)

def format_result(data):
  arm_cset_map = {}
  x86_cset_map = {}
  x64_cset_map = {}
  all_map = {
              22: x64_cset_map,
              23: x64_cset_map,
              24: x86_cset_map,
              25: x86_cset_map,
              26: arm_cset_map,
              27: arm_cset_map
  }
  for item in data:
    cset = item[4]
    mod = item[6]
    temp_map = all_map[mod]
    if cset in temp_map:
      temp_map[cset].append(item)
    else:
      temp_map[cset] = [item]

  all_result = {"arm":[],"x86":[],"x64":[]}
  write_data = []

  for key in arm_cset_map:
    temp_result = {}
    arm = get_two_mod(arm_cset_map[key])
    x64 = get_two_mod(x64_cset_map[key])
    x86 = get_two_mod(x86_cset_map[key])
    stamp = x86_cset_map[key][0][2]
    arm_score = "%.2f" % (float(arm[1][5])/float(arm[0][5])*100)
    x64_score = "%.2f" % (float(x64[1][5])/float(x64[0][5])*100)
    x86_score = "%.2f" % (float(x86[1][5])/float(x86[0][5])*100)
    all_result['arm'].append({"score": arm_score,"stamp": stamp, "cset": key})
    all_result['x64'].append({"score": x64_score,"stamp": stamp, "cset": key})
    all_result['x86'].append({"score": x86_score,"stamp": stamp, "cset": key})
    write_data.append([stamp, key, arm_score, x64_score, x86_score])
  for i in all_result:
    temp = all_result[i]
    temp = sorted(temp, key = lambda x:x["stamp"])
    for item in temp:
      item["stamp"] = time_to_string_with_hour(item["stamp"])
    all_result[i] = temp

  write_data = sorted(write_data, key = lambda x:x[0], reverse=True)
  return (all_result, write_data)



def write_csv(file_name, data):
  file = open(file_name, "wb")
  writer = csv.writer(file)
  header = ["time", "cset", "arm_score", "x64_score", "x86_score"]
  writer.writerows([tuple(header)])
  for i in data:
    i[0] = time_to_string(i[0])
    writer.writerows([tuple(i)])
  file.close()

def write_json(file_name, data):
  file = open(file_name, "wb")
  file.write(json.dumps(data))
  file.close()
def print_json(content):
  print json.dumps(content, ensure_ascii=False, indent=2)

def main():
  parser = argparse.ArgumentParser(
    usage='%(prog)s start=[time] end=[time]',
    epilog='Parse crankshaft and turbofan benchmark result with timezone. start default is 2016-09-01, end default is now')
  parser.add_argument(
    '--start', dest='start',
    help='Timezone start')
  parser.add_argument(
    '--end', dest='end',
    help='Timezone end')
  args = parser.parse_args(sys.argv[1:])
  start = args.start if args.start else DEFAULT_START
  end = args.end if args.end else DEFAULT_END
  result = query_from_db(start, end)
  print len(result)
  fresult = format_result(result)
  # print_json(fresult[0])
  write_json(JSON_PATH, fresult[0])
  write_csv(CSV_PATH, fresult[1])



if __name__ == '__main__':
  main()

