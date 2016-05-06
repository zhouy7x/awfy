BenchmarkSuite.scores = [];
var __suite = BenchmarkSuite.suites[0];
for (var __thing = __suite.RunStep({}); __thing; __thing = __thing());
JetStream.reportResult(BenchmarkSuite.GeometricMean(__suite.results) / 1000);
