import { spawn } from 'child_process';


// const curlCommand = 'bash test1.sh'
// const process = spawn(curlCommand, { shell: true });
// console.log("LATENCY")

// for (let i = 0; i < 10; i++)
// {
//   spawn(curlCommand, { shell: true });
// }

const commands = ['bash test1.sh','bash test2.sh','bash test3.sh','bash test4.sh','bash test5.sh','bash test6.sh',];

const start_times = {};
const promises = commands.map((command, index) => {
  console.log('A\n') // delete later, just proof this is parralel
  const start_time = Date.now();
  start_times[index] = start_time;

  return new Promise((resolve, reject) => {
    const [cmd, ...args] = command.split(' ');

    const child = spawn(cmd, args, { shell: true });

    child.on('close', (code) => {
      const endTime = Date.now();
      const runtime = endTime - start_time;
      resolve({ command, runtime });
    });

    child.on('error', (err) => {
      reject(err);
    });
  });
});

// Wait for all commands to finish and report their runtimes
Promise.all(promises)
  .then((results) => {
    results.forEach(({ command, runtime }, index) => {
      console.log(`Command ${index + 1} (${command}): ${runtime}ms`);
    });
  })
  .catch((err) => {
    console.error(err);
  });