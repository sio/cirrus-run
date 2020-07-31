'''
Command line interface for cirrus-run
'''


import argparse
import logging
import os
import sys
import traceback
from pprint import pformat

from jinja2 import Template

from . import CirrusAPI
from .throbber import ProgressBar
from .queries import build_log, get_repo, create_build, wait_build, CirrusBuildError

log = logging.getLogger(__name__)


ENVIRONMENT = {
    'github': 'CIRRUS_GITHUB_REPO',
    'branch': 'CIRRUS_GITHUB_BRANCH',
    'token': 'CIRRUS_API_TOKEN',
    'config': 'CIRRUS_CONFIG',
    'timeout': 'CIRRUS_TIMEOUT',
    'show_log': 'CIRRUS_SHOW_BUILD_LOG',
}


def main(*a, **ka):
    args = parse_args(*a, **ka)
    configure_logging(args.verbose)
    log.debug('Parsed command line arguments:\n{}'.format(pformat(vars(args), indent=2)))

    config = read_config(args.config)
    api = CirrusAPI(args.token)
    repo_id = get_repo(api, args.owner, args.repo)
    build_id = create_build(api, repo_id, args.branch, config)
    build_url = 'https://cirrus-ci.com/build/{}'.format(build_id)

    print('Build created: {}'.format(build_url))
    with ProgressBar('' if args.verbose else '.'):
        try:
            wait_build(api, build_id, abort=args.timeout*60)
            rc, status, message = 0, 'successful', ''
        except CirrusBuildError:
            rc, status, message = 1, 'failed', ''
        except Exception as exc:
            rc, status, message = 2, 'error', '{exception}: {text}'.format(
                                        exception=exc.__class__.__name__,
                                        text=str(exc))

    if args.show_build_log == 'always' \
    or (args.show_build_log == 'failure' and rc != 0):
        print('Build {}, see log below:'.format(status, build_url))
        try:
            for chunk in build_log(api, build_id):
                print(chunk)
        except Exception as exc:
            error = traceback.format_exc()
            log.error(error)

    print('Build {}: {}'.format(status, build_url))
    if message:
        print('  {}'.format(message))
    sys.exit(rc)


def read_config(path):
    '''Load YAML config from file or Jinja2 template'''
    with open(path) as config_file:
        raw = config_file.read()
    ext = os.path.splitext(path)[1].lower().lstrip('.')
    if ext in {'j2', 'jinja', 'jinja2'}:
        template = Template(raw)
        return template.render(os.environ)
    else:
        return raw


def fallback_config_path():
    '''Calculate default config path if none provided by user'''
    paths = [
        '.cirrus.yml',
        '.cirrus.yml.j2',
    ]
    for path in paths:
        if os.path.isfile(path):
            return path
    else:
        return paths[0]


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
        default=os.getenv(ENVIRONMENT['config'], fallback_config_path()),
        nargs='?',
        help=(
            'Path to YAML configuration file or Jinja2 template for such file. '
            'Filenames ending with .j2 or .jinja2 are assumed to provide the templates. '
            'All environment variables are available inside these templates. '
            'Default value: ${} or .cirrus.yml or .cirrus.yml.j2'
        ).format(ENVIRONMENT['config']),
    )
    parser.add_argument(
        '--token',
        default=os.getenv(ENVIRONMENT['token']),
        metavar='TOKEN',
        help=(
            'Access token for CirrusCI API. '
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
    parser.add_argument(
        '--timeout',
        default=os.getenv(ENVIRONMENT['timeout'], 120),
        metavar='MINUTES',
        help=(
            'Timeout (in minutes) before assuming that the build has hanged and '
            'that API responses are unreliable. Default value: ${} or 120'
        ).format(ENVIRONMENT['timeout']),
    )
    parser.add_argument(
        '--show-build-log',
        default=os.getenv(ENVIRONMENT['show_log'], 'failure'),
        choices={'always', 'never', 'failure'},
        type=str.lower,
        help=(
            'Specify whether to print the build log to stdout after completing CI run. '
            'Default value: ${} or "failure"'
        ).format(ENVIRONMENT['show_log']),
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
