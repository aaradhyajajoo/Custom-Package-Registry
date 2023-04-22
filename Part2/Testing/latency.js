"use strict";
exports.__esModule = true;
var child_process_1 = require("child_process");
// const curlCommand = 'bash test1.sh'
// const process = spawn(curlCommand, { shell: true });
// console.log("LATENCY")
// for (let i = 0; i < 10; i++)
// {
//   spawn(curlCommand, { shell: true });
// }
var commands = ['bash test1.sh', 'bash test2.sh', 'bash test3.sh', 'bash test4.sh', 'bash test5.sh', 'bash test6.sh',];
var start_times = {};
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
