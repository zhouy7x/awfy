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
REPO_PATH = "%s/repos" % WORK_DIR
REPOS = {
    "home": "%s/awfy/driver" % WORK_DIR,
    "v8": "%s/v8/v8" % REPO_PATH,
    "jerryscript": "%s/jerryscript" % REPO_PATH,
    "x64": "%s/chrome/x64/chromium/src" % REPO_PATH,
    "glm": "%s/chrome/glm/chromium/src" % REPO_PATH,
    "arm": "%s/chrome/arm/chromium/src" % REPO_PATH,
    "amd64": "%s/chrome/amd64/chromium/src" % REPO_PATH,
    "cyan-v8": "%s/compressed-pointer/v8/v8" % REPO_PATH,
    "cyan-chrome": "%s/compressed-pointer/x64/chromium/src" % REPO_PATH,
    "bigcore": "%s/compressed-pointer/v8-2/v8" % REPO_PATH,
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
    'query_server.py': "python query_server.py > %s/query_server_log.txt 2>&1 &" % LOG_PATH
}
TIMEOUT = 30
ERROR_MSG = "ERROR: You can choose one or two or all of the params from %s, " \
            "or none param means run them all." % ','.join(ALL_DEVICES)
KILL_ERROR_MSG = "ERROR: You can choose any of these params from %s, " \
            "or 'all' means run them all." % ','.join(ALL_PROCESSES)
