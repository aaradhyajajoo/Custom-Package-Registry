'''Import Statements'''

# Part 1  (inherited codebase)
from ECE_461_new import compiledqueries
from rate import *
import base64

# Error Class
from errors import Err_Class

# Firebase Connection
from firebase_admin import db, credentials
import firebase_admin
from flask import Flask, request, jsonify, render_template
import json
import os
from firestore import decode_service_account

# Regex Endpoint
import re

# Package Endpoint
import gzip
'''Global Variable(s)'''
PROJECT_ID = "ece-461-ae1a9"
PORT_NUMBER = 5000

'''Inits'''
err = Err_Class()  # Errors
app = Flask(__name__)  # Initializing Flask app
decode_service_account()
cred = credentials.Certificate("service_account.json")
firebase_admin.initialize_app(cred, options={
    'databaseURL': f'https://{PROJECT_ID}-default-rtdb.firebaseio.com'
})


'''Endpoints'''

#ENDPOINTS
# curl -X 'POST' 'http://127.0.0.1:8080/package/' -H 'accept: application/json' -H 'X-Authorization: j' -H 'Content-Type: application/json' -d '{"Content": "check", "JSProgram": "if (process.argv.length === 7) {\nconsole.log('\''Success'\'')\nprocess.exit(0)\n} else {\nconsole.log('\''Failed'\'')\nprocess.exit(1)\n}\n"}'
# POST Package Create and POST Package Ingest


@app.route('/package', methods=['POST'])
def create():

    # Checks Authorization
    authorization = None
    authorization = request.headers.get("X-Authorization")
    if authorization is None:
        return err.auth_failure()

    # Gets the JSON data from the request
    data = request.get_json()

    # Checking error 404
    if not data:
        if 'URL' not in data.keys() and 'Content' not in data.keys():
            return err.missing_fields()

    # URL examples
    # url = "https://github.com/jashkenas/underscore"
    # url = "https://www.npmjs.com/package/browserify"
    if 'URL' in data.keys():
        url = data['URL']
        if 'npm' in url:
            package_json = get_package_json(url, 'npm')
            print(package_json)
            ty = 'npm'
        elif 'github' in url:
            owner, repo, ty = extract_repo_info(url)
        else:
            return err.malformed_req()

    elif 'Content' in data.keys():
        content = data['Content']
        url = get_decoded_content(content)
        print(f'URL : {url}')
        if 'npm' in url:
            package_json = get_package_json(url, 'npm')
            print(f'Package json: {package_json}')
            ty = 'npm'
        elif 'github' in url:
            owner, repo, ty = extract_repo_info(url)
            print(f'In main: {owner},{repo}')
        else:
            return err.missing_fields()


    file_path = "package.json"

    # Construct the API URL for the package.json file
    if ty == 'github':
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
        print(f'API URL: {api_url}')
        package_json = get_package_json(api_url, 'github')
        print(f'Package json: {package_json}')
        if not package_json:
            return err.malformed_req()
        if 'name' not in package_json.keys() or 'version' not in package_json.keys():
            return err.missing_fields()

        name = package_json['name']
        version = package_json['version']
        ID = f"{name}_{version}"

    elif ty == 'npm':
        if not package_json:
            err.malformed_req()
        name = package_json['name']
        version = package_json['version']
        ID = f"{name}_{version}"

    metadata = {'Name': name, 'Version': version, 'ID': ID}
    data_field = data

    ''' NEED TO CALL RATING FUNCTION TO GET RATE AND CHECK ERROR 424 '''
    # Need to check error 424

    # if rate < 0.5:
    #     err.disqualified_rating()

    package = {
        'metadata': metadata,
        'data': data_field
    }

    ref = db.reference('packages')  # Reference to node in Firebase
    json_store = ref.get()  # Gets the data in the DB
    print(f'Json stored in the db = {json_store}')

    if json_store is None:
        print('DB is empty, adding new data')
        ref.push(package)  # Upload data to package
    else:  # If some packages already exist in the DB
        unique_id_list = []
        unique_version_list = []
        unique_name_list = []
        firebaseIDs_list = []

        # Extracts the IDs of the metadata in the DB
        for ids in json_store.keys():
            firebaseIDs_list.append(ids)
            unique_id_list.append(json_store[ids]['metadata']['ID'])
            unique_version_list.append(json_store[ids]['metadata']['Version'])
            unique_name_list.append(json_store[ids]['metadata']['Name'])

        # print(f'Unique id list = {unique_id_list}')
        if ID in unique_id_list and version not in unique_version_list and name not in unique_name_list:
            # Ingestion - Add/Update the Firebase Database
            i = unique_id_list.index(ID)
            firebaseID = firebaseIDs_list[i]  # Gets firebase ID
            if 'URL' in list(data_field.keys()):
                # Check if (URL does not exist in the DB) or if (it does then the one being uploaded is different)
                if (metadata == json_store[firebaseID]['metadata'] and 'URL' not in json_store[firebaseID]['data']) or \
                        (metadata == json_store[firebaseID]['metadata'] and 'URL' in json_store[firebaseID]['data'] and data_field['URL'] != json_store[firebaseID]['data']['URL']):
                    print('Ingestion required')
                    ref = db.reference('packages/' + firebaseID)
                    update_data = {
                        'data': {
                            'URL': data_field['URL'],
                            # Merge with existing data
                            **ref.child('data').get()
                        }
                    }
                    ref.update(update_data)  # Updates DB
                    package = ref.get('packages/' + firebaseID)
                    return json.dumps(package), 201
                else:
                    return err.package_exists()
        elif ID not in unique_id_list:
            ref.push(package)
        else:
            return err.package_exists()

    return json.dumps(package), 201

# Curl requests: curl --location 'http://127.0.0.1:8080/packages?offset=2' --header 'X-Authorization: bearer \
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c' \
# --header 'Content-Type: application/json' --data '[{"Version":"1.2.3","Name":"Underscore"},{"Version":"1.2.3-2.1.0","Name":"Lodash"}]'
# Modify "Name":"*" to test return of all packages
# POST Get Packages


@app.route('/packages', methods=['POST'])
def list_of_packages():
    # Checks Authorization
    authorization = None
    authorization = request.headers.get("X-Authorization")
    if authorization is None:
        return err.auth_failure()

    # Gets package query from request body
    package_queries = request.json
    offset = request.args.get('offset', default=0, type=int)

    # Default offset is 1 page
    limit = 1
    if not offset:
        offset = 1

    # Checking error 400
    if (not package_queries):
        return err.missing_fields()

    # print(f'Package Queries = {package_queries}')
    pack_list = []  # List of packages to be returned

    ref = db.reference('packages')

    # Gets the firebaseIDs as keys and the values as the packages we need
    all_packages = ref.get()
    uniq_pack_list = []
    for query in package_queries:
        # Returning all packages
        if query['Name'] == "*":
            for package in all_packages.values():
                pack_list.append(package['metadata'])
        # Returning specific packages
        else:
            for package in all_packages.values():  # Checking all packages in the DB for each query
                if package['metadata'] not in uniq_pack_list:
                    if query['Name'] == package['metadata']['Name'] and query['Version'] == package['metadata']['Version']:
                        pack_list.append(package['metadata'])

            uniq_pack_list = [dict(t)
                              for t in {tuple(d.items()) for d in pack_list}]

    save = []
    j = 0
    for i in range(offset):
        x = []
        while j < len(uniq_pack_list):
            if len(x) <= limit:
                x.append(uniq_pack_list[j])
                save.append(x[j])
                j += 1

    if len(save) == 0:
        return err.package_doesNot_exist()

    return json.dumps(save), 200

# Test Command: curl --location --request DELETE 'http://127.0.0.1:8080/reset' --header /
# 'X-Authorization: bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI /
# 6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
# DELETE Reset Registry


@app.route('/reset/', methods=['DELETE'])
def reset_registry():
    # Checks Authorization
    authorization = None
    authorization = request.headers.get("X-Authorization")
    if authorization is None:
        return err.no_permission()
    ref = db.reference('packages')
    ref.delete()


# GET, PUT, DELETE - Package with given ID in endpoint

@app.route('/package/<id>', methods=['GET', 'PUT', 'DELETE'])
def package_given_id(id):
    # Checks Authorization
    authorization = None
    authorization = request.headers.get("X-Authorization")
    if authorization is None:
        return err.auth_failure()
    if request.method == 'GET':
        return PackageRetrieve(id)
    if request.method == 'PUT':
        return PackageUpdate(id)
    if request.method == 'DELETE':
        return PackageDelete(id)


# Curl requests:
# Correct: curl -X 'GET' 'http://127.0.0.1:8080/package/underscore' -H 'accept: application/json' -H 'X-Authorization: bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
def PackageRetrieve(id):
    ref = db.reference('packages')
    all_packages = ref.get()

    for p_data in all_packages.values():
        metadata = p_data['metadata']
        if id == metadata['ID']:
            return json.dumps(p_data), 200
    return err.package_doesNot_exist()


# Correct: curl -X 'PUT' 'http://127.0.0.1:8080/package/underscore' -H 'accept: */*' -H 'X-Authorization: bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c' -H 'Content-Type: application/json' -d '{"metadata": {"Name": "Underscore","Version": "1.0.0","ID": "underscore"},"data": {"URL": "string","JSProgram": "string"}}'
def PackageUpdate(id):
    ref = db.reference('packages')
    all_packages = ref.get()

    data = request.json
    id_exists = False

    # As per PackageUpdate, only one field must be set
    if 'Content' in data['data'].keys() and 'URL' in data['data'].keys():
        return err.missing_fields()

    # Gets firebaseID of the package (metadata in this case) that we need to update
    # print(all_packages.items())
    for firebaseID, p_data in all_packages.items():
        metadata = p_data['metadata']
        if id == metadata['ID']:
            id_exists = True
            break

    if not id_exists:
        return err.malformed_req()

    # Name, version, ID must match
    if (metadata['Name'] != data['metadata']['Name']) or (metadata['Version'] != data['metadata']['Version']) \
            or (metadata['ID'] != data['metadata']['ID']):
        return err.package_doesNot_exist()

    # Updating the specific child node in the DB
    ref = db.reference('packages/' + firebaseID)
    if 'URL' in data['data'].keys():
        update_data = {
            'data': {
                'URL': data['data']['URL'],
                'JSProgram': data['data']['JSProgram']
            }
        }
    elif 'Content' in data['data'].keys():
        update_data = {
            'data': {
                'Content': data['data']['Content'],
                'JSProgram': data['data']['JSProgram']
            }
        }

    ref.update(update_data)  # Updates DB
    return json.dumps({'message': 'Version is updated.'}), 200


def PackageDelete(id):
    ref = db.reference('packages')
    all_packages = ref.get()

    id_exists = False

    # Gets firebaseID of the package (metadata in this case) that we need to update

    for firebaseID, p_data in all_packages.items():
        metadata = p_data['metadata']
        if not metadata:
            err.missing_fields()
        if id == metadata['ID']:
            id_exists = True
            del_ref = db.reference('packages/'+firebaseID)
            del_ref.delete()
            break  # What to do if there are multiple packages to be deleted
    if not id_exists:
        return err.package_doesNot_exist()

    return json.dumps({'message': 'Package is deleted.'}), 200


# Correct: curl -X 'GET' 'http://127.0.0.1:8080/package/underscore/rate' -H 'accept: application/json' -H 'X-Authorization: f'
@app.route('/package/<id>/rate/', methods=['GET'])
def metric_rate(id):
    # Checks Authorization
    authorization = None
    authorization = request.headers.get("X-Authorization")
    # print(f'req = {request}')
    # if authorization is None:
    #     return err.auth_failure()

    # Get package data from Firebase
    check_package = False

    ref = db.reference('packages')
    all_packages = ref.get()
    if not all_packages:
        return err.malformed_req()

    # Checks if Package exists in FireStore Databae
    print('Checking package_data')
    package_data = None
    for firebaseID, p_data in all_packages.items():
        metadata = p_data['metadata']
        if 'ID' not in metadata.keys():
            err.missing_fields()  # Error 400
        if id == metadata['ID']:
            package_data = p_data
            check_package = True
            break
    # Tries to find name and version in Database
    p_name = p_data['metadata']['Name']
    p_version = p_data['metadata']['Version']
    if not p_name or not p_version:
        return err.missing_fields()

    # Checking error 404
    if not check_package or not package_data or 'data' not in package_data.keys():
        return err.package_doesNot_exist()

    data = package_data['data']

    #Decodes the encoded content field from Data. Also checks if there is no URL in meta data
    if 'Content' in data.keys() and 'URL' not in data.keys():
        print('Reading content')
        content = data['Content']
        print('Content')
        if content is None:
            return err.missing_fields()
        url = get_decoded_content(content)

    elif 'Content' not in data.keys() and 'URL' in data.keys():
        # Get package URL from package data if it does not contain content
        url = data['URL']
        if url is None:
            return err.missing_fields()
    # Check if URL is npm or github
    if 'npm' in url:
            package_json = get_package_json(url, 'npm')
            print(f'Package json: {package_json}')
            ty = 'npm'
    elif 'github' in url:
            owner, repo, ty = extract_repo_info(url)
    else:
            return err.missing_fields()


    file_path = "package.json"

    # Construct the API URL for the package.json file
    if ty == 'github':
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
         #print(f'API URL: {api_url}')
        package_json = get_package_json(api_url,'github')
        if not package_json:
            return err.malformed_req()

    elif ty == 'npm':
        if not package_json:
            err.malformed_req()

    owner, name, ty = extract_repo_info(url)
    if owner is None or name is None or ty is None:
        return err.unexpected_error() # Error 500 (Did not find owner or repo)

    #  Calculate metrics (5 metrics from Part 1 and 2 new metrics)
    code_review = calculate_review_fraction(owner, name)
    if code_review is  None:
        #print('code review')
        return err.unexpected_error()
    dependency = calculate_dependency_metric(package_json, p_version)
    if dependency is None:
        #print('dependency')
        return err.unexpected_error()
    bus_factor = compiledqueries.getBusFactorScore(owner, name)
    if bus_factor is None:
        #('bus factor')
        return err.unexpected_error()
    responsiveness = compiledqueries.getResponsiveMaintainersScore(owner, name)
    if not responsiveness:
        #print('responsiveness')
        return err.unexpected_error()
    correctness = compiledqueries.getCorrectnessScore(owner, name)
    if not correctness:
        #print('correctness')
        return err.unexpected_error()
    license_score = licenseScore(owner,name)
    if not license_score:
        return err.unexpected_error()
    ramp_up = calculate_ramp_up_score(owner,name)
    if not ramp_up:
        return err.unexpected_error()

    net_score = 0.7 * (compiledqueries.calcFinalScore(bus_factor, license_score, correctness, ramp_up, responsiveness, owner) ) + 0.2 * dependency + 0.1 *code_review
    if not net_score:
        return err.unexpected_error() # Calculations for metrics choked
    metric_dict = {}
    metric_dict = {'BusFactor': bus_factor,
              'Correctness': correctness,
              'RampUp': ramp_up,
              'Responsiveness': responsiveness,
              'LicenseScore': license_score,
              'GoodPinningPractice': dependency,
              'CodeReviewFractiom': code_review,
              'NetScore': net_score
              }

    return json.dumps(metric_dict),200


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/authenticate/', methods=['PUT'])
def authenticate():
    return err.no_authentication()


@app.route('/package/byRegEx/', methods=['POST'])
def package_by_regex():
    # format the regex to make it compatible with code.
    regex = request.json
    regex_pattern = regex['RegEx']
    if not regex_pattern:
        return err.missing_fields()

    # get the packages from the regex
    matched_packages = search_packages_by_regex(regex_pattern)

    # Checking error 404
    if len(matched_packages) == 0:
        return err.package_doesNot_exist()

    print(f'm_p = {matched_packages}')

    # JSON format
    response = []
    for package in matched_packages:
        package_metadata = {
            'Version': package['Version'],
            'Name': package['Name']
        }
        response.append(package_metadata)

    return json.dumps(response), 200


def search_packages_by_regex(regex_pattern):
    # Implement the search logic that uses the regular expression pattern
    packages = []

    ref = db.reference('packages')
    all_packages = ref.get()

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


@app.route('/ui/package', methods=['GET', 'POST'])
def package_by_name():
    # do the same thing as app.route /ui/package but with a UI
    return render_template('ui_package.html')


@app.route('/upload', methods=['POST'])
def action():
    if 'file' not in request.files:
        return 'No file submitted', 400

    file = request.files['file']
    if file.filename == '':
        return 'No file submitted', 400

    with open("Zipfile/" + file.filename, 'wb') as f:
        f.write(file.read())

    with open("Zipfile/" + file.filename, 'rb') as file:
        # Read the file contents
        file_content = file.read()

        # Encode the compressed content into base64 format
        encoded_content = base64.b64encode(file_content)

        # Convert the encoded content to string
        encoded_string = encoded_content.decode('utf-8')

    # now we have the encoded content in the encoded_content variable.
    # we can use this to call the request.

    url = 'http://127.0.0.1:5000/package'
    headers = {
        'accept': 'application/json',
        'X-Authorization': 'j',
        'Content-Type': 'application/json'
    }
    data = {
        'Content': str(encoded_string),
        'JSProgram': 'if (process.argv.length === 7) {\nconsole.log(\'Success\')\nprocess.exit(0)\n} else {\nconsole.log(\'Failed\')\nprocess.exit(1)\n}\n'
    }
    res = requests.post(url, headers=headers, json=data)
    return res.text


@app.route('/upload_text', methods=['POST'])
def package_text():
    url = 'http://127.0.0.1:5000/package'
    headers = {
        'accept': 'application/json',
        'X-Authorization': 'j',
        'Content-Type': 'application/json'
    }
    data = {
        'URL': str(request.form.get('url')),
        'JSProgram': 'if (process.argv.length === 7) {\nconsole.log(\'Success\')\nprocess.exit(0)\n} else {\nconsole.log(\'Failed\')\nprocess.exit(1)\n}\n'
    }

    res = requests.post(url, headers=headers, json=data)
    return res.text


@app.route('/ui/packages', methods=['GET', 'POST'])
def render_all_packages():
    return render_template('ui_packages.html')


@app.route('/ui/packages_render', methods=['GET', 'POST'])
def render_all_packages_data():
    # call the function list_of_packages to get all the packages
    # create a dictionary to store the data
    url = 'http://127.0.0.1:8080/packages'
    headers = {
        'accept': 'application/json',
        'X-Authorization': 'j',
        'Content-Type': 'application/json'
    }
    data = [{
        "Version": str(request.form.get('version')),
        "Name": str(request.form.get('name'))
    }]

    response = requests.post(url, headers=headers, json=data)
    if response.status_code < 300:
        data = {
            'id': response.json()[0]["ID"],
            'name': response.json()[0]["Name"],
            'version': response.json()[0]["Version"]
        }
        return render_template('ui_packages_render.html', data=data)
    else:
        return response.text


@app.route('/ui/reset/', methods=['GET', 'POST'])
def reset_all():
    return render_template('ui_reset.html')


@app.route('/ui/reset_registry', methods=['GET', 'POST'])
def reset_all_packages():
    url = 'http://127.0.0.1:8000/reset/'
    headers = {
        'X-Authorization': 'j',
    }
    response = requests.delete(url, headers=headers)
    return response.text


if __name__ == '__main__':
    port = int(os.environ.get('PORT', PORT_NUMBER))
    app.run(host='127.0.0.1', port=port, debug=True)
