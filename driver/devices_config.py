ALL_DEVICES = ['v8', 'x64', 'arm', 'glm', 'amd64']
ALL_PROCESSES = ALL_DEVICES + ['apache2', 'query']
LOG_DIR = {
        'v8': 'v8',
        'x64': 'chrome/x64',
        'arm': 'chrome/arm',
        'glm': 'chrome/glm',
        'amd64': 'chrome/amd64',
    }
WORK_DIR = "/home/user/work"
LOG_PATH = "%s/logs" % WORK_DIR
REPOS = {
    "v8": "/home/user/work/repos/v8/v8",
    "jerryscript": "/home/user/work/repos/jerryscript",
    "x64": "/home/user/work/repos/chrome/x64/chromium/src",
    "glm": "/home/user/work/repos/chrome/glm/chromium/src",
    "arm": "/home/user/work/repos/chrome/arm/chromium/src",
    "amd64": "/home/user/work/repos/chrome/amd64/chromium/src",
    "home": "%s/awfy/driver" % WORK_DIR
}
MACHINES = {
    'amd64': 12,
    'glm': 11,
    'x64': 10,
    'arm': 9,
    'v8': 8
}
RELATED = {
    'apache2': "/etc/init.d/apache2 start",
    'query_server.py': "python query_server.py > /home/user/work/logs/query_server_log.txt 2>&1 &"
}
TIMEOUT = 30
ERROR_MSG = "ERROR: You can choose one or two or all of the params from %s, " \
            "or none param means run them all." % ','.join(ALL_DEVICES)
KILL_ERROR_MSG = "ERROR: You can choose one or two or all of the params from %s, " \
            "or none param means run them all." % ','.join(ALL_PROCESSES)
