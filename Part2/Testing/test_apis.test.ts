import { spawnSync } from 'child_process';
import { expect, test } from '@jest/globals';

test('package API', () => {

  const curlCommand = `curl -X 'POST' 'http://127.0.0.1:5000/package/' -H 'Content-Type: application/json' -H 'accept: application/json' -H 'X-Authorization: kkm' -d '{"metadata": {"Name": "Underscore","Version": "1.0.0","ID": "underscore"},"data": {"Content": "Check","JSProgram": "if (process.argv.length === 7) {\\nconsole.log(\\'Success\\')\\nprocess.exit(0)\\n} else {\\nconsole.log(\\'Failed\\')\\nprocess.exit(1)\\n}\\n"}}'`;
  const expectedJson = { message: 'Success.' };
  const process = spawnSync(curlCommand, { shell: true });
  const output = process.stdout?.toString();
  console.log('curl = ', curlCommand)
  const response = JSON.parse(output || '');
  expect(response).toEqual(expectedJson);
});

// test('check authorization', () => {
//   const curlCommand =  "curl -H 'Content-Type: application/json' --location 'http://127.0.0.1:8080/package'  --data '{\"metadata\":{\"Name\":\"Loadash\",\"Version\":\"1.0.0\",\"ID\":\"loadash\"},\"data\":{\"Content\":\"checking_content\",\"JSProgram\":\"if (process.argv.length === 7) {\\nconsole.log('Success')\\nprocess.exit(0)\\n} else {\\nconsole.log('Failed')\\nprocess.exit(1)\\n}\\n\"}}'";
//   const process = spawnSync(curlCommand, { shell: true });
//   const output = process.stdout?.toString();
//   const expectedJson = { message: 'Success.' }; //????????
//   const response = JSON.parse(output || '');
//   expect(response).toEqual(expectedJson);
// });

