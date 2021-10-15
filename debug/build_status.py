import json
import os
import sys
from datetime import datetime
from time import sleep


from cirrus_run import CirrusAPI
from cirrus_run.cli import ENVIRONMENT


def main():
    token = os.environ[ENVIRONMENT['token']]
    api = CirrusAPI(token)
    build_id = sys.argv[1]

    query = '''
        query GetBuild($build: ID!) {
            build(id: $build) {
                id
                durationInSeconds
                clockDurationInSeconds
                status
                buildCreatedTimestamp
                changeTimestamp
            }
        }
    '''
    print('https://cirrus-ci.com/build/{}'.format(build_id))
    while True:
        response = api(query, params=dict(build=build_id))
        now = datetime.utcnow()
        print(f'{now:%Y-%m-%d %H:%M:%S+00:00 (UTC)}')
        print(json.dumps(response, indent=2, ensure_ascii=False))
        try:
            if response['build']['status'] not in {'CREATED', 'TRIGGERED', 'EXECUTING'}:
                break
        except (TypeError, KeyError) as exc:
            pass
        sleep(2)


if __name__ == '__main__':
    main()
