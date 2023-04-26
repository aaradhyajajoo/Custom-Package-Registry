"use strict";
exports.__esModule = true;
var child_process_1 = require("child_process");
var commands = ['bash lattest.sh', 'bash lattest.sh', 'bash lattest.sh', 'bash lattest.sh', 'bash lattest.sh'];
var start_times = {};
var end_times = [0, 0, 0, 0, 0];
var promises = commands.map(function (command, index) {
    //console.log('A\n') // delete later, just proof this is parralel
    var start_time = Date.now();
    start_times[index] = start_time;
    return new Promise(function (resolve, reject) {
        var _a = command.split(' '), cmd = _a[0], args = _a.slice(1);
        var child = (0, child_process_1.spawn)(cmd, args, { shell: true });
        child.on('close', function (code) {
            var endTime = Date.now();
            var runtime = endTime - start_time;
            resolve({ command: command, runtime: runtime });
            end_times[index] = runtime;
        });
        child.on('error', function (err) {
            reject(err);
        });
    });
});
function MEAN(array) {
    var sum = array.reduce(function (acc, value) { return acc + value; }, 0);
    var mean = sum / array.length;
    return mean;
}
function MEDIAN(array) {
    var array_ = array.sort(function (x, y) { return x - y; });
    var ind = Math.floor(array_.length / 2);
    if (array_.length % 2 === 0) {
        var median = (array_[ind - 1] + array_[ind]) / 2;
        return median;
    }
    else {
        var median = array_[ind];
        return median;
    }
}
function P99(array) {
    var array_ = array.sort(function (x, y) { return y - x; });
    return array_[0];
}
Promise.all(promises)
    .then(function (results) {
    results.forEach(function (_a, index) {
        var command = _a.command, runtime = _a.runtime;
        //console.log(`Command ${index + 1} (${command}): ${runtime}ms`);
    });
    //console.log(end_times);
    console.log("mean: " + MEAN(end_times) + "ms");
    console.log("meadian: " + MEDIAN(end_times) + "ms");
    console.log("99th percentile: " + P99(end_times) + "ms");
})["catch"](function (err) {
    console.error(err);
});
