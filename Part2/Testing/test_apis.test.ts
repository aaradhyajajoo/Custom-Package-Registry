import { spawnSync } from 'child_process';
import { expect, test } from '@jest/globals';

test('package API', () => {

  const curlCommand = 'bash test1.sh'
  const expectedJson = { message: 'Success.' };
  const process = spawnSync(curlCommand, { shell: true });
  const output = process.stdout?.toString();
  //console.log('curl = ', curlCommand)
  const response = JSON.parse(output || '');
  expect(response).toEqual(expectedJson);
});

test('reset', () => {

  const curlCommand = 'bash test2.sh'
  //const expectedJson = { message: 'Success.' };
  const process = spawnSync(curlCommand, { shell: true });
  const output = process.stdout?.toString();
  const response = JSON.parse(output || '');
  expect(response).toEqual("Registry is reset.");
});

test('reset, no auth', () => {

  const curlCommand = 'bash test3.sh'
  const expectedJson = { message: 'You do not have permission to reset the registry.' };
  const process = spawnSync(curlCommand, { shell: true });
  const output = process.stdout?.toString();
  //console.log('curl = ', curlCommand)
  const response = JSON.parse(output || '');
  expect(response).toEqual(expectedJson);
});

test('regex found', () => {

  const curlCommand1 = 'bash test1.sh'
  const curlCommand2 = 'bash test4.sh'
  const expectedJson = [ { Version: '1.0.0', Name: 'Underscore' } ];
  const process1 = spawnSync(curlCommand1, { shell: true });
  const process2 = spawnSync(curlCommand2, { shell: true });
  const output = process2.stdout?.toString();
  const response = JSON.parse(output || '');
  expect(response).toEqual(expectedJson);
});

test('regex not found', () => {
  const curlCommand1 = 'bash test1.sh'
  const curlCommand2 = 'bash test5.sh'
  const expectedJson = { "message": "Package does not exist." };
  const process1 = spawnSync(curlCommand1, { shell: true });
  const process2 = spawnSync(curlCommand2, { shell: true });
  const output = process2.stdout?.toString();
  const response = JSON.parse(output || '');
  expect(response).toEqual(expectedJson);
});
