'''Import Statements'''
# Flask
from ECE_461_new import compiledqueries
from errors import Err_Class
from firebase_admin import db, credentials
import firebase_admin
from flask import Flask, request, jsonify
import json
import os
from firestore import decode_service_account
import re
import Rate
import base64
import io
import zipfile
PORT_NUMBER = 5000

# Errors
err = Err_Class()

app = Flask(__name__)  # Initializing Flask app
'''Global Variable(s)'''
PROJECT_ID = "ece-461-ae1a9"

decode_service_account()
'''Initialize Firebase Admin SDK with your project's service account credentials'''
cred = credentials.Certificate("service_account.json")
firebase_admin.initialize_app(cred, options={
    'databaseURL': f'https://{PROJECT_ID}-default-rtdb.firebaseio.com'
})
# Firestore

'''Endpoints'''

# Curl requests:
# Correct: curl -X 'POST' 'http://127.0.0.1:8080/package/' -H 'Content-Type: application/json'  -H 'accept: application/json' -H 'X-Authorization: kkm' -d '{"metadata": {"Name": "Underscore","Version": "1.0.0","ID": "underscore"},"data": {"Content": "Check","JSProgram": "if (process.argv.length === 7) {\nconsole.log('\''Success'\'')\nprocess.exit(0)\n} else {\nconsole.log('\''Failed'\'')\nprocess.exit(1)\n}\n"}}'
# No metadata: curl -X 'POST' 'http://127.0.0.1:8080/package/' -H 'accept: application/json' -H 'X-Authorization: j' -H 'Content-Type: application/json' -d '{"Content": "check", "JSProgram": "if (process.argv.length === 7) {\nconsole.log('\''Success'\'')\nprocess.exit(0)\n} else {\nconsole.log('\''Failed'\'')\nprocess.exit(1)\n}\n"}'

# POST Package Create and POST Package Ingest


@app.route('/package/', methods=['POST'])
def create():

    # Checks Authorization
    authorization = None
    authorization = request.headers.get("X-Authorization")
    if authorization is None:
        return err.auth_failure()

    # Gets the JSON data from the request
    data = request.get_json()

    # Checking error 404 - metadata or data is not in curl request
    if not data or 'metadata' not in data.keys() or 'data' not in data.keys():
        return err.missing_fields()

    metadata = data['metadata']
    ID = metadata['ID']

    data_field = data['data']

    # Checking error 404
    if not ID:
        return err.malformed_req()

    # Checking error 404
    if "Content" in data_field.keys() and "URL" in data_field.keys():
        return err.missing_fields()

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
        firebaseIDs_list = []

        # Extracts the IDs of the metadata in the DB
        for ids in json_store.keys():
            firebaseIDs_list.append(ids)
            unique_id_list.append(json_store[ids]['metadata']['ID'])

        print(f'Unique id list = {unique_id_list}')
        if ID in unique_id_list:
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
                    return json.dumps(metadata)
                else:
                    return err.package_exists()
        else:
            ref.push(package)

    return err.success()

# Curl requests: curl --location 'http://127.0.0.1:8080/packages?offset=2' --header 'X-Authorization: bearer \
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c' \
# --header 'Content-Type: application/json' --data '[{"Version":"1.2.3","Name":"Underscore"},{"Version":"1.2.3-2.1.0","Name":"Lodash"}]'
# Modify "Name":"*" to test return of all packages
# POST Get Packages


@app.route('/packages/', methods=['POST'])
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
    check_error = False
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
            length = len(pack_list)
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

    # print(save)

    return json.dumps(save), 200

    # if check_error:
    #     return json.dumps(uniq_pack_list), 500
    # else:
    #     return json.dumps(uniq_pack_list), 200
# Test Command: curl --location --request DELETE 'http://127.0.0.1:8080/reset' --header /
# 'X-Authorization: bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI /
# 6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
# DELETE Reset Registry


@app.route('/reset', methods=['DELETE'])
def reset_registry():
    # Checks Authorization
    authorization = None
    authorization = request.headers.get("X-Authorization")
    if authorization is None:
        return err.no_permission()
    ref = db.reference('packages')
    ref.delete()
    return json.dumps('Registry is reset.'),200

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
# Content and URL both set: curl -X 'PUT' 'http://127.0.0.1:8080/package/underscore' -H 'accept: */*' -H 'X-Authorization: bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c' -H 'Content-Type: application/json' -d '{"metadata": {"Name": "string","Version": "1.2.3","ID": "string"},"data": {"Content": "string","URL": "string","JSProgram": "string"}}'
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
    # print(all_packages.items())
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


@app.route('/package/<id>/rate/', methods=['GET'])
def metric_rate(id):
    # Checks Authorization
    # authorization = None
    # authorization = request.headers.get("X-Authorization")
    # if authorization is None:
    #     return err.auth_failure()

    # Get package data from Firebase
    check_package = False

    ref = db.reference('packages')
    all_packages = ref.get()
    package_data = None
    for firebaseID, p_data in all_packages.items():
        metadata = p_data['metadata']
        if id == metadata['ID']:
            package_data = p_data

            check_package = True
            break

    # Get package content
    data = package_data['data']
    content = data['Content']
    content += '=' * (-len(content) % 4)
    #encodings_to_try = ['utf-8', 'iso-8859-1', 'cp1252']
    decoded_content = base64.b64decode(content).decode('iso-8859-1')
    #decoded_content_bytes = decoded_content.encode('utf-8')


    #with open("package.zip", "wb") as f:
     #f.write(decoded_content_bytes)
    #with zipfile.ZipFile("package.zip", "r") as zip_ref:
     #zip_ref.extractall("/Part2")



    # Checking error 400
    if not check_package:
        return err.package_doesNot_exist()

    # Checking error 404
    if package_data is None:
        return err.package_doesNot_exist()

    # Get package URL from package data
   # data = package_data['data']
    #url = data['URL']
    #if url is None:
     #   return err.missing_fields()


    # Get owner and name from GitHub URL
    #owner, name = Rate.extract_repo_info(url)

    # Calculate metrics
   # code_review = Rate.calculate_review_fraction(owner, name)
    #dependency = Rate.calculate_dependency_metric(id)
    #bus_factor = compiledqueries.getBusFactorScore(owner, name)
    #responsiveness = compiledqueries.getResponsiveMaintainersScore(owner, name)
   # correctness = compiledqueries.getCorrectnessScore(owner, name)
    # license_score = compiledqueries.getLicenseScore(name, owner,'license.txt')
    # ramp_up = compiledqueries.getRampUpScore(owner, name,'rampup_time.txt')
    license_score = 0
    ramp_up = 0

    # if (code_review == None) or (dependency== None) or (bus_factor == None) or  (responsiveness ==None):
    #     # Calculate net score
    #     calcFinalScore(bf, lc, cr, ru, rm, owner_url)

  #  net_score = compiledqueries.calcFinalScore(
      #  bus_factor, license_score, correctness, ramp_up, responsiveness, owner)
    # net_score = 0
    # Return result
    metric = {#'BusFactor': bus_factor,
              #'Correctness': correctness,
              'RampUp': ramp_up,
              #'ResponsiveMaintainer': responsiveness,
              'LicenseScore': license_score,
              #'GoodPinningPractice': dependency,
              #'PullRequest': code_review,
              #'NetScore': net_score
              }
    return json.dumps(metric), 200


@app.route('/')
def index():
    return jsonify(db.reference('packages').get())


@app.route('/authenticate/', methods=['PUT'])
def authenticate():
    return err.no_authentication()


@app.route('/package/byRegEx/', methods=['POST'])
def package_by_regex():
    # format the regex to make it compatible with code.
    # regex_pattern = regex.strip()

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


if __name__ == '__main__':
    # import os

    port = int(os.environ.get('PORT', PORT_NUMBER))
    app.run(host='0.0.0.0', port=port, debug=True)
