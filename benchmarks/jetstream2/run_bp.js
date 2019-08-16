#!/home/user/.nvm/versions/node/v8.1.2/bin/node


const CDP = require('chrome-remote-interface');

const chromeLauncher = require('chrome-launcher');

const fs = require('fs')

const convert = require('./convert')

// Optional: set logging level of launcher to see its output.
// Install it using: yarn add lighthouse-logger
// const log = require('lighthouse-logger');
// log.setLevel('info');

/**
 * Launches a debugging instance of Chrome.
 * @param {boolean=} headless True (default) launches Chrome in headless mode.
 *     False launches a full version of Chrome.
 * @return {Promise<ChromeLauncher>}
 */
function launchChrome(headless = true) {
    return chromeLauncher.launch({
        port: 9222, // Uncomment to force a specific port of your choice.
        chromePath: process.argv[3] || '/opt/google/chrome/google-chrome',
        chromeFlags: [
            '--window-size=412,7as32',
            '--disable-gpu',
            '--no-sandbox',
            "--enable-logging",
            '--headless'
        ]
    });
}
(async function() {

    const chrome = await launchChrome();
    const protocol = await CDP({ port: chrome.port });

    // Extract the DevTools protocol domains we need and enable them.
    // See API docs: https://chromedevtools.github.io/devtools-protocol/
    const { Page, Runtime } = protocol;
    await Promise.all([Page.enable(), Runtime.enable()]);

    var path = process.argv[2]
    var path2 = "http://user-awfy.sh.intel.com/awfy/ARCworkloads/Speedometer/Speedometer/Full.html"
    var path3 = "http://user-awfy.sh.intel.com/awfy/ARCworkloads/Speedometer-Angular/Speedometer/Full.html"

    Page.navigate({ url: path });

    // Wait for window.onload before doing stuff.
    Page.loadEventFired(async() => {
        const js = "startTest()";
        await Runtime.evaluate({ expression: js });

        // var arr = ["138", [{ "0": "Iteration 1", "1": "130.1 runs/min" }, { "0": "Iteration 2", "1": "129.1 runs/min" }, { "0": "Iteration 3", "1": "124.9 runs/min" }, { "0": "Iteration 4", "1": "140.5 runs/min" }, { "0": "Iteration 5", "1": "139.4 runs/min" }, { "0": "Iteration 6", "1": "140.4 runs/min" }, { "0": "Iteration 7", "1": "142.7 runs/min" }, { "0": "Iteration 8", "1": "140.2 runs/min" }, { "0": "Iteration 9", "1": "140.1 runs/min" }, { "0": "Iteration 10", "1": "140.4 runs/min" }, { "0": "Iteration 11", "1": "139.1 runs/min" }, { "0": "Iteration 12", "1": "138.2 runs/min" }, { "0": "Iteration 13", "1": "138.2 runs/min" }, { "0": "Iteration 14", "1": "138.2 runs/min" }, { "0": "Iteration 15", "1": "140.9 runs/min" }, { "0": "Iteration 16", "1": "144.5 runs/min" }, { "0": "Iteration 17", "1": "138.0 runs/min" }, { "0": "Iteration 18", "1": "139.0 runs/min" }, { "0": "Iteration 19", "1": "138.3 runs/min" }, { "0": "Iteration 20", "1": "140.5 runs/min" }],
        //     [{ "0": "Subcase", "1": "Score (runs/min)", "2": "Time (ms)" }, { "0": "VanillaJS-TodoMVC", "1": "350.31", "2": "3457.03" }, { "0": "Vanilla-ES2015-TodoMVC", "1": "303.86", "2": "4002.61" }, { "0": "Vanilla-ES2015-Babel-Webpack-TodoMVC", "1": "305.88", "2": "3955.50" }, { "0": "React-TodoMVC", "1": "129.33", "2": "9299.66" }, { "0": "React-Redux-TodoMVC", "1": "109.16", "2": "11011.69" }, { "0": "EmberJS-TodoMVC", "1": "36.10", "2": "33251.16" }, { "0": "BackboneJS-TodoMVC", "1": "373.49", "2": "3228.58" }, { "0": "AngularJS-TodoMVC", "1": "122.49", "2": "9851.93" }, { "0": "Angular2-TypeScript-TodoMVC", "1": "435.43", "2": "2782.17" }, { "0": "VueJS-TodoMVC", "1": "942.39", "2": "1293.21" }, { "0": "jQuery-TodoMVC", "1": "81.81", "2": "14707.78" }, { "0": "Preact-TodoMVC", "1": "1330.93", "2": "924.14" }, { "0": "Inferno-TodoMVC", "1": "71.11", "2": "16880.64" }, { "0": "Elm-TodoMVC", "1": "113.87", "2": "10584.12" }, { "0": "Flight-TodoMVC", "1": "231.85", "2": "5231.45" }]
        // ]

        // console.log("Score: " + arr[0])
        // arr[2].shift()
        // arr[2].forEach((a) => {
        //     console.log(a['0'] + ": " + a["1"])
        // })

        var i = 0;

        // while (true) {
        //     console.log(i++)
        //     if (i > 10) {
        //         break;
        //     }
        //     await sleep(1000)
        // }

        var log_file = "./logs/log-" + Date.now() + ".txt"
            //await sleep(10000)


        while (true) {
            const js_res = "document.querySelector('#result-number').innerHTML";
            const result = await Runtime.evaluate({ expression: js_res });
            const js_info = "document.querySelector('#info').innerHTML";
            const info = await Runtime.evaluate({ expression: js_info });
            console.log(info.result.value)
            if (info.result.value == undefined) break
            i++
            fs.writeFileSync(log_file, JSON.stringify(info.result.value) + "\r\n", { flag: 'a' })
            if (result.result.value) {
                const js_detail = "document.querySelector('#detailed-results').innerHTML";
                const detail = await Runtime.evaluate({ expression: js_detail });
                //console.log(result.result.value)
                //console.log(detail.result.value)
                var arr = (convert.html(detail.result.value))
                arr.unshift(result.result.value)
                    //fs.writeFileSync("./results.json", JSON.stringify(arr))
                console.log("Score: " + arr[0])
                fs.writeFileSync(log_file, arr[0] + "\r\n", { flag: 'a' })
                arr[2].shift()
                arr[2].forEach((a) => {
                    fs.writeFileSync(log_file, a['0'] + ": " + a["1"] + "\r\n", { flag: 'a' })
                    console.log(a['0'] + ": " + a["1"])
                })
                break;
            }
            //if (i > 5) break;
            await sleep(1000)
        }

        protocol.close();
        chrome.kill(); // Kill Chrome.

    })


})().catch(function(err) { console.log('err', err) });

function sleep(time) {
    return new Promise(function(resolve) {
        setTimeout(function() {
            resolve();
        }, time);
    })
};