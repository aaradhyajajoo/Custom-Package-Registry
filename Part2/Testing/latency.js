"use strict";
exports.__esModule = true;
var child_process_1 = require("child_process");
var commands = ['bash lattest.sh', 'bash lattest.sh', 'bash lattest.sh', 'bash lattest.sh', 'bash lattest.sh'];
var start_times = {};
var end_times = {};
var promises = commands.map(function (command, index) {
    console.log('A\n'); // delete later, just proof this is parralel
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
// Wait for all commands to finish and report their runtimes
Promise.all(promises)
    .then(function (results) {
    results.forEach(function (_a, index) {
        var command = _a.command, runtime = _a.runtime;
        console.log("Command ".concat(index + 1, " (").concat(command, "): ").concat(runtime, "ms"));
    });
})["catch"](function (err) {
    console.error(err);
});
console.log(end_times);
