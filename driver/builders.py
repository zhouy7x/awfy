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
from utils import Run

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
            print('\n++++++++ Build-Time: ' + str(secs/3600) + "h:" + str(secs%3600/60) + "m:" + str(secs%60) + "s ++++++++\n\n")
    
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
        self.important = False # WebKit changes too frequently, we'd need to detect JSC changes.
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
        Run(["sed","-i.bac","s/GCC_TREAT_WARNINGS_AS_ERRORS = YES;/GCC_TREAT_WARNINGS_AS_ERRORS=NO;/","Source/JavaScriptCore/Configurations/Base.xcconfig"])
        Run(["sed","-i.bac","s/GCC_TREAT_WARNINGS_AS_ERRORS = YES;/GCC_TREAT_WARNINGS_AS_ERRORS=NO;/","Source/bmalloc/Configurations/Base.xcconfig"])
        Run(["sed","-i.bac","s/GCC_TREAT_WARNINGS_AS_ERRORS = YES;/GCC_TREAT_WARNINGS_AS_ERRORS=NO;/","Source/WTF/Configurations/Base.xcconfig"])
        Run(["sed","-i.bac","s/std::numeric_limits<unsigned char>::max()/255/","Source/bmalloc/bmalloc/Line.h"])
        Run(["sed","-i.bac","s/std::numeric_limits<unsigned char>::max()/255/","Source/bmalloc/bmalloc/Page.h"])

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

        Run(["svn","revert","Source/JavaScriptCore/Configurations/Base.xcconfig"])
        Run(["svn","revert","Source/bmalloc/Configurations/Base.xcconfig"])
        Run(["svn","revert","Source/WTF/Configurations/Base.xcconfig"])
        Run(["svn","revert","Source/bmalloc/bmalloc/Line.h"])
        Run(["svn","revert","Source/bmalloc/bmalloc/Page.h"])

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
            Run(['make', 'x64.release', 'werror=no', '-j8'], env)
        elif self.cpu == 'arm':
            make_cmd = ['make', 'werror=no', '-j8', 'arm.release',
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
            Run(['make', 'ia32.release', 'werror=no', '-j8'], env)
  
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

        return [{"path" : os.path.join('out', otgt, 'natives_blob.bin'), "exclude" : []},
                {"path" : os.path.join('out', otgt, 'snapshot_blob.bin'), "exclude" : []},
                {"path" : os.path.join('out', otgt, 'icudtl.dat'), "exclude" : []}
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
            #sourcePath = os.path.join(utils.RepoPath, self.source)
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
        return [{'path' : p, 'exclude' : ['obj', 'gen']}]

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

        #output = Run([self.cxx, '--version'])
        self.signature = 'gcc 5.4.0' #output.splitlines()[0].strip()

def build(engines, updateRepo=True, forceBuild=False, rev=None):
    Engines = []
    NumUpdated = 0
    for engine in engines:
        try:
            engine.updateAndBuild(updateRepo, forceBuild, rev)
        except Exception as err:
            print('Build failed!')
            print(err)
            traceback.print_exc(file=sys.stdout)
            continue
        if engine.updated and engine.important:
            NumUpdated += 1
        Engines.append(engine)
    return Engines, NumUpdated
