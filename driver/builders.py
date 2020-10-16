# vim: set ts=4 sw=4 tw=99 et:
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import sys
import time
import utils
import puller
import platform
import subprocess
import traceback
from devices_config import WORK_DIR, WIN_WORK_DIR
from utils import Run, winRun

import synctroubles

reload(sys)
sys.setdefaultencoding('utf8')


class Engine(object):
    def __init__(self):
        self.cpu = utils.config.get('main', 'cpu')

    def getPuller(self):
        if self.puller == 'svn':
            scm = puller.SVN
        elif self.puller == 'hg':
            scm = puller.HG
        elif self.puller == 'git':
            scm = puller.GIT
        return scm

    def updateAndBuild(self, update=True, forceRebuild=False, rev=None):
        with utils.FolderChanger(os.path.join(utils.RepoPath, self.source)):
            self._updateAndBuild(update, forceRebuild, rev=rev)

    def _updateAndBuild(self, update, forceRebuild, rev=None):
        scm = self.getPuller()
        shell = self.shell()

        if not os.path.isfile(shell):
            forceRebuild = True

        if update:
            self.updated = scm.Update(rev)
        else:
            self.updated = False
        if forceRebuild or self.updated:
            try:
                os.unlink(shell)
            except:
                pass

            beginTime = time.time()
            self.build()
            if not os.path.isfile(shell):
                if self.reconf():
                    self.build()

            self.updated = True
            secs = int(time.time() - beginTime)
            print('\n++++++++ Build-Time: ' + str(secs / 3600) + "h:" + str(secs % 3600 / 60) + "m:" + str(
                secs % 60) + "s ++++++++\n\n")

        if not os.path.isfile(shell):
            print(shell)
            raise Exception('could not find shell')

    def reconf(self):
        return False

    def env(self):
        return None

    def libpaths(self):
        return []


class Nitro(Engine):
    def __init__(self):
        super(Nitro, self).__init__()
        self.puller = 'svn'
        self.source = utils.config.get('jsc', 'source')
        if utils.config.has_option('jsc', 'conf'):
            self.extra = utils.config.get('jsc', 'conf').split(' ')
        else:
            self.extra = []
        self.args = None
        self.important = False  # WebKit changes too frequently, we'd need to detect JSC changes.
        self.modes = [
            {
                'mode': 'jsc',
                'args': None
            }
        ]

    def env(self):
        env = os.environ.copy()
        env['DYLD_FRAMEWORK_PATH'] = os.path.abspath(os.path.join('WebKitBuild', 'Release'))
        return env

    def build(self):
        # Hack 1: Remove reporting errors for warnings that currently are present.
        Run(["sed", "-i.bac", "s/GCC_TREAT_WARNINGS_AS_ERRORS = YES;/GCC_TREAT_WARNINGS_AS_ERRORS=NO;/",
             "Source/JavaScriptCore/Configurations/Base.xcconfig"])
        Run(["sed", "-i.bac", "s/GCC_TREAT_WARNINGS_AS_ERRORS = YES;/GCC_TREAT_WARNINGS_AS_ERRORS=NO;/",
             "Source/bmalloc/Configurations/Base.xcconfig"])
        Run(["sed", "-i.bac", "s/GCC_TREAT_WARNINGS_AS_ERRORS = YES;/GCC_TREAT_WARNINGS_AS_ERRORS=NO;/",
             "Source/WTF/Configurations/Base.xcconfig"])
        Run(["sed", "-i.bac", "s/std::numeric_limits<unsigned char>::max()/255/", "Source/bmalloc/bmalloc/Line.h"])
        Run(["sed", "-i.bac", "s/std::numeric_limits<unsigned char>::max()/255/", "Source/bmalloc/bmalloc/Page.h"])

        with utils.FolderChanger(os.path.join('Tools', 'Scripts')):
            # Hack 2: This check fails currently. Disable checking to still have a build.
            os.rename("check-for-weak-vtables-and-externals", "check-for-weak-vtables-and-externals2");

            if self.cpu == 'x86':
                args = ['/usr/bin/perl', 'build-jsc', '--32-bit']
            else:
                args = ['/usr/bin/perl', 'build-jsc']
            args.extend(self.extra)
            Run(args)

            os.rename("check-for-weak-vtables-and-externals2", "check-for-weak-vtables-and-externals");

        Run(["svn", "revert", "Source/JavaScriptCore/Configurations/Base.xcconfig"])
        Run(["svn", "revert", "Source/bmalloc/Configurations/Base.xcconfig"])
        Run(["svn", "revert", "Source/WTF/Configurations/Base.xcconfig"])
        Run(["svn", "revert", "Source/bmalloc/bmalloc/Line.h"])
        Run(["svn", "revert", "Source/bmalloc/bmalloc/Page.h"])

    def shell(self):
        return os.path.join('WebKitBuild', 'Release', 'jsc')


class V8(Engine):
    def __init__(self):
        super(V8, self).__init__()
        self.puller = 'git'
        self.source = utils.config.get('v8', 'source')
        self.cxx = utils.config_get_default('v8', 'cxx', None)
        self.cc = utils.config_get_default('v8', 'cc', None)
        self.cpp = utils.config_get_default('v8', 'cpp', None)
        self.link = utils.config_get_default('v8', 'link', None)
        self.cxx_host = utils.config_get_default('v8', 'cxx_host', None)
        self.cc_host = utils.config_get_default('v8', 'cc_host', None)
        self.cpp_host = utils.config_get_default('v8', 'cpp_host', None)
        self.link_host = utils.config_get_default('v8', 'link_host', None)
        self.ar = utils.config_get_default('v8', 'ar', None)

        self.args = ['--expose-gc']
        self.important = True
        self.hardfp = (utils.config.has_option('main', 'flags')) and \
                      ("hardfp" in utils.config.get('main', 'flags'))

        slaves = utils.config.get('main', 'slaves')
        self.slaveMachine = utils.config.get(slaves, 'machine')

    def build(self):
        env = os.environ.copy()
        if self.cxx is not None:
            env['CXX'] = self.cxx
        if self.cc is not None:
            env['CC'] = self.cc
        if self.cpp is not None:
            env['CPP'] = self.cpp
        if self.link is not None:
            env['LINK'] = self.link
        if self.cxx_host is not None:
            env['CXX_host'] = self.cxx_host
        if self.cc_host is not None:
            env['CC_host'] = self.cc_host
        if self.cpp_host is not None:
            env['CPP_host'] = self.cpp_host
        if self.link_host is not None:
            env['LINK_host'] = self.link_host
        if self.ar is not None:
            env['AR'] = self.ar

        Run(['git', 'log', '-1', '--pretty=short'])

        gn_shell = os.path.join(utils.DriverPath, 'gn-cmd.sh')
        Run([gn_shell, self.slaveMachine, self.cpu], env)

    def shell(self):
        return os.path.join('out.gn', self.slaveMachine, self.cpu + ".release", 'd8')

    def libpaths(self):
        otgt = self.slaveMachine + "/" + self.cpu + ".release"
        return [{"path": os.path.join('out.gn', otgt, 'natives_blob.bin'), "exclude": []},
                {"path": os.path.join('out.gn', otgt, 'snapshot_blob.bin'), "exclude": []},
                {"path": os.path.join('out.gn', otgt, 'icudtl.dat'), "exclude": []}
                ]


class V8Win64(Engine):
    def __init__(self):
        super(V8Win64, self).__init__()
        self.puller = 'git'
        self.source = utils.config.get('v8-win64', 'source')
        self.cxx = utils.config_get_default('v8-win64', 'cxx', None)
        self.cc = utils.config_get_default('v8-win64', 'cc', None)
        self.cpp = utils.config_get_default('v8-win64', 'cpp', None)
        self.link = utils.config_get_default('v8-win64', 'link', None)
        self.cxx_host = utils.config_get_default('v8-win64', 'cxx_host', None)
        self.cc_host = utils.config_get_default('v8-win64', 'cc_host', None)
        self.cpp_host = utils.config_get_default('v8-win64', 'cpp_host', None)
        self.link_host = utils.config_get_default('v8-win64', 'link_host', None)
        self.ar = utils.config_get_default('v8-win64', 'ar', None)

        self.args = ['--expose-gc']
        self.important = True
        self.hardfp = (utils.config.has_option('main', 'flags')) and \
                      ("hardfp" in utils.config.get('main', 'flags'))

        slaves = utils.config.get('main', 'slaves')
        self.slaveMachine = utils.config.get(slaves, 'machine')
        self.sourcePath = os.path.join(utils.config_get_default('main', 'build_repos'), self.source)

    def updateAndBuild(self, update=True, forceRebuild=False, rev=None):
        with utils.FolderChanger(self.sourcePath):
            self._updateAndBuild(update, forceRebuild, rev=rev)

    def build(self):
        env = os.environ.copy()
        if self.cxx is not None:
            env['CXX'] = self.cxx
        if self.cc is not None:
            env['CC'] = self.cc
        if self.cpp is not None:
            env['CPP'] = self.cpp
        if self.link is not None:
            env['LINK'] = self.link
        if self.cxx_host is not None:
            env['CXX_host'] = self.cxx_host
        if self.cc_host is not None:
            env['CC_host'] = self.cc_host
        if self.cpp_host is not None:
            env['CPP_host'] = self.cpp_host
        if self.link_host is not None:
            env['LINK_host'] = self.link_host
        if self.ar is not None:
            env['AR'] = self.ar

        winRun(['git', 'log', '-1', '--pretty=short'], env)

        in_argns_name = "v8-" + self.cpu + ".gn"
        in_argns = os.path.join(WIN_WORK_DIR, 'awfy', 'gn_file', in_argns_name)
        out_argns = os.path.join(self.sourcePath, 'out.gn', self.slaveMachine, self.cpu, 'args.gn')
        if not os.path.isdir(os.path.join(self.sourcePath, 'out.gn', self.slaveMachine, self.cpu)):
            winRun(["mkdir", "-p", os.path.join(self.sourcePath, 'out.gn', self.slaveMachine, self.cpu)])
        winRun(['cp', in_argns, out_argns], env)

        out_dir = os.path.join(self.sourcePath, "out.gn", self.slaveMachine, self.cpu+".release")
        winRun(['gn', 'gen', out_dir], env)
        winRun(['ninja', '-C', out_dir, 'd8', '-j40'])

    def shell(self):
        return os.path.join('out.gn', self.slaveMachine, self.cpu + ".release", 'd8.exe')

    def slave_shell(self):
        return os.path.join('out.gn', self.slaveMachine, self.cpu + ".release", 'd8.exe')

    def libpaths(self):
        otgt = self.slaveMachine + "/" + self.cpu + ".release"
        return [{"path": os.path.join('out.gn', otgt)+'/', "exclude": ['gen', 'obj']},
                ]


class V8_patch(Engine):
    def __init__(self):
        super(V8_patch, self).__init__()
        self.puller = 'git'
        self.source = utils.config.get('v8-patch', 'source')
        self.cxx = utils.config_get_default('v8-patch', 'cxx', None)
        self.cc = utils.config_get_default('v8-patch', 'cc', None)
        self.cpp = utils.config_get_default('v8-patch', 'cpp', None)
        self.link = utils.config_get_default('v8-patch', 'link', None)
        self.cxx_host = utils.config_get_default('v8-patch', 'cxx_host', None)
        self.cc_host = utils.config_get_default('v8-patch', 'cc_host', None)
        self.cpp_host = utils.config_get_default('v8-patch', 'cpp_host', None)
        self.link_host = utils.config_get_default('v8-patch', 'link_host', None)
        self.ar = utils.config_get_default('v8-patch', 'ar', None)

        self.args = ['--expose-gc']
        self.patch = 'patch'
        self.important = True
        self.hardfp = (utils.config.has_option('main', 'flags')) and \
                      ("hardfp" in utils.config.get('main', 'flags'))

        slaves = utils.config.get('main', 'slaves')
        self.slaveMachine = utils.config.get(slaves, 'machine')

    def build(self):
        env = os.environ.copy()
        if self.cxx is not None:
            env['CXX'] = self.cxx
        if self.cc is not None:
            env['CC'] = self.cc
        if self.cpp is not None:
            env['CPP'] = self.cpp
        if self.link is not None:
            env['LINK'] = self.link
        if self.cxx_host is not None:
            env['CXX_host'] = self.cxx_host
        if self.cc_host is not None:
            env['CC_host'] = self.cc_host
        if self.cpp_host is not None:
            env['CPP_host'] = self.cpp_host
        if self.link_host is not None:
            env['LINK_host'] = self.link_host
        if self.ar is not None:
            env['AR'] = self.ar

        Run(['git', 'log', '-1', '--pretty=short'])
        print env
        # add patch.
        # with utils.FolderChanger(os.path.join(utils.RepoPath, self.source)):
        # Run(['patch', '-p', '1', '-i', '/repos/enable-compressed-pointer.patch'], env)

        gn_shell = os.path.join(utils.DriverPath, 'gn-cmd.sh')
        Run([gn_shell, self.slaveMachine, self.cpu, self.patch], env)

    def shell(self):
        return os.path.join('out.gn', self.slaveMachine, self.cpu + ".patch", 'd8')

    def libpaths(self):
        otgt = self.slaveMachine + "/" + self.cpu + ".patch"
        return [{"path": os.path.join('out.gn', otgt, 'natives_blob.bin'), "exclude": []},
                {"path": os.path.join('out.gn', otgt, 'snapshot_blob.bin'), "exclude": []},
                {"path": os.path.join('out.gn', otgt, 'icudtl.dat'), "exclude": []}
                ]


class V8_gyp(Engine):
    def __init__(self):
        super(V8_gyp, self).__init__()
        self.puller = 'git'
        self.source = utils.config.get('v8', 'source')
        self.cxx = utils.config_get_default('v8', 'cxx', None)
        self.cc = utils.config_get_default('v8', 'cc', None)
        self.cpp = utils.config_get_default('v8', 'cpp', None)
        self.link = utils.config_get_default('v8', 'link', None)
        self.cxx_host = utils.config_get_default('v8', 'cxx_host', None)
        self.cc_host = utils.config_get_default('v8', 'cc_host', None)
        self.cpp_host = utils.config_get_default('v8', 'cpp_host', None)
        self.link_host = utils.config_get_default('v8', 'link_host', None)
        self.ar = utils.config_get_default('v8', 'ar', None)

        self.args = ['--expose-gc']
        self.important = True
        self.hardfp = (utils.config.has_option('main', 'flags')) and \
                      ("hardfp" in utils.config.get('main', 'flags'))

    def build(self):
        env = os.environ.copy()
        if self.cxx is not None:
            env['CXX'] = self.cxx
        if self.cc is not None:
            env['CC'] = self.cc
        if self.cpp is not None:
            env['CPP'] = self.cpp
        if self.link is not None:
            env['LINK'] = self.link
        if self.cxx_host is not None:
            env['CXX_host'] = self.cxx_host
        if self.cc_host is not None:
            env['CC_host'] = self.cc_host
        if self.cpp_host is not None:
            env['CPP_host'] = self.cpp_host
        if self.link_host is not None:
            env['LINK_host'] = self.link_host
        if self.ar is not None:
            env['AR'] = self.ar

        if self.cpu != 'arm':
            env["GYP_DEFINES"] = "clang=1"

        # *** MOVED TO schedule-run.sh ***
        #
        # with utils.FolderChanger('../'):
        #     syncAgain = True
        #     while (syncAgain):
        #         syncAgain = False
        #         try:
        #             Run(['gclient', 'sync', '-j8'], env)
        #         except subprocess.CalledProcessError as e:
        #             if synctroubles.fetchGsFileByHttp(e.output, ''):
        #                 syncAgain = True
        #             else:
        #                 raise e

        Run(['git', 'log', '-1'])

        if self.cpu == 'x64':
            Run(['make', 'x64.release', 'werror=no', '-j30'], env)
        elif self.cpu == 'arm':
            make_cmd = ['make', 'werror=no', '-j30', 'arm.release',
                        'armv7=true',
                        'armfloatabi=hard',
                        'disassembler=on',
                        'CC=\"arm-linux-gnueabihf-gcc-4.8\"',
                        'AR=\"arm-linux-gnueabihf-ar\"',
                        'CXX=\"arm-linux-gnueabihf-g++-4.8\"',
                        'LINK=\"arm-linux-gnueabihf-g++-4.8\"']
            if self.hardfp:
                make_cmd.append('hardfp=on')
            Run(make_cmd, env)
        elif self.cpu == 'x86':
            Run(['make', 'ia32.release', 'werror=no', '-j30'], env)

    def shell(self):
        if self.cpu == 'x64':
            return os.path.join('out', 'x64.release', 'd8')
        elif self.cpu == 'arm':
            return os.path.join('out', 'arm.release', 'd8')
        elif self.cpu == 'x86':
            return os.path.join('out', 'ia32.release', 'd8')

    def libpaths(self):
        otgt = ''
        if self.cpu == 'x64':
            otgt = 'x64.release'
        elif self.cpu == 'arm':
            otgt = 'arm.release'
        elif self.cpu == 'x86':
            otgt = 'ia32.release'

        return [{"path": os.path.join('out', otgt, 'natives_blob.bin'), "exclude": []},
                {"path": os.path.join('out', otgt, 'snapshot_blob.bin'), "exclude": []},
                {"path": os.path.join('out', otgt, 'icudtl.dat'), "exclude": []}
                ]


class ContentShell(Engine):
    def __init__(self):
        super(ContentShell, self).__init__()
        self.puller = 'git'
        self.source = utils.config.get('contentshell', 'source')

        self.args = []
        self.important = True

        if self.cpu == 'x64':
            cpu_mode = '-x64'
        elif self.cpu == 'x86':
            cpu_mode = '-x86'
        elif self.cpu == 'arm':
            cpu_mode = '-arm'

        self.modes = [{
            'mode': 'ContentShell' + cpu_mode,
            'args': None
        }]

    #        self.modes = [{'mode': 'ContentShell-temp-test', 'args': None}]

    def build(self):
        env = os.environ.copy()

        env["GYP_CHROMIUM_NO_ACTION"] = "0"

        if self.cpu == 'x86':
            env["GYP_DEFINES"] = "target_arch=ia32"
        elif self.cpu == 'x64':
            env["GYP_DEFINES"] = "target_arch=x64"
        elif self.cpu == 'arm':
            env["GYP_DEFINES"] = "target_arch=arm"
            env["GYP_CROSSCOMPILE"] = "1"

        with utils.FolderChanger('../'):
            syncAgain = True
            # sourcePath = os.path.join(utils.RepoPath, self.source)
            while (syncAgain):
                syncAgain = False
                try:
                    Run(['gclient', 'sync', '-j8'], env)
                except subprocess.CalledProcessError as e:
                    if synctroubles.fetchGsFileByHttp(e.output, ''):
                        syncAgain = True
                    else:
                        raise e

        Run(['ninja', '-C', 'out/Release', 'content_shell'], env)

    def shell(self):
        return os.path.join('out', 'Release', 'content_shell')

    def libpaths(self):
        p = os.path.join('out', 'Release/')
        return [{'path': p, 'exclude': ['obj', 'gen']}]


class JerryScript(Engine):
    def __init__(self):
        super(JerryScript, self).__init__()
        self.puller = 'git'
        self.source = utils.config.get('jerryscript', 'source')

        self.args = []
        self.important = True

        if self.cpu == 'x64':
            cpu_mode = '-x64'
        elif self.cpu == 'x86':
            cpu_mode = '-x86'
        elif self.cpu == 'arm':
            cpu_mode = '-arm'

        self.modes = [{
            'mode': 'JerryScript' + cpu_mode,
            'args': None
        }]

    def build(self):
        env = os.environ.copy()

        Run(['make', 'release.linux'], env)

    def shell(self):
        return os.path.join('build', 'bin', 'release.linux', 'jerry')


# add Headless Engine
class Headless(Engine):
    def __init__(self):
        super(Headless, self).__init__()
        self.puller = 'git'
        self.source = utils.config.get('headless', 'source')
        self.args = []
        self.important = True

        if self.cpu == 'x64':
            cpu_mode = '-x64'
        elif self.cpu == 'x86':
            cpu_mode = '-x86'
        elif self.cpu == 'arm':
            cpu_mode = '-arm'
        elif self.cpu == 'amd64':
            cpu_mode = '-amd64'

        self.modes = [{'mode': 'headless' + cpu_mode, 'args': None}]

    def build(self):
        env = os.environ.copy()
        env["NO_AUTH_BOTO_CONFIG"] = "/repos/boto.cfg"
        # env["GYP_CHROMIUM_NO_ACTION"] = "0"

        # if self.cpu == 'x86':
        #     env["GYP_DEFINES"] = "target_arch=ia32"
        # elif self.cpu == 'x64':
        #     env["GYP_DEFINES"] = "target_arch=x64"
        # elif self.cpu == 'arm':
        #     env["GYP_DEFINES"] = "target_arch=arm arm_float_abi=hard component=shared_library linux_use_gold_flags=1"
        #     env["GYP_CROSSCOMPILE"] = "1"
        # add build command code here
        with utils.FolderChanger('./'):
            syncAgain = True
            sourcePath = os.path.join(utils.RepoPath, self.source)
            in_argns_name = self.cpu + ".gn"
            # in_argns = os.path.join(utils.RepoPath, 'gn_file', in_argns_name)
            in_argns = os.path.join(WORK_DIR, 'awfy', 'gn_file', in_argns_name)
            out_argns = os.path.join(utils.RepoPath, self.source, 'out', self.cpu, 'args.gn')
            if not os.path.isdir(os.path.join(utils.RepoPath, self.source, 'out', self.cpu)):
                os.mkdir(os.path.join(utils.RepoPath, self.source, 'out', self.cpu))
            while (syncAgain):
                syncAgain = False
                try:
                    print 'env=%s' % env
                    Run(['cp', in_argns, out_argns])
                    Run(['gclient', 'sync', '-D', '-j25', '-f'], env)
                    # if self.cpu == 'arm':
                    # Run(['sed', '-i',
                    #     '/use_gold &&/{s/target_cpu == "x86"/target_cpu == "x86" || target_cpu == "arm"/g}',
                    #     os.path.join(sourcePath, "third_party", "swiftshader", "BUILD.gn")], env)
                    # Run(['sed', '-i',
                    #      '/use_lld && target_cpu == "x86"/{s/target_cpu == "x86"/(target_cpu == "x86" || target_cpu == "arm")/g}',
                    #      os.path.join(sourcePath, "third_party", "ffmpeg", "BUILD.gn")], env)
                    Run(['gn', 'gen', os.path.join(sourcePath, 'out', self.cpu)], env)
                    # Run(['/home/user/work/awfy/driver/patch_stddef.sh', os.path.join(sourcePath, "third_party", "angle", "src", "common", "platform.h")], env)
                except subprocess.CalledProcessError as e:
                    if synctroubles.fetchGsFileByHttp(e.output, ''):
                        syncAgain = True
                    else:
                        raise e
        try:
            Run(['ninja', '-C', os.path.join(sourcePath, 'out', self.cpu), 'chrome', '-j40'], env)
        except subprocess.CalledProcessError as e:
            print "Dirty build failed!"
            # add build command code here
            with utils.FolderChanger('./'):
                syncAgain = True
                sourcePath = os.path.join(utils.RepoPath, self.source)
                in_argns_name = self.cpu + ".gn"
                # in_argns = os.path.join(utils.RepoPath, 'gn_file', in_argns_name)
                in_argns = os.path.join(WORK_DIR, 'awfy', 'gn_file', in_argns_name)
                out_argns = os.path.join(utils.RepoPath, self.source, 'out', self.cpu, 'args.gn')
                while (syncAgain):
                    syncAgain = False
                    try:
                        # if self.cpu == 'arm':
                        #     in_cddl = os.path.join(utils.RepoPath, 'cddl')
                        #     out_cddl = os.path.join(utils.RepoPath, self.source, 'out', self.cpu)
                        #     Run(['cp', in_cddl, out_cddl])
                        # else:
                        # add 3 steps:
                        # 1. perl -pi -e "s/sudo //g" ./build/install-build-deps.sh
                        Run(['perl', '-pi', '-e', '"s/sudo //g"',
                             os.path.join(sourcePath, 'build', 'install-build-deps.sh')])
                        # 2. run build/install-build-deps.sh and reset
                        Run(['/bin/bash', os.path.join(sourcePath, 'build', 'install-build-deps.sh')])
                        Run(['git', 'checkout', os.path.join(sourcePath, 'build', 'install-build-deps.sh')])
                        # 3. ./build/linux/sysroot_scripts/install-sysroot.py --arch=arm
                        Run([os.path.join(sourcePath, 'build/linux/sysroot_scripts/install-sysroot.py'), '--arch=arm'])

                        Run(['rm', os.path.join(sourcePath, 'out', self.cpu), '-rf'])
                        Run(['mkdir', os.path.join(sourcePath, 'out', self.cpu)])
                        Run(['cp', in_argns, out_argns])
                        print 'env=%s' % env
                        Run(['gclient', 'sync', '-D', '-j25', '-f'], env)
                        # if self.cpu == 'arm':
                        # Run(['sed', '-i',
                        #     '/use_gold &&/{s/target_cpu == "x86"/target_cpu == "x86" || target_cpu == "arm"/g}',
                        #     os.path.join(sourcePath, "third_party", "swiftshader", "BUILD.gn")], env)
                        # Run(['sed', '-i',
                        #      '/use_lld && target_cpu == "x86"/{s/target_cpu == "x86"/(target_cpu == "x86" || target_cpu == "arm")/g}',
                        #      os.path.join(sourcePath, "third_party", "ffmpeg", "BUILD.gn")], env)
                        Run(['gn', 'gen', os.path.join(sourcePath, 'out', self.cpu)], env)
                        # Run(['/home/user/work/awfy/driver/patch_stddef.sh', os.path.join(sourcePath, "third_party", "angle", "src", "common", "platform.h")], env)
                    except subprocess.CalledProcessError as e:
                        if synctroubles.fetchGsFileByHttp(e.output, ''):
                            syncAgain = True
                        else:
                            raise e
            try:
                Run(['ninja', '-C', os.path.join(sourcePath, 'out', self.cpu), 'chrome', '-j40'], env)
            except subprocess.CalledProcessError as e:
                print "Clean build also failed!"

    def shell(self):
        return os.path.join(utils.RepoPath, self.source, 'out', self.cpu, 'chrome')

    def libpaths(self):
        p = os.path.join(utils.RepoPath, self.source, 'out', self.cpu)
        return [{'path': p, 'exclude': ['obj', 'gen', 'clang_x64', 'clang_x86_v8_arm', 'pyproto', 'resources']}]


class ChromiumWin64(Engine):
    def __init__(self):
        super(ChromiumWin64, self).__init__()
        self.target_os = utils.config.get('main', 'target_os')
        self.puller = 'git'
        self.source = utils.config.get('chromium-win64', 'source')
        self.args = []
        self.important = True

        if self.cpu == 'x64':
            cpu_mode = '-x64'
        elif self.cpu == 'x86':
            cpu_mode = '-x86'
        elif self.cpu == 'arm':
            cpu_mode = '-arm'
        elif self.cpu == 'amd64':
            cpu_mode = '-amd64'

        self.modes = [{'mode': 'headless' + cpu_mode, 'args': None}]
        self.sourcePath = os.path.join(utils.config_get_default('main', 'build_repos'), self.source)

    def updateAndBuild(self, update=True, forceRebuild=False, rev=None):
        with utils.FolderChanger(self.sourcePath):
            self._updateAndBuild(update, forceRebuild, rev=rev)

    def _update(self, rev):
        with utils.FolderChanger(self.sourcePath):
            env = os.environ.copy()
            # reset to master branch
            winRun(['git', 'reset', '--hard'], env)
            winRun(['git', 'checkout', 'master'], env)
            winRun(['git', 'fetch'], env)
            winRun(['git', 'reset', '--hard', rev])
            winRun(['gclient', 'sync', '-D', '-j8', '-f'], env)

    def build(self):
        env = os.environ.copy()

        # add build command code here
        with utils.FolderChanger(self.sourcePath):
            try:
                if os.path.exists(os.path.join(self.sourcePath, 'out', self.cpu, 'Chrome-bin')):
                    winRun(['rm', '-r', '-fo', os.path.join(self.sourcePath, 'out', self.cpu, 'Chrome-bin')],
                        env)
                in_argns_name = self.target_os + "-" + self.cpu + ".gn"
                in_argns = os.path.join(WIN_WORK_DIR, 'awfy', 'gn_file', in_argns_name)
                out_argns = os.path.join(self.sourcePath, 'out', self.cpu, 'args.gn')
                if not os.path.isdir(os.path.join(self.sourcePath, 'out', self.cpu)):
                    os.mkdir(os.path.join(self.sourcePath, 'out', self.cpu))
                winRun(['cp', in_argns, out_argns], env)
                winRun(['gclient', 'sync', '-D', '-j25', '-f'], env)
                winRun(['gn', 'gen', os.path.join(self.sourcePath, 'out', self.cpu)], env)
                winRun(['ninja', '-C', os.path.join(self.sourcePath, 'out', self.cpu), 'chrome', 'mini_installer', '-j40'],
                    env)
                winRun(['7z', 'x', os.path.join(self.sourcePath, 'out', self.cpu, 'chrome.7z'),
                        '-o'+os.path.join(self.sourcePath, 'out', self.cpu)], env)
            except subprocess.CalledProcessError as e:
                print("Dirty build failed!")
                try:
                    if os.path.exists(os.path.join(self.sourcePath, 'out', self.cpu, 'Chrome-bin')):
                        winRun(['rm', '-r', '-fo', os.path.join(self.sourcePath, 'out', self.cpu, 'Chrome-bin')],
                            env)
                    in_argns_name = self.target_os + "-" + self.cpu + ".gn"
                    in_argns = os.path.join(WIN_WORK_DIR, 'awfy', 'gn_file', in_argns_name)
                    out_argns = os.path.join(self.sourcePath, 'out', self.cpu, 'args.gn')
                    winRun(['rm', '-r', '-fo', os.path.join(self.sourcePath, 'out', self.cpu)])
                    winRun(['mkdir', os.path.join(self.sourcePath, 'out', self.cpu)])
                    winRun(['cp', in_argns, out_argns], env)
                    winRun(['gclient', 'sync', '-D', '-j25', '-f'], env)
                    winRun(['gn', 'gen', os.path.join(self.sourcePath, 'out', self.cpu)], env)
                    winRun(['ninja', '-C', os.path.join(self.sourcePath, 'out', self.cpu), 'chrome', 'mini_installer',
                         '-j40'], env)
                    winRun(['7z', 'x', os.path.join(self.sourcePath, 'out', self.cpu, 'chrome.7z'),
                            '-o'+os.path.join(self.sourcePath, 'out', self.cpu)], env)
                except subprocess.CalledProcessError as e:
                    print("Clean build failed!")
                    raise e

    # deprecated
    def shell(self):
        return os.path.join(self.sourcePath, 'out', self.cpu, 'Chrome-bin', 'chrome.exe')

    def slave_shell(self):
        return os.path.join('out', self.cpu, 'Chrome-bin', 'chrome.exe')

    def libpaths(self):
        p = os.path.join('out', self.cpu, 'Chrome-bin')
        return [{'path': p, 'exclude': []}]


# add Headless_patch Engine
class Headless_patch(Engine):
    def __init__(self):
        super(Headless_patch, self).__init__()
        self.puller = 'git'
        self.source = utils.config.get('headless-patch', 'source')
        self.args = []
        self.important = True

        if self.cpu == 'x64':
            cpu_mode = '-x64'
        elif self.cpu == 'x86':
            cpu_mode = '-x86'
        elif self.cpu == 'arm':
            cpu_mode = '-arm'
        elif self.cpu == 'amd64':
            cpu_mode = '-amd64'

        self.modes = [{'mode': 'headless-patch' + cpu_mode, 'args': None}]

    def build(self):
        env = os.environ.copy()
        env["NO_AUTH_BOTO_CONFIG"] = "/repos/boto.cfg"
        # env["GYP_CHROMIUM_NO_ACTION"] = "0"

        # if self.cpu == 'x86':
        #     env["GYP_DEFINES"] = "target_arch=ia32"
        # elif self.cpu == 'x64':
        #     env["GYP_DEFINES"] = "target_arch=x64"
        # elif self.cpu == 'arm':
        #     env["GYP_DEFINES"] = "target_arch=arm arm_float_abi=hard component=shared_library linux_use_gold_flags=1"
        #     env["GYP_CROSSCOMPILE"] = "1"
        # add build command code here
        with utils.FolderChanger('./'):
            syncAgain = True
            sourcePath = os.path.join(utils.RepoPath, self.source)
            in_argns_name = self.cpu + '-patch' + ".gn"
            # in_argns = os.path.join(utils.RepoPath, 'gn_file', in_argns_name)
            in_argns = os.path.join(WORK_DIR, 'awfy', 'gn_file', in_argns_name)
            out_argns = os.path.join(utils.RepoPath, self.source, 'out', self.cpu + '-patch', 'args.gn')
            if not os.path.isdir(os.path.join(utils.RepoPath, self.source, 'out', self.cpu + '-patch')):
                os.mkdir(os.path.join(utils.RepoPath, self.source, 'out', self.cpu + '-patch'))
            while (syncAgain):
                syncAgain = False
                try:
                    print 'env=%s' % env
                    Run(['cp', in_argns, out_argns])
                    Run(['gclient', 'sync', '-D', '-j25', '-f'], env)

                    # add patch to v8.
                    """
                    COMMAND:
                        patch -p 1 -i /repos/enable-compressed-pointer.patch
                    clean COMMAND:
                        patch -R -p 1 -i /repos/enable-compressed-pointer.patch
                        or 
                        git checkout .
                    """
                    # with utils.FolderChanger(os.path.join(utils.RepoPath, self.source, 'v8')):
                    #     Run(['patch', '-p', '1', '-i', '/repos/enable-compressed-pointer.patch'], env)

                    # if self.cpu == 'arm':
                    # Run(['sed', '-i',
                    #     '/use_gold &&/{s/target_cpu == "x86"/target_cpu == "x86" || target_cpu == "arm"/g}',
                    #     os.path.join(sourcePath, "third_party", "swiftshader", "BUILD.gn")], env)
                    # Run(['sed', '-i',
                    #      '/use_lld && target_cpu == "x86"/{s/target_cpu == "x86"/(target_cpu == "x86" || target_cpu == "arm")/g}',
                    #      os.path.join(sourcePath, "third_party", "ffmpeg", "BUILD.gn")], env)
                    Run(['gn', 'gen', os.path.join(sourcePath, 'out', self.cpu + '-patch')], env)
                    # Run(['/home/user/work/awfy/driver/patch_stddef.sh', os.path.join(sourcePath, "third_party", "angle", "src", "common", "platform.h")], env)
                except subprocess.CalledProcessError as e:
                    if synctroubles.fetchGsFileByHttp(e.output, ''):
                        syncAgain = True
                    else:
                        raise e
        try:
            Run(['ninja', '-C', os.path.join(sourcePath, 'out', self.cpu + '-patch'), 'chrome', '-j40'], env)
        except subprocess.CalledProcessError as e:
            print "Dirty build failed!"
            # add build command code here
            with utils.FolderChanger('./'):
                syncAgain = True
                sourcePath = os.path.join(utils.RepoPath, self.source)
                in_argns_name = self.cpu + '-patch' + ".gn"
                # in_argns = os.path.join(utils.RepoPath, 'gn_file', in_argns_name)
                in_argns = os.path.join(WORK_DIR, 'awfy', 'gn_file', in_argns_name)
                out_argns = os.path.join(utils.RepoPath, self.source, 'out', self.cpu + '-patch', 'args.gn')
                while (syncAgain):
                    syncAgain = False
                    try:
                        # add 3 steps:
                        # 1. perl -pi -e "s/sudo //g" ./build/install-build-deps.sh
                        Run(['perl', '-pi', '-e', '"s/sudo //g"',
                             os.path.join(sourcePath, 'build', 'install-build-deps.sh')])
                        # 2. run build/install-build-deps.sh
                        Run(['/bin/bash', os.path.join(sourcePath, 'build', 'install-build-deps.sh')])
                        # 3. git checkout build/install-build-deps.sh
                        Run(['git', 'checkout', os.path.join(sourcePath, 'build', 'install-build-deps.sh')])
                        # 4. ./build/linux/sysroot_scripts/install-sysroot.py --arch=arm
                        Run([os.path.join(sourcePath, 'build/linux/sysroot_scripts/install-sysroot.py'), '--arch=arm'])

                        Run(['rm', os.path.join(sourcePath, 'out', self.cpu + '-patch'), '-rf'])
                        Run(['mkdir', os.path.join(sourcePath, 'out', self.cpu + '-patch')])
                        Run(['cp', in_argns, out_argns])
                        print 'env=%s' % env
                        Run(['gclient', 'sync', '-D', '-j25', '-f'], env)

                        # add patch to v8. move to args.gn
                        # with utils.FolderChanger(os.path.join(utils.RepoPath, self.source, 'v8')):
                        #     Run(['patch', '-p', '1', '-i', '/repos/enable-compressed-pointer.patch'], env)

                        # if self.cpu == 'arm':
                        # Run(['sed', '-i',
                        #     '/use_gold &&/{s/target_cpu == "x86"/target_cpu == "x86" || target_cpu == "arm"/g}',
                        #     os.path.join(sourcePath, "third_party", "swiftshader", "BUILD.gn")], env)
                        # Run(['sed', '-i',
                        #      '/use_lld && target_cpu == "x86"/{s/target_cpu == "x86"/(target_cpu == "x86" || target_cpu == "arm")/g}',
                        #      os.path.join(sourcePath, "third_party", "ffmpeg", "BUILD.gn")], env)
                        Run(['gn', 'gen', os.path.join(sourcePath, 'out', self.cpu + '-patch')], env)
                        # Run(['/home/user/work/awfy/driver/patch_stddef.sh', os.path.join(sourcePath, "third_party", "angle", "src", "common", "platform.h")], env)
                    except subprocess.CalledProcessError as e:
                        if synctroubles.fetchGsFileByHttp(e.output, ''):
                            syncAgain = True
                        else:
                            raise e
            try:
                Run(['ninja', '-C', os.path.join(sourcePath, 'out', self.cpu + '-patch'), 'chrome', '-j40'], env)
            except subprocess.CalledProcessError as e:
                print "Clean build also failed!"
        finally:
            # clean patch to v8.
            with utils.FolderChanger(os.path.join(utils.RepoPath, self.source, 'v8')):
                # Run(['patch', '-R', '-p', '1', '-i', '/repos/enable-compressed-pointer.patch'], env)
                Run(['git', 'checkout', '.'], env)

    def shell(self):
        return os.path.join(utils.RepoPath, self.source, 'out', self.cpu + '-patch', 'chrome')

    def libpaths(self):
        p = os.path.join(utils.RepoPath, self.source, 'out', self.cpu + '-patch')
        return [{'path': p, 'exclude': ['obj', 'gen', 'clang_x64', 'clang_x86_v8_arm', 'pyproto', 'resources']}]


# add Headless Engine
class JavaScriptCore(Engine):
    def __init__(self):
        super(JavaScriptCore, self).__init__()
        self.puller = 'git'
        self.source = utils.config.get('jsc', 'source')
        self.args = []
        self.important = True

        if self.cpu == 'x64':
            cpu_mode = '-x64'
        elif self.cpu == 'x86':
            cpu_mode = '-x86'
        elif self.cpu == 'arm':
            cpu_mode = '-arm'
        elif self.cpu == 'amd64':
            cpu_mode = '-amd64'
        self.output_dir = 'WebKitBuild/Release'
        self.modes = [{'mode': 'jsc' + cpu_mode, 'args': None}]

    def env(self):
        return {
            "LD_LIBRARY_PATH": os.path.join(utils.RepoPath, self.source,
                                            "WebKitBuild/Release/lib") + ":/home/user/jsc-dependence:$LD_LIBRARY_PATH"
        }

    def build(self):
        env = os.environ.copy()

        try:
            with utils.FolderChanger(os.path.join(os.path.join(utils.RepoPath, self.source))):
                Run(['Tools/Scripts/build-webkit', '--jsc-only', '-j40'], env)
        except subprocess.CalledProcessError as e:
            print "Dirty build failed!"
            # remove output dir
            if os.path.isdir(os.path.join(utils.RepoPath, self.source, self.output_dir)):
                os.rmdir(os.path.join(utils.RepoPath, self.source, self.output_dir))

            try:
                with utils.FolderChanger(os.path.join(os.path.join(utils.RepoPath, self.source))):
                    Run(['Tools/Scripts/build-webkit', '--jsc-only', '-j40'], env)
            except subprocess.CalledProcessError as e:
                print "Clean build also failed!"

    def shell(self):
        return os.path.join(utils.RepoPath, self.source, self.output_dir, 'bin', 'jsc')

    def libpaths(self):
        return [{'path': os.path.join(utils.RepoPath, self.source, self.output_dir, 'lib'), 'exclude': []}]


class IoTjs(Engine):
    def __init__(self):
        super(IoTjs, self).__init__()
        self.puller = 'git'
        self.source = utils.config.get('iotjs', 'source')

        self.args = []
        self.important = True

        if self.cpu == 'x64':
            cpu_mode = '-x64'
        elif self.cpu == 'x86':
            cpu_mode = '-x86'
        elif self.cpu == 'arm':
            cpu_mode = '-arm'

        self.modes = [{
            'mode': 'IoTjs' + cpu_mode,
            'args': None
        }]

    def build(self):
        env = os.environ.copy()

        Run(['tools/build.py', '--target-arch=i686', '--buildtype=release'], env)

    def shell(self):
        return os.path.join('build', 'i686-linux', 'release', 'iotjs', 'iotjs')


class Mozilla(Engine):
    def __init__(self, source):
        super(Mozilla, self).__init__()
        self.puller = 'hg'
        self.source = utils.config.get(source, 'source')
        self.config_line = utils.config.get(source, 'conf')
        self.args = None
        self.important = True
        self.objdir = 'Opt'

    def reconf(self):
        # Step 1. autoconf.
        with utils.FolderChanger(os.path.join('js', 'src')):
            if platform.system() == "Darwin":
                utils.Shell("autoconf213")
            elif platform.system() == "Linux":
                utils.Shell("autoconf2.13")
            elif platform.system() == "Windows":
                utils.Shell("autoconf-2.13")

        # Step 2. configure
        if not os.path.exists(os.path.join('js', 'src', self.objdir)):
            os.mkdir(os.path.join('js', 'src', self.objdir))
        with utils.FolderChanger(os.path.join('js', 'src', self.objdir)):
            utils.Shell(self.config_line)

        return True

    def build(self):
        utils.Shell("make -j 3 -C " + os.path.join('js', 'src', self.objdir))

    def shell(self):
        return os.path.join('js', 'src', self.objdir, 'dist', 'bin', 'js')


class MozillaInbound(Mozilla):
    def __init__(self):
        super(MozillaInbound, self).__init__('mi')
        self.modes = [
            {
                'mode': 'jmim',
                'args': ['--ion-offthread-compile=on', '-W']
            },
            {
                'mode': 'noasmjs',
                'args': ['--ion-offthread-compile=on', '-W', '--no-asmjs']
            }
        ]


class MozillaInboundGGC(Mozilla):
    def __init__(self):
        super(MozillaInboundGGC, self).__init__('mi')
        self.config_line += ' --enable-exact-rooting --enable-gcgenerational'
        self.objdir = 'OptGGC'
        self.modes = [
            {
                'mode': 'ggc',
                'args': ['--ion-offthread-compile=on', '-W']
            }
        ]


class NativeCompiler(Engine):
    def __init__(self):
        super(NativeCompiler, self).__init__()
        self.cc = utils.config.get('native', 'cc')
        self.cxx = utils.config.get('native', 'cxx')
        self.args = utils.config.get('native', 'options').split(' ')
        self.mode = utils.config.get('native', 'mode')

        # output = Run([self.cxx, '--version'])
        self.signature = 'gcc 5.4.0'  # output.splitlines()[0].strip()


def build(engines, updateRepo=True, forceBuild=False, rev=None):
    print "build"
    Engines = []
    NumUpdated = 0
    if len(engines) == 1:
        try:
            print "updateAndBuild"
            engines[0].updateAndBuild(updateRepo, forceBuild, rev)
            status = 0
        except Exception as err:
            print('Build failed!')
            print(err)
            traceback.print_exc(file=sys.stdout)
            status = 1
        return status
    else:
        for engine in engines:
            try:
                print "updateAndBuild"
                engine.updateAndBuild(updateRepo, forceBuild, rev)
                status = 0
            except Exception as err:
                print('Build failed!')
                print(err)
                traceback.print_exc(file=sys.stdout)
                continue
            if engine.updated and engine.important:
                NumUpdated += 1
            Engines.append(engine)
        return Engines, NumUpdated
