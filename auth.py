# Authentication functions
import requests
from requests.auth import HTTPBasicAuth
from requests_aws4auth import AWS4Auth


def gen_signature(access_key, secret_key, region, service):
    """Generate the AWSv4 signature"""
    auth = AWS4Auth(access_key,
                    secret_key,
                    region,
                    service)
    return auth


def get_token(endpoint, mgmt_user, mgmt_pass):
    """Get a token for management API access"""
    # print("in get_token")
    try:
        response = requests.get(endpoint + '/login', auth=HTTPBasicAuth(mgmt_user, mgmt_pass))
        if response.status_code != 200:
            print(response.text)
    except requests.exceptions.RequestException as e:
        print(e)
        return 1

    token = response.headers['X-SDS-AUTH-TOKEN']
    # print(token)

    return token
