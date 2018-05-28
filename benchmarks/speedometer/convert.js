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

exports.html = html

exports.file = file