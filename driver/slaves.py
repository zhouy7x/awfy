import sys
import utils
import re
import pickle
import os
import subprocess
import __main__
from collections import namedtuple

import benchmarks


class Slave(object):
    def __init__(self, name):
        self.name = name
        self.machine = utils.config.get(name, 'machine')

    def prepare(self, engines):
        pass

    def synchronize(self):
        pass

    def benchmark(self, submit, native, modes):
        benchmarks.run(submit, native, modes, utils.Includes, utils.Excludes)


class RemoteSlave(Slave):
    def __init__(self, name):
        super(RemoteSlave, self).__init__(name)
        self.target_os = utils.config_get_default('main', 'target_os', 'linux')
        self.HostName = utils.config_get_default(name, 'hostname', name)
        self.RepoPath = utils.config_get_default(name, 'repos', utils.RepoPath)
        self.BenchmarkPath = utils.config_get_default(name, 'benchmarks', utils.BenchmarkPath)
        self.DriverPath = utils.config_get_default(name, 'driver', utils.DriverPath)
        self.Timeout = utils.config_get_default(name, 'timeout', str(utils.Timeout))
        # calculate timeoutmake multiplication work!
        self.Timeout = eval(self.Timeout, {}, {})
        self.PythonName = utils.config_get_default(name, 'python', utils.PythonName)
        self.Includes = utils.config_get_default(name, 'includes', utils.Includes)
        self.Excludes = utils.config_get_default(name, 'excludes', utils.Excludes)
        self.delayed = None
        self.delayedCommand = None

        #windows remote build related
        self.BuildHost = utils.config_get_default('main', 'build_host', '')
        self.BuildRepoPath = utils.config_get_default('main', 'build_repos', self.RepoPath)
        self.BuildDriverPath = utils.config_get_default('main', 'build_driver', self.DriverPath)

    def prepare(self, engines):
        self.pushRemote(utils.DriverPath + os.path.sep, self.DriverPath)
        self.pushRemote(utils.BenchmarkPath + os.path.sep, self.BenchmarkPath)
        for engine in engines:
            if engine.source == "v8":
                # if build windows binary, must sync from build server to local at first.
                # if self.target_os == 'win64':
                bshell = os.path.join(self.BuildRepoPath, engine.source, engine.shell()).replace('\\', '/')
                shell = os.path.join(utils.RepoPath, engine.source, engine.shell()).replace('\\', '/')
                rshell = os.path.join(self.RepoPath, engine.source, engine.shell()).replace('\\', '/')
                if self.target_os == 'win64':
                    os.system('rm -rf '+os.path.dirname(shell))
                    os.system('mkdir -p '+os.path.dirname(shell))
                    self.pullRemote(bshell, shell, follow=True)
                try:
                    self.runRemote(["mkdir", "-p", os.path.dirname(rshell)])
                except:
                    pass
                self.pushRemote(shell, rshell, follow=True)
                libpaths = engine.libpaths()
                for libp in libpaths:
                    blib = os.path.join(self.BuildRepoPath, engine.source, libp['path']).replace('\\', '/')
                    llib = os.path.join(utils.RepoPath, engine.source, libp['path']).replace('\\', '/')
                    rlib = os.path.join(self.RepoPath, engine.source, libp['path']).replace('\\', '/')
                    if self.target_os == 'win64':
                        os.system('rm -rf ' + llib)
                        self.pullRemote(blib, os.path.dirname(llib), follow=True, excludes=libp['exclude'])
                    if os.path.isfile(llib) or os.path.isdir(llib):
                        try:
                            self.runRemote(["mkdir", "-p", os.path.dirname(rlib)])
                        except:
                            pass
                        self.pushRemote(llib, rlib, follow=True, excludes=libp['exclude'])

            elif engine.source == "chromium/src":
                shell = os.path.join(utils.RepoPath, engine.source, engine.shell())
                rshell = os.path.join(self.RepoPath, engine.source, engine.shell())
                self.runRemote(["rm", "-rf", os.path.dirname(rshell)])
                self.runRemote(["mkdir", "-p", os.path.dirname(rshell)])
                self.pushRemote(shell, rshell, follow=True)
                libpaths = engine.libpaths()
                for libp in libpaths:
                    llib = os.path.join(utils.RepoPath, libp['path'])
                    rlib = os.path.join(self.RepoPath, libp['path'])
                    rlib2 = os.path.abspath(os.path.join(rlib, os.path.pardir))
                    if os.path.isfile(llib) or os.path.isdir(llib):
                        # self.runRemote(["rm", "-rf", os.path.dirname(rlib)])
                        # self.runRemote(["mkdir", "-p", os.path.dirname(rlib)])
                        self.runRemote(["rm", "-rf", rlib])
                        self.pushRemote(llib, rlib2, follow=True, excludes=libp['exclude'])

            elif engine.source == "chromium\src":
                bshell = os.path.join(self.BuildRepoPath, engine.source, engine.slave_shell()).replace('\\', '/')
                shell = os.path.join(utils.RepoPath, engine.source, engine.slave_shell()).replace('\\', '/')
                rshell = os.path.join(self.RepoPath, engine.source, engine.slave_shell()).replace('\\', '/')
                if self.target_os == 'win64':
                    os.system('rm -rf ' + os.path.dirname(shell))
                    os.system('mkdir -p ' + os.path.dirname(shell))
                    self.pullRemote(bshell, shell, follow=True)
                try:
                    self.runRemote(["rm", "-r", "-fo", os.path.dirname(rshell)])
                except:
                    pass
                self.runRemote(["mkdir", "-p", os.path.dirname(rshell)])
                self.pushRemote(shell, rshell, follow=True)
                libpaths = engine.libpaths()
                for libp in libpaths:
                    blib = os.path.join(self.BuildRepoPath, engine.source, libp['path']).replace('\\', '/')
                    llib = os.path.join(utils.RepoPath, engine.source, libp['path']).replace('\\', '/')
                    rlib = os.path.join(self.RepoPath, engine.source, libp['path']).replace('\\', '/')
                    rlib2 = os.path.dirname(rlib)
                    if self.target_os == 'win64':
                        os.system('rm -rf ' + llib)
                        self.pullRemote(blib, os.path.dirname(llib), follow=True, excludes=libp['exclude'])
                    if os.path.isfile(llib) or os.path.isdir(llib):
                        try:
                            self.runRemote(["rm", "-r", "-fo", rlib])
                        except:
                            pass
                        # self.runRemote(["mkdir", "-p", rlib])
                        self.pushRemote(llib, rlib2, follow=True, excludes=libp['exclude'])

            elif engine.source == "webkit":
                shell = os.path.join(utils.RepoPath, engine.source, engine.shell())
                rshell = os.path.join(self.RepoPath, engine.source, engine.shell())
                self.runRemote(["rm", "-rf", os.path.dirname(rshell)])
                self.runRemote(["mkdir", "-p", os.path.dirname(rshell)])
                self.pushRemote(shell, rshell, follow=True)
                libpaths = engine.libpaths()
                for libp in libpaths:
                    llib = os.path.join(utils.RepoPath, engine.source, libp['path'])
                    rlib = os.path.join(self.RepoPath, engine.source, libp['path'])
                    if os.path.isfile(llib) or os.path.isdir(llib):
                        self.runRemote(["rm", "-rf", rlib])
                        self.runRemote(["mkdir", "-p", rlib])
                        self.pushRemote(llib, os.path.dirname(rlib), follow=True, excludes=libp['exclude'])

    def benchmark(self, submit, native, modes):
        state_p = "/tmp/__awfy_" + self.name + "_state.p"
        fd = open(state_p, "wb")
        # dump the global state gathered from the config file
        pickle.dump(utils.config, fd)
        # dump out the per-slave path *as* the global path for the rpc
        pickle.dump(self.RepoPath, fd)
        pickle.dump(self.BenchmarkPath, fd)
        pickle.dump(self.DriverPath, fd)
        pickle.dump(self.Timeout, fd)
        pickle.dump(self.PythonName, fd)
        pickle.dump(self.Includes, fd)
        pickle.dump(self.Excludes, fd)

        # dump out all the arguments
        pickle.dump(submit, fd)
        pickle.dump(native, fd)
        pickle.dump(modes, fd)
        fd.close()

        # send the pickled data over the wire so we can make a call
        self.pushRemote(state_p, os.path.join(self.DriverPath, "state.p"))
        # cd into the driver's directory, then start running the module.
        if self.target_os == "win64":
            cmds = ["cd", self.DriverPath.replace('\\', '/'), ";", self.PythonName, 'slaves.py', os.path.join(self.DriverPath, "state.p").replace('\\', '/')]
        else:
            cmds = ["cd", self.DriverPath, ";", self.PythonName, 'slaves.py', os.path.join(self.DriverPath, "state.p")]
        self.runRemote(cmds, async=True)

    def runRemote(self, cmds, async=False):
        # no matter what, we don't want to start running a new command until the old one is gone.
        self.synchronize()
        if self.target_os == "win64":
            cmds = ['powershell', '/c'] + cmds
        fullcmd = ["ssh", self.HostName, "--"] + cmds
        if async:
            print ("ASYNC: " + " ".join(fullcmd))
            # self.delayed = subprocess.Popen(fullcmd, stderr = subprocess.STDOUT, stdout = subprocess.PIPE)
            self.delayed = subprocess.Popen(fullcmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
            subprocess.Popen(['sed', '-e', 's/^/' + self.name + ': /'], stdin=self.delayed.stdout)
            self.delayedCommand = str(fullcmd)
        else:
            utils.Run(fullcmd, enable_log=False)

    def pushRemote(self, file_loc, file_remote, follow=False, excludes=[]):
        print file_remote
        reger = re.match(r"^(\w):(.*)$", file_remote)
        if reger:
            tmp = reger.groups()
            # print tmp
            file_remote = "/cygdrive/" + tmp[0] + tmp[1]
            file_remote = file_remote.replace('\\', '/')
            print file_remote
        rsync_flags = "-aP"
        # if they asked us to follow symlinks, then add '-L' into the arguments.
        if follow:
            rsync_flags += "L"
        sync_cmd = ["rsync", rsync_flags]
        for exclude in excludes:
            sync_cmd.append("--exclude" + "=" + exclude)

        sync_cmd += [file_loc, self.HostName + ":" + file_remote]
        try:
            utils.Run(sync_cmd, enable_log=False)
        except:
            # run again.
            rsync_flags = "-aP"
            if follow:
                rsync_flags += "L"
            flags = "--delete-excluded"
            sync_cmd = ["rsync", rsync_flags, flags]
            for exclude in excludes:
                sync_cmd.append("--exclude" + "=" + exclude)

            sync_cmd += [file_loc, self.HostName + ":" + file_remote]
            utils.Run(sync_cmd)

    def pullRemote(self, file_remote, file_loc, follow=False, excludes=[]):
        print file_remote
        reger = re.match(r"^(\w):(.*)$", file_remote)
        if reger:
            tmp = reger.groups()
            # print tmp
            file_remote = "/cygdrive/" + tmp[0] + tmp[1]
            file_remote = file_remote.replace('\\', '/')
            print file_remote
        rsync_flags = "-aP"
        # if they asked us to follow symlinks, then add '-L' into the arguments.
        if follow:
            rsync_flags += "L"
        sync_cmd = ["rsync", rsync_flags]
        for exclude in excludes:
            sync_cmd.append("--exclude" + "=" + exclude)

        sync_cmd += [self.BuildHost + ":" + file_remote, file_loc]
        try:
            utils.Run(sync_cmd)
        except:
            pass

    def synchronize(self):
        if self.delayed:
            print("Waiting for: " + self.delayedCommand)
            # retval = self.delayed.wait()
            output, retval = self.delayed.communicate()
            # if retval != 0:
            if self.delayed.returncode != 0:
                # raise Exception(self.delayedCommand + ": failed with exit code" + str(retval))
                raise Exception(self.delayedCommand + ": failed with exit code" + str(self.delayed.returncode))
            self.delayed = None
            self.delayedCommand = None


def init():
    slaves = []
    slaveNames = utils.config_get_default('main', 'slaves', None)
    if slaveNames:
        slaveNames = slaveNames.split(",")
        for name in slaveNames:
            # check ssh status
            # hostname = utils.config_get_default(name, 'hostname', None)
            # if hostname:
            #     utils.check_host_status(hostname)
            remote = utils.config_get_default(name, 'remote', 1)
            if remote:
                slaves.append(RemoteSlave(name))
            else:
                slaves.append(Slave(name))

    # if not slaves:
    # slaves = [Slave("main")]
    return slaves


if __name__ == "__main__":
    Mode = namedtuple('Mode', ['shell', 'args', 'env', 'name', 'cset', 'target_os'])
    state = sys.argv[1]

    fd = open(state, "rb")
    # pull out the global configuration
    utils.config = pickle.load(fd)
    utils.RepoPath = pickle.load(fd)
    utils.BenchmarkPath = pickle.load(fd)
    utils.DriverPath = pickle.load(fd)
    utils.Timeout = pickle.load(fd)
    utils.PythonName = pickle.load(fd)
    utils.Includes = pickle.load(fd)
    utils.Excludes = pickle.load(fd)

    # pull out the pickled arguments
    submit = pickle.load(fd)
    native = pickle.load(fd)
    modes = pickle.load(fd)
    fd.close()

    # call the one true function
    benchmarks.run(submit, native, modes, utils.Includes, utils.Excludes)
