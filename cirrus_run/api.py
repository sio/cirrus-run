'''
CirrusCI API interaction
'''


import logging
from time import sleep
from pprint import pformat

import requests


log = logging.getLogger(__name__)


class CirrusAPIError(Exception):
    def __init__(self, errors):
        message = 'API returned {num} error(s):\n{errors}'.format(
            num=len(errors),
            errors=pformat(errors, indent=2)
        )
        super().__init__(message)


class CirrusHTTPError(Exception):
    def __init__(self, response):
        code = response.status_code
        text = response.text
        url = response.url
        message = 'HTTP {code}: {url}\n{text}'.format(**locals())
        super().__init__(message)
        self.code = code
        self.response = response

    def __repr__(self):
        return '<{cls} [{code}]>'.format(cls=self.__class__.__name__, code=self.code)


class CirrusAPI:
    '''Interact with Cirrus via GraphQL API'''

    DEFAULT_URL = 'https://api.cirrus-ci.com/graphql'
    USER_AGENT = 'Cirrus remote CLI <https://github.com/sio/cirrus-run>'
    RETRY_ATTEMPTS = 3
    RETRY_DELAY = 2  # seconds
    RETRY_LONG_DELAY = 30

    def __init__(self, token, url=None):
        if url is None:
            url = self.DEFAULT_URL
        self._url = url

        session = requests.Session()
        session.headers.update({
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(token),
            'User-Agent': self.USER_AGENT,
        })
        session.timeout = 5
        self._requests = session

    def __call__(self, query, params=None, retries=None, delay=None):
        if retries is None:
            retries = self.RETRY_ATTEMPTS
        if delay is None:
            delay = self.RETRY_DELAY

        payload = dict(query=query.strip(), variables=params or {})
        log.debug('Calling API with: {}'.format(payload))

        error_count = 0
        long_wait_happened = False
        while True:
            try:
                answer = self._post(json=payload)
                return self._parse_api_response(answer)
            except Exception as exc:
                error_count += 1
                if error_count > retries:
                    raise exc
                elif isinstance(exc, CirrusHTTPError) \
                and 'try again in 30 seconds' in exc.response.text \
                and not long_wait_happened:
                    long_wait_happened = True
                    log.debug('API server asked for longer retry delay: {}, retrying'.format(exc))
                    sleep(self.RETRY_LONG_DELAY)
                else:
                    log.debug('Error when calling API: {}, retrying'.format(exc))
                    sleep(delay)

    def _parse_api_response(self, data):
        if 'errors' in data and data['errors']:
            raise CirrusAPIError(data['errors'])
        return data['data']

    def _post(self, **ka):
        response = self._requests.post(self._url, **ka)
        if response.status_code != 200:
            raise CirrusHTTPError(response)
        return response.json()

    def get(self, *a, **ka):
        '''Perform GET request using API session'''
        return self._requests.get(*a, **ka)
