"use strict";
exports.__esModule = true;
var fs = require("fs");
var readline = require('readline');
var json = require('../package.json'); // Package json as a json object
var dependencies = json.dependencies; // Dependencies as a json object
var count = Object.keys(dependencies).length; // Number of dependencies in package.json
var rl = readline.createInterface({
    input: fs.createReadStream('src/license.txt')
});
rl.on('line', function (line) {
    count += 1;
});
console.log(count + ' dependencies installed.');
