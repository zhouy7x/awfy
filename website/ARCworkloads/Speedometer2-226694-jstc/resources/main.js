window.benchmarkClient = {
    displayUnit: 'runs/min',
    iterationCount: 10,
    stepCount: null,
    suitesCount: null,
    autoRun: false,
    _measuredValuesList: [],
    _finishedTestCount: 0,
    _progressCompleted: null,
    willAddTestFrame: function (frame) {
        var main = document.querySelector('main');
        var style = getComputedStyle(main);
        frame.style.left = main.offsetLeft + parseInt(style.borderLeftWidth) + parseInt(style.paddingLeft) + 'px';
        frame.style.top = main.offsetTop + parseInt(style.borderTopWidth) + parseInt(style.paddingTop) + 'px';
    },
    willRunTest: function (suite, test) {
        document.getElementById('info').textContent = suite.name + ' ( ' + this._finishedTestCount + ' / ' + this.stepCount + ' )';
    },
    didRunTest: function () {
        this._finishedTestCount++;
        this._progressCompleted.style.width = (this._finishedTestCount * 100 / this.stepCount) + '%';
    },
    didRunSuites: function (measuredValues) {
        this._measuredValuesList.push(measuredValues);
    },
    willStartFirstIteration: function () {
        this._measuredValuesList = [];
        this._finishedTestCount = 0;
        this._progressCompleted = document.getElementById('progress-completed');
        document.getElementById('logo-link').onclick = function (event) { event.preventDefault(); return false; }
    },
    didFinishLastIteration: function () {
        document.getElementById('logo-link').onclick = null;
        var results = this._computeResults(this._measuredValuesList, this.displayUnit);
        var suiteScores = results.suiteScores;
        var suiteTimes = results.suiteTimes;
        for (var suiteName in suiteScores)
            console.log(suiteName + "," + suiteScores[suiteName].toFixed(2) + ",Time(ms)," + suiteTimes[suiteName].toFixed(2));

        running_end = performance.now();
        var running_time = running_end - running_start;
        this._updateGaugeNeedle(results.mean);
        console.log("Arithmetic-Mean," + results.mean.toFixed(2) + "Total-Time(ms)," + results.totalTime.toFixed(2));
        document.getElementById('result-number').textContent = results.formattedMean;
        if (results.formattedDelta)
            document.getElementById('confidence-number').textContent = '\u00b1 ' + results.formattedDelta;

        this._populateDetailedResults(results.formattedValues, suiteScores, suiteTimes);
        document.getElementById('results-with-statistics').textContent = results.am_formattedMeanAndDelta;
        document.getElementById('geomean-score').textContent = results.formattedMeanAndDelta;
        document.getElementById('total-score-time').textContent = results.totalTime.toFixed(2);
        document.getElementById('total-running-time').textContent = running_time.toFixed(2);

        if (this.displayUnit == 'ms') {
            document.getElementById('show-summary').style.display = 'none';
            showResultDetails();
        } else
            showResultsSummary();
    },
    _computeResults: function (measuredValuesList, displayUnit) {
        var suitesCount = this.suitesCount;
        var iterationCount = this.iterationCount;
        function valueForUnit(measuredValues) {
            if (displayUnit == 'ms')
                return measuredValues.geomean;
            return measuredValues.score;
        }

        function totalTimeInDisplayUnit(measuredValues) {
            if (displayUnit == 'ms')
                return measuredValues.total;
            return computeScore(measuredValues.total);
        }

        function addSuiteScores(sumSuiteScores, measuredValues) {
            for (var suiteName in measuredValues.tests) {
                var sum = sumSuiteScores[suiteName] || 0.0;
                sumSuiteScores[suiteName] = sum + measuredValues.tests[suiteName].score;
            }
            return sumSuiteScores;
        }

        function addSuiteTimes(sumSuiteTimes, measuredValues) {
            for (var suiteName in measuredValues.tests) {
                var sum = sumSuiteTimes[suiteName] || 0.0;
                sumSuiteTimes[suiteName] = sum + measuredValues.tests[suiteName].total;
            }
            return sumSuiteTimes;
        }

        function sigFigFromPercentDelta(percentDelta) {
            return Math.ceil(-Math.log(percentDelta)/Math.log(10)) + 3;
        }

        function toSigFigPrecision(number, sigFig) {
            var nonDecimalDigitCount = number < 1 ? 0 : (Math.floor(Math.log(number)/Math.log(10)) + 1);
            return number.toPrecision(Math.max(nonDecimalDigitCount, Math.min(6, sigFig)));
        }

        // Compute arithmetic mean
        var am_values = measuredValuesList.map(totalTimeInDisplayUnit);
        var am_sum = am_values.reduce(function (a, b) { return a + b; }, 0);
        var am_arithmeticMean = am_sum / am_values.length;
        var am_meanSigFig = 4;
        var am_formattedDelta;
        var am_formattedPercentDelta;
        if (window.Statistics) {
            var am_delta = Statistics.confidenceIntervalDelta(0.95, am_values.length, am_sum, Statistics.squareSum(am_values));
            if (!isNaN(am_delta)) {
                var am_percentDelta = am_delta * 100 / am_arithmeticMean;
                am_meanSigFig = sigFigFromPercentDelta(am_percentDelta);
                am_formattedDelta = toSigFigPrecision(am_delta, 2);
                am_formattedPercentDelta = toSigFigPrecision(am_percentDelta, 2) + '%';
            }
        }

        var am_formattedMean = toSigFigPrecision(am_arithmeticMean, Math.max(am_meanSigFig, 3));

        //Compute sub-score and geometric mean
        var sumSuiteScores = measuredValuesList.reduce(addSuiteScores, []);
        var suiteScores = [];
        for (var suiteName in sumSuiteScores)
            suiteScores[suiteName] = sumSuiteScores[suiteName] / iterationCount;
        var sumSuiteTimes = measuredValuesList.reduce(addSuiteTimes, []);

        var totalTime = measuredValuesList.reduce(function (a, b) { return a + b.total; }, 0);
        var values = measuredValuesList.map(valueForUnit);

        var sum = values.reduce(function (a, b) { return a + b; }, 0);
        var arithmeticMean = sum / values.length;
        var meanSigFig = 4;
        var formattedDelta;
        var formattedPercentDelta;
        if (window.Statistics) {
            var delta = Statistics.confidenceIntervalDelta(0.95, values.length, sum, Statistics.squareSum(values));
            if (!isNaN(delta)) {
                var percentDelta = delta * 100 / arithmeticMean;
                meanSigFig = sigFigFromPercentDelta(percentDelta);
                formattedDelta = toSigFigPrecision(delta, 2);
                formattedPercentDelta = toSigFigPrecision(percentDelta, 2) + '%';
            }
        }

        var formattedMean = toSigFigPrecision(arithmeticMean, Math.max(meanSigFig, 3));

        return {
            totalTime: totalTime,
            formattedValues: values.map(function (value) {
                return toSigFigPrecision(value, 4) + ' ' + displayUnit;
            }),
            mean: arithmeticMean,
            formattedMean: formattedMean,
            formattedDelta: formattedDelta,
            formattedMeanAndDelta: formattedMean + (formattedDelta ? ' \xb1 ' + formattedDelta + ' (' + formattedPercentDelta + ')' : ''),
            suiteScores: suiteScores,
            suiteTimes: sumSuiteTimes,
            am_formattedMeanAndDelta: am_formattedMean + (am_formattedDelta ? ' \xb1 ' + am_formattedDelta + ' (' + am_formattedPercentDelta + ')' : ''),
        };
    },
    _addFrameworksRow: function (table, name, cb) {
        var row = document.createElement('tr');
        var th = document.createElement('th');
        th.textContent = name;
        row.appendChild(th);
        row.appendChild(cb);
        table.appendChild(row);
    },
    _addDetailedResultsRow: function (table, iterationNumber, value) {
        var row = document.createElement('tr');
        var th = document.createElement('th');
        th.textContent = 'Iteration ' + (iterationNumber + 1);
        var td = document.createElement('td');
        td.textContent = value;
        row.appendChild(th);
        row.appendChild(td);
        table.appendChild(row);
    },
    _addSuiteScoresRow: function (table, suite, value, time) {
        if (table.innerHTML == '') {
            var row = document.createElement('tr');
            var th = document.createElement('th');
            var td1 = document.createElement('td');
            var td2 = document.createElement('td');
            th.textContent = "Subcase";
            td1.textContent = "Score (runs/min)";
            td2.textContent = "Time (ms)";
            row.appendChild(th);
            row.appendChild(td1);
            row.appendChild(td2);
            table.appendChild(row);
        }
        var row = document.createElement('tr');
        var th = document.createElement('th');
        var td1 = document.createElement('td');
        var td2 = document.createElement('td');
        th.textContent = suite;
        td1.textContent = value;
        td2.textContent = time;
        row.appendChild(th);
        row.appendChild(td1);
        row.appendChild(td2);
        table.appendChild(row);
    },
    _prepareFrameworks: function () {
        var singleSuiteRun = '';
        if (location.search.length > 1) {
            var parts = location.search.substring(1).split('&');
            for (var i = 0; i < parts.length; i++) {
                var keyValue = parts[i].split('=');
                var key = keyValue[0];
                var value = keyValue[1];
                switch (key) {
                case 'auto':
                    if (value == '1')
                        this.autoRun = true;
                    break;
                case 'suite':
                    if (enableOneSuite(Suites, value))
                        singleSuiteRun = value.toLowerCase();
                    break;
                }
            }
        }

        var frameworksTables = document.querySelectorAll('.frameworks-table');
        frameworksTables[0].innerHTML = '';
        for (var i = 0; i < Suites.length; i++) {
            Suites[i].checkbox = document.createElement("INPUT");
            Suites[i].checkbox.setAttribute("type", "checkbox");
            if (singleSuiteRun)
                Suites[i].checkbox.checked = singleSuiteRun == Suites[i].name.toLowerCase() ? true : false;
            else
                Suites[i].checkbox.checked = !Suites[i].disabled;
            this._addFrameworksRow(frameworksTables[0], Suites[i].name, Suites[i].checkbox);
        }
    },
    _updateGaugeNeedle: function (rpm) {
        var needleAngle = Math.max(0, Math.min(rpm, 140)) - 70;
        var needleRotationValue = 'rotate(' + needleAngle + 'deg)';

        var gaugeNeedleElement = document.querySelector('#summarized-results > .gauge .needle');
        gaugeNeedleElement.style.setProperty('-webkit-transform', needleRotationValue);
        gaugeNeedleElement.style.setProperty('-moz-transform', needleRotationValue);
        gaugeNeedleElement.style.setProperty('-ms-transform', needleRotationValue);
        gaugeNeedleElement.style.setProperty('transform', needleRotationValue);
    },
    _populateDetailedResults: function (formattedValues, suiteScores, suiteTimes) {
        var resultsTables = document.querySelectorAll('.results-table');
        resultsTables[0].innerHTML = '';
        for (var i = 0; i < formattedValues.length; i++)
            this._addDetailedResultsRow(resultsTables[0], i, formattedValues[i]);
        resultsTables[1].innerHTML = '';
        for (var suit in suiteScores)
            this._addSuiteScoresRow(resultsTables[1], suit, suiteScores[suit].toFixed(2), suiteTimes[suit].toFixed(2));
    },
    prepareUI: function () {
        this._prepareFrameworks();
        window.addEventListener('popstate', function (event) {
            if (event.state) {
                var sectionToShow = event.state.section;
                if (sectionToShow) {
                    var sections = document.querySelectorAll('main > section');
                    for (var i = 0; i < sections.length; i++) {
                        if (sections[i].id === sectionToShow)
                            return showSection(sectionToShow, false);
                    }
                }
            }
            return showSection('home', false);
        }, false);

        function updateScreenSize() {
            // FIXME: Detect when the window size changes during the test.
            var screenIsTooSmall = window.innerWidth < 850 || window.innerHeight < 650;
            document.getElementById('screen-size').textContent = window.innerWidth + 'px by ' + window.innerHeight + 'px';
            document.getElementById('screen-size-warning').style.display = screenIsTooSmall ? null : 'none';
        }

        window.addEventListener('resize', updateScreenSize);
        updateScreenSize();
    }
}

function enableOneSuite(suites, suiteToEnable)
{
    suiteToEnable = suiteToEnable.toLowerCase();
    var found = false;
    for (var i = 0; i < suites.length; i++) {
        var currentSuite = suites[i];
        if (currentSuite.name.toLowerCase() == suiteToEnable) {
            currentSuite.disabled = false;
            found = true;
        } else
            currentSuite.disabled = true;
    }
    return found;
}

function startBenchmark() {
    for (var i = 0; i < Suites.length; i++)
        Suites[i].disabled = !Suites[i].checkbox.checked;

    if (location.search.length > 1) {
        var parts = location.search.substring(1).split('&');
        for (var i = 0; i < parts.length; i++) {
            var keyValue = parts[i].split('=');
            var key = keyValue[0];
            var value = keyValue[1];
            switch (key) {
            case 'unit':
                if (value == 'ms')
                    benchmarkClient.displayUnit = 'ms';
                else
                    console.error('Invalid unit: ' + value);
                break;
            case 'iterationCount':
                var parsedValue = parseInt(value);
                if (!isNaN(parsedValue))
                    benchmarkClient.iterationCount = parsedValue;
                else
                    console.error('Invalid iteration count: ' + value);
                break;
            case 'suite':
                if (!enableOneSuite(Suites, value)) {
                    alert('Suite "' + value + '" does not exist. No tests to run.');
                    return false;
                }
                break;
            }
        }
    }

    var enabledSuites = Suites.filter(function (suite) { return !suite.disabled; });
    var totalSubtestsCount = enabledSuites.reduce(function (testsCount, suite) { return testsCount + suite.tests.length; }, 0);
    benchmarkClient.stepCount = benchmarkClient.iterationCount * totalSubtestsCount;
    benchmarkClient.suitesCount = enabledSuites.length;
    var runner = new BenchmarkRunner(Suites, benchmarkClient);
    runner.runMultipleIterations(benchmarkClient.iterationCount);

    return true;
}

function computeScore(time) {
    return 60 * 1000 * benchmarkClient.suitesCount / time;
}

function showSection(sectionIdentifier, pushState) {
    var currentSectionElement = document.querySelector('section.selected');
    console.assert(currentSectionElement);

    var newSectionElement = document.getElementById(sectionIdentifier);
    console.assert(newSectionElement);

    currentSectionElement.classList.remove('selected');
    newSectionElement.classList.add('selected');

    if (pushState)
        history.pushState({section: sectionIdentifier}, document.title);
}

function showHome() {
    showSection('home', true);
}

function startTest() {
    running_start = performance.now();
    if (startBenchmark())
        showSection('running');
}

function showResultsSummary() {
    showSection('summarized-results', true);
}

function showResultDetails() {
    showSection('detailed-results', true);
}

function showFrameworks() {
    showSection('frameworks', true);
}

function defaultFrameworks() {
    for (var i = 0; i < Suites.length; i++)
        Suites[i].checkbox.checked = Suites[i].name == "FlightJS-MailClient" ? false : true;
}

function clearFrameworks() {
    for (var i = 0; i < Suites.length; i++)
        Suites[i].checkbox.checked = false;
}

function showAbout() {
    showSection('about', true);
}

window.addEventListener('DOMContentLoaded', function () {
    if (benchmarkClient.prepareUI)
        benchmarkClient.prepareUI();
    if (benchmarkClient.autoRun)
        startTest();
});
