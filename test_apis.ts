import { spawnSync } from 'child_process';

test('package API', () => {
  const curlCommand =  "curl -H 'Content-Type: application/json' --location 'http://127.0.0.1:8080/package' --header 'X-Authorization: bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c' --data '{\"metadata\":{\"Name\":\"Loadash\",\"Version\":\"1.0.0\",\"ID\":\"loadash\"},\"data\":{\"Content\":\"checking_content\",\"JSProgram\":\"if (process.argv.length === 7) {\\nconsole.log('Success')\\nprocess.exit(0)\\n} else {\\nconsole.log('Failed')\\nprocess.exit(1)\\n}\\n\"}}'";
  const expectedJson = { message: 'Success.' };
  const process = spawnSync(curlCommand, { shell: true });
  const output = process.stdout?.toString();
  const response = JSON.parse(output || '');
  expect(response).toEqual(expectedJson);
});