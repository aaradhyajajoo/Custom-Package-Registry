"use strict";
exports.__esModule = true;
var child_process_1 = require("child_process");
test('package API', function () {
    var _a;
    var curlCommand = "curl -H 'Content-Type: application/json' --location 'http://127.0.0.1:8080/package' --header 'X-Authorization: bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c' --data '{\"metadata\":{\"Name\":\"Loadash\",\"Version\":\"1.0.0\",\"ID\":\"loadash\"},\"data\":{\"Content\":\"checking_content\",\"JSProgram\":\"if (process.argv.length === 7) {\\nconsole.log('Success')\\nprocess.exit(0)\\n} else {\\nconsole.log('Failed')\\nprocess.exit(1)\\n}\\n\"}}'";
    var expectedJson = { message: 'Success.' };
    var process = (0, child_process_1.spawnSync)(curlCommand, { shell: true });
    var output = (_a = process.stdout) === null || _a === void 0 ? void 0 : _a.toString();
    var response = JSON.parse(output || '');
    expect(response).toEqual(expectedJson);
});
test('check authorization', function () {
    var _a;
    var curlCommand = "curl -H 'Content-Type: application/json' --location 'http://127.0.0.1:8080/package'  --data '{\"metadata\":{\"Name\":\"Loadash\",\"Version\":\"1.0.0\",\"ID\":\"loadash\"},\"data\":{\"Content\":\"checking_content\",\"JSProgram\":\"if (process.argv.length === 7) {\\nconsole.log('Success')\\nprocess.exit(0)\\n} else {\\nconsole.log('Failed')\\nprocess.exit(1)\\n}\\n\"}}'";
    var process = (0, child_process_1.spawnSync)(curlCommand, { shell: true });
    var output = (_a = process.stdout) === null || _a === void 0 ? void 0 : _a.toString();
    var expectedJson = { message: 'Success.' }; //????????
    var response = JSON.parse(output || '');
    expect(response).toEqual(expectedJson);
});
