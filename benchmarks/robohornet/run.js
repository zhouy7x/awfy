load("object_scope.js");
load("property_accessors.js");
load("varargs.js");
load("robohornet.js");
load("benchmarks.json");
load("benchmark.js");

var __robohornet__ = new robohornet.Runner(ROBOHORNET_DATA);
__robohornet__.run();
//__robohornet__.benchmarkLoaded();
