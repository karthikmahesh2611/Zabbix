#Script to request an auth token to be used for API communication

import requests

api_url = 'api_url'
headers = {'content-type': 'application/json',}

auth_data = {"jsonrpc": "2.0","method": "user.login","params": {"user": "username","password": "password"},"id":1,"auth": None}

connect = requests.post(api_url, data=json.dumps(auth_data), headers=headers, verify=False)

reply = connect.json()

print(reply['result'])
