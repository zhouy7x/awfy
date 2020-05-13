import re
import sys
import os
import subprocess


def Run(vec, env=os.environ.copy()):
    try:
        o = subprocess.check_output(vec, stderr=subprocess.STDOUT, env=env)
    except subprocess.CalledProcessError as e:
        print 'output was: ' + e.output
        print e
        raise e
    return o


discards = commits = 0

for commit in sys.stdin:
    commit = commit.rstrip()
    output = Run(['git', 'show', '--pretty=short', '--name-only', commit])
    files = skips = 0
    for s in output.splitlines():
        if s == '' or s[0].isspace() or s.startswith('Author:'):
            continue
        files += 1
        if s.find('Source/JavaScriptCore/') == 0:
            # print s
            skips += 1
        skips += 1

    if skips != files:
        print(commit)
    else:
        discards += 1

    commits += 1

print >> sys.stderr, 'commit discard: ' + str(discards) + '/' + str(commits)