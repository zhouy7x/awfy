var tabletojson = require('tabletojson');
var fs = require("fs")

var html = function (html) {

    var str = html.replace(/th/g, "td")
    var tablesAsJson = tabletojson.convert(str);
    return (tablesAsJson)
}

var file = function (path) {

    var html = fs.readFileSync(path).toString().replace(/th/g, "td")
    var tablesAsJson = tabletojson.convert(html);
    return (tablesAsJson)
}

var regex = function (myStr) {
    // var data = [];
    let regex1 = new RegExp('<h3 class="benchmark-name"><a href=".+?">(.+?)</a></h3>');
    let regex2 = new RegExp('<h4 class="score" id=".+?">(.+?)</h4>');
    let text1 = regex1.exec(myStr);
    let text2 = regex2.exec(myStr);

    if (text1 == null) {
        return
    } else {
        text1 = text1[1]
    }; 
    if (text2 == null) {
        return
    } else {
        text2 = text2[1]
    }; 

    // console.log([text1, text2]);
    return [text1, text2]
}

exports.html = html
exports.file = file
exports.regex = regex
