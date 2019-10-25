ALL_DEVICES = ['v8', 'x64', 'arm', 'glm', 'amd64', 'cyan', 'bigcore']
ALL_PROCESSES = ALL_DEVICES + ['apache2', 'query']
LOG_DIR = {
        'v8': 'v8',
        'x64': 'chrome/x64',
        'arm': 'chrome/arm',
        'glm': 'chrome/glm',
        'amd64': 'chrome/amd64',
        'cyan': 'compressed-pointer',
        'bigcore': 'compressed-pointer/bigcore',
    }
WORK_DIR = "/home/user/work"
LOG_PATH = "%s/logs" % WORK_DIR
REPOS = {
    "home": "%s/awfy/driver" % WORK_DIR,
    "v8": "/home/user/work/repos/v8/v8",
    "jerryscript": "/home/user/work/repos/jerryscript",
    "x64": "/home/user/work/repos/chrome/x64/chromium/src",
    "glm": "/home/user/work/repos/chrome/glm/chromium/src",
    "arm": "/home/user/work/repos/chrome/arm/chromium/src",
    "amd64": "/home/user/work/repos/chrome/amd64/chromium/src",
    "cyan-v8": "/home/user/work/repos/compressed-pointer/v8/v8",
    "cyan-chrome": "/home/user/work/repos/compressed-pointer/x64/chromium/src",
    "bigcore": "/home/user/work/repos/compressed-pointer/v8-2/v8",
}
MACHINES = {
    'bigcore': 14,
    'cyan-v8': 13,
    'cyan-chrome': 13,
    'amd64': 12,
    'glm': 11,
    'x64': 10,
    'arm': 9,
    'v8': 8
}
MODES = {
    'cyan-v8': 22,
    'cyan-chrome': 18,
}
RELATED = {
    'apache2': "/etc/init.d/apache2 start",
    'query_server.py': "python query_server.py > /home/user/work/logs/query_server_log.txt 2>&1 &"
}
TIMEOUT = 30
ERROR_MSG = "ERROR: You can choose one or two or all of the params from %s, " \
            "or none param means run them all." % ','.join(ALL_DEVICES)
KILL_ERROR_MSG = "ERROR: You can choose any of these params from %s, " \
            "or 'all' means run them all." % ','.join(ALL_PROCESSES)
