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

test('reset no permission', () => {

  const curlCommand = 'bash test9.sh'
  const expectedJson = {"message": "You do not have permission to reset the registry."}
  const process = spawnSync(curlCommand, { shell: true });
  const output = process.stdout?.toString();
  const response = JSON.parse(output || '');
  expect(response).toEqual(expectedJson);
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

test('null regex', () => {
  const curlCommand1 = 'bash test1.sh'
  const curlCommand2 = 'bash test6.sh'
  const expectedJson = {"message": "There is missing field(s) in the PackageData/AuthenticationToken or it is formed improperly (e.g. Content and URL are both set), or the AuthenticationToken is invalid."}
  const process1 = spawnSync(curlCommand1, { shell: true });
  const process2 = spawnSync(curlCommand2, { shell: true });
  const output = process2.stdout?.toString();
  const response = JSON.parse(output || '');
  expect(response).toEqual(expectedJson);
});

// UNSURE ABOUT THIS ONE, OUTPUT OF bash test7.sh LOOKS WEIRD
test('get ID, ID exists', () => {

  const curlCommand1 = 'bash test1.sh'
  const curlCommand2 = 'bash test7.sh'
  const expectedJson = {"data": {"Content": "Check", "JSProgram": "if (process.argv.length === 7) {\nconsole.log('Success')\nprocess.exit(0)\n} else {\nconsole.log('Failed')\nprocess.exit(1)\n}\n"}, "metadata": {"ID": "underscore", "Name": "Underscore", "Version": "1.0.0"}};
  const process1 = spawnSync(curlCommand1, { shell: true });
  const process2 = spawnSync(curlCommand2, { shell: true });
  const output = process2.stdout?.toString();
  const response = JSON.parse(output || '');
  expect(response).toEqual(expectedJson);
});

// UNSURE ABOUT THIS ONE, OUTPUT OF bash test7.sh LOOKS WEIRD
test('get ID, ID does not exists', () => {

  const curlCommand1 = 'bash test1.sh'
  const curlCommand2 = 'bash test8.sh'
  const expectedJson = {"message": "Package does not exist."};
  const process1 = spawnSync(curlCommand1, { shell: true });
  const process2 = spawnSync(curlCommand2, { shell: true });
  const output = process2.stdout?.toString();
  const response = JSON.parse(output || '');
  expect(response).toEqual(expectedJson);
});

// SKIPPING PUT... DO NOT REALLY UNDERSTAND IT FOR NOW
// same for POST
// unsure why rate isnt working
// put authenticate im putting on hold. Curl says '"message": "This system does not support authentication."'. If its supposed to do that implementing this is easy
// package by name isnt working... dont think its a problem with curl command
// most likely delete by name isnt working for same reason.