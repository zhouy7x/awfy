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
        port: 9223, // Uncomment to force a specific port of your choice.
        chromePath: process.argv[3] || '/opt/google/chrome/google-chrome',
        chromeFlags: [
            '--window-size=412,732',
            '--disable-gpu',
            '--no-sandbox',
            "--enable-logging",
            '--headless',
            process.argv[4] ? '--js-flags='+process.argv[4] : ''
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
    var path2 = "http://user-awfy.sh.intel.com:8080/awfy/ARCworkloads/JetStream2-JSTC/"
    var path3 = "http://user-awfy.sh.intel.com/awfy/ARCworkloads/Speedometer-Angular/Speedometer/Full.html"

    Page.navigate({ url: path });

    // Wait for window.onload before doing stuff.
    Page.loadEventFired(async() => {
        await sleep(1000);
	    var i = 0;
        while (true) {
            console.log('loading page ...')
            const js_prepare = "document.querySelector('#status a').innerHTML";
            await sleep(1000);
            const status = await Runtime.evaluate({ expression: js_prepare });
            if (status.result.value == "Start Test") {
                console.log(status.result.value);
                break
            } else {
                if (i > 60) break ;
                // console.log(i);
                i++;
            }
        }
        if (i <= 6) {

            const js = "JetStream.start()";
            await Runtime.evaluate({ expression: js });

            var log_file = "./logs/log-" + Date.now() + ".txt"
            var tmp = undefined;
            while (true) {
                await sleep(1000);
                const js_res = "document.querySelector('#result-summary .score').innerHTML";
                const result = await Runtime.evaluate({ expression: js_res });
                const js_info = "document.querySelector('#results .benchmark-done h3.benchmark-name a').innerHTML";
                const info = await Runtime.evaluate({ expression: js_info });
                // console.log(info.result.value);
                if (tmp != info.result.value) {
                    tmp = await info.result.value;
                    console.log("Running " + tmp + " ...");
                }
                // console.log(detail2.result.value)
                i++;
                if (result.result.value == undefined) continue
                // console.log(result.result.value)
                console.log("Score: " + result.result.value)
                var j = 0;
                // fs.writeFileSync(log_file, JSON.stringify(info.result.value) + "\r\n", { flag: 'a' })
                if (result.result.value) {
                    while (true) {
                        const js_detail = "document.querySelectorAll('div.benchmark-done')["+j+"].innerHTML";
                        const detail = await Runtime.evaluate({ expression: js_detail });
                        //console.log(result.result.value)

                        if (detail.result.value == undefined) break
                        // console.log(detail.result.value)
                        j++;

                        var arr = (convert.regex(detail.result.value))

                        if (arr == undefined) {
                            fs.writeFileSync(log_file, 'Wrong data!' + "\r\n", { flag: 'a' });
                            console.log('Wrong data!');
                        } else {
                            fs.writeFileSync(log_file, arr[0] + ": " + arr[1] + "\r\n", { flag: 'a' });
                            console.log(arr[0] + ": " + arr[1]);
                        }
                    } break;
                    // var arr = (convert.html(detail.result.value))

                    // arr.unshift(result.result.value)
                    // console.log(arr)
                    //     //fs.writeFileSync("./results.json", JSON.stringify(arr))
                    // console.log("Score: " + arr[0])
                    // fs.writeFileSync(log_file, arr[0] + "\r\n", { flag: 'a' })
                    // arr[2].shift()
                    // arr[2].forEach((a) => {
                    //     fs.writeFileSync(log_file, a['0'] + ": " + a["1"] + "\r\n", { flag: 'a' })
                    //     console.log(a['0'] + ": " + a["1"])
                    // })
                    // break;
                }
                //if (i > 5) break;
            }
        } else {
            console.log('loading page failed, killed.')
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
