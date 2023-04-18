from flask import request
import re

def package_by_regex():
    # get the unformatted regex
    req_body = request.get_data(as_text=True)

    # format the regex to make it compatible with code.
    regex_pattern = req_body.strip()

    # get the packages from the regex
    matched_packages = search_packages_by_regex(regex_pattern)

    # JSON format
    response = []
    for package in matched_packages:
        package_metadata = {
            'Version': package.version,
            'Name': package.name
        }
        response.append(package_metadata)

    # Return the response as the HTTP response body with 200 status code
    return {'packages': response}, 200

def search_packages_by_regex(regex_pattern):
    # Implement the search logic that uses the regular expression pattern
    packages = [
        #Not really sure of package structure, can change later. Below is an example
        {'name': '...'},
    ]

    matched_packages = []
    for package in packages:
        #Also subjest to change based of structure. For now this is based off of structure
        if re.search(regex_pattern, package['name']):
            matched_packages.append(package)

    return matched_packages

