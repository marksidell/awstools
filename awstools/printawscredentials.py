'''
Print the credentials for an AWS profile from ~/.aws/credentials as env var declarations
'''

import os
import sys
import configparser


def main():
    ''' Do it
    '''
    credentials_file = os.path.expanduser(os.path.join('~', '.aws', 'credentials'))

    config = configparser.ConfigParser()
    config.read(credentials_file)

    profile_name = sys.argv[1]

    if not config.has_section(profile_name):
        raise RuntimeError(f'Profile "{profile_name}" not found in {credentials_file}.')

    # Get the credentials from the specified profile
    access_key = config.get(profile_name, 'aws_access_key_id')
    secret_key = config.get(profile_name, 'aws_secret_access_key')

    # Optional: Get session token if it exists
    session_token = config.get(profile_name, 'aws_session_token', fallback=None)

    # Set environment variables
    print(f'export AWS_ACCESS_KEY_ID={access_key}')
    print(f'export AWS_SECRET_ACCESS_KEY={secret_key}')

    if session_token:
        print(f'export AWS_SESSION_TOKEN={session_token}')


if __name__ == '__main__':
    main()
