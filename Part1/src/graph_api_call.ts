import * as fs from 'fs';
import axios from 'axios';
import { exit } from 'process';
const { exec } = require('child_process');
const readline = require('readline')


// Global variables
var license_compatibility: number
var bus_factor: number
var ramp_upTime: number
var responsiveness: string
var correctness: number
var net_score: number
var licenseName: string
var issuesCount: number
var forksCount: number
var watchersCount: number
var stargazerCount: number
var repo_URL: string
var verbosity: number;
var filename: string;
var filename = String(process.env.LOG_FILE);
var verbosity = Number(process.env.LOG_LEVEL);
var to_sort: { [key: number]: any[] } = {};
var global_url_count = 0;
var i: number;
var licenseArray:string[] = [];
var count: number;

//  get the github token from the environment variable
var github_token = process.env.GITHUB_TOKEN

// function that writes to the log file for verbosity
export function write_to_log_file() {    //0 means silent  
  if (verbosity == 0) {
    return;
  }
  if (verbosity == 1) {    //1 means informational messages
    var Console = new console.Console(fs.createWriteStream(filename, { flags: 'a' }));  //displays the scores to console
    Console.log("URL: " + repo_URL);
    Console.log("NET_SCORE: " + net_score);
    Console.log("RAMP_UP_SCORE: " + ramp_upTime);
    Console.log("CORRECTNESS_SCORE: " + correctness);
    Console.log("BUS_FACTOR_SCORE: " + bus_factor);
    Console.log("RESPONSIVENESS_SCORE: " + responsiveness);
    Console.log("LICENSE_COMPATIBILITY_SCORE: " + license_compatibility);
    Console.log("\n")
  }
  if (verbosity == 2) {    //2 means debug message
    var Console = new console.Console(fs.createWriteStream(filename, { flags: 'a' })); //displa
    Console.log("URL: " + repo_URL);
    Console.log("NET_SCORE: " + net_score);
    Console.log("RAMP_UP_SCORE: " + ramp_upTime);
    Console.log("CORRECTNESS_SCORE: " + correctness);
    Console.log("BUS_FACTOR_SCORE: " + bus_factor);
    Console.log("RESPONSIVENESS_SCORE: " + responsiveness);
    Console.log("LICENSE_COMPATIBILITY_SCORE: " + license_compatibility);
    Console.log("The following are how the individual scores are calculated: " + repo_URL);
    Console.log("Bus Factor = ((issuesCount / (issuesCount + forksCount + watchersCount + stargazerCount)) * license_compatibility)");
    Console.log("Responsiveness = (Math.abs(1 - (1 / issuesCount)))")
    Console.log("Correctness = (Math.abs(1 - (1 / forksCount)))")
    Console.log("Ramp Up Time = (Math.abs(1 - (1 / watchersCount)))")
    Console.log("\n")
    Console.log("\n")
  }
  return 0;
}

function ramp_upTime_calc() {
  // read from a file called rampedUp.txt
  var rampedUp = fs.readFileSync('src\/ramp_up.txt', 'utf-8');
  var rampedUp_arr = rampedUp.split(/\r?\n/);
  return rampedUp_arr[0];
}

// Function to request APIs from github GraphQL API
async function getData_github(requestUrl: string, owner: string, repo: string, flag: number) {
  var query = `
    query {
      repository(owner: "owner123", name: "repo1") {
        name
        url
        description
        watchers {
        totalCount
        }
        forks{
          totalCount
        }
        issues {
            totalCount
        }
        stargazerCount
        }
        }
      `;

  // replace the owner and repo name in the query
  var prev_owner = "owner123";
  var prev_repo = "repo1";

  query = query.replace(prev_owner, owner);
  query = query.replace(prev_repo, repo);

  // make the request to the github graphql api
  try {
    await axios({
      url: requestUrl,
      method: 'post',
      headers: {
        Authorization: `Token ${github_token}`,
        Accept: 'application/vnd.github+json; application/vnd.github.hellcat-preview+json; application/vnd.github.squirrel-girl-preview+json'
      },
      data: {
        query: query
      }
    }).then((response) => {

      // get the data from the response
      if (flag == 0) {
        repo_URL = response.data.data.repository.url;
      }
      else {
        repo_URL = "https://npmsjs.com/package/" + response.data.data.repository.name;
      }

      issuesCount = response.data.data.repository.issues.totalCount;       //store the number of issues
      forksCount = response.data.data.repository.forks.totalCount;         //store the number of forks
      watchersCount = response.data.data.repository.watchers.totalCount;   //store the number of watchers
      stargazerCount = response.data.data.repository.stargazerCount;       //store the number of stargazers
      

      // call the function to calculate the scores
      calculate_scores(issuesCount, forksCount, watchersCount, stargazerCount,net_score);
    });
  } catch (error) {
    console.error("There was a problem with the fetch operation with ", requestUrl);  //throws an error if a bad URL was inputted 
    console.error(error);
  }
}

// Function to request APIs
async function getData_npmjs(requestUrl: string) {
  var response = await axios.get(requestUrl);
  var npmjs_urls = response.data['repository']['url'];     //Extract Data from the URL
  npmjs_urls = npmjs_urls.split('//');
  npmjs_urls = npmjs_urls[1].split('@');    //This to remove "@" symbol from the 
  if (npmjs_urls.length > 1) {
    npmjs_urls = npmjs_urls[1];
  }

  if (typeof npmjs_urls == 'object') {
    npmjs_urls = npmjs_urls[0];
  }
  npmjs_urls = npmjs_urls.replace('.git', '');
  var owner = npmjs_urls.split("/")[1];
  var repo = npmjs_urls.split("/")[2];
  var request_url = "https://api.github.com/graphql"
  getData_github(request_url, owner, repo, 1);   //Get and store the respone from github API
}

function calculate_scores(issuesCount: number, forksCount: number, watchersCount: number, stargazerCount: number, net_score: number) {
  // check what license the repo has
  // console.log("License Name: " + licenseName);

  // calculate license compatibility:
  licenseName = licenseArray[i]

  if (licenseName.includes('MIT')){
    license_compatibility = 1;
  }
  
  else if (licenseName.includes('Other')){
    license_compatibility = 1;
  }
  else{
    license_compatibility = 0;
  }

  // calculate the bus_factor time
  if (license_compatibility == 0) {
    bus_factor = 0;
  }
  else {
    var bus_factor_str = (((issuesCount) / (issuesCount + forksCount + watchersCount + stargazerCount)) * license_compatibility).toFixed(2);   // Bus factor Formula
    bus_factor = Number(bus_factor_str);
  }

  // calculate the responsiveness time
  if (watchersCount < issuesCount) {
    responsiveness = (Math.abs(1 - (watchersCount / issuesCount))).toFixed(2);  //Responsiveness formula
  }
  else {
    responsiveness = (Math.abs(1 - (issuesCount / watchersCount))).toFixed(2);
  }
  // calculate the ramp_upTime
  ramp_upTime = Number(ramp_upTime_calc())        //Ramp-up formula

  correctness = Number(((Number(responsiveness) + license_compatibility) / 2).toFixed(2));

  // calculate the net_score time
  var net_score = Number(((0.4 * Number(responsiveness) + 0.1 * bus_factor + 0.2 * license_compatibility + 0.1 * ramp_upTime + 0.2 * correctness)).toFixed(2))   //NET score formula

  write(license_compatibility, bus_factor, ramp_upTime, Number(responsiveness), correctness, net_score);
}

function write(license_compatibility: number, bus_factor: number, ramp_upTime: number, responsiveness: number, correctness: number, net_score: number) {
  // write to the console
  write_to_log_file() // Environment Variable



  i += 1 // Updating counter for urls
  to_sort[net_score] = [repo_URL, ramp_upTime, correctness, bus_factor, responsiveness, license_compatibility]
  // var line_to_print = "{\"URL\":\"" + repo_URL + "\", \"NET_SCORE\":" + net_score + ", \"RAMP_UP_SCORE\":" + ramp_upTime + 
  // ", \"CORRECTNESS_SCORE\":" + correctness + ", \"BUS_FACTOR_SCORE\":" + bus_factor + ", \"RESPONSIVE_MAINTAINER_SCORE\":" 
  // + responsiveness + ", \"LICENSE_SCORE\":" + license_compatibility + "}"
  if (i == global_url_count) {
    // console.log(to_sort)
    var Console = new console.Console(fs.createWriteStream("results.txt", { flags: 'w' }));
    Console.log(to_sort)
  }

  // console.log(line_to_print);
}

// Main function
function main() {


  // get the arguments from the command line
  var args = process.argv;

  // get the filename from the command line
  var filename = args[2]
  filename = filename.replace(/\r/g, '');

  // read the file
  const string_urls = fs.readFileSync(filename, 'utf-8');
  var arr_urls = string_urls.split(/\r?\n/);


  // read license txt file
  const rl = readline.createInterface({
    input: fs.createReadStream('src/license.txt'),
  });
  
  rl.on('line', (line:string) => {
    licenseArray.push(line);
  });
  
  // Stack Overflow Citation 
  // https://stackoverflow.com/questions/30016773/javascript-filter-true-booleans
  arr_urls = arr_urls.filter(Boolean);
  i = 0;
  count = 0;
  global_url_count = arr_urls.length
  arr_urls.forEach((url) => {
    // get the owner and repo name from the url
    var owner = url.split('/')[3]
    var repo = url.split('/')[4]

    // GitHub URLs 
    if (url.includes('github')) {
      var request_url = "https://api.github.com/graphql"
      getData_github(request_url, owner, repo, 0);
    }

    // NPM URLs
    else if (url.includes('npm')) {
      var request_url = "https://replicate.npmjs.com/" + repo
      getData_npmjs(request_url);
    }

    // Invalid URL
    else {
      console.log("Invalid URL: ");
      console.log(url);
    }
  });
}

if (process.env.LOG_FILE == null)
{
  console.log("Invalid Log File")
  process.exit(1)
}

if (process.env.LOG_LEVEL == null)
{
  console.log("Invalid Log Level")
  process.exit(1)
}

main(); // Main 



