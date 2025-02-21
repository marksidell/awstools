'''
Obtain the AWS account for a given AWS profile
'''

import argparse
import boto3


def main():
    ''' Do it
    '''
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--profile',
        help='The AWS profile (defaults to AWS_PROFILE or the default profile)')

    args = parser.parse_args()

    print(
        boto3.Session(
            profile_name=args.profile if args.profile else None).client(
            'sts').get_caller_identity()['Account'])


if __name__ == '__main__':
    main()
