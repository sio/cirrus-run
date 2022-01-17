'''
Tests in this module are not "pure",
i.e. they call out to outside URLs to test that upstream API provider did not
change GraphQL schema in a backwards incompatible way
'''

import pytest

from cirrus_run.queries import get_repo
from cirrus_run.api import CirrusAPI


@pytest.fixture
def api():
    '''Reusable fake API object'''
    yield CirrusAPI()


def test_known_repo_id(api):
    '''Check that repo ID query still works'''
    assert get_repo(api, 'sio', '.cirrus-ci-jobs') == '4749235174244352'
