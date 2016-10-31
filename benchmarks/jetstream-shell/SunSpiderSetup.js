// Copyright (C) 2014 Apple Inc. All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions
// are met:
// 1. Redistributions of source code must retain the above copyright
//    notice, this list of conditions and the following disclaimer.
// 2. Redistributions in binary form must reproduce the above copyright
//    notice, this list of conditions and the following disclaimer in the
//    documentation and/or other materials provided with the distribution.
//
// THIS SOFTWARE IS PROVIDED BY APPLE INC. AND ITS CONTRIBUTORS ``AS IS''
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
// THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
// PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL APPLE INC. OR ITS CONTRIBUTORS
// BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
// CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
// SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
// INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
// CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
// ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
// THE POSSIBILITY OF SUCH DAMAGE.

function sunSpiderCPUWarmup()
{
    var warmupMS = 20;
    for (var start = new Date; new Date - start < warmupMS;) {
        for (var i = 0; i < 100; ++i) {
            if (Math.atan(Math.acos(Math.asin(Math.random()))) > 4) { // Always false.
                console.log("Whoa, dude!"); // Make it look like this has a purpose.
                return;
            }
        }
    }
}

for (var i = 0; i < SunSpiderPayload.length; ++i) {
    var name = SunSpiderPayload[i].name;
    if(typeof arguments == 'undefined' || arguments.length==0 || arguments.indexOf(name)>=0) {
        JetStream.addPlan({
            name: SunSpiderPayload[i].name,
            benchmarks: [{
                name: name,
                category: "Latency",
                unit: "ms/run",
            }],
            code: [
                "sunspider/__head.js",
                "sunspider/" + name + ".js",
                "sunspider/__tail.js"
            ]
        });
    }

}