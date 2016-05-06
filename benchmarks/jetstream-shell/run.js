load("./SunSpiderPayload.js");
load("./SimplePayload.js");
load("./JetStreamDriver.js");
load("./SunSpiderSetup.js");
load("./SimpleSetup.js");
load("./OctaneSetup.js");
load("./Octane2Setup.js");
load("./CDjsSetup.js");
load("./Reference.js");

if (JetStream.getPlans().length==0) {
    print("Wrong sub-case is selected!");
    print("Usage: ./d8 run.js -- [subcase]");
    quit(-1);
}else {
    JetStream.initialize();
    JetStream.start();    
}

