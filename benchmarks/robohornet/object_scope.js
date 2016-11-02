// Object Scope Access Test
var NAME = "Object Scope Access Test";

// This test is pretty slow in Chrome, a lot faster in Opera and even faster in Firefox.
function ClassWithThisEverywhere(n) {
  this.a = 1, this.sum = 0, this.count = n || 10000000;
  this.unnamed = function() {
    for (var i = 0; i < this.count; i++) this.sum += this.a;
  }
  this.named = function calcWithThisEverywhere() {
    for (var i = 0; i < this.count; i++) this.sum += this.a;
  }
}

// This test runs relatively fast in Chrome and Firefox. This is the only test with a difference between the
// unnamed and named versions. The named version is horribly slow in Opera.
function ClassWithoutThis(n) {
  var a = 1, sum = 0, count = n || 10000000;
  this.unnamed = function() {
    for (var i = 0; i < count; i++) sum += a;
  }
  this.named = function calcWithoutThis() {
    for (var i = 0; i < count; i++) sum += a;
  }
}

// This is the fastest of the three tests in all browsers.
function ClassLocal(n) {
  this.unnamed = function() {
    var a = 1, sum = 0, count = n || 10000000;
    for (var i = 0; i < count; i++) sum += a;
  }
  this.named = function calcLocal() {
    var a = 1, sum = 0, count = n || 10000000;
    for (var i = 0; i < count; i++) sum += a;
  }
}

// Benchmark stuff and a bit eye candy...
//function setUp(n) {
function object_scope_setUp(n) {
// print("object_scope_setUp: n is:"+n+"   --\n");
  objectWithThisEverywhere = new ClassWithThisEverywhere(n);
  objectWithoutThis = new ClassWithoutThis(n);
  objectLocal = new ClassLocal(n);
}

function prettyTest(id, t) {
  var t1 = new Date().getTime();
  if (!this.times) {
    this.times = [];
  }

  if (typeof id !== 'undefined') {
    this.times[id] = t1 - t;
  }
  var min = -1, max = -1;
  for (var i = this.times.length; i--; ) {
    min = min < 0 ? this.times[i] : Math.min(min, this.times[i]);
    max = Math.max(max, this.times[i]);
  }
  for (var i = this.times.length; i--; ) {
    //var e = document.getElementById('id' + i);
    var e;
    if (this.times.length < 6) {
      //e.firstChild.data = this.times[i] ? this.times[i] + ' ms' : '?';
      e = this.times[i] ? this.times[i] + ' ms' : '?';
    } else {
      //e.firstChild.data = this.times[i] ? Math.round(this.times[i] * 10 / min) * 10 + ' percent of the time' : '?';
      e = this.times[i] ? Math.round(this.times[i] * 10 / min) * 10 + ' percent of the time' : '?';
    }

    if (this.times[i] > min * 6) {
      e.className = 'bad';
    } else if (this.times[i] < min * 2) {
      e.className = 'top';
    } else {
      e.className = '';
    }
  }
  return new Date().getTime();
}

//function test() {
function object_scope_test() {
//  var startTime = new Date().getTime();
  var t = prettyTest();
  objectWithThisEverywhere.unnamed();
  t = prettyTest(0, t);
  objectWithThisEverywhere.named();
  t = prettyTest(1, t);
  objectWithoutThis.unnamed();
  t = prettyTest(2, t);
  objectWithoutThis.named();
  t = prettyTest(3, t);
  objectLocal.unnamed();
  t = prettyTest(4, t);
  objectLocal.named();
  prettyTest(5, t);
//  var endTime = new Date().getTime();
//  print('Ran test in ' + (endTime - startTime) + ' ms.');
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
