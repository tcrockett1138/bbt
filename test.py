import requests
from awsv2_auth import AwsV2Auth

access_key = "131734217793108142@ecstestdrive.emc.com"
secret_key = "c9wFEikxOMgbUR6Vlcw6519kwd9y8hUv6FgKUDh5"
endpoint = "https://object.ecstestdrive.com"
bucket = "newbucket1"

auth = AwsV2Auth(access_key, secret_key)

# Make Bucket
response = requests.put(endpoint + "/" + bucket, auth=auth)
print(str(response.status_code))
print(response.text)

# List Buckets
response = requests.get(endpoint + "/" + bucket, auth=auth)
print(str(response.status_code))
print(response.text)
