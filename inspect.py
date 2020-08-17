from cirrus_run import CirrusAPI
from cirrus_run.cli import parse_args
from cirrus_run.queries import get_repo


def main(*a, **ka):
    args = parse_args(*a, **ka)
    api = CirrusAPI(args.token)
    repo_id = get_repo(api, args.owner, args.repo)

    print('Recent builds in {args.owner}/{args.repo} with more than 1 task:'.format(**locals()))
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
