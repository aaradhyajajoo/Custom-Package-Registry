curl -X 'POST' \
  'http://ece-461-ae1a9.uc.r.appspot.com/packages' \
  -H 'accept: application/json' \
  -H 'X-Authorization: RANDOM' \
  -H 'Content-Type: application/json' \
  -d '[
  {
    "Version": "4.2.3",
    "Name": "fecha"
  }
]'