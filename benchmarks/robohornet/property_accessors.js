// ES5 Property Accessors

"use strict"
var TIMES = 1e5;
var OBJ;
var NAME = "ES5 Property Accessors";

//function setUp() {
function property_accessors_setUp() {
  OBJ = {
    prop: 1,
    get bar() {
      return this.prop;
    },
    set bar(value) {
      this.prop = value;
    }
  };
}

function reset() {
  if (!OBJ) return;
  OBJ.prop = 1;
}

function test_get() {
  for (var i = 0; i < TIMES; i++) {
    var x = OBJ.bar + 1;
  }
}

function test_set() {
  for (var i = 0; i < TIMES; i++) {
    OBJ.bar = 42;
  }
}

function test_combined() {
  for (var i = 0; i < TIMES; i++) {
    OBJ.bar = OBJ.bar + 1;
  }
}

//function test(opt_mode) {
function property_accessors_test(opt_mode) {
  switch(opt_mode) {
    case 'GET':
      test_get();
      break;
    case 'SET':
      test_set();
      break;
    default:
      test_combined();
      break;
  }
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
//  test('GET');
//  test('SET');
//  test();
//  var endTime = new Date().getTime();
//  print('Ran test in ' + (endTime - startTime) + ' ms.');
//}
//
//Run();

