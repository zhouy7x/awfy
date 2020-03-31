import os
import re

from driver import utils


class JetStream2D8(Benchmark):
    def __init__(self):
        super(JetStream2D8, self).__init__('jetstream2-d8', '', 'jetstream2-d8')

    def benchmark(self, shell, env, args):
        full_args = [shell, './run.js']
        if args:
            full_args.extend(args)
        print(os.getcwd())
        output = utils.RunTimedCheckOutput(full_args, env=env)

        tests = []
        """
        Running 3d-cube-SP:
            Startup: 87.719
            Worst Case: 294.118
            Average: 358.002
            Score: 209.814
            Wall time: 0:01.720
        
        Total Score:  107.968 
        """
        subcases = re.findall(r'Running *(.+):\n[\w\W]+?Score: (\d+\.\d*)', output)
        # print subcases
        for subcase in subcases:
            name = subcase[0]
            score = utils.myround(subcase[1], 2)
            tests.append({'name': name, 'time': score})
            print(score + '     - ' + name)
        total = re.search(r'Total Score: *(\d+\.\d*)', output)
        name = '__total__'
        score = utils.myround(total.group(1))
        tests.append({'name': name, 'time': score})
        print(score + '     - ' + name)
        return tests
