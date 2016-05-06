// Copyright (C) 2014 Apple Inc. All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions
// are met:
// 1. Redistributions of source code must retain the above copyright
//    notice, this list of conditions and the following disclaimer.
// 2. Redistributions in binary form must reproduce the above copyright
//    notice, this list of conditions and the following disclaimer in the
//    documentation and/or other materials provided with the distribution.
//
// THIS SOFTWARE IS PROVIDED BY APPLE INC. AND ITS CONTRIBUTORS ``AS IS''
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
// THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
// PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL APPLE INC. OR ITS CONTRIBUTORS
// BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
// CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
// SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
// INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
// CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
// ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
// THE POSSIBILITY OF SUCH DAMAGE.

var JetStream = (function() {
    var isRunning;
    var hasAlreadyRun;
    var currentPlan;
    var currentIteration;
    var numberOfIterations;
    var accumulator;
    var selectBenchmark;

    var givenPlans = [];
    var givenReferences = {};
    var categoryNames;
    var plans;
    var benchmarks;

    // Import Octane benchmarks.

    var tDistribution = [NaN, NaN, 12.71, 4.30, 3.18, 2.78, 2.57, 2.45, 2.36, 2.31, 2.26, 2.23, 2.20, 2.18, 2.16, 2.14, 2.13, 2.12, 2.11, 2.10, 2.09, 2.09, 2.08, 2.07, 2.07, 2.06, 2.06, 2.06, 2.05, 2.05, 2.05, 2.04, 2.04, 2.04, 2.03, 2.03, 2.03, 2.03, 2.03, 2.02, 2.02, 2.02, 2.02, 2.02, 2.02, 2.02, 2.01, 2.01, 2.01, 2.01, 2.01, 2.01, 2.01, 2.01, 2.01, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.99, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.98, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.96];
    var tMax = tDistribution.length;
    var tLimit = 1.96;

    function tDist(n)
    {
        if (n > tMax)
            return tLimit;
        return tDistribution[n];
    }

    function displayResultMessage(name, message, style)
    {
        print(name + "," + message);
    }

    function displayResultMessageForPlan(plan, message, style)
    {
        for (var i = plan.benchmarks.length; i--;)
            displayResultMessage(plan.benchmarks[i].name, message, style);
    }

    function computeStatistics(values)
    {
        if (!values.length)
            return {n: 0};

        var sum = 0;
        var n = 0;
        for (var i = 0; i < values.length; ++i) {
            if (!(i in values))
                continue;
            sum += values[i];
            n++;
        }

        if (n != values.length)
            return {n: values.length, failed: values.length - n};

        var mean = sum / n;

        if (n <= 2)
            return {n: n, mean: mean};

        var sumForStdDev = 0;
        for (var i = 0; i < values.length; ++i) {
            if (!(i in values))
                continue;
            sumForStdDev += Math.pow(values[i] - mean, 2);
        }
        var standardDeviation = Math.sqrt(sumForStdDev / (n - 1));
        var standardError = standardDeviation / Math.sqrt(n);
        var interval = tDist(n) * standardError;
        return {n: n, mean: mean, interval: interval};
    }

    function formatResult(values, options)
    {
        options = options || {};
        var extraPrecision = options.extraPrecision || 0;

        function prepare(value)
        {
            var precision = 4 + extraPrecision;
            var digitsAfter;
            if (value) {
                var log = Math.log(value) / Math.log(10);
                if (log >= precision)
                    digitsAfter = 0;
                else if (log < 0)
                    digitsAfter = precision;
                else
                    digitsAfter = precision - 1 - (log | 0);
            } else
                digitsAfter = precision - 1;

            return value.toFixed(digitsAfter);
        }

        var statistics = computeStatistics(values);

        if (!statistics.n)
            return "";

        if ("failed" in statistics) {
            if (statistics.n == 1)
                return "ERROR";
            return "ERROR <i>(failed " + statistics.failed + "/" + statistics.n + ")</i>";
        }

        if ("interval" in statistics)
            return prepare(statistics.mean) + " +- " + prepare(statistics.interval);

        return prepare(statistics.mean);
    }

    function runCode(list)
    {
        for (var i=0; i<list.length; i++)
            load(list[i]);
    }

    function addPlan(plan)
    {
        givenPlans.push(plan);
    }

    function addReferences(references)
    {
        for (var s in references)
            givenReferences[s] = references[s];
    }

    function reset()
    {
        var categoryMap = {};
        benchmarks = [];
        for (var i = 0; i < givenPlans.length; ++i) {
            var plan = givenPlans[i];
            if (selectBenchmark && plan.name != selectBenchmark)
                continue;
            for (var j = 0; j < plan.benchmarks.length; ++j) {
                var benchmark = plan.benchmarks[j];
                benchmarks.push(benchmark);
                var benchmarksForCategory = categoryMap[benchmark.category];
                if (!benchmarksForCategory)
                    benchmarksForCategory = categoryMap[benchmark.category] = [];
                benchmarksForCategory.push(benchmark);
                benchmark.plan = plan;
                benchmark.reference = givenReferences[benchmark.name] || 1;
            }
        }
        categoryNames = [];
        for (var category in categoryMap)
            categoryNames.push(category);
        categoryNames.sort();

        var cells = [];
        for (var i = 0; i < categoryNames.length; ++i) {
            var categoryName = categoryNames[i];
            cells.push({kind: "category", name: categoryName});
            var benchmarksForCategory = categoryMap[categoryName];
            benchmarksForCategory.sort(function(a, b) {
                return a.name.localeCompare(b.name);
            });
            for (var j = 0; j < benchmarksForCategory.length; ++j)
                cells.push({kind: "benchmark", benchmark: benchmarksForCategory[j]});
        }

        plans = [];
        var remainingPlans = [].concat(givenPlans);
        for (var i = 0; i < cells.length; ++i) {
            var cell = cells[i];
            switch (cell.kind) {
            case "category":
                break;

            case "benchmark":
                var plan = cell.benchmark.plan;
                var index = remainingPlans.indexOf(plan);
                if (index < 0)
                    break;
                plans.push(plan);
                remainingPlans.splice(index, 1);
                break;

            default:
                throw "Bad cell kind: " + cell.king;
            }
        }

        for (var i = benchmarks.length; i--;) {
            benchmarks[i].results = [];
            benchmarks[i].times = [];
        }

        currentIteration = 0;
        currentPlan = -1;
        isRunning = false;
        hasAlreadyRun = false;
    }

    function initializeWithMode(modeLine)
    {
        reset();

        selectBenchmark = null;
        var modes = modeLine.split(",");
        for (var i = 0; i < modes.length; ++i) {
            var mode = modes[i];

            if (/benchmark=/.test(mode)) {
                selectBenchmark = RegExp.rightContext;
                continue;
            }

            switch (mode) {
            case "quick":
                numberOfIterations = 1;
                break;

            case "long":
                numberOfIterations = 7;
                break;

            default:
                numberOfIterations = 1;
                break;
            }
        }
    }

    function initialize()
    {
        initializeWithMode("");
    }

    function switchMode(mode)
    {
        window.location.hash = "#" + mode;
        initializeWithMode(mode);
    }

    function start()
    {
        reset();
        isRunning = true;
        iterate();
    }

    function allSelector(benchmark) { return true; }
    function createCategorySelector(category) {
        return function(benchmark) {
            return benchmark.category == category;
        };
    }

    function computeGeomeans(selector)
    {
        var geomeans = [];

        for (var iterationIndex = 0; ; ++iterationIndex) {
            var sum = 0;
            var numDone = 0;
            var numSelected = 0;
            var allFinished = true;
            for (var i = 0; i < benchmarks.length; ++i) {
                if (!selector(benchmarks[i]))
                    continue;
                numSelected++;
                if (iterationIndex >= benchmarks[i].results.length) {
                    allFinished = false;
                    break;
                }
                if (!(iterationIndex in benchmarks[i].results))
                    continue;
                sum += Math.log(benchmarks[i].results[iterationIndex]);
                numDone++;
            }
            if (!allFinished)
                break;
            if (numDone != numSelected)
                geomeans.length++;
            else
                geomeans.push(Math.exp(sum * (1 / numDone)));
        }
        return geomeans;
    }

    function formatGeomean(selector)
    {
        return formatResult(computeGeomeans(selector), {extraPrecision: 1});
    }

    function updateGeomeans()
    {
        for (var i = 0; i < categoryNames.length; ++i) {
            var categoryName = categoryNames[i];
            displayResultMessage(
                "geomean-" + categoryName,
                formatGeomean(createCategorySelector(categoryName)),
                "result");
        }
        displayResultMessage(
            "geomean", formatGeomean(allSelector),
            computeGeomeans(allSelector).length == numberOfIterations ? "highlighted-result" : "result");
    }

    function computeRawResults()
    {
        function rawResultsLine(values) {
            return {
                result: values,
                statistics: computeStatistics(values)
            };
        }

        var rawResults = {};
        for (var i = 0; i < benchmarks.length; ++i) {
            var line = rawResultsLine(benchmarks[i].results);
            line.times = benchmarks[i].times;
            line.category = benchmarks[i].category;
            line.reference = benchmarks[i].reference;
            rawResults[benchmarks[i].name] = line;
        }
        rawResults.geomean = rawResultsLine(computeGeomeans(allSelector));

        return rawResults;
    }

    function end()
    {
        print("Geometric-Mean," + formatGeomean(allSelector));

        isRunning = false;
        hasAlreadyRun = true;
    }

    function iterate()
    {
        ++currentPlan;

        if (currentPlan >= plans.length) {
            if (++currentIteration >= numberOfIterations) {
                end();
                return;
            } else
                currentPlan = 0;
        }


        accumulator = void 0;

        if (!isRunning)
            return;
        runCode(plans[currentPlan].code);

    }

    function reportError(message, url, lineNumber)
    {
        var plan = plans[currentPlan];
        if (!plan)
            return;
        console.error(plan.name + ": ERROR: " + url + ":" + lineNumber + ": " + message);

        for (var i = plan.benchmarks.length; i--;) {
            plan.benchmarks[i].times.length++;
            plan.benchmarks[i].results.length++;
            displayResultMessage(
                plan.benchmarks[i].name,
                formatResult(plan.benchmarks[i].results, plan.benchmarks[i]),
                "result");
        }
        iterate();
    }

    function reportResult()
    {
        var plan = plans[currentPlan];
        for (var i = plan.benchmarks.length; i--;) {
            var benchmark = plan.benchmarks[i];
            benchmark.times.push(arguments[i]);
            benchmark.results.push(100 * benchmark.reference / arguments[i]);
            displayResultMessage(
                benchmark.name,
                formatResult(benchmark.results, plan.benchmarks[i]),
                "result");
        }
        iterate();
    }

    function accumulate(data)
    {
        accumulator = data;
        if (!isRunning)
            return;
        runCode(plans[currentPlan].code);

    }

    function getAccumulator()
    {
        return accumulator;
    }

    function getPlans()
    {
        return givenPlans;
    }
    return {
        addPlan: addPlan,
        addReferences: addReferences,
        initialize: initialize,
        switchToQuick: function() { switchMode("quick") },
        switchToNormal: function() { switchMode("normal") },
        switchToLong: function() { switchMode("long") },
        start: start,
        reportResult: reportResult,
        reportError: reportError,
        accumulate: accumulate,
        getAccumulator: getAccumulator,
        goodTime: Date.now,
        getPlans: getPlans
    };
})();
