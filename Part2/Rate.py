
def get_package_version(package_name):
    try:
        return pkg_resources.get_distribution(package_name).version
    except pkg_resources.DistributionNotFound:
        return None
        
import requests
import re

def calculate_dependency_pinning(package_name, specific_version):
    # Get the package's metadata from PyPI
    response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
    data = response.json()

    # Extract the dependencies from the metadata
    dependencies = []
    if "dependencies" in data["info"]:
        dependencies += data["info"]["dependencies"]
    if "dev_dependencies" in data["info"]:
        dependencies += data["info"]["dev_dependencies"]

    # Count the number of dependencies that are pinned to the specific version
    pinned_count = 0
    for dependency in dependencies:
        match = re.search(f"{specific_version}\\b", dependency)
        if match:
            pinned_count += 1

    # Calculate the rating based on the pinned count
    if len(dependencies) == 0:
        rating = 1.0
    else:
        rating = pinned_count / len(dependencies)

    return rating


