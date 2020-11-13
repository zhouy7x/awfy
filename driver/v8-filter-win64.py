import re
import sys
import os
import subprocess


def Run(vec, env=os.environ.copy()):
    try:
        vec = "ssh ssgs3@ssgs3-test.sh.intel.com \"powershell /c cd d:/src/v8/v8/ ; " + ' '.join(vec) + "\""
        o = subprocess.check_output(vec, stderr=subprocess.STDOUT, env=env, shell=True)
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
        if s == '' or s[0].isspace() or s.startswith('commit ') or s.startswith('Author:'):
            continue
        files += 1
        if s.find('/x87/') >= 0 or s.find('/s390/') >= 0 or s.find('/ppc/') >= 0 or s.find('/mips/') >= 0 or s.find(
                '/mips64/') >= 0 or s.find('/arm64/') >= 0:
            skips += 1

    if skips != files:
        print(commit)
    else:
        discards += 1

    commits += 1

print >> sys.stderr, 'commit discard: ' + str(discards) + '/' + str(commits)
