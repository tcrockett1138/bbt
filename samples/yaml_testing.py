import yaml

with open("secrets.yml", 'r') as stream:
    try:
        cruft = yaml.load(stream)
       # print(cruft)
    except yaml.YAMLError as e:
        print(e)

keys = cruft.keys()
# print(keys)
if 'env2' in keys:
    env = cruft.get('env2')
    access_key = env['access_key']
    secret_key = env['secret_key']
    print(access_key, secret_key)

# for key in keys:
#     if key == 'env2':
#         print(key)
#     else:
#         print("key not found")