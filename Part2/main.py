'''Import Statements'''
# Part 1  (inherited codebase)
from ECE_461_new import compiledqueries
import rate
import base64
import regex
from datetime import datetime
import random
import requests
import binascii


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
'''Global Variable(s)'''
PROJECT_ID = "ece-461-ae1a9"
PORT_NUMBER = 8080

'''Inits'''
err = Err_Class()  # Errors
app = Flask(__name__)  # Initializing Flask app
# decode_service_account()
# cred = credentials.Certificate("service_account.json")
# firebase_admin.initialize_app(cred, options={
firebase_admin.initialize_app(options={
    'databaseURL': f'https://{PROJECT_ID}-default-rtdb.firebaseio.com'
})

bad_creds = False

'''Endpoints'''

# ENDPOINTS
# curl -X 'POST' 'http://127.0.0.1:8080/package/' -H 'accept: application/json' -H 'X-Authorization: j' -H 'Content-Type: application/json' -d '{"Content": "check", "JSProgram": "if (process.argv.length === 7) {\nconsole.log('\''Success'\'')\nprocess.exit(0)\n} else {\nconsole.log('\''Failed'\'')\nprocess.exit(1)\n}\n"}'
# POST Package Create and POST Package Ingest


@app.route('/package', methods=['POST'])
def create():

    # Checks Authorization
    # authorization = None
    # authorization = request.headers.get("X-Authorization")
    # if authorization is None:
    #     return err.auth_failure(bad_creds)

    # Gets the JSON data from the request
    data = request.get_json()
    # Checking error 404
    if not data:
        if 'URL' not in data.keys() and 'Content' not in data.keys():
            print('Could not find URL and Content')
            return err.missing_fields()

    url_check = False
    # URL examples
    # url = "https://github.com/jashkenas/underscore"
    # url = "https://www.npmjs.com/package/browserify"

    if 'URL' in data.keys() and 'Content' in data.keys():
        str_value_content = str(data['Content'])
        str_value_url = str(data['URL'])
        if data['URL'] is not None and (str_value_content == 'None' or str_value_content == 'null') :
            print('URL is set - Rating is required')
            url_check = True
            url = data['URL']
            print(f'URL that is being checked: {url}')
            if 'npm' in url:
                package_json = rate.get_package_json(url, 'npm')
                ty = 'npm'
            elif 'github' in url:
                owner, repo, ty = rate.extract_repo_info(url)
            else:
                return err.malformed_req()
        
        elif data['Content'] is not None and (str_value_url == 'None' or str_value_url == 'null'):
            print('Content is set - Rating is not required')
            content = data['Content']
            url = rate.get_decoded_content(content)
            print(f'URL that is being checked: {url}')
            if 'npm' in url:
                package_json = rate.get_package_json(url, 'npm')
                ty = 'npm'
            elif 'github' in url:
                owner, repo, ty = rate.extract_repo_info(url)
                if owner is None:
                    return err.unexpected_error('the URL')
            else:
                return err.missing_fields()
        else:
            print('Either one is not None')
            return err.missing_fields()

    file_path = "package.json"

    # Construct the API URL for the package.json file
    if ty == 'github':
        print('Package from github')
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
        package_json = rate.get_package_json(api_url, 'github')
        if not package_json:
            return err.malformed_req()
        if 'name' not in package_json.keys() or 'version' not in package_json.keys():
            return err.missing_fields()

        name = package_json['name']
        version = package_json['version']
        ID = f"{name}_{version}"

    elif ty == 'npm':
        print('Package from npm')
        if not package_json:
            err.malformed_req()
        name = package_json['name']
        version = package_json['version']
        ID = f"{name}_{version}"

    metadata = {'Name': name, 'Version': version, 'ID': ID}
    data_field = data

    ''' NEED TO CALL RATING FUNCTION TO GET RATE AND CHECK ERROR 424 '''
    if url_check:
        # Need to check error 424
        owner, name, ty = rate.extract_repo_info(url)
        print(f'Owner is {owner} and Name is {name}')
        if owner is None or name is None or ty is None:
            # Error 500 (Did not find owner or repo) marcelklehr,nodist
            print("Could not find owner or repo")
            return err.unexpected_error('the URL')

        #  Calculate metrics (5 metrics from Part 1 and 2 new metrics
        code_review = rate.calculate_review_fraction(owner, name)
        if code_review is None:
            print('Code review chokes')
            return err.unexpected_error('CodeReviewFractiom')
        dependency = rate.calculate_dependency_metric(package_json, version)
        if dependency is None:
            print('Dependency chokes')
            return err.unexpected_error('GoodPinningPractice')
        bus_factor = compiledqueries.getBusFactorScore(owner, name)
        if bus_factor is None:
            print('Bus Factor chokes')
            return err.unexpected_error('BusFactor')
        # elif bus_factor == -1:
        #     print('Bus Factor chokes with Bad creds')
        #     return err.unexpected_error('BusFactor')
        responsiveness = compiledqueries.getResponsiveMaintainersScore(
            owner, name)
        if responsiveness is None:
            print('Responsiveness chokes')
            return err.unexpected_error('Responsiveness')
        correctness = compiledqueries.getCorrectnessScore(owner, name)
        if correctness is None:
            print('Correctness chokes')
            return err.unexpected_error('Correctness')

        license_score = rate.licenseScore(owner, name)
        if license_score is None:
            print('LicenseScore chokes')
            return err.unexpected_error('LicenseScore')
        ramp_up = rate.calculate_ramp_up_score(owner, name)

        if ramp_up is None:
            print('Ramp Up chokes')
            return err.unexpected_error('RampUp')

        net_score = 0.7 * (compiledqueries.calcFinalScore(bus_factor, license_score, correctness,
                                                          ramp_up, responsiveness, owner)) + 0.2 * dependency + 0.1 * code_review
        if net_score is None:
            # Calculations for metrics choked
            print('Net Score chokes')
            return err.unexpected_error('NetScore')

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

        print(f'See metric_dict: {metric_dict}')
        if net_score < 0.5:
            print(f'Disqualified score. See metric_dict: {metric_dict}')
            return err.disqualified_rating(key)

    package = {
        'metadata': metadata,
        'data': data_field
    }

    ref = db.reference('packages')  # Reference to node in Firebase
    json_store = ref.get()  # Gets the data in the DB

    if json_store is None:
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

        ID = metadata['ID']
        if ID in unique_id_list:
            # Ingestion - Add/Update the Firebase Database
            i = unique_id_list.index(ID)
            firebaseID = firebaseIDs_list[i]  # Gets firebase ID
            if str_value_url != 'None':
                # Check if (URL does not exist in the DB) or if (it does then the one being uploaded is different)
                if (metadata == json_store[firebaseID]['metadata'] and str(json_store[firebaseID]['data']['URL'])) == 'None' or \
                        (metadata == json_store[firebaseID]['metadata'] and str(json_store[firebaseID]['data']['URL'])!='None' and data_field['URL'] != json_store[firebaseID]['data']['URL']):
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
            else:
                return err.package_exists()
        elif ID not in unique_id_list:
            ref.push(package)
        else:
            return err.package_exists()

    print("Package is created successfully.")
    return json.dumps(package), 201

# Curl requests: curl --location 'http://127.0.0.1:8080/packages?offset=2' --header 'X-Authorization: bearer \
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c' \
# --header 'Content-Type: application/json' --data '[{"Version":"1.2.3","Name":"Underscore"},{"Version":"1.2.3-2.1.0","Name":"Lodash"}]'
# Modify "Name":"*" to test return of all packages
# POST Get Packages


@app.route('/packages', methods=['POST'])
def list_of_packages():
    # Checks Authorization
    # authorization = None
    # authorization = request.headers.get("X-Authorization")
    # if authorization is None:
    #     return err.auth_failure(bad_creds)

    # Gets package query from request body
    package_queries = request.json
    print(f'Packages to be queried = {package_queries}')
    offset = request.args.get('offset', default=0, type=int)

    # Default offset is 1 page
    limit = 1
    if not offset:
        offset = 1

    # Checking error 400
    if (not package_queries):
        return err.missing_fields()

    pack_list = []  # List of packages to be returned

    ref = db.reference('packages')

    # Gets the firebaseIDs as keys and the values as the packages we need
    all_packages = ref.get()
    uniq_pack_list = []
    for query in package_queries:
        # Returning all packages
        if query['Name'] == "*":
            if all_packages is None:
                return err.package_doesNot_exist()
            for package in all_packages.values():
                pack_list.append(package['metadata'])
        # Returning specific packages
        else:
            if all_packages is None:
                return err.package_doesNot_exist()
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
            else:
                return err.too_many_packages()

    if len(save) == 0:
        return err.package_doesNot_exist()



    print("Packages endpoint is working.")
    return json.dumps(save), 200

# Test Command: curl --location --request DELETE 'http://127.0.0.1:8080/reset' --header /
# 'X-Authorization: bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI /
# 6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
# DELETE Reset Registry


@app.route('/reset', methods=['DELETE'])
def reset_registry():
    # Checks Authorization
    # authorization = None
    # authorization = request.headers.get("X-Authorization")
    # if authorization is None:
    #     return err.no_permission()
    ref = db.reference('packages')
    ref.delete()
    print("Reset endpoint is working.")
    return json.dumps('Registry is reset.'), 200

# GET, PUT, DELETE - Package with given ID in endpoint


@app.route('/package/<id>', methods=['GET', 'PUT', 'DELETE'])
def package_given_id(id):
    # Checks Authorization
    # authorization = None
    # authorization = request.headers.get("X-Authorization")
    # if authorization is None:
    #     return err.auth_failure(bad_creds)
    # print(f"Request headers in /package/<id>:{request.headers}")

    if request.method == 'GET':
        print("Get for package with given ID is working.")
        return PackageRetrieve(id)
    if request.method == 'PUT':
        print("Put for package with given ID is working.")
        return PackageUpdate(id)
    if request.method == 'DELETE':
        print("Delete for package with given ID is working.")
        return PackageDelete(id)


# Curl requests:
# Correct: curl -X 'GET' 'http://127.0.0.1:8080/package/underscore' -H 'accept: application/json' -H 'X-Authorization: bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
def PackageRetrieve(id):
    str_value_content = 'None'
    str_value_url = 'None'
    ref = db.reference('packages')
    all_packages = ref.get()

    pack_exists = False

    for p_data in all_packages.values():
        metadata = p_data['metadata']
        if id == metadata['ID']:
            pack_exists = True
            break

    if not pack_exists:
        return err.package_doesNot_exist()

    data_field = p_data['data']
    print(f'data_field = {data_field}')
    if 'Content' in data_field.keys():
        str_value_content = data_field['Content']
    if 'URL' in data_field.keys():
        str_value_url = data_field['URL']

    if str_value_content != 'None' and str_value_url == 'None':
        directory = f'ZipFile_decoded_{datetime.now().strftime("%H_%M_%S")}_{random.randint(0, 1000)}'
        content = data_field['Content']

        try:
            decoded_content = base64.b64decode(content)
        except binascii.Error:
            print('Binascii error')
            return err.malformed_req()

        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(os.path.join(directory, 'package.zip'), 'wb') as zip_file:
            zip_file.write(decoded_content)

        return json.dumps(p_data), 200
    elif str_value_url != 'None':
        return json.dumps(p_data), 200


         


# Correct: curl -X 'PUT' 'http://127.0.0.1:8080/package/underscore' -H 'accept: */*' -H 'X-Authorization: bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c' -H 'Content-Type: application/json' -d '{"metadata": {"Name": "Underscore","Version": "1.0.0","ID": "underscore"},"data": {"URL": "string","JSProgram": "string"}}'
def PackageUpdate(id):
    ref = db.reference('packages')
    all_packages = ref.get()

    data = request.json
    print(f'data = {data}')
    id_exists = False

    # As per PackageUpdate, only one field must be set
    if str(data['data']['Content']) != 'None' and str(data['data']['URL']) != 'None':
        return err.missing_fields()

    # Gets firebaseID of the package (metadata in this case) that we need to update
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
        if str(data['data']['URL']) != 'None':
            update_data = {
                'data': {
                    'URL': data['data']['URL'],
                    'JSProgram': data['data']['JSProgram']
                }
            }
    if 'Content' in data['data'].keys():
        elif str(data['data']['Content']) != 'None':
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
    if not all_packages:
        return err.package_doesNot_exist()
    id_exists = False

    # Gets firebaseID of the package (metadata in this case) that we need to update

    for firebaseID, p_data in all_packages.items():
        metadata = p_data['metadata']
        if not metadata:
            err.missing_fields()
        if id == metadata['ID']:
            id_exists = True
            del_ref = db.reference('packages/' + firebaseID)
            del_ref.delete()
            break  # What to do if there are multiple packages to be deleted
    if not id_exists:
        return err.package_doesNot_exist()

    return json.dumps({'message': 'Package is deleted.'}), 200


# Correct: curl -X 'GET' 'http://127.0.0.1:8080/package/underscore/rate' -H 'accept: application/json' -H 'X-Authorization: f'
@app.route('/package/<id>/rate', methods=['GET'])
def metric_rate(id):
    # Checks Authorization
    # authorization = None
    # authorization = request.headers.get("X-Authorization")
    # if authorization is None:
    #     with open("Testing/test14rate.json", "w") as outfile:
    #         json.dump({"message": "Authentication failed."}, outfile)
    #     return err.auth_failure()


    str_value_content = 'None'
    str_value_url = 'None'
    # Get package data from Firebase
    check_package = False

    ref = db.reference('packages')
    all_packages = ref.get()
    if not all_packages:
        return err.malformed_req()

    # Checks if Package exists in FireStore Databae
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
    print(f"data = {data}")

    if 'Content' in data.keys():
        str_value_content = str(data['Content'])
    if 'URL' in data.keys():
        str_value_url = str(data['URL'])
        
    # Decodes the encoded content field from Data. Also checks if there is no URL in meta data
    if str_value_content != 'None' and str_value_url == 'None':
        content = data['Content']
        url = rate.get_decoded_content(content)

    elif str_value_content == 'None' and str_value_url != 'None':
        # Get package URL from package data if it does not contain content
        url = data['URL']
        if url is None:
            return err.missing_fields()
    # Check if URL is npm or github
    if 'npm' in url:
        package_json = rate.get_package_json(url, 'npm')
        ty = 'npm'
    elif 'github' in url:
        owner, repo, ty = rate.extract_repo_info(url)

    else:
        return err.missing_fields()

    file_path = "package.json"

    # Construct the API URL for the package.json file
    if ty == 'github':
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
        package_json = rate.get_package_json(api_url, 'github')

        if not package_json:
            return err.malformed_req()

    elif ty == 'npm':
        if not package_json:
            err.malformed_req()

    owner, name, ty = rate.extract_repo_info(url)
    if owner is None or name is None or ty is None:
        return err.unexpected_error()  # Error 500 (Did not find owner or repo)

    #  Calculate metrics (5 metrics from Part 1 and 2 new metrics)

    code_review = rate.calculate_review_fraction(owner, name)
    if code_review is None:
        return err.unexpected_error()
    dependency = rate.calculate_dependency_metric(package_json, p_version)
    if dependency is None:
        return err.unexpected_error()
    bus_factor = compiledqueries.getBusFactorScore(owner, name)
    if bus_factor is None:
        return err.unexpected_error()
    responsiveness = compiledqueries.getResponsiveMaintainersScore(owner, name)
    if responsiveness is None:
        return err.unexpected_error()
    correctness = compiledqueries.getCorrectnessScore(owner, name)
    if correctness is None:
        return err.unexpected_error()
    license_score = rate.licenseScore(owner, name)
    if license_score is None:
        return err.unexpected_error()
    ramp_up = rate.calculate_ramp_up_score(owner, name)
    if ramp_up is None:
        return err.unexpected_error()

    net_score = 0.7 * (compiledqueries.calcFinalScore(bus_factor, license_score, correctness,
                       ramp_up, responsiveness, owner)) + 0.2 * dependency + 0.1 * code_review
    if net_score is None:
        return err.unexpected_error()  # Calculations for metrics choked
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


    with open("Testing/test14rate.json", "w") as outfile:
        json.dump(metric_dict, outfile)
    return json.dumps(metric_dict), 200


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/authenticate', methods=['PUT'])
def authenticate():
    print("Hit authenticate endpoint")
    return err.no_authentication()


@app.route('/package/byRegEx', methods=['POST'])
def package_by_regex():
    # format the regex to make it compatible with code.
    r = request.json
    regex_pattern = r['RegEx']
    if not regex_pattern:
        return err.missing_fields()

    ref = db.reference('packages')
    all_packages = ref.get()

    if all_packages is None:
        return err.package_doesNot_exist()

    # get the packages from the regex
    matched_packages = regex.search_packages_by_regex(regex_pattern, all_packages)

    # Checking error 404
    if len(matched_packages) == 0:
        return err.package_doesNot_exist()


    # JSON format
    response = []
    for package in matched_packages:
        package_metadata = {
            'Version': package['Version'],
            'Name': package['Name']
        }
        response.append(package_metadata)

    return json.dumps(response), 200


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

    url = request.url[:len(request.url) - len(request.path)] + '/package'
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
    url = request.url[:len(request.url) - len(request.path)] + '/package'
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
    url = request.url[:len(request.url) - len(request.path)] + '/packages'
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
    url = request.url[:len(request.url) - len(request.path)] + '/reset'
    headers = {
        'X-Authorization': 'j',
    }
    response = requests.delete(url, headers=headers)
    return response.text


@app.route('/ui/download/', methods=['GET', 'PUT', 'DELETE'])
def package_by_id():
    return render_template('ui_package_id.html')


@app.route('/ui/packages_get', methods=['POST'])
def packages_get():
    headers = {
        'X-Authorization': 'j',
    }
    id = request.form.get('id')
    method = request.form.get('method')
    url = '{}{}'.format(
        request.url[:len(request.url) - len(request.path)] + '/package/', id)
    if id and method:
        # make the appropriate request based on the selected method
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'PUT':
            # perform PUT request with data from request.form
            response = requests.put(url, data=request.form, headers=headers)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        if response.status_code == 200:
            return response.content
    # render the template with the form if no ID or method is provided or if the server returns an error
    return render_template('ui_package_id.html')


@app.route("/ui/", methods=['GET', 'POST'])
def main_ui():
    return render_template('ui.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', PORT_NUMBER))
    app.run(host='127.0.0.1', port=port, debug=True)
