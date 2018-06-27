import requests
import time
from requests_aws4auth import AWS4Auth
import base64 
import hashlib
import xml.etree.ElementTree as ET

access_key = "131734217793108142@ecstestdrive.emc.com"
secret_key = "c9wFEikxOMgbUR6Vlcw6519kwd9y8hUv6FgKUDh5"
endpoint = "https://object.ecstestdrive.com/"
region = "us-east-1"
service = "s3"
ticks = time.time()
bucket = "bucket" + str(ticks)

auth = AWS4Auth(access_key,
                secret_key,
                region,
                service)

# Make Bucket
response = requests.put(endpoint + bucket, auth=auth)
print(str(response.status_code))
print(response.text)

# List Buckets
response = requests.get(endpoint + bucket, auth=auth)
# response = requests.get(endpoint, auth=auth)


# print(str(response.status_code))
# print(response.text)

# Set Bucket Lifecycle
template = """
<LifecycleConfiguration>
   <Rule>
      <ID>%(id)s</ID>
      <Status>%(status)s</Status>
      <Filter/>
      <NoncurrentVersionExpiration>
         <NoncurrentDays>%(noncurrentdays)s</NoncurrentDays>
      </NoncurrentVersionExpiration>
   </Rule>
</LifecycleConfiguration>
"""
#print("template\n" + template)

# Squash template so we have a clean, single line xml for encoding
template = template.replace('\n', '')
template = template.replace(' ', '')
data = {'id':'DeleteNonCurrentVersionsAfter60Days', 'status':'Enabled', 'noncurrentdays':'60'}
payload = template%data
print("payload\n" + payload)

# Generate Content-MD5 header
h = hashlib.md5()
h.update(bytes(payload, encoding='utf-8'))
hash = h.digest()
content_md5 = base64.b64encode(hash).decode('utf-8')

# Make it so...
# This will silently overwrite an existing lifecycle configuration with the same id
headers = {'Content-MD5': content_md5}
response = requests.put(endpoint + bucket + "/?lifecycle", auth=auth, headers=headers, data=payload)
print(response.text)

# Show the new lifecycle configuration
response = requests.get(endpoint + bucket + "/?lifecycle", auth=auth)
print("lifecycle configuration: \n" + response.text + "\n")
