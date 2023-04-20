import requests

# Test the API
url = "http://127.0.0.1:8080/"

payload = "[\n  {\n    \"Version\": \"1.2.3\",\n    \"Name\": \"Underscore\"\n  },\n  {\n    \"Version\": \"1.2.3-2.1.0\",\n    \"Name\": \"Lodash\"\n  }\n]"
headers = {
    'X-Authorization': 'bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
}

response = requests.request("GET", url)

print(response.text)
