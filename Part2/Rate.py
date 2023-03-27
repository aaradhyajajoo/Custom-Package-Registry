import zipfile
import re

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
    """Calculate the fraction of dependencies that are pinned to a specific major+minor version"""
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

def get_package_url(package_name):
    """Get the URL of a package on GitHub"""
    # Replace this with your own logic for obtaining the URL
    return f'https://github.com/{package_name}'

