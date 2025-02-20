from setuptools import setup

setup(
    name='awstools',
    version='1.0',
    description='Tools for doing AWS things',
    author='Mark Sidell',
    author_email='mark@sidell.org',

    packages=[
        'awstools'
    ],
    entry_points={
        'console_scripts': [
            'print-aws-credentials=awstools.printawscredentials:main',
            'update-aws-stack=awstools.update_aws_stack:main',
            'get-aws-account=awstools.getawsaccount:main',
        ]
    },
    scripts=[
        'call-local',
        'call-aws',
        'debug-aws',
        'debug-local',
        'docker-deploy',
        'docker-kill',
        'docker-logs',
        'docker-run',
        'docker-upload-image',

        'refresh-asg',
        'kick-asg',
    ],
    install_requires=[
        'boto3',
    ]
)
