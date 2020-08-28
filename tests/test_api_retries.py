import pytest
import responses

from cirrus_run.api import CirrusAPI, CirrusAPIError, CirrusHTTPError


@pytest.fixture
def api():
    '''Reusable fake API object'''
    yield CirrusAPI('faketoken')


@responses.activate
def test_unrecoverable_http_error(api):
    '''Check handling of unrecoverable HTTP errors'''
    responses.add(
        responses.Response(
            method='POST',
            url=api._url,
            status=502,
        )
    )

    with pytest.raises(CirrusHTTPError):
        api('fake query text', delay=0)

    assert responses.assert_call_count(api._url, 1 + 3), \
           'Incorrect number of _post calls before raising CirrusHTTPError'


@responses.activate
def test_recoverable_http_error(api):
    '''Check handling of interminent HTTP errors'''
    for params in [
        {'status': 502,},
        {'status': 502,},
        {'status': 200, 'json': {'data': {'hello': 'world'}}},
    ]:
        responses.add(responses.Response(method='POST', url=api._url, **params))
    reply = api('fake query text', delay=0)
    assert reply == {'hello': 'world'}
    assert responses.assert_call_count(api._url, 3)


@responses.activate
def test_unrecoverable_api_error(api):
    '''Check handling of unrecoverable API errors'''
    responses.add(
        responses.Response(
            method='POST',
            url=api._url,
            status=200,
            json={'errors': ['fake error message']},
        )
    )

    with pytest.raises(CirrusAPIError):
        api('fake query text', delay=0)

    assert responses.assert_call_count(api._url, 1 + 3), \
           'Incorrect number of _post calls before raising CirrusAPIError'


@responses.activate
def test_recoverable_api_error(api):
    '''Check handling of interminent api errors'''
    for params in [
        {'status': 200, 'json': {'errors': ['fake error message']},},
        {'status': 200, 'json': {'errors': ['fake error message']},},
        {'status': 200, 'json': {'data': {'hello': 'world'}}},
    ]:
        responses.add(responses.Response(method='POST', url=api._url, **params))
    reply = api('fake query text', delay=0)
    assert reply == {'hello': 'world'}
    assert responses.assert_call_count(api._url, 3)
