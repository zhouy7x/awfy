# vim: set ts=4 sw=4 tw=99 et:
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
import os
import sys
import urllib2
import StringIO
import subprocess
import signal
import pickle
import time

import ConfigParser
import submitter
import utils
import socket
import chromiumclient
import pserver

class Benchmark(object):
    def __init__(self, suite, version, folder):
        self.suite = suite
        self.version = suite+" "+version
        self.folder = folder

    def run(self, submit, native, modes, includes):
        if includes != None and includes.find(self.suite) < 0:
            return
        with utils.chdir(os.path.join(utils.BenchmarkPath, self.folder)):
            return self._run(submit, native, modes)

    def omit(self, mode):
        if mode.name == 'noasmjs':
            return True
        if 'ContentShell' in mode.name:
            return True
        if 'JerryScript' in mode.name:
            return True
        if 'IoTjs' in mode.name:
            return True

    def _run(self, submit, native, modes):
        for mode in modes:
            if self.omit(mode):
                continue
            try:
                tests = None
                print('Running ' + self.version + ' under ' + mode.shell + ' ' + ' '.join(mode.args))
                beginTime = time.time()
                tests = self.benchmark(mode.shell, mode.env, mode.args)
                passTime = time.time() - beginTime
                print('Suite-Time ' + self.version + ':'), passTime
            except Exception as e:
                print('Failed to run ' + self.version + '!')
                print("Exception: " +  repr(e))
                pass
            if tests:
                submit.AddTests(tests, self.suite, self.version, mode.name)

class AsmJS(Benchmark):
    def __init__(self, suite, version, folder):
        super(AsmJS, self).__init__(suite, version, folder)

    def omit(self, mode):
        if mode.name == 'noasmjs':
            return False
        return super(AsmJS, self).omit(mode)

    def _run(self, submit, native, modes):
        # Run the C++ mode.
        full_args = [utils.PythonName, 'harness.py', '--native']
        full_args += ['--cc="' + native.cc + '"']
        full_args += ['--cxx="' + native.cxx + '"']
        full_args += ['--'] + native.args
        output = utils.RunTimedCheckOutput(full_args)
        
        tests = self.parse(output)
        submit.AddTests(tests, self.suite, self.version, native.mode)

        # Run normal benchmarks.
        super(AsmJS, self)._run(submit, native, modes)

    def benchmark(self, shell, env, args):
        full_args = [utils.PythonName, 'harness.py', shell, '--'] + args
        print(' '.join(full_args))
        
        output = utils.RunTimedCheckOutput(full_args, env=env)
        return self.parse(output)

    def parse(self, output):
        total = 0.0
        tests = []
        for line in output.splitlines():
            m = re.search("(.+) - (\d+(\.\d+)?)", line)
            if not m:
                continue
            name = m.group(1)
            score = m.group(2)
            total += float(score)
            tests.append({ 'name': name, 'time': score })
        tests.append({ 'name': '__total__', 'time': total })
        return tests

class AsmJSMicro(AsmJS):
    def __init__(self):
        super(AsmJSMicro, self).__init__('asmjs-ubench', '0.3', 'asmjs-ubench')

class AsmJSApps(AsmJS):
    def __init__(self):
        super(AsmJSApps, self).__init__('asmjs-apps', '0.2', 'asmjs-apps')

class Octane(Benchmark):
    def __init__(self):
        super(Octane, self).__init__('octane', '2.0.1', 'octane')

    def benchmark(self, shell, env, args):
        full_args = [shell]
        if args:
            full_args.extend(args)
        full_args.append('run.js')

        print(os.getcwd())
        output = utils.RunTimedCheckOutput(full_args, env=env)

        tests = []
        lines = output.splitlines()

        for x in lines:
            m = re.search("(.+): (\d+)", x)
            if not m:
                continue
            name = m.group(1)
            score = m.group(2)
            if name[0:5] == "Score":
                name = "__total__"
            tests.append({ 'name': name, 'time': score})
            print(score + '    - ' + name)

        return tests

class OctaneV1(Octane):
    def __init__(self):
        super(Octane, self).__init__('octane1', '1.0', 'octane1')

 
class SunSpiderBased(Benchmark):
    def __init__(self, suite, version, folder, runs):
        super(SunSpiderBased, self).__init__(suite, version, folder)
        self.runs = runs

    def benchmark(self, shell, env, args):
        if args != None:
            args = '--args=' + ' '.join(args)
        else:
            args = ''

        output = utils.RunTimedCheckOutput(["./sunspider",
                                            "--shell=" + shell,
                                            "--runs=" + str(self.runs),
                                            args],
                                           env=env)
        tests = []

        lines = output.splitlines()
        found = False
        for x in lines:
            if x == "--------------------------------------------" or \
               x == "-----------------------------------------------":
                found = True
            if x[0:5] == "Total":
                m = re.search(":\s+(\d+\.\d+)ms", x)
                tests.append({ 'name': '__total__', 'time': m.group(1)})
                print(m.group(1) + '    - __total__')
            elif found == True and x[0:4] == "    ":
                m = re.search("    (.+):\s+(\d+\.\d+)ms", x)
                if m != None:
                    tests.append({ 'name': m.group(1), 'time': m.group(2)})
                    print(m.group(2) + '    - ' + m.group(1))

        if found == False:
            print(output)
            raise Exception("output marker not found")

        return tests

class SunSpider(SunSpiderBased):
    def __init__(self):
        super(SunSpider, self).__init__('ss', '1.0.1', 'SunSpider', 20)

class Kraken(SunSpiderBased):
    def __init__(self):
        super(Kraken, self).__init__('kraken', '1.1', 'kraken', 5)

class Assorted(SunSpiderBased):
    def __init__(self):
        super(Assorted, self).__init__('misc', '0.1', 'misc', 3)

class Embenchen(Benchmark):
    def __init__(self):
        super(Embenchen, self).__init__('embenchen', '0.0.2', 'embenchen')

    def benchmark(self, shell, env, args):
        # Only run turbofan
        if '--turbo' not in args:
            return None

        full_args = [utils.PythonName, 'harness.py', shell, '--'] + args
        print(' '.join(full_args))

        output = utils.RunTimedCheckOutput(full_args, env=env)
        return self.parse(output)

    def parse(self, output):
        total = 0.0
        tests = []
        for line in output.splitlines():
            m = re.search("(.+) - (\d+(\.\d+)?)", line)
            if not m:
                continue
            name = m.group(1)
            score = m.group(2)
            total += float(score)
            tests.append({ 'name': name, 'time': score })
        tests.append({ 'name': '__total__', 'time': total })
        return tests

class JetStream(Benchmark):
    def __init__(self):
        super(JetStream, self).__init__('jetstream', '1.0.1', 'jetstream-asmjs')

    def benchmark(self, shell, env, args):
        full_args = [utils.PythonName, 'harness.py', shell, '--'] + args
        print(' '.join(full_args))

        output = utils.RunTimedCheckOutput(full_args, env=env)
        return self.parse(output)

    def parse(self, output):
        total = 0.0
        tests = []
        for line in output.splitlines():
            m = re.search("(.+) - (\d+(\.\d+)?)", line)
            if not m:
                continue
            name = m.group(1)
            score = m.group(2)
            total += float(score)
            tests.append({ 'name': name, 'time': score })
        tests.append({ 'name': '__total__', 'time': total })
        return tests

class BrowserMark(Benchmark):
    def __init__(self):
        super(BrowserMark, self).__init__('browsermark', '2.1', 'bm2.1-js')

    def benchmark(self, shell, env, args):
        full_args = [shell]
        if args:
            full_args.extend(args)
        full_args.append('runbm.js')

        print(os.getcwd())
        output = utils.RunTimedCheckOutput(full_args, env=env)

        tests = []
        lines = output.splitlines()

        total = 0.0
        for x in lines:
            m = re.search("^(\w+): (.+) score: (\d+(\.\d+)?)", x)
            if not m:
                continue
            name = m.group(1)
            score = m.group(3)
            tests.append({ 'name': name, 'time': score})
            print(score + '    - ' + name)
            total += float(score);

        tests.append({ 'name': "__total__", 'time': total})

        return tests

class VellamoSurfWaxBinder(Benchmark):
    def __init__(self):
        super(VellamoSurfWaxBinder, self).__init__('VellamoSurfWaxBinder', '3.1', 'Vellamo')

    def benchmark(self, shell, env, args):
        full_args = [shell]
        if args:
            full_args.extend(args)
        full_args.append('Vellamo3.1_SurfWaxBinder_d8.js')

        print(os.getcwd())
        output = utils.RunTimedCheckOutput(full_args, env=env)

        tests = []
        lines = output.splitlines()

        total = 0.0
        for x in lines:
            m = re.search("^(\w+) (\d+(\.\d+)?)", x)
            if not m:
                continue
            name = m.group(1)
            score = m.group(2)
            tests.append({ 'name': name, 'time': score})
            print(score + '    - ' + name)
            total += float(score);

        tests.append({ 'name': "__total__", 'time': total})

        return tests

class VellamoKruptein(Benchmark):
    def __init__(self):
        super(VellamoKruptein, self).__init__('VellamoKruptein', '3.1',
                'Vellamo')

    def benchmark(self, shell, env, args):
        full_args = [shell]
        if args:
            full_args.extend(args)
        full_args.append('Vellamo3.1_Kruptein_d8.js')

        print(os.getcwd())
        output = utils.RunTimedCheckOutput(full_args, env=env)

        tests = []
        lines = output.splitlines()

        for x in lines:
            m = re.search("^(\w+) (\d+(\.\d+)?)", x)
            if not m:
                continue
            name = m.group(1)
            score = m.group(2)
            
            if name == "vscore":
                name = "__total__"
            tests.append({ 'name': name, 'time': score})

        return tests

class VellamoDeepCrossfader(Benchmark):
    def __init__(self):
        super(VellamoDeepCrossfader, self).__init__('VellamoDeepCrossfader', '3.0',
                'Vellamo')

    def benchmark(self, shell, env, args):
        full_args = [shell]
        if args:
            full_args.extend(args)
        full_args.append('DeepCrossfader.js')

        print(os.getcwd())
        output = utils.RunTimedCheckOutput(full_args, env=env)

        tests = []
        lines = output.splitlines()

        for x in lines:
            m = re.search("^(\w+): (\d+(\.\d+)?)ms", x)
            if not m:
                continue
            name = m.group(1)
            score = m.group(2)
            
            if name == "total":
                name = "__total__"
            tests.append({ 'name': name, 'time': score})

        return tests

class WebXPRTStock(Benchmark):
    def __init__(self):
        super(WebXPRTStock, self).__init__('WebXPRTStock', '2013',
                'WebXPRT2013')

    def benchmark(self, shell, env, args):
        full_args = [shell]
        if args:
            full_args.extend(args)
        full_args.append('WebXPRT2013-stockslibrary-d8.js')

        print(os.getcwd())
        output = utils.RunTimedCheckOutput(full_args, env=env)

        tests = []
        lines = output.splitlines()

        cnt = 0
        total = 0.0
        for x in lines:
            m = re.search("(\d+(\.\d+)?)", x)
            if not m:
                continue
            cnt = cnt + 1
            score = m.group(1)
            tests.append({ 'name': cnt, 'time': score})
            total += float(score)

        tests.append({ 'name': '__total__', 'time': total})

        return tests

class WebXPRTStorage(Benchmark):
    def __init__(self):
        super(WebXPRTStorage, self).__init__('WebXPRTStorage', '2013',
                'WebXPRT2013')

    def benchmark(self, shell, env, args):
        full_args = [shell]
        if args:
            full_args.extend(args)
        full_args.append('WebXPRT2013-StorageNotes-d8.js')

        print(os.getcwd())
        output = utils.RunTimedCheckOutput(full_args, env=env)

        tests = []
        lines = output.splitlines()

        cnt = 0
        total = 0.0
        for x in lines:
            m = re.search("(\d+(\.\d+)?)", x)
            if not m:
                continue
            cnt = cnt + 1
            score = m.group(1)
            tests.append({ 'name': cnt, 'time': score})
            total += float(score)

        tests.append({ 'name': '__total__', 'time': total})

        return tests

class ContentShellBased(Benchmark):
    def __init__(self, suite, version, folder):
        super(ContentShellBased, self).__init__(suite, version, folder)

    def omit(self, mode):
        if 'ContentShell' not in mode.name:
            return True

    def webscore(self, shell, env, args, url, timeout=600):
        full_args = []
        if args:
            full_args.extend(args)
        full_args.append('--no-sandbox')
        full_args.append(url)

        # use chromium client to start contentshell on slave machine
        chromiumclient.startChromium(args=full_args) 

        try:
            data = pserver.getTestDataBySocket(timeout=timeout)
        except socket.timeout:
            print "CONTENT SHELL TEST TIME OUT!"
            data = ''
        finally:
            #phttpserver.kill()
            #pcontentshell.kill()
            chromiumclient.stopChromium()

        return data

class BmDom(ContentShellBased):
    def __init__(self):
        super(BmDom, self).__init__('browsermark1', '2.1',
                'contentshell-bm')

    def benchmark(self, shell, env, args):
        url = '' 

        # read test url
        f = open('dom2.1', 'r')
        url = f.read()
        f.close()

        output = self.webscore(shell, env, args, url)

        tests = []
        lines = output.splitlines()

        for x in lines:
            parts = x.split(':')
            name = parts[0]
            score = parts[1]

            print(name + '    - ' + score) 
            if name == 'overall':
                name = '__total__'

            tests.append({ 'name': name, 'time': score})

        return tests

class BmScalable(ContentShellBased):
    def __init__(self):
        super(BmScalable, self).__init__('browsermark2', '2.1',
                'contentshell-bm')

    def benchmark(self, shell, env, args):
        url = ''

        # read test url
        f = open('scalable_solutions2.1', 'r')
        url = f.read()
        f.close()

        output = self.webscore(shell, env, args, url)

        tests = []
        lines = output.splitlines()

        for x in lines:
            parts = x.split(':')
            name = parts[0]
            score = parts[1]

            print(name + '    - ' + score)
            if name == 'overall':
                name = '__total__'

            tests.append({ 'name': name, 'time': score})

        return tests

class JerrySimple(Benchmark):
    def __init__(self):
        super(JerrySimple, self).__init__('JerryBasic', '1.0',
                'JerryTest')
 
    def omit(self, mode):
        if 'JerryScript' not in mode.name and 'IoTjs' not in mode.name:
            return True

    def benchmark(self, shell, env, args):
        if 'jerry' in shell:
            test_script = 'jerrytest.sh'
        else:
            test_script = 'iotjstest.sh'

        full_args = ['bash', test_script, shell]

        print(os.getcwd())
        output = utils.RunTimedCheckOutput(full_args, env=env)

        tests = []
        lines = output.splitlines()
        for x in lines:
            m = re.search("@(\w+): (\d+(\.\d+)?)", x)
            if not m:
                continue

            name = m.group(1)
            score = m.group(2)

            print(name + '    - ' + score)
            if name == 'binary_size':
                tests.append({ 'name': '__total__', 'time': score})

            tests.append({ 'name': name, 'time': score})

        return tests

class JerrySunspider(Benchmark):
    def __init__(self):
        super(JerrySunspider, self).__init__('JerrySunspider', '1.0.1', 'JerrySs')

    def omit(self, mode):
        if 'JerryScript' not in mode.name and 'IoTjs' not in mode.name:
            return True

    def benchmark(self, shell, env, args):
        f = open('sslist')
        cases = f.readlines()
        f.close()

        total = 0
        tests = []
        for subcase in cases:
            # remove new line
            subcase = subcase[:-1]

            full_args = [shell, subcase]
            beginTime = time.time()
            # run sub-case
            utils.RunTimedCheckOutput(full_args, env=env)
            passTime = (time.time() - beginTime) * 1000

            tests.append({ 'name': subcase, 'time': passTime})
            total += passTime

        tests.append({ 'name': 'overall', 'time': total})
        tests.append({ 'name': '__total__', 'time': total})
        return tests

class JerrySunspiderPerf(Benchmark):
    def __init__(self):
        super(JerrySunspiderPerf, self).__init__('JerrySunspiderPerf', '1.0.2', 'JerrySs')

    def omit(self, mode):
        if 'JerryScript' not in mode.name and 'IoTjs' not in mode.name:
            return True

    def benchmark(self, shell, env, args):
        full_args = ['./jerry-perf.sh', shell, '1', '60', 'ss-1.0.2']

        output = utils.RunTimedCheckOutput(full_args, env=env)
        lines = output.splitlines()

        scorebase = {
            '3d-cube.js':1.88,
            # '3d-morph.js':4.268,
            '3d-raytrace.js':0.052,
            'access-binary-trees.js':1.108,
            'access-fannkuch.js':5.936,
            'access-nbody.js':2.696,
            # 'access-nsieve.js':8.6,
            'bitops-3bit-bits-in-byte.js':1.54,
            'bitops-bits-in-byte.js':2.092,
            'bitops-bitwise-and.js':2.116,
            'bitops-nsieve-bits.js':1,
            'controlflow-recursive.js':0.964,
            'crypto-aes.js':3.356,
            'crypto-md5.js':13.772,
            'crypto-sha1.js':6.444,
            'date-format-tofte.js':1.98,
            'date-format-xparb.js':1.08,
            'math-cordic.js':2.208,
            'math-partial-sums.js':1.224,
            'math-spectral-norm.js':1.348,
            # 'regexp-dna.js':0.092,
            'string-base64.js':1,
            'string-fasta.js':3.504,
            # 'string-tagcloud.js':0.028,
            # 'string-unpack-code.js':1,
            # 'string-validate-input.js':1.424,
        }

        tests = []
        total = 0.0
        refscore = 0.0

        for x in lines:
            m = re.search("(.+) \| (\d+(\.\d+)?)", x)
            if not m:
                continue

            name = m.group(1)
            score = m.group(2)
            score = float(score) * 1000

            if name in scorebase:
                refscore = score / scorebase[name]

            tests.append({ 'name': name, 'time': score})
            total += refscore

        tests.append({ 'name': '__total__', 'time': total})
        return tests

class JerrySunspiderMem(Benchmark):
    def __init__(self):
        super(JerrySunspiderMem, self).__init__('JerrySunspiderMem', '1.0.2', 'JerrySs')

    def omit(self, mode):
        if 'JerryScript' not in mode.name and 'IoTjs' not in mode.name:
            return True

    def benchmark(self, shell, env, args):
        full_args = ['./jerry-mem.sh', shell, '15', '60', 'ss-1.0.2']

        output = utils.RunTimedCheckOutput(full_args, env=env)
        lines = output.splitlines()

        scorebase = {
            '3d-cube.js':116,
            # '3d-morph.js':50,
            '3d-raytrace.js':50 ,
            'access-binary-trees.js':84,
            'access-fannkuch.js':40,
            'access-nbody.js':50,
            # 'access-nsieve.js':50,
            'bitops-3bit-bits-in-byte.js':28,
            'bitops-bits-in-byte.js':28,
            'bitops-bitwise-and.js':32,
            'bitops-nsieve-bits.js':50,
            'controlflow-recursive.js':256,
            'crypto-aes.js':124,
            'crypto-md5.js':50,
            'crypto-sha1.js':132,
            'date-format-tofte.js':76,
            'date-format-xparb.js':76,
            'math-cordic.js':36,
            'math-partial-sums.js':50,
            'math-spectral-norm.js':32,
            # 'regexp-dna.js':50,
            'string-base64.js':50,
            'string-fasta.js':48,
            # 'string-tagcloud.js':50,
            # 'string-unpack-code.js':50,
            # 'string-validate-input.js':50,
        }

        tests = []
        total = 0.0
        refscore = 0.0

        for x in lines:
            m = re.search("(.+) \| (\d+(\.\d+)?)", x)
            if not m:
                continue

            name = m.group(1)
            score = m.group(2)

            if name in scorebase:
                refscore = float(score) / scorebase[name]

            tests.append({ 'name': name, 'time': score})
            total += refscore

        tests.append({ 'name': '__total__', 'time': total})
        return tests

class JerryPassrate(Benchmark):
    def __init__(self):
        super(JerryPassrate, self).__init__('JerryPassrate', '1.0',
                'test262')
 
    def omit(self, mode):
        if 'JerryScript' not in mode.name:
            return True

    def benchmark(self, shell, env, args):
        test_script = 'runall.sh'

        full_args = ['bash', test_script, shell]

        print(os.getcwd())
        output = utils.RunTimedCheckOutput(full_args, env=env)

        tests = []
        lines = output.splitlines()
        for x in lines:
            m = re.search("- Passed (\d+) tests \((\d+(\.\d+)?)%\)", x)
            if not m:
                continue

            passed = m.group(1)
            passrate = m.group(2)

            print('passed    - ' + passed)
            print('passrate    - ' + passrate)

            tests.append({ 'name': '__total__', 'time': passrate})
            tests.append({ 'name': 'passrate', 'time': passrate})

            break

        return tests

class JetStreamShell(Benchmark):
    def __init__(self):
        super(JetStreamShell, self).__init__('JetStreamShell', '1.0',
                'jetstream-shell')

    def benchmark(self, shell, env, args):
        full_args = [shell]
        if args:
            full_args.extend(args)
        full_args.append('run.js')

        print(os.getcwd())
        output = utils.RunTimedCheckOutput(full_args, env=env)

        tests = []
        lines = output.splitlines()

        cnt = 0
        for x in lines:
            m = re.search("(.+),(\d+(\.\d+)?)", x)
            if not m:
                continue
            name = m.group(1)
            score = m.group(2)
            print(name + ' - ' + score)

            if name == 'Geometric-Mean':
                name = '__total__'

            tests.append({ 'name': name, 'time': score})

        return tests

class WebXPRTStockLib(Benchmark):
    def __init__(self):
        super(WebXPRTStockLib, self).__init__('WebXPRTStockLib', '2015',
                'WebXPRT2015')

    def benchmark(self, shell, env, args):
        full_args = [shell]
        if args:
            full_args.extend(args)
        full_args.append('WebXPRT2015-stockslibrary-d8.js')

        print(os.getcwd())
        output = utils.RunTimedCheckOutput(full_args, env=env)

        tests = []
        lines = output.splitlines()

        cnt = 0
        total = 0.0
        for x in lines:
            m = re.search("(\d+(\.\d+)?)", x)
            if not m:
                continue
            cnt = cnt + 1
            score = m.group(1)
            tests.append({ 'name': cnt, 'time': score})
            total += float(score)

        tests.append({ 'name': '__total__', 'time': total})

        return tests

class WebXPRTDNA(Benchmark):
    def __init__(self):
        super(WebXPRTDNA, self).__init__('WebXPRTDNA', '2015',
                'WebXPRT2015')

    def benchmark(self, shell, env, args):
        full_args = [shell]
        if args:
            full_args.extend(args)
        full_args.append('WebXPRT2015-sequencing-d8.js')

        print(os.getcwd())
        output = utils.RunTimedCheckOutput(full_args, env=env)

        tests = []
        lines = output.splitlines()

        cnt = 0
        total = 0.0
        for x in lines:
            m = re.search("(\d+(\.\d+)?)", x)
            if not m:
                continue
            cnt = cnt + 1
            score = m.group(1)
            tests.append({ 'name': cnt, 'time': score})
            total += float(score)

        tests.append({ 'name': '__total__', 'time': total})

        return tests

Benchmarks = [#AsmJSApps(),
              #AsmJSMicro(),
              SunSpider(),
              Kraken(),
              #Assorted(),
              #OctaneV1(),
              Octane(),
              Embenchen(),
              #JetStream(),
              BrowserMark(),
              VellamoSurfWaxBinder(),
              VellamoKruptein(),
              #VellamoDeepCrossfader(),
              WebXPRTStock(),
              WebXPRTStorage(),
              WebXPRTStockLib(),
              WebXPRTDNA(),
              BmDom(),
              BmScalable(),
			  # JerrySunspiderPerf(),
			  # JerrySunspiderMem(),
              JetStreamShell(),
             ]

def run(submit, native, modes, includes):
    for benchmark in Benchmarks:
        benchmark.run(submit, native, modes, includes)
    submit.Finish(1)

#def run(slave, submit, native, modes):
#    slave.rpc(sys.modules[__name__], submit, native, modes, async=True)
#
#default_function = run_
if __name__ == "__main__":
    remote.takerpc()
