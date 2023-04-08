import regex as re
import os
import time
from main import check_files_exists
import pytest


# check if program appropriatley handles cases where user enters a file that is not in directory
def test_file_DNE():
    with open("DNE_OUTPUT") as file:
        lines = [line.rstrip() for line in file]
    
    assert(len(lines) == 1)
    assert(lines[0]== "File file_DNE does not exist")
    
    

# check if program appropriatley handles cases where user enters a URL that is not valid
def test_invalid_URL():
    with open("OUTPUT") as file:
        lines = [line.rstrip() for line in file]
    assert(len(lines) == 2)
    assert(lines[0]=="Invalid URL:")
    assert(lines[1]=="youtube.com")
    pass

#  makes sure that the correct number of dictionaries are outputted
def test_list():
    with open('OUTPUT2') as file:
            dic_list = [eval(line.rstrip()) for line in file] 
    assert(type(dic_list) == list)
    assert(len(dic_list) == 5)
    pass

#   makes sure that each dictionary is of correct size
def test_size():
    with open('OUTPUT2') as file:
            dic_list = [eval(line.rstrip()) for line in file] 
    dic = dic_list[0]
    assert(type(dic) == dict)
    assert(len(dic) == 7)
    pass

# makes sure that the URL is in the dictionary of first URL input
def test_url_0():
    with open('OUTPUT2') as file:
            dic_list = [eval(line.rstrip()) for line in file] 
    dic = dic_list[0]
    assert "URL" in dic
    pass

# makes sure that the NET_SCORE is in the dictionary of first URL input
def test_NET_SCORE_0():
    with open('OUTPUT2') as file:
            dic_list = [eval(line.rstrip()) for line in file] 
    dic = dic_list[0]
    assert "NET_SCORE" in dic
    assert 0 <= dic["NET_SCORE"] <= 1
    pass

# makes sure that the RAMP_UP_SCORE is in the dictionary of first URL input
def test_RAMP_UP_SCORE_0():
    with open('OUTPUT2') as file:
            dic_list = [eval(line.rstrip()) for line in file] 
    dic = dic_list[0]
    assert "RAMP_UP_SCORE" in dic
    assert 0 <= dic["RAMP_UP_SCORE"] <= 1
    pass

# makes sure that the CORRECTNESS_SCORE is in the dictionary of first URL input
def test_CORRECTNESS_SCORE_0():
    with open('OUTPUT2') as file:
            dic_list = [eval(line.rstrip()) for line in file] 
    dic = dic_list[0]
    assert "CORRECTNESS_SCORE" in dic
    assert 0 <= dic["CORRECTNESS_SCORE"] <= 1
    pass

# makes sure that the BUS FACTOR is in the dictionary of first URL input
def test_BUS_FACTOR_SCORE_0():
    with open('OUTPUT2') as file:
            dic_list = [eval(line.rstrip()) for line in file] 
    dic = dic_list[0]
    assert "BUS_FACTOR_SCORE" in dic
    assert 0 <= dic["BUS_FACTOR_SCORE"] <= 1
    pass

# makes sure that the RESPONSIVE_MAINTAINER_SCORE is in the dictionary of first URL input
def test_RESPONSIVE_MAINTAINER_SCORE_0():
    with open('OUTPUT2') as file:
            dic_list = [eval(line.rstrip()) for line in file] 
    dic = dic_list[0]
    assert "RESPONSIVE_MAINTAINER_SCORE" in dic
    assert 0 <= dic["RESPONSIVE_MAINTAINER_SCORE"] <= 1
    pass


# makes sure that the LICENSE SCORE is in the dictionary of first URL input
def test_LICENSE_SCORE_0():
    with open('OUTPUT2') as file:
            dic_list = [eval(line.rstrip()) for line in file] 
    dic = dic_list[0]
    assert "LICENSE_SCORE" in dic
    assert 0 <= dic["LICENSE_SCORE"] <= 1
    pass

# make sure that the output dicitonaries are in order of NET_SCORE (descending)
def test_sorted():
    x = 2
    with open('OUTPUT2') as file:
        dic_list = [eval(line.rstrip()) for line in file] 
    for dic in dic_list:
        y = dic['NET_SCORE']
        assert(y <= x)
        x = y

# makes sure that the LICENSE SCORE is in the dictionary of second URL input
def test_url_1():
    with open('OUTPUT2') as file:
            dic_list = [eval(line.rstrip()) for line in file] 
    dic = dic_list[1]
    assert "URL" in dic
    pass

# makes sure that the NET SCORE is in the dictionary of second URL input
def test_NET_SCORE_1():
    with open('OUTPUT2') as file:
            dic_list = [eval(line.rstrip()) for line in file] 
    dic = dic_list[1]
    assert "NET_SCORE" in dic
    assert 0 <= dic["NET_SCORE"] <= 1
    pass

# makes sure that the RAMP UP SCORE is in the dictionary of second URL input
def test_RAMP_UP_SCORE_1():
    with open('OUTPUT2') as file:
            dic_list = [eval(line.rstrip()) for line in file] 
    dic = dic_list[1]
    assert "RAMP_UP_SCORE" in dic
    assert 0 <= dic["RAMP_UP_SCORE"] <= 1
    pass

# makes sure that the CORRECTNESS SCORE is in the dictionary of second URL input
def test_CORRECTNESS_SCORE_1():
    with open('OUTPUT2') as file:
            dic_list = [eval(line.rstrip()) for line in file] 
    dic = dic_list[1]
    assert "CORRECTNESS_SCORE" in dic
    assert 0 <= dic["CORRECTNESS_SCORE"] <= 1
    pass

# makes sure that the BUS FACTOR SCORE is in the dictionary of second URL input
def test_BUS_FACTOR_SCORE_1():
    with open('OUTPUT2') as file:
            dic_list = [eval(line.rstrip()) for line in file] 
    dic = dic_list[1]
    assert "BUS_FACTOR_SCORE" in dic
    assert 0 <= dic["BUS_FACTOR_SCORE"] <= 1
    pass

# makes sure that the RESPONSIVE MAINTAINER SCORE is in the dictionary of second URL input
def test_RESPONSIVE_MAINTAINER_SCORE_1():
    with open('OUTPUT2') as file:
            dic_list = [eval(line.rstrip()) for line in file] 
    dic = dic_list[1]
    assert "RESPONSIVE_MAINTAINER_SCORE" in dic
    assert 0 <= dic["RESPONSIVE_MAINTAINER_SCORE"] <= 1
    pass

# makes sure that the LICENSE SCORE is in the dictionary of second URL input
def test_LICENSE_SCORE_1():
    with open('OUTPUT2') as file:
            dic_list = [eval(line.rstrip()) for line in file] 
    dic = dic_list[1]
    assert "LICENSE_SCORE" in dic
    assert 0 <= dic["LICENSE_SCORE"] <= 1
    pass        

# makes sure that the LICENSE SCORE is in the dictionary of third URL input
def test_LICENSE_SCORE_3():
    with open('OUTPUT2') as file:
            dic_list = [eval(line.rstrip()) for line in file] 
    dic = dic_list[3]
    assert "LICENSE_SCORE" in dic
    assert 0 <= dic["LICENSE_SCORE"] <= 1
    pass    

# makes sure that the program can handle URLs that yield same NET_SCORE
def test_duplicates():
    with open('OUTPUT3') as file:
            dic_list = [eval(line.rstrip()) for line in file] 
    assert(len(dic_list) == 10)
    pass   
