//var frame0 and frame1 are defined in imagedata.js
load("./imagedata.js");

var width = 512, height = 512;
var len = width * height * 4;
var k;

var source = {};
source.width = width;
source.height = height;
source.data = new Uint8ClampedArray(len);

var target = {};
target.width = width;
target.height = height;
target.data = new Uint8ClampedArray(len);

var result = {};
result.width = width;
result.height = height;
result.data = new Uint8ClampedArray(len);

for (k = 0; k < len; k++) {
	target.data[k] = parseInt(frame0[k*2] + frame0[k*2+1], 16);
	source.data[k] = parseInt(frame1[k*2] + frame1[k*2+1], 16);
}

function tween(factor) {
	var i, s, t, r;
	s = source.data;
	t = target.data;
	r = result.data;
	for (i = 0; i < len; i += 4) {
		r[i] = t[i] + (s[i] - t[i]) * factor;
		r[i + 1] = t[i + 1] + (s[i + 1] - t[i + 1]) * factor;
		r[i + 2] = t[i + 2] + (s[i + 2] - t[i + 2]) * factor;
		r[i + 3] = 255;
	}
}

var value = 0;
var cumulativeTime = 0;

function unitOfWork(k) {
	value += 0.1;
	var factor = 0.5 + 0.5 * Math.sin(value);

	var startTime = new Date();
	//console.time("cf");

	var i;
	for (i = 0; i < 30; i++)
		tween(factor);

	var time = new Date() - startTime;
	//console.timeEnd("cf");
	cumulativeTime += time;
	print(k + ": " + time + "ms");
}

for (k = 0; k < 10; k++) {
	unitOfWork(k);
}
print("total: " + cumulativeTime + "ms");
