''' Import Statements '''
import zipfile
import re
import os
import tempfile
import requests
import binascii
import base64
import io


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
                    repo_url = url_handler.get_github_url(clean_url)
                    zipped_repo.close()
                    return repo_url

    return 'No URL found' # For now

def calculate_dependency_metric(package_id):
    # Retrieve package metadata
    response = requests.get(f'https://pypi.org/pypi/{package_id}/json/')
    if response.status_code != 200:
        return 1.0
    metadata = response.json()

    # Extract package name and version requirements
    name = metadata['info']['name']
    if 'requires_dist' not in metadata['info']:
        return 1.0
    requirements = metadata['info']['requires_dist']

    #requirements = metadata['info']['requires_dist']

    # Download and extract package files
    download_url = metadata['urls'][0]['url']
    with tempfile.TemporaryDirectory() as tmpdir:
        package_zip_file = os.path.join(tmpdir, f'{name}.zip')
        with open(package_zip_file, 'wb') as f:
            response = requests.get(download_url)
            f.write(response.content)
        with zipfile.ZipFile(package_zip_file, 'r') as zip_ref:
            zip_ref.extractall(tmpdir)

        # Calculate dependency metric
        requirements_file = os.path.join(tmpdir, name, 'requirements.txt')
        if not os.path.exists(requirements_file):
            return 1.0
        with open(requirements_file, 'r') as f:
            lines = f.readlines()
            if len(lines) == 0:
                return 1.0
            num_deps = len(lines)
            num_pinned_deps = 0
            for line in lines:
                match = re.search(r'==([0-9]+\.[0-9]+)', line)
                if match:
                    version = match.group(1)
                    if version.count('.') == 1:
                        num_pinned_deps += 1
            if num_deps == 0:
                return 1.0
            elif num_pinned_deps == 0:
                return 0.0
            elif num_pinned_deps == 1:
                return 0.5
            else:
                return float(num_pinned_deps) / num_deps

def extract_repo_info(url):
    # Check if URL is an npm package URL
    npm_match = re.match(r'^https?://(?:www\.)?npmjs\.com/package/([^/]+)/?$', url)
    if npm_match:
        response = requests.get(url)
        repo_url = response.json()['repository']['url']
        repo_url = repo_url.split('//')[1].split('@')[-1].split(':')[0].replace('.git', '')
        owner, repo_name = repo_url.split('/')
        return owner, repo_name
    # Check if URL is a GitHub repository URL
    github_match = re.match(r'^https?://(?:www\.)?github\.com/([^/]+)/([^/]+)/?$', url)
    if github_match:
        owner = github_match.group(1)
        repo_name = github_match.group(2)
        return owner, repo_name
    # URL is not a valid npm package URL or GitHub repository URL
    return None, None


def calculate_review_fraction(owner, repo):
    # Get pull request data from GitHub API
    api_url = f'https://api.github.com/repos/{owner}/{repo}/pulls'
    headers = {'Accept': 'application/vnd.github.v3+json'}
    response = requests.get(api_url, headers=headers)


    # Check for errors
    if response.status_code != 200:
        return 0.0

    # Calculate review fraction
    pull_requests = response.json()
    reviewed_code = 0
    total_code = 0
    for pr in pull_requests:
        if pr['state'] == 'closed' and pr['merged_at'] is not None:
            pr_response = requests.get(pr['url'], headers=headers)
            pr_data = pr_response.json()
            total_code += pr_data['additions'] + pr_data['deletions']
            if pr_data['review_comments'] > 0 or pr_data['comments'] > 0:
                reviewed_code += pr_data['additions'] + pr_data['deletions']
    if total_code == 0:
        return 0.0
    return reviewed_code / total_code



