'''
Create or update an aws cloudformation stack
'''

import os.path
import sys
from datetime import datetime, timezone
import argparse
import boto3


def main():
    ''' do it
    '''
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'stack',
        help='The name of the stack')

    parser.add_argument(
        '--template-file',
        help='Path to the template file (defaults to <stack>.yaml)')

    parser.add_argument(
        '--artifact-file',
        help='Path to the artifact (defaults to <stack>.artifact)')

    parser.add_argument(
        '--aws-profile',
        default='default',
        help='An optional AWS profile, to select the target account')

    parser.add_argument(
        '--params',
        nargs='+',
        help='Optional stack parameters, as a list of key=value pairs')

    args = parser.parse_args()

    with open(
        args.template_file if args.template_file else f'{args.stack}.yaml',
        'r',
        encoding='ascii') as fil:

        template = fil.read()

    artifact_path = (
        args.artifact_file if args.artifact_file
        else f'{args.stack}{"."+args.aws_profile if args.aws_profile else ""}.artifact')

    update_artifact = not os.path.isfile(artifact_path)

    cf_client = boto3.Session(profile_name=args.aws_profile).client('cloudformation')

    try:
        cf_client.describe_stacks(StackName=args.stack)
        stack_exists = True
    except cf_client.exceptions.ClientError:
        stack_exists = False

    params = {
        'StackName': args.stack,
        'TemplateBody': template,
        'Capabilities': ['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM'],
    }

    if args.params:
        params['Parameters'] = [
            {'ParameterKey': key_value[0], 'ParameterValue': key_value[1]}
            for key_value in (item.split('=') for item in args.params)
        ]

    try:
        if stack_exists:
            print(f'Updating stack {args.stack}')
            cf_client.update_stack(**params)
            waiter = cf_client.get_waiter('stack_update_complete')
        else:
            print(f'Creating stack {args.stack}')
            cf_client.create_stack(**params)
            waiter = cf_client.get_waiter('stack_create_complete')

        print('Waiting for stack operation to complete...')
        waiter.wait(StackName=args.stack)
        print('Stack operation completed successfully')
        update_artifact = True

    except cf_client.exceptions.ClientError as err:
        error_message = err.response['Error']['Message']
        if 'No updates are to be performed' in error_message:
            print(f'No updates were performed on stack {args.stack}')
        else:
            sys.exit(f'Error: {error_message}')

    if update_artifact:
        with open(artifact_path, 'w', encoding='ascii') as fil:
            fil.write(datetime.now(timezone.utc).isoformat(timespec='seconds') + '\n')


if __name__ == "__main__":
    main()
