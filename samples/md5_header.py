# An example for generating a 'Content-MD5' header for an S3 'PUT Bucket Lifecycle' operation
"""Reference material.
This template is sourced from:
http://doc.isilon.com/ECS/3.1/API/S3BucketLifecycleOperation_setBucketLifeCycle_c7f834e336282fd0bbee6fe8fb03fca1_ba672412ac371bb6cf4e69291344510e_detail.html

Additional documentation can be found here:
https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketPUTlifecycle.html
"""
import base64 
import hashlib

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

# Squash template so we have a clean, sinlge line xml for encoding
template = template.replace('\n', '')
template = template.replace(' ', '')

data = {'id':'myNewRule', 'status':'Enabled', 'noncurrentdays':'45'}
payload = bytes(template%data, encoding='utf-8')
print(payload)

h = hashlib.md5()
h.update(payload)
hash = h.digest()
print(hash)

encoded = base64.b64encode(hash)
print(encoded)

encoded_utf8 = base64.b64encode(hash).decode('utf-8')
print("Content-MD5 Header:\n" + encoded_utf8)
