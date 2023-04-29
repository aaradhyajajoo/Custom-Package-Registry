curl -X 'POST' \
  'http://127.0.0.1:15264/package' \
  -H 'accept: application/json' \
  -H 'X-Authorization: xauth' \
  -H 'Content-Type: application/json' \
  -d '{
  "JSProgram": "if (process.argv.length === 7) {\nconsole.log('\''Success'\'')\nprocess.exit(0)\n} else {\nconsole.log('\''Failed'\'')\nprocess.exit(1)\n}\n",
  "URL": "https://www.npmjs.com/package/lodash"
}'