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
        chromePath: process.argv[2],
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

    var path = "chrome://settings/help"

    Page.navigate({ url: path });

    // Wait for window.onload before doing stuff.
    Page.loadEventFired(async() => {

        var log_file = "./logs/log-" + Date.now() + ".txt"

        const js_res = "document.innerHTML";
        const result = await Runtime.evaluate({ expression: js_res });

        console.log(navigator.userAgent)


        // while (true) {
        //     const js_res = "document.querySelector('#result-number').innerHTML";
        //     const result = await Runtime.evaluate({ expression: js_res });
        //     const js_info = "document.querySelector('#info').innerHTML";
        //     const info = await Runtime.evaluate({ expression: js_info });
        //     console.log(info.result.value)
        //     i++
        //     fs.writeFileSync(log_file, JSON.stringify(info.result.value) + "\r\n", { flag: 'a' })
        //     if (result.result.value) {
        //         const js_detail = "document.querySelector('#detailed-results').innerHTML";
        //         const detail = await Runtime.evaluate({ expression: js_detail });
        //         //console.log(result.result.value)
        //         //console.log(detail.result.value)
        //         var arr = (convert.html(detail.result.value))
        //         arr.unshift(result.result.value)
        //             //fs.writeFileSync("./results.json", JSON.stringify(arr))
        //         console.log("Score: " + arr[0])
        //         arr[2].shift()
        //         arr[2].forEach((a) => {
        //             console.log(a['0'] + ": " + a["1"])
        //         })
        //         break;
        //     }
        //     //if (i > 5) break;
        //     await sleep(1000)
        // }

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