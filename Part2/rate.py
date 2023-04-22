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
                    clean_url = [i for i in segments if "github" in i or "npmjs" in i][0].strip()
                    if clean_url.endswith(".git"):
                        clean_url = clean_url[:-4]
                    repo_url = get_github_url(clean_url)
                    zipped_repo.close()
                    return repo_url

    return 'No URL found' # For now

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
    npm_match = re.match(r'^https?://(?:www\.)?npmjs\.com/package/([^/]+)/?$', url)
    if npm_match:
        print('NPM Match')
        response = requests.get(url)
        repo_url = response.json()['repository']['url']
        repo_url = repo_url.split('//')[1].split('@')[-1].split(':')[0].replace('.git', '')
        owner, repo_name = repo_url.split('/')
        return owner, repo_name, 'npm'
    # Check if URL is a GitHub repository URL
    github_match = re.match(r'^https?://(?:www\.)?github\.com/([^/]+)/([^/]+)/?$', url)
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
