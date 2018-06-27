# Function definitions for bbt
import requests
from lifecycle import generate_lifecycle
import hashlib
import base64
import yaml
import xml.etree.ElementTree as ET


# TODO: Add 'raise' to functions so they can be handled in try/except blocks

def read_creds(secrets_file, env):
    """Read the access & secret keys"""
#    try:
    with open(secrets_file, 'r') as stream:
        try:
            secrets = yaml.load(stream)
        except yaml.YAMLError as e:
            print(e)

    if env in secrets.keys():
        creds = secrets.get(env)
    else:
        print("Unable to find credentials for environment '" + env + "'")
        return 1
    # except:
    #     print("\nPlease ensure there is a properly configured secrets file"
    #           "in the current directory")

    return creds


def content_md5(payload):
    # Generate Content-MD5 header
    h = hashlib.md5()
    h.update(bytes(payload, encoding='utf-8'))
    hash = h.digest()
    content_md5 = base64.b64encode(hash).decode('utf-8')
    return content_md5


def create_bucket(endpoint, bucket, versioning, auth):
    """Create a new bucket"""
    try:
        response = requests.put(endpoint + bucket, auth=auth)
        if response.status_code != 200:
            print(response.text)
            response.raise_for_status()
        print("Bucket '" + bucket + "' has been successfully created.\n")
    except requests.exceptions.RequestException as e:
        print(e)
        print("\n\nUnable to create bucket '" + bucket + "'\n")
        return 1
    if versioning:
        set_versioning(endpoint, bucket, versioning, auth)

    return 0


def delete_bucket(endpoint, bucket, auth):
    """Delete an existing bucket"""
    # TODO: test this with objects in bucket to verify exception
    try:
        response = requests.delete(endpoint + bucket, auth=auth)
        if response.status_code != 200:
            print(response.text)
            response.raise_for_status()
        print("Bucket '" + bucket + "' has been successfully deleted.\n")
    except requests.exceptions.RequestException as e:
        print(e)
        print("\n\nUnable to delete bucket '" + bucket + "'\n")
        return 1

    return 0


def list_buckets(endpoint, auth):
    """List all buckets for the object user"""
    # TODO: Cleanup XML output so it is more human friendly
    print("in list_buckets")
    try:
        response = requests.get(endpoint, auth=auth)
        if response.status_code != 200:
            print(response.text)
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(e)
        return 1

    root = ET.fromstring(response.text)
    ns = {'aws_s3': 'http://s3.amazonaws.com/doc/2006-03-01/'}
    # names = root.findall('.//Name') # <-- THIS WORKS W/O NAMESPACE
    names = root.findall('.//aws_s3:Name', ns)  # <-- THIS WORKS WITH NAMESPACE
    print(len(names))
    for i in range(len(names)):
        print(names[i].text)
    return 0


def apply_lifecycle(endpoint, bucket, auth):
    """Generate and apply an opinionated lifecycle based on a template"""
    # TODO: set application/json on GET
    # This will overwrite an existing lifecycle configuration with the same id
    payload = generate_lifecycle()
    headers = {'Content-MD5': content_md5(payload)}
    try:
        response = requests.put(endpoint + bucket + "/?lifecycle", auth=auth,
                                headers=headers, data=payload)
        if response.status_code != 200:
            print(response.text)
            response.raise_for_status()
        print("\nLifecycle successfully applied.")
    except requests.exceptions.RequestException as e:
        print(e)
        print("\n\nA LIFECYCLE HAS NOT BEEN APPLIED!  IN THE CASE OF A "
              "VERSIONED BUCKET, THE NUMBER OF VERSIONS IS UNLIMITED!\n\n")
        return 1
    # Show the new lifecycle configuration
    try:
        response = requests.get(endpoint + bucket + "/?lifecycle", auth=auth)
        if response.status_code != 200:
            print(response.text)
            print("\n\nUnable to show lifecycle configuration...not fatal\n")
        print("Lifecycle configuration: \n" + response.text + "\n")
    except requests.exceptions.RequestException as e:
        print(e)
        print("\n\nUnable to show lifecycle configuration...not fatal\n")
        return 0


def set_versioning(endpoint, bucket, versioning, auth):
    """Set the versioning state of a bucket [enabled / suspended].
    If state is not explicitly set, then the state is 'undefined' (unversioned).
    This will also set a default, opinionated lifecycle configuration.
    """
    # TODO: put version GET in a try/except
    # TODO: error checking for apply_lifecycle
    payload = '<VersioningConfiguration>' \
              '<Status>' + versioning + '</Status>' \
              '</VersioningConfiguration>'
    try:
        response = requests.put(endpoint + bucket + '/?versioning', auth=auth,
                                data=payload)
        if response.status_code != 200:
            print(response.text)
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(e)
        print("\n\nUnable to set versioning state to " + versioning +
              " for bucket '" + bucket + "'\n")
        return 1

    print("\nBucket " + bucket + " has versioning state " + versioning)
    response = requests.get(endpoint + bucket + '/?versioning', auth=auth)
    print(response.text)
    apply_lifecycle(endpoint, bucket, auth)
    return 0


def make_std_buckets(endpoint, buckets_file, auth):
    """Create a set of 'standard' buckets defined by buckets_file"""
    print("in make_std_bucket")
    with open(buckets_file, 'r') as buckets:
        for line in buckets:
            if line.startswith('#'):
                continue
            line = line.replace(' ', '')
            line = line.replace('\n', '')
            if len(line.split(',')) == 1:
                bucket = line
                versioning = None
                print(bucket)
                create_bucket(endpoint, bucket, versioning, auth)
            elif len(line.split(',')) == 2:
                bucket = (line.split(',')[0])
                versioning = (line.split(',')[1])
                print(bucket, versioning)
                create_bucket(endpoint, bucket, versioning, auth)
                if versioning != 'Enabled' and versioning != 'Suspended':
                    print("Incorrectly formatted buckets file")
                    return 1

    return 0
