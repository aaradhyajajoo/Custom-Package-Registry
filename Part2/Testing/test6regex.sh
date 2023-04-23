curl -X 'POST' \
  'http://127.0.0.1:50002/package/byRegEx' \
  -H 'accept: application/json' \
  -H 'X-Authorization: bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c' \
  -H 'Content-Type: application/json' \
  -d '{
  "RegEx": ""
}'