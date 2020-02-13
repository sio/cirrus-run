'''
Command line interface for cirrus-run
'''


import os
import argparse


ENVIRONMENT = {
    'github': 'CIRRUS_GITHUB_REPO',
    'token': 'CIRRUS_API_TOKEN',
    'config': 'CIRRUS_CONFIG',
}


def parse_args(*a, **ka):
    parser = argparse.ArgumentParser(
        description=(
            'Execute CI jobs in CirrusCI'
        ),
        epilog='Licensed under the Apache License, version 2.0',
    )
    parser.add_argument(
        'config',
        metavar='CONFIG',
        default=os.getenv(ENVIRONMENT['config']) or './.cirrus.yml',
        nargs='?',
        help=(
            'Path to YAML configuration file. '
            'Default value: ${} or ./.cirrus.yml'
        ).format(ENVIRONMENT['config']),
    )
    parser.add_argument(
        '--token',
        default=os.getenv(ENVIRONMENT['token']),
        metavar='TOKEN',
        help=(
            'API token for accessing CirrusCI API. '
            'Recommended and more secure way of providing the token is via '
            'environment variable. '
            'Default value: ${}'
        ).format(ENVIRONMENT['token']),
    )
    parser.add_argument(
        '--github',
        default=os.getenv(ENVIRONMENT['github'], ''),
        metavar='REPO',
        help=(
            'GitHub repo id that will own the build ("owner/reponame"). '
            'This repo may have no relation to the CI job being executed. '
            'It may even be empty. '
            'Default value: ${}'
        ).format(ENVIRONMENT['github']),
    )
    parser.add_argument(
        '--owner',
        default='',
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        '--repo',
        default='',
        help=argparse.SUPPRESS,
    )
    args = parser.parse_args(*a, **ka)

    if not args.token:
        parser.error('API token is not defined')

    repo_parts = args.github.split('/')
    if len(repo_parts) != 2 or not all(repo_parts):
        parser.error('Invalid repo identificator: {}'.format(args.repo))
    args.owner, args.repo = repo_parts

    return args


if __name__ == '__main__':
    print(parse_args())
