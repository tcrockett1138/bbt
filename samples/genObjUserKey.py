import requests
from requests.auth import HTTPBasicAuth

# json = {
#     "user_secret_key_create": {
#     "existing_key_expiry_time_mins": { "-null": "true" },
#     "namespace": "s3",
#     "secretkey": "aNewHappyLittleKey"
#   }
# }

xml_key = '<?xml version="1.0" encoding="UTF-8"?>' \
           '<user_secret_key_create>' \
           '<existing_key_expiry_time_mins null="true"/>' \
           '<namespace>131734217793108142</namespace>' \
           '<secretkey>aNewHappyLittleKey</secretkey>' \
           '</user_secret_key_create>'

# xml_user = '<?xml version="1.0" encoding="UTF-8"?>' \
#            '<user_create_param>' \
#            '<user>wuser1@SANITY.LOCAL</user>' \
#            '<namespace>131734217793108142</namespace>' \
#            '</user_create_param>'

endpoint = 'https://portal.ecstestdrive.com'
obj_user = '131734217793108142@ecstestdrive.emc.com'
obj_pass = 'c9wFEikxOMgbUR6Vlcw6519kwd9y8hUv6FgKUDh5'
mgmt_user = '131734217793108142-admin'
mgmt_pass = 'ZGRjOWQxYWExY2M5MjM3ZmRjZTBmNGMxZDVkMTQxMTU='

# login & get the token
response = requests.get(endpoint + '/login', auth=HTTPBasicAuth(mgmt_user, mgmt_pass))
token = response.headers['X-SDS-AUTH-TOKEN']
print("token: " + token)
print(response.status_code)

headers = {'X-SDS-AUTH-TOKEN': token}
print(headers)
#    'x-emc-namespace': '131734217793108142'

# response = requests.get(endpoint + '/object/bucket', headers=headers)   # list buckets
# response = requests.get(endpoint + '/object/users', headers=headers)   # list object users
response = requests.get(endpoint + '/object/user-secret-keys/' + obj_user, headers=headers)   # get secret keys
response = requests.put(endpoint + '/object/user-secret-keys/' + obj_user, data=xml_key, headers=headers)   # new secret key
# response = requests.put(endpoint + '/object/users', data=xml_user, headers=headers)   # new user

print(response.text)