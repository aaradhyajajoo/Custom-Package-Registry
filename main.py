#!/usr/bin/ python3

import sys
import os 
from contextlib import redirect_stdout
urls = set() # list of urls


# install function
# TODO: install the requirements TANVI change here
def install():
    with open("/dev/null", "w") as f, redirect_stdout(f):
     os.system("pip install -r requirements.txt")
   # sys.stdout = open("/dev/null", "w")

def main(args, *kwargs):

    # no arguments provided
    if (len(args) == 0):
        sys.exit("No arguments provided")
    
    # check if the first argument is install or test
    if (args[0].strip() == "install"):
        install()

    elif (args[0].strip() == "test"):
        # test function to be called here
        print("test")
    
    # default test: check if the files exist
    else:
        check_files_exists(*args, **kwargs)


# read the file
def read_file(file, *kwargs):

    # check if the file is readable
    if not (os.access(file, os.R_OK)):
        sys.exit("File {} is not readable".format(file))

    with open(file, "r") as f:
        for line in f:
            urls.add(line.strip())
    

# check if the files with the input path exist
def check_files_exists(args, *kwargs):

    # no files provided
    if (len(args) == 0):
        sys.exit("No files provided")

    # check if the files exist
    for arg in args:
        if not os.path.exists(arg):
            sys.exit("File {} does not exist".format(arg))
        else:
            read_file(arg)
    
    
if __name__ == "__main__":
    main(sys.argv[1:])
    print(urls)