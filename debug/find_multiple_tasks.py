'''
Helper script for issue #4: https://github.com/sio/cirrus-run/issues/4

Find recent builds that contain more than one task. This is helpful for finding
builds where a single defined task was automatically restarted by CirrusCI due
to GCP instance termination.

Execute `make debug/find_multiple_tasks` from repo top-level directory
'''

import os
from cirrus_run import CirrusAPI
from cirrus_run.cli import ENVIRONMENT
from cirrus_run.queries import get_repo


def main(*a, **ka):
    token = os.environ.get(ENVIRONMENT['token'], "")
    api = CirrusAPI(token)
    owner, repo = os.environ[ENVIRONMENT['github']].split('/')
    repo_id = get_repo(api, owner, repo)

    print('Recent builds in {owner}/{repo} with more than 1 task:'.format(**locals()))
    for url in filter_builds(api, repo_id):
        print('  {}'.format(url))


def filter_builds(api, repo_id):
    query = '''
        query tasks_by_job($repo_id: ID!) {
            repository(id: $repo_id) {
                builds(last: 100) {
                    edges {
                        node {
                            id
                            tasks {
                                id
                            }
                        }
                    }
                }
            }
        }
    '''
    params = dict(repo_id=repo_id)
    response = api(query, params)
    url = 'https://cirrus-ci.com/build/{}'

    for build in response['repository']['builds']['edges']:
        if len(build['node']['tasks']) > 1:
            build_id = build['node']['id']
            yield url.format(build_id)


if __name__ == '__main__':
    main()
