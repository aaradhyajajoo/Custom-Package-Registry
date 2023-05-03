curl -X 'POST' \
  'http://ece-461-ae1a9.uc.r.appspot.com/package' \
  -H 'accept: application/json' \
  -H 'X-Authorization: xauth' \
  -H 'Content-Type: application/json' \
  -d '{ "JSProgram": "if (process.argv.length === 7) {\nconsole.log('\''Success'\'')\nprocess.exit(0)\n} else {\nconsole.log('\''Failed'\'')\nprocess.exit(1)\n}\n",
  "URL": "https://github.com/nullivex/nodist", "Content": "None"
}'