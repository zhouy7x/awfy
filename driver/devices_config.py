ALL_DEVICES = ['v8', 'x64', 'arm', 'glm', '2500u', '1800x', 'cyan', 'bigcore', '3800x']
ALL_AVAILABLE_DEVICES = ['v8', 'arm', 'x64']
ALL_PROCESSES = ALL_DEVICES + ['apache2', 'query']
REVIEW_DEVICES = ['v8', 'x64']
DEFAULT_DEVICES = ALL_AVAILABLE_DEVICES
LOG_DIR = {
    'v8': 'v8',
    'x64': 'mixture/x64',
    'arm': 'chrome/arm',
    'glm': 'chrome/glm',
    '2500u': 'chrome/2500u',
    '1800x': 'mixture/1800x',
    '3800x': 'mixture/3800x',
    'cyan': 'mixture/cyan',
    'bigcore': 'mixture/bigcore',
}
WORK_DIR = "/home/user/work"
WIN_WORK_DIR = "c:\work"
LOG_PATH = "%s/logs" % WORK_DIR
REPO_PATH = "%s/repos" % WORK_DIR
REPOS = {
    "home": "%s/awfy/driver" % WORK_DIR,
    "v8": "%s/v8/base/v8" % REPO_PATH,
    "v8-jsc": "%s/jsc/base/webkit" % REPO_PATH,
    "jerryscript": "%s/jerryscript" % REPO_PATH,
    "x64-v8": "%s/v8/x64/v8" % REPO_PATH,
    "x64-chrome": "%s/chrome/x64/chromium/src" % REPO_PATH,
    "glm": "%s/chrome/glm/chromium/src" % REPO_PATH,
    "arm": "%s/chrome/arm/chromium/src" % REPO_PATH,
    "2500u": "%s/chrome/2500u/chromium/src" % REPO_PATH,
    "cyan-v8": "%s/v8/cyan/v8" % REPO_PATH,
    "cyan-chrome": "%s/chrome/cyan/chromium/src" % REPO_PATH,
    "bigcore-v8": "%s/v8/bigcore/v8" % REPO_PATH,
    "bigcore-chrome": "%s/chrome/bigcore/chromium/src" % REPO_PATH,
    "1800x-v8": "%s/v8/1800x/v8" % REPO_PATH,
    "1800x-chrome": "%s/chrome/1800x/chromium/src" % REPO_PATH,
    "3800x-v8": "%s/v8/3800x/v8" % REPO_PATH,
    "3800x-chrome": "%s/chrome/3800x/chromium/src" % REPO_PATH,
}
MACHINES = {
    "3800x-v8": 17,
    "3800x-chrome": 17,
    "1800x-v8": 15,
    "1800x-chrome": 15,
    'bigcore-v8': 14,
    'bigcore-chrome': 14,
    'cyan-v8': 13,
    'cyan-chrome': 13,
    'amd64': 12,
    'glm': 11,
    'x64-v8': 18,
    'x64-chrome': 18,
    'arm': 9,
    'v8': 1,
    'v8-jsc': 16,
}
MODES = {
    'cyan-v8': 22,
    'cyan-chrome': 18,
    "1800x-v8": 22,
    "1800x-chrome": 18,
    "3800x-v8": 22,
    "3800x-chrome": 18,
    "x64-v8": 22,
    "x64-chrome": 18,
    "bigcore-v8": 22,
    "bigcore-chrome": 18,
    "v8": 22,
    "v8-jsc": 35,
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
