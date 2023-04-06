import base64

with open('service_account.txt', 'r') as f:
    with open('service_account.json', 'wb') as f2:
        f2.write(base64.b64decode(f.readline()))
