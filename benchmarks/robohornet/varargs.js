// arguments instantiation is slow

var args;
var runs;
var DEFAULT_RUNS = 100000;
var NAME = "arguments instantiation";

function varargs_setUp(opt_runs) {
  runs = opt_runs || DEFAULT_RUNS;
  args = new Array(runs);
}

function reset() {
  args = new Array(runs);
}

function tearDown() {
  delete args;
}

function varargs_test() {
  for (var i = 0; i < runs; i++) {
    checkArgs(args[i], args[i], args[i]);
  }
}

function checkArgs() {
  return Array.prototype.slice.call(arguments);
}

// To make the benchmark results predictable, we replace Math.random with a
// 100% deterministic alternative.
function resetMathRandom() {
  Math.random = (function() {
    var seed = 49734321;
    return function() {
      // Robert Jenkins' 32 bit integer hash function.
      seed = ((seed + 0x7ed55d16) + (seed << 12))  & 0xffffffff;
      seed = ((seed ^ 0xc761c23c) ^ (seed >>> 19)) & 0xffffffff;
      seed = ((seed + 0x165667b1) + (seed << 5))   & 0xffffffff;
      seed = ((seed + 0xd3a2646c) ^ (seed << 9))   & 0xffffffff;
      seed = ((seed + 0xfd7046c5) + (seed << 3))   & 0xffffffff;
      seed = ((seed ^ 0xb55a4f09) ^ (seed >>> 16)) & 0xffffffff;
      return (seed & 0xfffffff) / 0x10000000;
    };
  })();
}

//function Run() {
//  print('Running ' + NAME + 'test standalone...');
//  resetMathRandom()
//  setUp();
//  var startTime = new Date().getTime();
//  test();
//  var endTime = new Date().getTime();
//  print('Ran test in ' + (endTime - startTime) + ' ms.');
//}
//
//Run();

