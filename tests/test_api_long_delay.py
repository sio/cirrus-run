import logging
import pytest
import responses
from time import monotonic as time

from cirrus_run.api import CirrusAPI, CirrusAPIError, CirrusHTTPError


@pytest.fixture
def api():
    '''Fake API instance with shorter retry delays'''
    api = CirrusAPI('faketoken')
    api.RETRY_DELAY=0.1
    api.RETRY_LONG_DELAY = 1
    yield api


@responses.activate
def test_long_retry_delay_required(api, caplog):
    '''Wait out intermittent API server errors'''
    responses.add(
        responses.Response(
            method='POST',
            url=api._url,
            status=502,
            body='The server encountered a temporary error and could not complete your request. Please try again in 30 seconds.',
        )
    )

    caplog.set_level(logging.DEBUG, logger='cirrus_run')

    time_start = time()
    with pytest.raises(CirrusHTTPError):
        api('fake query text')
    time_end = time()

    assert time_end - time_start > api.RETRY_LONG_DELAY + api.RETRY_DELAY * 2
    assert time_end - time_start < api.RETRY_LONG_DELAY * 3

    long_delay_log_message_count = 0
    for record in caplog.records:
        if 'API server asked for longer retry delay' in record.message:
            long_delay_log_message_count += 1
    assert long_delay_log_message_count == 1

    assert responses.assert_call_count(api._url, 1 + 3), \
           'Incorrect number of _post calls before raising CirrusHTTPError'


@responses.activate
def test_long_retry_not_required(api, caplog):
    '''Some 502 errors do not require a long delay'''
    responses.add(
        responses.Response(
            method='POST',
            url=api._url,
            status=502,
        )
    )

    caplog.set_level(logging.DEBUG, logger='cirrus_run')

    time_start = time()
    with pytest.raises(CirrusHTTPError):
        api('fake query text')
    time_end = time()

    assert time_end - time_start > api.RETRY_DELAY * 3
    assert time_end - time_start < api.RETRY_LONG_DELAY + api.RETRY_DELAY * 2

    long_delay_log_message_count = 0
    for record in caplog.records:
        if 'API server asked for longer retry delay' in record.message:
            long_delay_log_message_count += 1
    assert long_delay_log_message_count == 0

    assert responses.assert_call_count(api._url, 1 + 3), \
           'Incorrect number of _post calls before raising CirrusHTTPError'


@responses.activate
def test_long_retry_internal_server_error_recoverable(api, caplog):
    '''Retry GraphQL internal server error - with recovery'''
    caplog.set_level(logging.DEBUG, logger='cirrus_run')
    for params in [
        {'status': 200, 'json': {'errors': [{'locations': [], 'message': 'Internal Server Error(s) while executing query'}]}},
        {'status': 200, 'json': {'errors': [{'locations': [], 'message': 'Internal Server Error(s) while executing query'}]}},
        {'status': 200, 'json': {'data': {'hello': 'world'}}},
    ]:
        responses.add(responses.Response(method='POST', url=api._url, **params))

    time_start = time()
    reply = api('fake query text', delay=0)
    time_end = time()

    assert reply == {'hello': 'world'}
    assert responses.assert_call_count(api._url, 3)

    assert time_end - time_start > api.RETRY_DELAY * 2
    assert time_end - time_start < api.RETRY_LONG_DELAY * 2

    long_delay_log_message_count = 0
    for record in caplog.records:
        if 'API server asked for longer retry delay' in record.message:
            long_delay_log_message_count += 1
    assert long_delay_log_message_count == 1


@responses.activate
def test_long_retry_internal_server_error_unrecoverable(api, caplog):
    '''Retry GraphQL internal server error - unrecoverable'''
    caplog.set_level(logging.DEBUG, logger='cirrus_run')
    for params in [
        {'status': 200, 'json': {'errors': [{'locations': [], 'message': 'Internal Server Error(s) while executing query'}]}},
    ]:
        responses.add(responses.Response(method='POST', url=api._url, **params))

    time_start = time()
    with pytest.raises(CirrusAPIError):
        reply = api('fake query text', delay=0)
    time_end = time()

    assert responses.assert_call_count(api._url, 1 + 3)

    assert time_end - time_start > api.RETRY_DELAY * 3
    assert time_end - time_start < api.RETRY_LONG_DELAY * 2 + api.RETRY_DELAY

    long_delay_log_message_count = 0
    for record in caplog.records:
        if 'API server asked for longer retry delay' in record.message:
            long_delay_log_message_count += 1
    assert long_delay_log_message_count == 1
