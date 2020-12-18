import requests
import time
from requests_aws4auth import AWS4Auth
import xml.etree.ElementTree as ET

access_key = ""
secret_key = ""
endpoint = "https://object.ecstestdrive.com/"
region = "us-east-1"
service = "s3"
ticks = time.time()
bucket = "bucket" + str(ticks)

auth = AWS4Auth(access_key,
                secret_key,
                region,
                service)

response = requests.get(endpoint, auth=auth)
#print(response.text)

root = ET.fromstring(response.text)
# for child in root:
#     print(child.tag, child.tag)
#     # print(root[1][0].text)

# for item in root.itertext():
#     print(item)

# for item in root.iterfind('Name'):
#     print(item)
# xmlns="http://s3.amazonaws.com/doc/2006-03-01/"
s3 = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<ListAllMyBucketsResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
  <Owner>
    <ID>131734217793108142@ecstestdrive.emc.com</ID>
    <DisplayName>131734217793108142@ecstestdrive.emc.com</DisplayName>
  </Owner>
  <Buckets>
    <Bucket>
      <Name>bucket1530142811.484572</Name>
      <CreationDate>2018-06-27T23:37:55.242Z</CreationDate>
      <ServerSideEncryptionEnabled>false</ServerSideEncryptionEnabled>
    </Bucket>
    <Bucket>
      <Name>bucket1530294532.9354072</Name>
      <CreationDate>2018-06-29T17:46:36.093Z</CreationDate>
      <ServerSideEncryptionEnabled>false</ServerSideEncryptionEnabled>
    </Bucket>
    <Bucket>
      <Name>bucket1530312204.9379368</Name>
      <CreationDate>2018-06-29T22:41:11.663Z</CreationDate>
      <ServerSideEncryptionEnabled>false</ServerSideEncryptionEnabled>
    </Bucket>
  </Buckets>
  <IsTruncated>false</IsTruncated>
</ListAllMyBucketsResult>'''

# root = ET.fromstring(s3)

ns = {'aws_s3': 'http://s3.amazonaws.com/doc/2006-03-01/'}
# names = root.findall('.//Name') # <-- THIS WORKS W/O NAMESPACE
names = root.findall('.//aws_s3:Name', ns)  # <-- THIS WORKS WITH NAMESPACE
print(len(names))
for i in range(len(names)):
    print(names[i].text)



ns = {'aws_s3': 'http://s3.amazonaws.com/doc/2006-03-01/'}
# for child in root.iter():
#     print(child.tag, child.attrib)

# buckets = root.findall('.//Buckets')
#
# for bucket in buckets:
#     name = bucket.find('.//Bucket/Name')
#     print(name)

# buckets = root.findall('Buckets')
# print(type(buckets))
# print(len(buckets))
# print(buckets[0])
# for bucket in buckets[0]:
#     print(type(bucket))
#     print(bucket.tag)


#print(foo[0].text)
    # for bucket in item.find('Bucket'):
    #     # name = bucket.find('Name')
    #     name = bucket.iter()
    #     print(type(name))
    #     print(name)

#buckets = root.findall('aws_s3:Buckets', ns)
#buckets = root.findall('./')
#print(buckets)
# foo = buckets.findall('aws_s3:.//Bucket', ns)
# print(foo)


# sample = '''<?xml version="1.0"?>
# <actors xmlns:fictional="http://characters.example.com"
#         xmlns="http://people.example.com">
#     <actor>
#         <name>John Cleese</name>
#         <fictional:character>Lancelot</fictional:character>
#         <fictional:character>Archie Leach</fictional:character>
#     </actor>
#     <actor>
#         <name>Eric Idle</name>
#         <fictional:character>Sir Robin</fictional:character>
#         <fictional:character>Gunther</fictional:character>
#         <fictional:character>Commander Clement</fictional:character>
#     </actor>
# </actors>
# '''
#
# root = ET.fromstring(sample)
# ns = {'real_person': 'http://people.example.com',
#       'role': 'http://characters.example.com'}
# for actor in root.findall('real_person:actor', ns):
#     name = actor.find('real_person:name', ns)
#     print(name.text)
#     for char in actor.findall('role:character', ns):
#         print(' |-->', char.text)
#
# # for bucket in root.findall('Bucket'):
# #     b = bucket.find('Name').text
# #     print(b)
#
# # print(root.findall('Buckets'))
