'''Import Statements'''
# https://github.com/Purdue-ECE-461/project-2-3/blob/main/api/main.py 

# Flask
from flask import Flask, request
import json
import os

# Errors
from errors import Err_Class
err = Err_Class()

app = Flask(__name__) # Initializing Flask app

# Firestore
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

'''Global Variable(s)'''
PROJECT_ID = "ece-461-ae1a9" # Project ID on GCP


'''Initialize Firebase Admin SDK with your project's service account credentials''' # ***-firebase-adminsdk-602lt-2aa8f39403.json
cred_file = os.environ['GCP_SA_KEY']

cred = credentials.Certificate(cred_file) 
firebase_admin.initialize_app(cred, {
     'databaseURL': f'https://{PROJECT_ID}-default-rtdb.firebaseio.com'
})

'''Endpoints'''

# Test Command: curl -H "Content-Type: application/json" --location 'http://127.0.0.1:8080/package' --header 'X-Authorization: bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c' --data '{"metadata":{"Name":"Underscore","Version":"1.0.0","ID":"underscore"},"data":{"Content":"checking_content","JSProgram":"if (process.argv.length === 7) {\nconsole.log('\''Success'\'')\nprocess.exit(0)\n} else {\nconsole.log('\''Failed'\'')\nprocess.exit(1)\n}\n"}}'
# POST Package Create and POST Package Ingest
@app.route('/package/', methods=['POST'])
def create():
    
    # Checks Authorization
    authorization = None
    authorization = request.headers.get("X-Authorization")
    if(authorization == None):
        return err.auth_failure() 

    # Gets the JSON data from the request
    data = request.get_json()
    metadata = data['metadata']
    ID = metadata['ID']
    data_field = data['data']
    package = {
    'metadata': metadata,
    'data': data_field
    }
    if not ID:
        return err.malformed_req()

    ref = db.reference('packages') # Reference to node in Firebase
    json_store = ref.get() # Gets the data in the DB
    print(f'Json stored in the db = {json_store}')
    # ref.delete() # Deletes every node in the DB

    if json_store == None:
        print('DB is empty, adding new data')
        ref.push(package) # Upload data to package
    else: # If packages already exist in the DB
        unique_id_list = []
        firebaseIDs_list = []

        # Extracts the IDs of the metadata in the DB
        for ids in json_store.keys():
            firebaseIDs_list.append(ids)
            unique_id_list.append(json_store[ids]['metadata']['ID'])

        # print(f'Unique id list = {unique_id_list}')
        if ID in unique_id_list:
            # Ingestion - Add/Update the Firebase Database
            i = unique_id_list.index(ID)
            firebaseID = firebaseIDs_list[i] # Gets firebase ID 

            if 'URL' in list(data_field.keys()):
                # print(f'json_store[ID] = {json_store[firebaseID]}')
                # print(f'metadata = {metadata}')

                # Check if (URL does not exist in the DB) or if (it does then the one being uploaded is different)
                if (metadata == json_store[firebaseID]['metadata'] and 'URL' not in json_store[firebaseID]['data']) or (metadata == json_store[firebaseID]['metadata'] and 'URL' in json_store[firebaseID]['data'] and data_field['URL'] != json_store[firebaseID]['data']['URL']):
                    print('Ingestion required')
                    ref = db.reference('packages/' + firebaseID) 
                    update_data = {
                    'data': {
                        'URL': data_field['URL'],
                        **ref.child('data').get()  # Merge with existing data
                    }
                }
                    ref.update(update_data) # Updates DB
                    return json.dumps(metadata)
                else:
                    return err.package_exists() 

    return json.dumps(metadata),200

# Test Command:  curl --location 'http://127.0.0.1:8080/packages?offset=2' --header 'X-Authorization: bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c' --header 'Content-Type: application/json' --data '[{"Version":"1.2.3","Name":"Underscore"},{"Version":"1.2.3-2.1.0","Name":"Lodash"}]'
# Modify "Name":"*" to test return of all packages 
# POST Get Packages
@app.route('/packages/', methods=['POST'])
def list_of_packages():
    # Checks Authorization
    authorization = None
    authorization = request.headers.get("X-Authorization")
    if(authorization == None):
        return err.auth_failure() 

    # Gets package query from request body
    package_queries = request.json
    print(f'Package Queries = {package_queries}')
    if not package_queries:
        return err.unexpected_error()
    offset = request.args.get('offset', default=0, type=int)
    
    check_error = False
    pack_list = [] # List of packages to be returned
    ref = db.reference('packages')
    all_packages = ref.get() # Gets the firebaseIDs as keys and the values as the packages we need
    for query in package_queries:
        # Returning all packages
        if query['Name'] == "*": # As given in specsv2
            for package in all_packages.values():
                pack_list.append(package['metadata'])
        # Returning specific packages
        else:
            length = len(pack_list)
            for package in all_packages.values(): # Checking all packages in the DB for each query
                if query['Name'] == package['metadata']['Name']:
                    pack_list.append(package['metadata'])
                    break # Move to the next query if found

            if length == len(pack_list): # Unexpected error
                pack_list.append({"code": -1,"message": "An unexpected error occurred"})
                check_error = True
        
        if check_error:
            return json.dumps(pack_list),500
        else:
            return json.dumps(pack_list),200

# Test Command: curl --location --request DELETE 'http://127.0.0.1:8080/reset' --header 'X-Authorization: bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
# DELETE Reset Registry
@app.route('/reset/', methods = ['DELETE'])
def reset_registry():
    # Checks Authorization
    authorization = None
    authorization = request.headers.get("X-Authorization")
    if(authorization == None):
        return err.no_permission()
    
    ref = db.reference('packages')
    ref.delete()

    return json.dumps({'success':True}),200 # Check return value

# GET, PUT, DELETE - Package with given ID in endpoint
@app.route('/package/<id>', methods = ['GET', 'PUT', 'DELETE'])
def package_given_id(id):
    # Checks Authorization
    authorization = None
    authorization = request.headers.get("X-Authorization")

    if(authorization == None):
        return err.auth_failure()
    if request.method == 'GET':
        return PackageRetrieve(id)
    if request.method == 'PUT':
        return PackageUpdate(id)
    if request.method == 'DELETE':
        # return (id)
        pass

# Test Command: curl --location --request GET 'http://127.0.0.1:8080/package/underscore' --header 'X-Authorization: bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c' --data '{"metadata": {"Name": "Underscore", "Version": "1.0.0", "ID": "underscore"}, "data": {"Content": "Updating", "URL": "https://github.com/jashkenas/underscore","JSProgram": "if (process.argv.length === 7) {\nconsole.log('\''Success'\'')\nprocess.exit(0)\n} else {\nconsole.log('\''Failed'\'')\nprocess.exit(1)\n}\n"}}'
def PackageRetrieve(id):
    ref = db.reference('packages')
    all_packages = ref.get()

    for p_data in all_packages.values():
        metadata = p_data['metadata']
        if id == metadata['ID']:
            return json.dumps(metadata),200
    return err.package_doesNot_exist()

# Test Command: curl -H "Content-Type: application/json" --location --request PUT 'http://127.0.0.1:8080/package/underscore'--header 'X-Authorization: bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c' --data '{"metadata": {"Name": "Underscore", "Version": "1.0.0", "ID": "underscore"}, "data": {"Content": "Updating", "URL": "https://github.com/jashkenas/underscore","JSProgram": "if (process.argv.length === 7) {\nconsole.log('\''Success'\'')\nprocess.exit(0)\n} else {\nconsole.log('\''Failed'\'')\nprocess.exit(1)\n}\n"}}'
def PackageUpdate(id):
    ref = db.reference('packages')
    all_packages = ref.get()

    data = request.json
    id_exists = False

    # Gets firebaseID of the package (metadata in this case) that we need to update
    print(all_packages.items())
    for firebaseID, p_data in all_packages.items():
        metadata = p_data['metadata']
        if id == metadata['ID']:
            id_exists = True
            break

    if not id_exists:
        return err.malformed_req()
    if (metadata['Name'] != data['metadata']['Name']) or (metadata['Version'] != data['metadata']['Version']) or (metadata['ID'] != data['metadata']['ID']):
        return err.package_doesNot_exist()


    # Updating the specific child node in the DB 
    ref = db.reference('packages/'+firebaseID) 
    update_data = {
                    'data': {
                        'URL': data['data']['URL'],
                        'Content': data['data']['Content'],
                        'JSProgram': data['data']['JSProgram']
                    }
                }
    ref.update(update_data) # Updates DB

    return json.dumps({'Success':'True'}),200


@app.route('/')
def index():
    return 'Hello, from Aaradhya, Eshaan, Tanvi and Ilan!'

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

