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

def search_packages_by_regex(regex_pattern, all_packages):
    # Implement the search logic that uses the regular expression pattern
    packages = []

    for firebaseID, p_data in all_packages.items():
        metadata = p_data['metadata']
        packages.append(metadata)

    count = 0
    matched_packages = []
    for package in packages:
        # Also subject to change based of structure. For now this is based off of structure
        if re.search(regex_pattern, package['Name']):
            matched_packages.append(package)
            count += 1

    return matched_packages