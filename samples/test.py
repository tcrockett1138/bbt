import requests
import time
from requests_aws4auth import AWS4Auth

access_key = "131734217793108142@ecstestdrive.emc.com"
secret_key = "c9wFEikxOMgbUR6Vlcw6519kwd9y8hUv6FgKUDh5"
endpoint = "https://object.ecstestdrive.com"
region = "us-east-1"
service = "s3"
ticks = time.time()
bucket = "bucket" + str(ticks)

auth = AWS4Auth(access_key,
                secret_key,
                region,
                service)
# Make Bucket
response = requests.put(endpoint + "/" + bucket, auth=auth)
print(str(response.status_code))
print(response.text)

# List Buckets
response = requests.get(endpoint + "/" + bucket, auth=auth)
print(str(response.status_code))
print(response.text)
