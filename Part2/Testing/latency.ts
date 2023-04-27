import { spawn } from 'child_process';

//  list of simultanious commands to run
const commands = ['bash lattest.sh','bash lattest.sh','bash lattest.sh','bash lattest.sh','bash lattest.sh'];

console.log('Latency details for “many clients download lodash”:');

//  kep track of when each thread begins its tasks
const start_times = {};

//  initiate total runtime list
var end_times = [0, 0, 0, 0, 0];

//  task for each thread
const promises = commands.map((command, index) => {
  //console.log('A\n') // uncomment to prove that processes are happening simultaniously, just proof this is parralel
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
  //console.log('B\n') // uncomment to prove that processes are happening simultaniously, just proof this is parralel
});

//  get the mean of an array
function MEAN(array) {  
  const sum = array.reduce((acc, value) => acc + value, 0);
  const mean = sum / array.length;
  return mean;
}

//  get the median of an array
function MEDIAN(array) {
  const array_ = array.sort((x, y) => x - y);
  const ind = Math.floor(array_.length / 2);

  if (array_.length % 2 === 0) {
    const median = (array_[ind - 1] + array_[ind]) / 2;
    return median;
  } else {
    const median = array_[ind];
    return median;
  }
}

//  get the 99th percentile of an array
function P99(array) {
  const array_ = array.sort((x, y) => y-x);
  return array_[0];
}



Promise.all(promises)
  .then((results) => {
    results.forEach(({ command, runtime }, index) => {
      //console.log(`Command ${index + 1} (${command}): ${runtime}ms`);
    });
    //console.log(end_times);
    console.log("mean: " + MEAN(end_times) + "ms");
    console.log("median: " + MEDIAN(end_times) + "ms");
    console.log("99th percentile: " + P99(end_times) + "ms");
  })
  .catch((err) => {
    console.error(err);
  });
