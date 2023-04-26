import { spawn } from 'child_process';

const commands = ['bash lattest.sh','bash lattest.sh','bash lattest.sh','bash lattest.sh','bash lattest.sh'];

const start_times = {};
const end_times = {}
const promises = commands.map((command, index) => {
  console.log('A\n') // delete later, just proof this is parralel
  const start_time = Date.now();
  start_times[index] = start_time;

  return new Promise((resolve, reject) => {
    const [cmd, ...args] = command.split(' ');

    const child = spawn(cmd, args, { shell: true });

    child.on('close',(code) => {
      const endTime = Date.now();
      const runtime = endTime - start_time;
      resolve({ command, runtime });
      end_times[index] = runtime;
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

  console.log(end_times);