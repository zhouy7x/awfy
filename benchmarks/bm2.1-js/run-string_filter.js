load("string_filter/test.js");
var startTime = 0;
var counter = 0;
var operationsCount = 0;
var animateReverse = false;
var preloadDone = false;
var benchmark = {
    startTimer: function() {
        var d = new Date();
        startTime = d.getTime();
    },
    elapsedTime: function() {
        var d = new Date();
        var endTime = d.getTime();
        return endTime - startTime;
    },
    increaseCounter: function()
    {
        counter++;
    },
    increaseElapsedTime: function(milliseconds)
    {
        // To increase elapsed time we actually modify start time
        startTime = startTime - milliseconds;
    },
    run: function()
    {
        // Initialize test to receive guidance for test
        guide = test.init();

        // In case of redirect
        if (typeof guide == 'undefined')
        {
            // Do nothing
        }

        // Ensure browser can run this test
        else if (guide.isDoable == true)
        {
            // Conformity tests are ran only once
            if (guide.isConformity == true)
            {
                // Show content two seconds before execute
                test.run(true, 1);
            }
            // Other tests are ran multiple times
            else
            {
                // Start global timer
                benchmark.startTimer();

                // If test is time based, loop test.run inside while until elapsed time reach the top
                if (guide.time != null && guide.time != 0)
                {
                    while (benchmark.elapsedTime() < guide.time)
                    {
                        // run test isFinal = false
                        test.run(false, operationsCount);

                        // If test do not have any internal counter method, handle counting on main loop
                        if (guide.internalCounter == false)
                        {
                            benchmark.increaseCounter();
                        }
                        operationsCount++;
                    }
                }

                // Otherwise if test is operations based, loop test.run inside for until enough operations is done
                else
                {
                    for (operationsCount = 0; operationsCount < guide.operations; operationsCount++)
                    {
                        // run test isFinal = false
                        test.run(false, operationsCount);

                        // If test do not have any internal counter method, handle counting on main loop
                        if (guide.internalCounter == false)
                        {
                            benchmark.increaseCounter();
                        }
                    }
                }

                // Run final test run
                test.run(true, operationsCount);
            }
        }
    },
};

benchmark.run();
