# vim: set ts=4 sw=4 tw=99 et:
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import os
import sys
import commands
import subprocess
import signal
import ConfigParser

config = None
TargetOS = None
RepoPath = None
BenchmarkPath = None
DriverPath = None
BuildHost = None
BuildPort = None
RemoteBuild = False
RemoteRsync = False
RemotePull = False
Timeout = 15 * 60
PythonName = None
Includes = None
Excludes = None


def InitConfig(name):
    global config, TargetOS, RepoPath, BenchmarkPath, DriverPath, BuildHost, BuildPort, RemoteBuild, RemoteRsync, \
        RemotePull, Timeout, PythonName, Includes, Excludes

    config = ConfigParser.RawConfigParser()
    if not os.path.isfile(name):
        raise Exception('could not find file: ' + name)
    config.read(name)
    RepoPath = config.get('main', 'repos')
    BenchmarkPath = config.get('main', 'benchmarks')
    DriverPath = config_get_default('main', 'driver', os.getcwd())
    BuildHost = config_get_default('main', 'host', 'localhost')
    BuildPort = config_get_default('main', 'port', 8799)
    try:
        BuildPort = int(BuildPort)
    except ValueError as e:
        raise ValueError("port must be int, not " + BuildPort)

    # remote build related
    RemoteBuild = config_get_default('main', 'remote_build', False)
    if RemoteBuild and RemoteBuild.lower() != 'false':
        RemoteBuild = True
    else:
        RemoteBuild = False
    if RemoteBuild:
        RemoteRsync = config_get_default('build', 'rsync', True)
        if str(RemoteRsync).lower() == 'false':
            RemoteRsync = False
        else:
            RemoteRsync = True
    RemotePull = config_get_default('build', 'pull', True)
    if str(RemotePull).lower() == 'false':
        RemotePull = False
    else:
        RemotePull = True
    #     global RemoteBuildRepoPath, RemoteBuildDriverPath, RemoteBuildHost
    #     RemoteBuildRepoPath = config_get_default('build', 'repos', RepoPath)
    #     RemoteBuildDriverPath = config_get_default('build', 'driver', DriverPath)
    #     RemoteBuildHost = config_get_default('build', 'hostname', 'localhost')

    Timeout = config_get_default('main', 'timeout', str(Timeout))
    # silly hack to allow 30*60 in the config file.
    Timeout = eval(Timeout, {}, {})
    PythonName = config_get_default(name, 'python', sys.executable)
    Includes = config_get_default(name, 'includes', None)
    Excludes = config_get_default(name, 'excludes', None)


class FolderChanger:
    def __init__(self, folder):
        self.old = os.getcwd()
        self.new = folder

    def __enter__(self):
        os.chdir(self.new)

    def __exit__(self, type, value, traceback):
        os.chdir(self.old)


def chdir(folder):
    return FolderChanger(folder)


def get_result_of_spec2k6(ls, digit=2):
    c_times = []
    e_times = []
    if type(ls) not in (list, tuple):
        print ls
        raise Exception('Type error: type of source data must be "list" or "tuple"!')
    for i in ls:
        if type(i) not in (list, tuple):
            print i
            raise Exception('Type error: type of element in source data must be "list" or "tuple"!')
        if len(i) != 2:
            print i
            raise Exception('Data format error: length of element in source data must be 2!')
        c = float(myround(i[0], digit))
        if c:
            c_times.append(c)
        e = float(myround(i[1], digit))
        if e:
            e_times.append(e)

    compilation_time = myround(sum(c_times) / len(c_times), digit)
    execution_time = myround(sum(e_times), digit)

    return compilation_time, execution_time


def myround(num, digit=2):
    try:
        num = float(num)
    except:
        print "Error: must send a number or a string in numeric format!"
        return
    else:
        return str(round(num, digit))


def winRun(vec, env=os.environ.copy()):
    print(">> Executing in " + os.getcwd())
    if vec[0] == 'cmd' and vec[1] == '/c':
        vec = ' '.join(vec)
    else:
        # vec = ' '.join(vec)
        vec = 'powershell /c ' + ' '.join(vec)
    print(vec)
    try:
        o = subprocess.check_output(vec, stderr=subprocess.STDOUT, env=env, shell=True)
    except subprocess.CalledProcessError as e:
        print('output was: ' + e.output)
        print(e)
        raise e
    o = o.decode("utf-8")
    try:
        print(o)
    except:
        print("print exception...")
    return o


def Run(vec, env=os.environ.copy(), enable_log=True):
    print(">> Executing in " + os.getcwd())
    print(' '.join(vec))
    # print("with: " + str(env))
    try:
        o = subprocess.check_output(vec, stderr=subprocess.STDOUT, env=env)
    except subprocess.CalledProcessError as e:
        print 'output was: ' + e.output
        print e
        raise e
    o = o.decode("utf-8")
    try:
        if enable_log:
            print(o)
    except:
        print("print exception...")
    return o


def Shell(string):
    print(string)
    status, output = commands.getstatusoutput(string)
    print(output)
    return output


def config_get_default(section, name, default=None):
    if config.has_option(section, name):
        return config.get(section, name)
    return default


class TimeException(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeException()


class Handler():
    def __init__(self, signum, lam):
        self.signum = signum
        self.lam = lam
        self.old = None

    def __enter__(self):
        self.old = signal.signal(self.signum, self.lam)

    def __exit__(self, type, value, traceback):
        signal.signal(self.signum, self.old)


def RunTimedCheckOutput(args, env=os.environ.copy(), timeout=None, **popenargs):
    if timeout is None:
        timeout = Timeout
    if type(args) == list:
        print('Running: "' + '" "'.join(args) + '" with timeout: ' + str(timeout) + 's')
    elif type(args) == str:
        print('Running: "' + args + '" with timeout: ' + str(timeout) + 's')
    else:
        print('Running: ' + args)
    try:
        if type(args) == list:
            print("list......................")
            p = subprocess.Popen(args, bufsize=-1, env=env, close_fds=True, preexec_fn=os.setsid,
                                 stdout=subprocess.PIPE, **popenargs)

            with Handler(signal.SIGALRM, timeout_handler):
                try:
                    signal.alarm(timeout)
                    output = p.communicate()[0]
                    # if we get an alarm right here, nothing too bad should happen
                    signal.alarm(0)
                    if p.returncode:
                        print "ERROR: returned" + str(p.returncode)
                except TimeException:
                    # make sure it is no longer running
                    # p.kill()
                    os.killpg(p.pid, signal.SIGINT)
                    # in case someone looks at the logs...
                    print ("WARNING: Timed Out 1st.")
                    # try to get any partial output
                    output = p.communicate()[0]
                    print ('output 1st =', output)

                    # try again.
                    p = subprocess.Popen(args, bufsize=-1, shell=True, env=env, close_fds=True,
                                         preexec_fn=os.setsid,
                                         stdout=subprocess.PIPE, **popenargs)
                    try:
                        signal.alarm(timeout)
                        output = p.communicate()[0]
                        # if we get an alarm right here, nothing too bad should happen
                        signal.alarm(0)
                        if p.returncode:
                            print "ERROR: returned" + str(p.returncode)
                    except TimeException:
                        # make sure it is no longer running
                        # p.kill()
                        os.killpg(p.pid, signal.SIGINT)
                        # in case someone looks at the logs...
                        print ("WARNING: Timed Out 2nd.")
                        # try to get any partial output
                        # output = p.communicate()[0]

        else:
            import subprocess32
            p = subprocess32.Popen(args, bufsize=-1, shell=True, env=env, close_fds=True, preexec_fn=os.setsid,
                                   stdout=subprocess32.PIPE, stderr=subprocess32.PIPE, **popenargs)
            # with Handler(signal.SIGALRM, timeout_handler):
            try:
                output = p.communicate(timeout=timeout)[0]
                # if we get an alarm right here, nothing too bad should happen
                if p.returncode:
                    print "ERROR: returned" + str(p.returncode)
            except subprocess32.TimeoutExpired:
                # make sure it is no longer running
                # p.kill()
                os.killpg(p.pid, signal.SIGINT)
                # in case someone looks at the logs...
                print ("WARNING: Timed Out 1st.")
                # try to get any partial output
                output = p.communicate()[0]
                print ('output 1st =', output)

                # try again.
                p = subprocess32.Popen(args, bufsize=-1, shell=True, env=env, close_fds=True, preexec_fn=os.setsid,
                                       stdout=subprocess32.PIPE, stderr=subprocess32.PIPE, **popenargs)
                try:
                    output = p.communicate(timeout=timeout)[0]
                    # if we get an alarm right here, nothing too bad should happen
                    if p.returncode:
                        print "ERROR: returned" + str(p.returncode)
                except subprocess32.TimeoutExpired:
                    # make sure it is no longer running
                    # p.kill()
                    os.killpg(p.pid, signal.SIGINT)
                    # in case someone looks at the logs...
                    print ("WARNING: Timed Out 2nd.")
                    # try to get any partial output
                    # output = p.communicate()[0]

        # print ('output final =',output)
        return output
    except Exception as e:
        print e
        pass


def WinRunTimedCheckOutput(args, env=os.environ.copy(), timeout=None, **popenargs):
    if timeout is None:
        timeout = Timeout
    if type(args) == list:
        print('Running: "' + '" "'.join(args) + '" with timeout: ' + str(timeout) + 's')
        args = ' '.join(args)
    elif type(args) == str:
        print('Running: "' + args + '" with timeout: ' + str(timeout) + 's')
    else:
        print('Running: ' + args)
    try:
        import subprocess32
        p = subprocess32.Popen(args, bufsize=-1, shell=True, env=env,
                               stdout=subprocess32.PIPE, stderr=subprocess32.PIPE, **popenargs)
        # with Handler(signal.SIGALRM, timeout_handler):
        try:
            output = p.communicate(timeout=timeout)[0]
            # if we get an alarm right here, nothing too bad should happen
            if p.returncode:
                print "ERROR: returned" + str(p.returncode)
        except subprocess32.TimeoutExpired:
            # make sure it is no longer running
            # p.kill()
            os.killpg(p.pid, signal.SIGINT)
            # in case someone looks at the logs...
            print ("WARNING: Timed Out 1st.")
            # try to get any partial output
            output = p.communicate()[0]
            print ('output 1st =', output)

            # try again.
            p = subprocess32.Popen(args, bufsize=-1, shell=True, env=env,
                                   stdout=subprocess32.PIPE, stderr=subprocess32.PIPE, **popenargs)
            try:
                output = p.communicate(timeout=timeout)[0]
                # if we get an alarm right here, nothing too bad should happen
                if p.returncode:
                    print "ERROR: returned" + str(p.returncode)
            except subprocess32.TimeoutExpired:
                # make sure it is no longer running
                # p.kill()
                os.killpg(p.pid, signal.SIGINT)
                # in case someone looks at the logs...
                print ("WARNING: Timed Out 2nd.")
                # try to get any partial output
                # output = p.communicate()[0]

        # print ('output final =', output)
        return output
    except Exception as e:
        print e
        pass