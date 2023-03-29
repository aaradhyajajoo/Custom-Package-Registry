# ECE 461 Project Group 30

## Part 1 

### Introduction
Our team is helping the ACME Corporation to develop a custom NPM registry. The ACME Corporation has successfully ported one of their back-end components to Node.js and is considering bringing up new Node.js-based services. They have over 2 million modules available through npm, but are concerned about the quality and maintainability of open-source modules. In part one of the project, we bulit a Command-line interface.that takes command line arguments as input and produces an ordered list of repositories with their overall and sub-scores for different metrics. 
### Our Design

 Programming language: Python, TypeScript and Bash
 
 Our system is designed to test the ‘trustworthiness’ of URLs provided by the user. 
We used main.py to evaluate the user input, and direct the program to the correct path, such as installing dependencies, testing, and evaluating the input URLs. When a URL file is given, main.py redirects the control to graph_api_call.ts, which uses different APIs  to gather the information used to calculate the various metrics. For example, GitHub API was used to calculate bus factor and license compatibility. Responsiveness was calculated using GraphQl. Correctness was calculated using REST API, utilizing number of issues, forks, stargazers, and watchers. After the metrics were determined, the net score was calculated using a weighted sum of the other metrics.The net score represents the ‘trustworthiness’ of the URL.  After the net score is determined, the console outputs a dictionary storing the net score and metrics for each URL, and dictionaries are displayed in descending order by net score. If the user wants to test the program, various URL files are created, including invalid ones, to test the CLI output.

 Net_Score = (0.4 * responsiveness + 0.1 * bus factor + 0.2 * license compatibility + 0.1 * ramp-up time + 0.2 * correctness) /  5
 
 There is an executable file in the root directory of th project called "run".
 It should has the following CLI when executed on a Linux machine:
 
 ./run install
  Installs any dependencies in userland
 
 ./run build
   Completes any compilation needed
 
./run URL_FILE
 where URL_FILE is the absolute location of a file consisting of an ASCII-encoded newline-delimited set of URLs
 This invocation produces NDJSON output. Each row should include the fields: “URL”, “NetScore”, “RampUp”, “Correctness”, “BusFactor”, “ResponsiveMaintainer”, and “License
 
 

 
 
  
