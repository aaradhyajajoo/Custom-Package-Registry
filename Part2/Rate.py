import zipfile
import re
import os
from github import Github

def get_package_name(package_file):
    """Extract the package name from a zipped package file"""
    with zipfile.ZipFile(package_file, 'r') as z:
        for filename in z.namelist():
            if filename.endswith('setup.py'):
                with z.open(filename) as f:
                    setup_content = f.read().decode('utf-8')
                    match = re.search(r'name\s*=\s*[\'"]([^\'"]+)[\'"]', setup_content)
                    if match:
                        return match.group(1)
    return None

def unzip_package(file_path, target_dir):
    """Unzip a package to the target directory"""
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(target_dir)


def calculate_dependency_metric(package_file):
    """Calculate the fraction of dependencies
      that are pinned to a specific major+minor version"""
    target_dir = 'temp_unzip_dir'
    unzip_package(package_file, target_dir)
    requirements_file = os.path.join(target_dir, 'requirements.txt')
    if not os.path.exists(requirements_file):
        return 1.0
    with open(requirements_file, 'r') as f:
        lines = f.readlines()
        if len(lines) == 0:
            return 1.0
        num_deps = len(lines)
        num_pinned_deps = 0
        for line in lines:
            match = re.search(r'==(\d+\.\d+)', line)
            if match:
                version = match.group(1)
                if version.startswith('2.3.'):
                    num_pinned_deps += 1
        return float(num_pinned_deps) / num_deps

def get_github_url(package_id): #Need to find a way to get github URL , this only works if its on PYPI 
    """Get the GitHub URL of a package given its ID"""
    url = f'https://pypi.org/pypi/{package_id}/json'
    response = re.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    info = data['info']
    if 'project_urls' in info:
        project_urls = info['project_urls']
        if 'Source' in project_urls:
            source_url = project_urls['Source']
            if 'github.com' in source_url:
                return source_url
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
