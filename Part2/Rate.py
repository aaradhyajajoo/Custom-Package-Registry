import zipfile
import re
import os
from github import Github
import tempfile
import requests


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
        package_name = npm_match.group(1)
        # Make request to npm registry API
        npm_api_url = f'https://registry.npmjs.org/{package_name}'
        response = requests.get(npm_api_url)
        if response.status_code != 200:
            return None
        package_info = response.json()
        # Extract repository information from package info
        repo_url = package_info.get('repository', {}).get('url')
        if not repo_url:
            return None
        github_match = re.match(r'^https?://(?:www\.)?github\.com/([^/]+)/([^/]+)/?$', repo_url)
        if github_match:
            owner = github_match.group(1)
            repo_name = github_match.group(2)
            return (owner, repo_name)
    # Check if URL is a GitHub repository URL
    github_match = re.match(r'^https?://(?:www\.)?github\.com/([^/]+)/([^/]+)/?$', url)
    if github_match:
        owner = github_match.group(1)
        repo_name = github_match.group(2)
        return (owner, repo_name)
    # URL is not a valid npm package URL or GitHub repository URL
    return None


def calculate_reviewed_code_fraction(github_url):
    """Calculate the fraction of project code introduced through pull requests with code reviews"""
    g = Github()
    repo = g.get_repo(github_url.split('github.com/')[1].strip('/'))
    pull_request_commits = set()
    for pr in repo.get_pulls(state='closed'):
        if pr.merged:
            for commit in pr.get_commits():
                pull_request_commits.add(commit.sha)
    total_lines = 0
    reviewed_lines = 0
    for commit in repo.get_commits():
        if commit.sha in pull_request_commits:
            for file in commit.files:
                reviewed_lines += file.changes
        for file in commit.files:
            total_lines += file.changes
    return float(reviewed_lines) / total_lines if total_lines > 0 else 0.0
#hi
