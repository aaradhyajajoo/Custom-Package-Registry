curl -X 'POST' \
  'http://127.0.0.1:5000/packages' \
  -H 'accept: application/json' \
  -H 'X-Authorization: RANDOM' \
  -H 'Content-Type: application/json' \
  -d '[
  {
    "Version": "0.9.1",
    "Name": "nodist"
  }
]'