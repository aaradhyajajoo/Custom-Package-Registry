curl -X 'POST' \
  'http://127.0.0.1:50004/packages' \
  -H 'accept: application/json' \
  -H 'X-Authorization: RANDOM' \
  -H 'Content-Type: application/json' \
  -d '[
  {
    "Version": "Exact (0.9.1)\nBounded range (1.2.3-2.1.0)\nCarat (^0.1.9)\nTilde (~0.1.0)",
    "Name": "string"
  }
]'