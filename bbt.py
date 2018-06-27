#!/usr/local/bin/python
# Basic Bucket Tool
# Simple but opinionated utility for basic S3 bucket/object management
# Originally written to help with ECS object storage
# Tim Crockett, Altoros, 2018-06-27

# TODO: pretty-print list buckets

# Install prerequsites
# https://pypi.org/project/requests-aws4auth/
# http://docs.python-requests.org/en/master/#
# https://pyyaml.org
# pip install aws4auth requests pyyaml

import argparse
import sys
from bbt_functions import *
from auth import *

# Endpoint is fixed and should never change within the lifetime of this script
# Dell ECS has no regions, thus uses the default region
endpoint = 'https://object.ecstestdrive.com/'
region = 'us-east-1'
service = 's3'
secrets_file = 'secrets.yml'

# Standard buckets file
std_buckets = "standard_buckets.txt"


def parse_args():
    """some docstring here"""
    # Initialize argparse and configure parent parsers
    parser = argparse.ArgumentParser(description='A tool to make basic bucket'
                                                 ' management simple')
    subparsers = parser.add_subparsers(title='Commands', dest='command')

    parser_bucket = argparse.ArgumentParser(add_help=False)
    parser_bucket.add_argument('bucket', type=str, help='The bucket name')

    parser_env = argparse.ArgumentParser(add_help=False)
    parser_env.add_argument('-e', '--environment', type=str, required=True,
                            help='The environment to lookup the credentials')

    parser_versioning = argparse.ArgumentParser(add_help=False)
    parser_versioning.add_argument('-s', '--set-versioning',
                               choices=['Enabled', 'Suspended'],
                               help='Set the versioning state of the '
                                    'bucket.  If not set (default), the '
                                    'versioning state is "null".  PROCEED WITH'
                                    ' CAUTION!')

    # Configure 'create bucket' parser
    parser_create = subparsers.add_parser('create',
                                          parents=[parser_env, parser_bucket,
                                                   parser_versioning],
                                          help='Create a new bucket')

    # Configure 'list buckets' parser
    parser_list = subparsers.add_parser('list',
                                        parents=[parser_env],
                                        help='List buckets')

    # Configure 'delete bucket' parser
    parser_delete = subparsers.add_parser('delete',
                                          parents=[parser_env, parser_bucket],
                                          help='Delete an existing bucket')

    # Configure 'make standard buckets' parser
    parser_mkstd = subparsers.add_parser('mkstd', parents=[parser_env],
                                         help='Make all the standard buckets'
                                              ' required for a PCF foundation,'
                                              ' defined in pcfbuckets.txt')

    # Configure 'set versioning' parser
    parser_versioning = subparsers.add_parser('set-versioning',
                                              parents=[parser_env,
                                                       parser_bucket,
                                                       parser_versioning],
                                              help='Set versioning on an '
                                                   'existing bucket')

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(0)

    return args


def main():
    args = parse_args()
    # print(args)
    creds = read_creds(secrets_file, args.environment)

    if creds == 1:
        sys.exit(1)
    else:
        access_key = creds['access_key']
        secret_key = creds['secret_key']
        auth = gen_signature(access_key, secret_key, region, service)
        # Uncomment to fetch a token to authenticate with the management API
        # mgmt_user = creds['mgmt_user']
        # mgmt_pass = creds['mgmt_pass']
        # token = get_token(endpoint, mgmt_user, mgmt_pass)

    if args.command == 'create':
        result = create_bucket(endpoint, args.bucket, args.set_versioning, auth)
    elif args.command == 'delete':
        result = delete_bucket(endpoint, args.bucket, auth)
    elif args.command == 'list':
        result = list_buckets(endpoint, auth)
    elif args.command == 'set-versioning':
        result = set_versioning(endpoint, args.bucket, args.set_versioning, auth)
    elif args.command == "mkstd":
        result = make_std_buckets(endpoint, std_buckets, auth)

    return result


if __name__ == '__main__':
    main()
