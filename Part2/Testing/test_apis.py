import unittest
import subprocess
import json

# Errors
from errors import Err_Class
err = Err_Class()


class TestCurlCommand(unittest.TestCase):

    def test_package_api(self):
        curl_command = "curl -H 'Content-Type: application/json' --location 'http://127.0.0.1:8080/package' --header 'X-Authorization: bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c' --data '{\"metadata\":{\"Name\":\"Loadash\",\"Version\":\"1.0.0\",\"ID\":\"loadash\"},\"data\":{\"Content\":\"checking_content\",\"JSProgram\":\"if (process.argv.length === 7) {\\nconsole.log('Success')\\nprocess.exit(0)\\n} else {\\nconsole.log('Failed')\\nprocess.exit(1)\\n}\\n\"}}'"
        # expected_json = {"Name": "Loadash", "Version": "1.0.0", "ID": "loadash"}
        expected_json = {"message": "Success."}
        process = subprocess.Popen(
            curl_command, stdout=subprocess.PIPE, shell=True)
        output, _ = process.communicate()
        response = json.loads(output.decode('utf-8'))
        self.assertEqual(response, expected_json)

    def test_check_auth(self):
        curl_command = "curl -H 'Content-Type: application/json' --location 'http://127.0.0.1:8080/package'  --data '{\"metadata\":{\"Name\":\"Loadash\",\"Version\":\"1.0.0\",\"ID\":\"loadash\"},\"data\":{\"Content\":\"checking_content\",\"JSProgram\":\"if (process.argv.length === 7) {\\nconsole.log('Success')\\nprocess.exit(0)\\n} else {\\nconsole.log('Failed')\\nprocess.exit(1)\\n}\\n\"}}'"
        process = subprocess.Popen(
            curl_command, stdout=subprocess.PIPE, shell=True)
        output, _ = process.communicate()
        expected_json = err.auth_failure()[0]['message']
        response = json.loads(output.decode('utf-8'))['message']
        self.assertEqual(response, expected_json)

    # def test_malformed_req(self):
    #     curl_command = "curl -H 'Content-Type: application/json' --location 'http://127.0.0.1:8080/package' --header 'X-Authorization: bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c' --data '{\"metadata\":{\"Name\":\"Loadash\",\"Version\":\"1.0.0\"},\"data\":{\"Content\":\"checking_content\",\"JSProgram\":\"if (process.argv.length === 7) {\\nconsole.log('Success')\\nprocess.exit(0)\\n} else {\\nconsole.log('Failed')\\nprocess.exit(1)\\n}\\n\"}}'"
    #     process = subprocess.Popen(curl_command, stdout=subprocess.PIPE, shell=True)
    #     output, _ = process.communicate()
    #     expected_json = err.malformed_req()[0]['message']
    #     response = json.loads(output.decode('utf-8'))['message']
    #     self.assertEqual(response, expected_json)

    def test_permission_reset(self):
        curl_command = "curl --location --request DELETE 'http://127.0.0.1:8080/reset'"
        process = subprocess.Popen(
            curl_command, stdout=subprocess.PIPE, shell=True)
        output, _ = process.communicate()
        expected_json = err.no_permission()[0]['message']
        response = json.loads(output.decode('utf-8'))['message']
        self.assertEqual(response, expected_json)

    def test_return_type_json(self):
        curl_command = "curl -H 'Content-Type: application/json' --location 'http://127.0.0.1:8080/package'  --data '{\"metadata\":{\"Name\":\"Loadash\",\"Version\":\"1.0.0\",\"ID\":\"loadash\"},\"data\":{\"Content\":\"checking_content\",\"JSProgram\":\"if (process.argv.length === 7) {\\nconsole.log('Success')\\nprocess.exit(0)\\n} else {\\nconsole.log('Failed')\\nprocess.exit(1)\\n}\\n\"}}'"
        process = subprocess.Popen(
            curl_command, stdout=subprocess.PIPE, shell=True)
        output, _ = process.communicate()
        expected_json = err.auth_failure()[0]['message']
        response = json.loads(output.decode('utf-8'))['message']
        self.assertEqual(type(response), type(expected_json))

    def test_return_type_tuple(self):
        curl_command = "curl -H 'Content-Type: application/json' --location 'http://127.0.0.1:8080/package'  --data '{\"metadata\":{\"Name\":\"Loadash\",\"Version\":\"1.0.0\",\"ID\":\"loadash\"},\"data\":{\"Content\":\"checking_content\",\"JSProgram\":\"if (process.argv.length === 7) {\\nconsole.log('Success')\\nprocess.exit(0)\\n} else {\\nconsole.log('Failed')\\nprocess.exit(1)\\n}\\n\"}}'"
        process = subprocess.Popen(
            curl_command, stdout=subprocess.PIPE, shell=True)
        output, _ = process.communicate()
        expected_json = err.auth_failure()
        self.assertIsInstance(expected_json, tuple)

    # def test_packages_api_return_type(self):
    #     curl_command = "curl --location 'http://127.0.0.1:8080/packages?offset=2' --header 'X-Authorization: bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c' --header 'Content-Type: application/json' --data '[{\"Version\":\"1.2.3\",\"Name\":\"Underscore\"},{\"Version\":\"1.2.3-2.1.0\",\"Name\":\"Lodash\"}]'"
    #     process = subprocess.Popen(curl_command, stdout=subprocess.PIPE, shell=True)
    #     output, _ = process.communicate()
    #     response = json.loads(output.decode('utf-8'))
    #     self.assertIsInstance(response, list)

    def test_deletion(self):
        curl_command = "curl --location --request DELETE 'http://127.0.0.1:8080/reset' --header 'X-Authorization: bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'"
        process = subprocess.Popen(
            curl_command, stdout=subprocess.PIPE, shell=True)
        output, _ = process.communicate()
        response = json.loads(output.decode('utf-8'))['message']
        self.assertEqual(response, "Success.")


if __name__ == '__main__':
    unittest.main()
