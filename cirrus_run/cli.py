'''
Command line interface for cirrus-run
'''


import argparse
import logging
import os
import sys

from . import CirrusAPI
from .queries import get_repo, create_build, wait_build, CirrusBuildError

log = logging.getLogger(__name__)


ENVIRONMENT = {
    'github': 'CIRRUS_GITHUB_REPO',
    'branch': 'CIRRUS_GITHUB_BRANCH',
    'token': 'CIRRUS_API_TOKEN',
    'config': 'CIRRUS_CONFIG',
}


def main(*a, **ka):
    args = parse_args(*a, **ka)
    configure_logging(args.verbose)

    with open(args.config) as config_file:
        config = config_file.read()

    api = CirrusAPI(args.token)
    repo_id = get_repo(api, args.owner, args.repo)
    build_id = create_build(api, repo_id, args.branch, config)

    print('Build created: https://cirrus-ci.com/build/{id}'.format(id=build_id))

    try:
        wait_build(api, build_id)
        print('Build successful: https://cirrus-ci.com/build/{id}'.format(id=build_id))
    except CirrusBuildError:
        print('Build failed: https://cirrus-ci.com/build/{id}'.format(id=build_id))
        sys.exit(1)
    except Exception as exc:
        print('Build error: https://cirrus-ci.com/build/{id}'.format(id=build_id))
        print('  {exc.__class__.__name__}: {str(exc)}'.format(exc=exc))
        sys.exit(2)


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
        default=os.getenv(ENVIRONMENT['config'], '.cirrus.yml'),
        nargs='?',
        help=(
            'Path to YAML configuration file. '
            'Default value: ${} or .cirrus.yml'
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
        '--branch',
        default=os.getenv(ENVIRONMENT['branch'], 'master'),
        metavar='BRANCH',
        help=(
            'GitHub repo branch that will own the build. '
            'This branch may have no relation to the CI job being executed. '
            'Default value: ${} or master'
        ).format(ENVIRONMENT['branch']),
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
    parser.add_argument(
        '-v',
        '--verbose',
        action='count',
        default=0,
        help=('Increase output verbosity. Repeating this argument multiple times '
              'increases verbosity level even further.'),
    )
    args = parser.parse_args(*a, **ka)

    if not args.token:
        parser.error('API token is not defined')

    if not args.github:
        parser.error('GitHub repo is not defined')

    repo_parts = args.github.split('/')
    if len(repo_parts) != 2 or not all(repo_parts):
        parser.error('invalid repo identifier: {}'.format(args.github))
    args.owner, args.repo = repo_parts

    if not os.path.isfile(args.config):
        parser.error('config file not found: {}'.format(args.config))

    return args


def configure_logging(verbosity):
    verbosity_levels = {
        0: logging.WARNING,
        1: logging.INFO,
        2: logging.DEBUG,
        3: logging.NOTSET + 1,
    }
    if verbosity > max(verbosity_levels):
        verbosity = max(verbosity_levels)
    level = verbosity_levels.get(verbosity)
    log = logging.getLogger(__name__.split('.')[0])
    log.level = min(log.level, level)


if __name__ == '__main__':
    print(parse_args())
