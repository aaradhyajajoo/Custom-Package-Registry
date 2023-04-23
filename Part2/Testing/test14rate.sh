curl -X 'GET' \
  'http://127.0.0.1:50002/package/nodist_0.9.1/rate' \
  -H 'accept: application/json' \
  -H 'X-Authorization: rand_auth' &> ignore.txt

cat test14rate.json