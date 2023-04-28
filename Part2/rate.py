''' Import Statements '''
import zipfile
import re
import os
import tempfile
import requests
import binascii
import base64
import io
import json
from url_handler import *
import os
import shutil
import git
from bs4 import BeautifulSoup


def decode_into_zipFile(content):
    with open('ZipFile_decoded/package.zip', 'wb') as zip_file:
        zip_file.write(decoded_content)

def get_decoded_content(content):
    # Get decoded file contents
    try:
        decoded_contents = base64.b64decode(content)
    except binascii.Error:
        return 'Binascii Error'

    # Write to temporary file
    tmpfile = tempfile.NamedTemporaryFile()
    with open(tmpfile.name, "wb") as writefile:
        writefile.write(decoded_contents)

    try:
        zipped_repo = zipfile.ZipFile(tmpfile.name)
    except zipfile.BadZipFile:
        return 'Invalid Zipfile'

    # Get URL from package.json
    for filename in zipped_repo.namelist():
        if os.path.basename(filename) == "package.json":
            for line in zipped_repo.open(filename):
                if "github" in str(line) or "npmjs" in str(line):
                    line_string = str(line, 'utf-8').strip()
                    segments = line_string.split('"')
                    clean_url = [
                        i for i in segments if "github" in i or "npmjs" in i][0].strip()
                    if clean_url.endswith(".git"):
                        clean_url = clean_url[:-4]
                    repo_url = get_github_url(clean_url)
                    zipped_repo.close()
                    return repo_url

    # print("No URL found")
    return 'No URL found'  # For now


def calculate_dependency_metric(package_json, version_spec):
    if not package_json:
        return None
    dependencies = package_json['dependencies']
    num_pinned_dependencies = sum(1 for version in dependencies.values() if version.startswith(version_spec))
    total_dependencies = len(dependencies)

    fraction = num_pinned_dependencies / total_dependencies if total_dependencies > 0 else 1.0
    return fraction


def extract_repo_info(url):
    # Check if URL is an npm package URL
    npm_match = re.match(
        r'^https?://(?:www\.)?npmjs\.com/package/([^/]+)/?$', url)
    if npm_match:
        print('NPM Match')
        response = requests.get(url)
        repo_url = response.json()['repository']['url']
        repo_url = repo_url.split(
            '//')[1].split('@')[-1].split(':')[0].replace('.git', '')
        owner, repo_name = repo_url.split('/')
        return owner, repo_name, 'npm'
    # Check if URL is a GitHub repository URL
    github_match = re.match(
        r'^https?://(?:www\.)?github\.com/([^/]+)/([^/]+)/?$', url)
    if github_match:
        print('GitHub match')
        owner = github_match.group(1)
        repo_name = github_match.group(2)
        print(f'Owner. Repo name = {owner},{repo_name}')
        return owner, repo_name, 'github'
    # URL is not a valid npm package URL or GitHub repository URL
    return None, None, None


def calculate_review_fraction(owner, repo):
    # Get pull request data from GitHub API
    api_url = f'https://api.github.com/repos/{owner}/{repo}/pulls'
    headers = {'Accept': 'application/vnd.github.v3+json'}
    response = requests.get(api_url, headers=headers)

    # Check for errors
    if response.status_code != 200:
        return None


    # Calculate review fraction
    pr = response.json()[0]
    # print(pr)
    # print(type(pull_requests))

    # if 'state' in pr.keys() or 'merged_at' in pr.keys():
    #     print('Found')
    reviewed_code = 0
    total_code = 0

    if pr['state'] == 'closed' and pr['merged_at'] is not None:
        # print('here')
        pr_response = requests.get(pr['url'], headers=headers)
        pr_data = pr_response.json()
        print(pr_data['addditions'], pr_datadata['deletions'], pr['review_comments'],pr['comments'])
        total_code += pr_data['additions'] + pr_data['deletions']
        if pr_data['review_comments'] > 0 or pr_data['comments'] > 0:
            reviewed_code += pr_data['additions'] + pr_data['deletions']
    if total_code == 0:
        return 0
    return reviewed_code / total_code


def get_package_json(package_url, ty):

    if ty == 'npm':
        package_name = package_url.split("/")[-1]
        # Construct package metadata API URL
        metadata_url = f"https://registry.npmjs.org/{package_name}"
        response = requests.get(metadata_url)
        # Get the latest version of the package
        version = json.loads(response.text)["dist-tags"]["latest"]
        # Construct package.json file URL
        package_json_url = f"https://cdn.jsdelivr.net/npm/{package_name}@{version}/package.json"
        # Send GET request to package.json file URL
        response = requests.get(package_json_url)
        package_json = response.json()
        return package_json
        # return response.text

    elif ty == 'github':
        response = requests.get(package_url)
        package_json = response.json()
        if package_json and 'content' not in package_json.keys():
            return None
        file_contents = package_json['content']
        decoded_contents = base64.b64decode(file_contents).decode('utf-8')
        return_json = json.loads(decoded_contents)
        return return_json
    return None

def licenseScore(owner,repo_name):

    try:
        # Check if it is an npm package
        response = requests.get(f"https://registry.npmjs.org/{repo_name}")
        if response.status_code == 200:
            data = response.json
            try:
               license_key = data["versions"][data["dist-tags"]["latest"]]["license"]

            except KeyError:
              license_key = "N/A"

    except:
     url = f"https://api.github.com/repos/{owner}/{repo_name}"
     headers = {"Accept": "application/vnd.github.v3+json"}
     res = requests.get(url, headers=headers)
     data = res.json()
     license_info = data["license"]
     license_key = license_info["key"]


    # These are set for outputting to the file that the final Python file reads

    try:
        score = CheckCompatibility(license_key)


    except:
        score = CheckCompatibility('N/A')
    return score

def CheckCompatibility(license):
    # These lists of compatible and incompatible licenses are based on documents found online under the GPL licensing information website, will be linked in readme
    # If its listed as other, that means that there is a license, but not explicitly stated within the repository and is under a readme.
    # We were not able to regex readme, so we are assuming that lgpl is compatible as it is more common than not, compatible with licenses
    incompatible = ['afl-3.0', 'cc', 'cc0-1.0', 'cc-by-4.0', 'epl-1.0', 'epl-2.0', 'agpl-3.0', 'postgresql', 'N/A']
    compatible = ['artistic-2.0', 'bsl-1.0', 'bsd-2-clause', 'bsd-3-clause', 'BSD-3-Clause', 'Apache-2.0', 'BSD-2-Clause', 'Unlicense', 'bsd-3-clause-clear', 'mit', 'MIT', 'wtfpl', 'gpl', 'gpl-2.0', 'gpl-3.0', 'lgpl', 'lgpl-2.1', 'lgpl-3.0', 'isc', 'lppl-1.3c', 'ms-pl', 'mpl-2.0', 'osl-3.0', 'ofl-1.1', 'unlicense', 'zlib', 'ncsa', 'other', 'apache-2.0', 'ISC']

    # These lists will now compared with the license passed in the parameter to see it is compatible
    score = 0
    if license in compatible:
        score = 1
    return score


def get_github_repo_readme(owner, repo):
    """Retrieve the contents of the README file for a given GitHub repository."""
    repo_url = f'https://github.com/{owner}/{repo}'

    # response = requests.get(url)
    # print(f'RESPONSE = {response.json}')
    # if response.status_code == 200:
    #     return response.text
    # return None

    # repo_url = "https://github.com/username/repo"

    response = requests.get(repo_url)
    soup = BeautifulSoup(response.content, "html.parser")

    readme_link = soup.find("a", {"title": "README.md"})
    if readme_link:
        readme_url = "https://github.com" + readme_link["href"]
        response = requests.get(readme_url)
        readme_text = response.text
        return True
    else:
        return False

def calculate_ramp_up_score(owner, repo):
    """Calculate the ramp-up score for a given GitHub repository."""
    readme = get_github_repo_readme(owner, repo)

    if readme:
        rampup_time = 1
    else:
        rampup_time = 0
    print(f'Ramp_up = {rampup_time}')
    return rampup_time
