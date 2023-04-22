curl -X 'PUT' \
  'http://127.0.0.1:50001/authenticate/' \
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