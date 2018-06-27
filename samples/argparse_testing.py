import argparse

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(title='Commands', dest='command')

parser_bucket = argparse.ArgumentParser(add_help=False)
parser_bucket.add_argument('bucket', type=str, help='The bucket name')

parser_env = argparse.ArgumentParser(add_help=False)
parser_env.add_argument('-e', type=str, required=True,
                        help='The environment file containing object '
                             'user credentials')

parser_create = subparsers.add_parser('create',
                                      parents=[parser_env, parser_bucket],
                                      help='Create a new bucket')
parser_create.add_argument('-V', '--set-versioning',
                           choices=['enabled', 'suspended'],
                           help='Set the versioning state of the bucket.  '
                                'If not set (default), the versioning state is'
                                ' "null".  PROCEED WITH CAUTION!')

parser_list = subparsers.add_parser('list',
                                    parents=[parser_env, parser_bucket],
                                    help='List buckets')

parser_delete = subparsers.add_parser('delete',
                                      parents=[parser_env],
                                      help='Delete an existing bucket')

parser_mkstd = subparsers.add_parser('mkstd', parents=[parser_env],
                                     help='Make all the standard buckets'
                                          ' required for a PCF foundation, '
                                          'defined in pcfbuckets.txt')

args = parser.parse_args()

print(args)
if args.command == 'create':
    print(args.bucket)