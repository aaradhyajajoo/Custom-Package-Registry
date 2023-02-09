import * as fs from 'fs';
import axios from 'axios';

// Global variables
var license_compatibility: number // done 
var bus_factor: number // Tanvi - done
var ramp_upTime: number // Eshaan 
var responsiveness: string // Aaradhya - done
var correctness: number //  Ilan
var net_score: number 
var licenseName: string
var issuesCount: number
var forksCount: number
var watchersCount: number
var stargazerCount: number
var repo_URL : string

// Function to request APIs from github GraphQL API
async function getData_github(requestUrl: string, owner: string, repo: string) {
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
        licenseInfo{
          name
        }
        }
        }
      `;

    //  get the github token from the environment variable
    var github_token = process.env.GITHUB_TOKEN

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
        repo_URL = response.data.data.repository.url;
        issuesCount = response.data.data.repository.issues.totalCount;
        forksCount = response.data.data.repository.forks.totalCount;
        watchersCount = response.data.data.repository.watchers.totalCount;
        stargazerCount = response.data.data.repository.stargazerCount;
        if (response.data.data.repository.licenseInfo == null)
        {
          licenseName = "None";
        }
        else
        {
          licenseName = response.data.data.repository.licenseInfo.name;
        }

        // call the function to calculate the scores
        calculate_scores(issuesCount, forksCount, watchersCount, stargazerCount, licenseName, net_score);
    });
  } catch (error) {
    console.log(query)
    console.log(owner, repo)
    console.error("There was a problem with the fetch operation with ", requestUrl);
    console.error(error);
  }
}

// Function to request APIs
async function getData_npms(requestUrl: string)
{
    var response = await axios.get(requestUrl);
    const Console = new console.Console(fs.createWriteStream('./NPMJS_API_data_repsonse.txt'));
    Console.log(response.data);
}

function calculate_scores(issuesCount: number, forksCount : number, watchersCount : number, stargazerCount : number, licenseName : string, net_score: number)
{
  // check what license the repo has
  if (licenseName.includes('MIT')) 
  {
    license_compatibility = 1;
  }
  else
  {
    license_compatibility = 0;
  }

  // calculate the bus_factor time
  if (license_compatibility == 0)
  {
    bus_factor = 0;
  }
  else
  {
    var bus_factor_str = ((issuesCount / (issuesCount + forksCount + watchersCount + stargazerCount)) * license_compatibility).toFixed(2);
    bus_factor = Number(bus_factor_str);
  }

  // calculate the responsiveness time
  responsiveness = (Math.abs(1 - (1 / issuesCount))).toFixed(2);

  // calculate the ramp_upTime

  // calculate the net_score time
  var net_score = (0.4 * Number(responsiveness) + 0.1 * bus_factor + 0.2 * license_compatibility + 0.1 * ramp_upTime + 0.2 * correctness)/ 5
  write_to_console(license_compatibility, bus_factor, ramp_upTime,  Number(responsiveness), correctness, net_score);
}

function write_to_console(license_compatibility: number, bus_factor : number, ramp_upTime : number, responsiveness : number, correctness : number, net_score : number) {
  
  // write to a file
  // var filename = process.env.LOG_FILE;
  // var verbosity = process.env.LOG_LEVEL;

  // write to the console
  var line_to_print = "{\"URL\":\"" + repo_URL + "\", \"NET_SCORE\":" + net_score + ", \"RAMP_UP_SCORE\":" + ramp_upTime + ", \"CORRECTNESS_SCORE\":" + correctness + ", \"BUS_FACTOR_SCORE\":" + bus_factor + ", \"RESPONSIVE_MAINTAINER_SCORE\":" + responsiveness + ", \"LICENSE_SCORE\":" + license_compatibility + "}"
  console.log(line_to_print);
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

  // Stack Overflow Citation 
  // https://stackoverflow.com/questions/30016773/javascript-filter-true-booleans
  arr_urls = arr_urls.filter(Boolean);


  arr_urls.forEach((url) => {
    // get the owner and repo name from the url
    var owner = url.split('/')[3]
    var repo = url.split('/')[4]

    // GitHub URLs 
    if (url.includes('github')) 
    {
      var request_url = "https://api.github.com/graphql"
      getData_github(request_url, owner, repo);
    }

    // NPM URLs
    else if (url.includes('npm'))
    {
      var request_url = "https://api.npms.io/v2/" + owner + "/" + repo
      getData_npms(request_url);
    }
    
    // Invalid URL
    else
    {
      console.log("Invalid URL: ");
      console.log(url);
    }
  });
}

main(); // Main 
