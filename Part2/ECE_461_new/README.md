# ECE 461 Project

Our project for ECE 461 (Software Engineering) is to help ACME Corporation's software architects by providing infrastructure services for implementing new Node.js-based services easily. We use npm (the package manager for Node.js) with certain requirements shown below. The main product of our project is a command-line interface that ACME service engineering teams can use to help them choose their modules. It should "not be super slow", according to the customer.

## Project Requirements

Executable file in the root directory of your project called "run" that includes
- “./run install”
    - Installs any dependencies in userland
    - Should exit 0 on success
- “./run build”
    - Completes any compilation needed
    - Should exit 0 on success
- "./run URL_FILE", where URL_FILE is the  location of a file consisting of an ASCII-encoded newline-delimited set of URLs.
    - This invocation should produce NDJSON output; Each row should include the fields:
        - “URL”
        - “NetScore”
        - “RampUp”
        - “Correctness”
        - “BusFactor”
        - “ResponsiveMaintainer”
        - “License”.
    - Each score should be in the range [0,1] where 0 indicates total failure and 1 indicates perfection. The specific operationalizations are up to you, but you must provide rationales as part of your documentation.
    - The “NetScore” should be calculated as [0,1] as well, as a weighted sum. You should choose the weights based on Sarah’s priorities, and explain your choice.
    - Should exit 0 on success
- "./run test", which runs a test suite and exits 0 if everything is working.
    - The minimum requirement for this test suite is that it contain at least 20 distinct test cases and achieve at least 80% code coverage as measured by line coverage.
    - The output from this invocation should be a line written to stdout of the form: “X/Y test cases passed. Z% line coverage achieved.”2
    - Should exit 0 on success.
- In the event of an error, your program should exit with return code 1, and print a useful error message to the console. Look at the resource on error message design for guidance.

Your software must produce a log file stored in the location named in the environment variable $LOG_FILE and using the verbosity level indicated in the environment variable $LOG_LEVEL (0 means silent, 1 means informational messages, 2 means debug messages). Default log verbosity is 0.

## Getting Started

ACME Corporation currently offers its web service product directly via a REST API. However, they want a licensed version of the web service that its customers can self deploy. This means it needs to be open-sourced so it can be easily adaptable to their needs (ACME uses GNU Lesser Public License v2.1 for all open-source software so it must be compatible). 

### Requirements for npm packackages

The packages chosen have the main goal of a “low ramp-up time” for the future engineers. Therefore they have to follow the below requirements
- the package is correct
- the maintainers will be responsive to fix any bugs that are blocking ACME’s teams
- the open-source module has enough maintainers to continue to apply critical fixes such as a security patch. [highest priority]

It should be noted that more requirements for the npm packages could be added at a later time, so the design should be able to accommodate adding new aspects.

### Installing

A step by step series of examples that tell you how to get a development
environment running

Download any software application that has a command-line interface

    i.e. terminal, VSCode, eclipse

Run the module on the command-line to determine the score of the module

## Running the tests

To run the tests, write the following in terminal:
    
    ./run install
    ./run build
    ./run test_modules/urls_for_test.txt
    ./run test

### Sample Tests

The sample tests are a selection of different repository URLs that are then pushed through the grading software and given a score.

    https://github.com/996icu/996.ICU = 0.97/1


## Built With

  - [Contributor Covenant](https://www.contributor-covenant.org/) - Used
    for the Code of Conduct
  - [Creative Commons](https://creativecommons.org/) - Used to choose
    the license
  - [GPL Compatible Licenses](https://gplv3.fsf.org/wiki/index.php/Compatible_licenses) - Used for License Compatibility
  - [GNU Operating System](https://www.gnu.org/licenses/license-list.en.html) - Used for License Compatibility

## Authors

  - **Elizabeth McNaughton** - 
    [lizziesarah](https://github.com/lizziesarah)
  - **Aiden Goen** - 
    [Agoen](https://github.com/Agoen)
  - **Kaylee Smith** - 
    [kaylee-smith](https://github.com/kaylee-smith)
  - **Collin Sell** - 
    [collinsell](https://github.com/collinsell)

## License

Node.js is available under the MIT license. Node.js also includes external libraries that are available under a variety of licenses. See LICENSE for the full license text.

## Acknowledgments

  - stackoverflow
  - TA in office hours

