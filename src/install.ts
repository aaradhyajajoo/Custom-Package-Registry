
import * as fs from 'fs';
const readline = require('readline');

var json = require('../package.json'); // Package json as a json object
var dependencies = json.dependencies; // Dependencies as a json object
var count = Object.keys(dependencies).length; // Number of dependencies in package.json

const rl = readline.createInterface({ // Number of packages/modules in requirements.txt
    input: fs.createReadStream('src/license.txt'),
  });
  
  rl.on('line', (line:string) => {
    count += 1
  });
console.log(count+' dependencies installed.')