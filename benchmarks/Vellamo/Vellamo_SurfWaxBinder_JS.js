var AVGRUNS = 4;

var c2d;
var cameraFrame;
var canvasElement;

var prImageData = {};

var outputImageData = {};

var summary;

function init() {
  'use strict';
  summary = {};

  outputImageData.width = 200;
  outputImageData.height = 200;
  outputImageData.data = new Uint8ClampedArray(200 * 200 * 4);

  prImageData.width = 200;
  prImageData.height = 200;
  prImageData.data = new Uint8ClampedArray(200 * 200 * 4);

  execute("jsarray_sweep_mrps");
}

function execute(what) {
  'use strict';
  start(what);
}

var _runs;
var _aggregated;
function reset() {
  'use strict';
  _aggregated = 0;
  _runs = 0;
}

var clearMessage = true;
var runTimes = 1;
var tests = {
  "jsarray_sweep_mrps": testSequentialJSArrayRead,
  "jsarray_single_mrps": testSingleJSArrayRead,
  "jsarray_sweep_mwps": testSequentialJSArrayWrite,
  "jsarray_single_mwps": testSingleJSArrayWrite,
  "jsarray_sweep_mcps": testSequentialJSArrayCopy,
  "imagedata_seq_mrps": testSequentialPixelRead,
  "imagedata_seq_mwps": testSequentialPixelWrite
};
var testNames = {
  "jsarray_sweep_mrps": "Array sweep",
  "jsarray_single_mrps": "Array cell",
  "jsarray_sweep_mwps": "Array fill",
  "jsarray_single_mwps": "Array assign",
  "jsarray_sweep_mcps": "Array copy",
  "imagedata_seq_mrps": "ImageData sweep",
  "imagedata_seq_mwps": "ImageData fill"
};

function start(state) {
  'use strict';
  var result;

  reset();

  result = tests[state](-1);

  runTimes += 1;

  summary[state] = result;

  if (state === "jsarray_sweep_mrps") { execute("jsarray_single_mrps"); }
  else if (state === "jsarray_single_mrps") { execute("jsarray_sweep_mwps"); }
  else if (state === "jsarray_sweep_mwps") { execute("jsarray_single_mwps"); }
  else if (state === "jsarray_single_mwps") { execute("jsarray_sweep_mcps"); }
  else if (state === "jsarray_sweep_mcps") { execute("imagedata_seq_mrps"); }
  else if (state === "imagedata_seq_mrps") { execute("imagedata_seq_mwps"); }
  else { endWithResultsJSON(summary); }
}

function toMillionRounded(number) {
  'use strict';
  return Math.round(number / 10000) / 100;
}

function sequentialPixelReadLoop(aData) {
  'use strict';
  var i, sum = 0;
  for (i = 0; i < 100000; i += 4) {
    sum += aData[i] + aData[i + 1] + aData[i + 2] + aData[i + 3];
  }
  return sum;
}

function testSequentialPixelRead(sumIn) {
  'use strict';
  var sum, aData, numAccesses, final_time, initial_time;

  if (sumIn < 0) {
    reset();
    //c2d.clearRect(0, 0, canvasElement.width, canvasElement.height);
  }
  if (_runs >= AVGRUNS) {
    return toMillionRounded(_aggregated/AVGRUNS);
  }

  aData = prImageData.data;
  numAccesses = 0;
  initial_time = new Date().getTime();
  do {
    sum = sequentialPixelReadLoop(aData);
    numAccesses += 100000;
    final_time = new Date().getTime();
  } while (final_time - initial_time <= 300);

  _aggregated += 1000 * numAccesses / (final_time - initial_time);
  _runs += 1;

  return testSequentialPixelRead(sum);
}

function sequentialPixelAssignmentLoop(aData) {
  'use strict';
  var i, sum = 255;
  for (i = 0; i < 100000; i += 4) {
    aData[i] = sum;
    aData[i + 1] = sum;
    aData[i + 2] = sum;
    aData[i + 3] = sum;
  }
}
function testSequentialPixelWrite(sumIn) {
  'use strict';
  var aData, numAccesses, final_time, initial_time;

  if (sumIn < 0) {
    reset();
    //c2d.clearRect(0, 0, canvasElement.width, canvasElement.height);
  }
  if (_runs >= AVGRUNS) {
    return toMillionRounded(_aggregated/AVGRUNS);
  }

  aData = prImageData.data;
  numAccesses = 0;
  initial_time = new Date().getTime();
  do {
    sequentialPixelAssignmentLoop(aData);
    numAccesses += 100000;
    final_time = new Date().getTime();
  } while (final_time - initial_time <= 300);

  _aggregated += 1000 * numAccesses / (final_time - initial_time);
  _runs += 1;

  return testSequentialPixelWrite(0);
}

function sequentialArrayReadLoop(aData) {
  'use strict';
  var i, sum = 0;
  for (i = 0; i < 100000; i += 4) {
    sum += aData[i] + aData[i + 1] + aData[i + 2] + aData[i + 3];
  }
  return sum;
}
function testSequentialJSArrayRead(sumIn) {
  'use strict';
  var sum, i, aData, numAccesses, final_time, initial_time;

  if (sumIn < 0) {
    reset();
    //c2d.clearRect(0, 0, canvasElement.width, canvasElement.height);
  }
  if (_runs >= AVGRUNS ) {
    return toMillionRounded(_aggregated/AVGRUNS);
  }

  aData = [];
  numAccesses = 0;

  // Populate an array with values
  for (i = 0; i < 100000; i += 1) {
    aData[i] = i; //Math.random() * 10 + 1;
  }
  initial_time = new Date().getTime();
  do {
    sum = sequentialArrayReadLoop(aData);
    numAccesses += 100000;
    final_time = new Date().getTime();
  } while (final_time - initial_time <= 300);

  _aggregated += 1000 * numAccesses / (final_time - initial_time);
  _runs += 1;

  return testSequentialJSArrayRead(sum);
}

function sequentialArrayAssignmentLoop(aData) {
  'use strict';
  var i;
  for (i = 0; i < 100000; i += 4) {
    aData[i] = i;
    aData[i + 1] = 1;
    aData[i + 2] = 2;
    aData[i + 3] = 3;
  }
}
function testSequentialJSArrayWrite(sumIn) {
  'use strict';
  var i, aData, numAccesses, final_time, initial_time;

  if (sumIn < 0) {
    reset();
    //c2d.clearRect(0, 0, canvasElement.width, canvasElement.height);
  }
  if (_runs >= AVGRUNS ) {
    return toMillionRounded(_aggregated/AVGRUNS);
  }

  aData = [];
  numAccesses = 0;

  // Populate an array with 0
  for (i = 0; i < 100000; i += 1) {
    aData[i] = 0;
  }
  initial_time = new Date().getTime();
  do {
    sequentialArrayAssignmentLoop(aData);
    numAccesses += 100000;
    final_time = new Date().getTime();
  } while (final_time - initial_time <= 300);

  _aggregated += 1000 * numAccesses / (final_time - initial_time);
  _runs += 1;

  return testSequentialJSArrayWrite(0);
}

function sequentialArrayCopyLoop(aData1, aData2) {
  'use strict';
  var i;
  for (i = 0; i < 100000; i += 1) {
    aData2[i] = aData1[i];
  }
}
function testSequentialJSArrayCopy(sumIn) {
  'use strict';
  var i, aData1, aData2, numAccesses, final_time, initial_time;

  if (sumIn < 0) {
    reset();
    //c2d.clearRect(0, 0, canvasElement.width, canvasElement.height);
  }
  if (_runs >= AVGRUNS ) {
    return toMillionRounded(_aggregated/AVGRUNS);
  }

  aData1 = [];
  aData2 = [];
  numAccesses = 0;

  // Populate arrays
  for (i = 0; i < 100000; i += 1) {
    aData1[i] = i;
    aData2[i] = 0;
  }
  initial_time = new Date().getTime();
  do {
    sequentialArrayCopyLoop(aData1, aData2);
    numAccesses += 100000;
    final_time = new Date().getTime();
  } while (final_time - initial_time <= 300);

  _aggregated += 1000 * numAccesses / (final_time - initial_time);
  _runs += 1;

  return testSequentialJSArrayCopy(0);
}

function nonsequentialArrayReadLoop(initSum, aData) {
  'use strict';
  var i, sum = initSum;
  for (i = 0; i < 100000; i += 1) {
    sum += aData[sum];  //sum is always zero, but this forces compiler to emit code to always load element
  }
  return sum;
}
function testSingleJSArrayRead(sumIn) {
  'use strict';
  var sum, i, aData, numAccesses, final_time, initial_time;

  if (sumIn < 0) {
    reset();
    //c2d.clearRect(0, 0, canvasElement.width, canvasElement.height);
  }
  if (_runs >= AVGRUNS) {
    return toMillionRounded(_aggregated/AVGRUNS);
  }

  aData = [];
  numAccesses = 0;

  // Populate an array with 0
  for (i = 0; i < 4; i += 1) {
    aData[i] = 0;
  }

  initial_time = new Date().getTime();
  do {
    sum = nonsequentialArrayReadLoop(0, aData);
    numAccesses += 100000;
    final_time = new Date().getTime();
  } while (final_time - initial_time <= 300);

  _aggregated += 1000 * numAccesses / (final_time - initial_time);
  _runs += 1;

  return testSingleJSArrayRead(sum);
}

function nonsequentialArrayAssignmentLoop(initIndex, aData) {
  'use strict';
  var i, baseIndex = initIndex;
  // In order to not be overly optimizable, use 4 elements, far enough apart to not be in same cache line
  for (i = 0; i < 100000; i += 4) {
    aData[baseIndex] = i;
    aData[baseIndex+1000] = i+1;
    aData[baseIndex+2000] = i+2;
    aData[baseIndex+3000] = i+3;
    baseIndex = (baseIndex << 1);  //baseIndex is always zero, but we want compiler to think it might be changing
  }
}
function testSingleJSArrayWrite(sumIn) {
  'use strict';
  var i, aData, numAccesses, final_time, initial_time;

  if (sumIn < 0) {
    reset();
    //c2d.clearRect(0, 0, canvasElement.width, canvasElement.height);
    sumIn = 0;
  }
  if (_runs >= AVGRUNS) {
    return toMillionRounded(_aggregated/AVGRUNS);
  }

  aData = [];
  numAccesses = 0;

  // Populate an array with 0
  for (i = 0; i < 4000; i += 1) {
    aData[i] = 0;
  }

  initial_time = new Date().getTime();
  do {
    nonsequentialArrayAssignmentLoop(0, aData);
    numAccesses += 100000;
    final_time = new Date().getTime();
  } while (final_time - initial_time <= 300);

  _aggregated += 1000 * numAccesses / (final_time - initial_time);
  _runs += 1;

  return testSingleJSArrayWrite(0);
}

function endWithResultsJSON(summary) {
  var attr;
  for(attr in summary) {
    print(attr + " " + summary[attr] + "\n");
  }
}

init();

