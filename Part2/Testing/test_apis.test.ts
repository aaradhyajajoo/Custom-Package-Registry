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
  console.log(output)
  console.log('curl = ', curlCommand)
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
  console.log(response)
  expect(response).toEqual(expectedJson);
});
