curl -X 'PUT' \
  'http://ece-461-ae1a9.uc.r.appspot.com/authenticate/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "User": {
    "name": "ece30861defaultadminuser",
    "isAdmin": true
  },
  "Secret": {
    "password": "correcthorsebatterystaple123(!__+@**(A’”`;DROP TABLE packages;"
  }
}'