import requests
from datetime import date
import os

token = ""
# https://github.com/octocat/Hello-World
try:
    token = os.environ['GITHUB_TOKEN']
except KeyError:
    print("No Github token environment variable set")

header = {'Authorization': 'Bearer {}'.format(token)}


# takes in a file with GitHub urls
# returns a dictionary mapping owners and repository names
def readFile(urlfile):
    owners_and_names = {}
    owners_and_urls = {}
    file_pointer = open(urlfile, "r")

    for line in file_pointer.readlines():
        owner = ""
        name = ""
        # read in name and owner from GitHub url
        i = 19
        if line[8] == 'g':
            while line[i] != '/':
                owner += line[i]
                i += 1
            name = line[i + 1:]
        if owner != "":
            owners_and_names[owner] = name.strip('\n')
            owners_and_urls[owner] = line.strip('\n')
    return owners_and_names, owners_and_urls


def getBusFactorScore(owner, name):
    # username = "lizziesarah"

    owner = '"' + f"{owner}" + '"'
    name = '"' + f"{name}" + '"'

    query1 = "{\n" + f"\trepository(owner: {owner}, name: {name})\n" + \
        "\t{ mentionableUsers{\n\ttotalCount\n}\n}\n}"

    # req=requests.get(url='https://api.github.com/graphql', auth=(username,token)) headers=header
    req = requests.post(url='https://api.github.com/graphql',
                        json={'query': query1}, headers=header)

    result = req.json()
    if result['data']['repository'] == None:
        return 0
    numContributors = result['data']['repository']['mentionableUsers']['totalCount']
    if numContributors >= 5:
        score = 1
    else:
        score = numContributors / 5
    # print(f"Number of contributors: {numContributors}")
    # print(f"Bus Factor: {score}")

    return score


# measures correctness score by seeing how many users have starred a repository (1 if more than 100 stars, else 0)
def getCorrectnessScore(owner, name):
    # username = "lizziesarah"

    owner = '"' + f"{owner}" + '"'
    name = '"' + f"{name}" + '"'

    query1 = "{\n" + f"\trepository(owner: {owner}, name: {name})" + \
        " { \n\t\tstargazerCount }}"

    # req=requests.get(url='https://api.github.com/graphql', auth=(username,token)) headers=header
    req = requests.post(url='https://api.github.com/graphql',
                        json={'query': query1}, headers=header)
    result = req.json()
    if result['data']['repository'] == None:
        return 0
    number_of_stars = result['data']['repository']['stargazerCount']

    if number_of_stars > 100:
        return 1
    else:
        return 0


# measures responsive maintainers score by seeing if there have been commits within the last year (0 or 1)
def getResponsiveMaintainersScore(owner, name):
    owner = '"' + f"{owner}" + '"'
    name = '"' + f"{name}" + '"'
    master = '"' + "master" + '"'

    # create github timestamp of last year's date
    todaysDateDateTime = date.today()
    lastyear = todaysDateDateTime.year - 1
    # format time stamp accordingly as a string
    gts = ""
    if todaysDateDateTime.day < 10 and todaysDateDateTime.month < 10:
        gts = '"' + str(lastyear) + "-0" + str(todaysDateDateTime.month) + "-0" + str(
            todaysDateDateTime.day) + "T01:01:00Z" + '"'
    if todaysDateDateTime.day < 10 and todaysDateDateTime.month >= 10:
        gts = '"' + str(lastyear) + "-" + str(todaysDateDateTime.month) + "-0" + str(
            todaysDateDateTime.day) + "T01:01:00Z" + '"'
    if todaysDateDateTime.day >= 10 and todaysDateDateTime.month < 10:
        gts = '"' + str(lastyear) + "-0" + str(todaysDateDateTime.month) + "-" + str(
            todaysDateDateTime.day) + "T01:01:00Z" + '"'
    if todaysDateDateTime.day >= 10 and todaysDateDateTime.month >= 10:
        gts = '"' + str(lastyear) + "-" + str(todaysDateDateTime.month) + "-" + str(
            todaysDateDateTime.day) + "T01:01:00Z" + '"'

    query1 = "{\n" + f"\trepository(owner: {owner}, name: {name})" + " { \n" + "\t ref(qualifiedName:" + f" {master})" + \
        " { " + "\n\t\ttarget { \n\t\t ... on Commit {\n\t" + \
        f"history(since:{gts})" + "{" + "\n\t\ttotalCount}}}}}\n\t\t}"

    req = requests.post(url='https://api.github.com/graphql',
                        json={'query': query1}, headers=header)
    result = req.json()
    if result['data']['repository'] == None or result['data']['repository']['ref'] == None:
        return 0
    numCommits = result['data']['repository']['ref']['target']['history']['totalCount']
    rm_score = 0
    if numCommits > 1:
        rm_score = 1

    # print(f"Responsive Maintainers: {rm_score}")
    return (rm_score)


def getLicenseScore(name, owner, file):
    file_pointer = open(file, "r")

    for line in file_pointer.readlines():

        split = (line.split(" "))
        url = split[0]
        score = split[1].split('\n')
        # score = split[1].split('\n')
        if url[8] == 'w':
            if url[30:] == name:
                return float(score[0])
        else:
            i = 19
            o = ""
            while line[i] != '/':
                o += line[i]
                i += 1

            if o == owner:
                return float(score[0])


def getRampUpScore(name, owner, file):
    file_pointer = open(file, "r")
    for line in file_pointer.readlines():
        split = (line.split(" "))
        score = split[1].split('\n')
        i = 19
        o = ""
        while line[i] != '/':
            o += line[i]
            i += 1
        if o == owner:
            return float(score[0])


def calcFinalScore(bf, lc, cr, ru, rm, owner_url):
    score = (bf * 4 + cr * 3 + ru * 2 + rm * 1) / 10
    score *= lc
    score_truncated = round(score, 3)
    return score_truncated


def writeFinalScore(arr, score_truncated, owner_url, outfile):
    '''
    score = (bf * 4 + cr * 3 + ru * 2 + rm * 1) / 14
    score *= lc
    score_truncated = round(score, 3)
    '''

    outfile_pointer = open(outfile, "a")
    url = '"' + 'URL' + '"'
    net = '"' + 'NET_SCORE' + '"'
    rampup = '"' + 'RAMP_UP_SCORE' + '"'
    correct = '"' + 'CORRECTNESS_SCORE' + '"'
    busfactor = '"' + 'BUS_FACTOR_SCORE' + '"'
    respmaint = '"' + 'RESPONSIVE_MAINTAINER_SCORE' + '"'
    licen = '"' + 'LICENSE_SCORE' + '"'
    # ru, cr, bf, rm, lc
    ru = arr[0]
    cr = arr[1]
    bf = arr[2]
    rm = arr[3]
    lc = arr[4]
    outfile_pointer.write(
        "{" + f"{url}:\"{owner_url}\", {net}:{score_truncated}, {rampup}:{ru}, {correct}:{cr}, {busfactor}:{bf}, {respmaint}:{rm}, {licen}:{lc}" + "}\n")
    outfile_pointer.close()


if __name__ == '__main__':
    owners_and_names = {}
    urls_and_final_scores = {}
    urls_ranked_by_score = {}
    attributes_of_url = {}
    # owners_and_names, owners_and_urls = readFile(urlfile='cloning_repos/git_urls.txt')
    owners_and_names, owners_and_urls = readFile(
        urlfile='cloning_repos/git_urls.txt')
    for owner in owners_and_names:
        cr = getCorrectnessScore(owner=owner,
                                 name=owners_and_names[owner])
        rm = getResponsiveMaintainersScore(
            owner=owner, name=owners_and_names[owner])
        bf = getBusFactorScore(owner=owner,
                               name=owners_and_names[owner])
        lc = getLicenseScore(
            name=owners_and_names[owner], owner=owner, file='license.txt')
        ru = getRampUpScore(
            name=owners_and_names[owner], owner=owner, file='rampup_time.txt')

        final_score = calcFinalScore(
            bf=bf, cr=cr, rm=rm, lc=lc, ru=ru, owner_url=owners_and_urls[owner])
        # url, ru, cr, bf, rm, lc
        urls_and_final_scores[owners_and_urls[owner]] = final_score
        attributes_of_url[owners_and_urls[owner]] = [ru, cr, bf, rm, lc]

    urls_ranked_by_score = dict(
        sorted(urls_and_final_scores.items(), key=lambda x: x[1], reverse=True))
    for url in urls_ranked_by_score:
        writeFinalScore(
            arr=attributes_of_url[url], score_truncated=urls_ranked_by_score[url], owner_url=url, outfile='outfile.txt')
