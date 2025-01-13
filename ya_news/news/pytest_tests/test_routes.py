from http import HTTPStatus

import pytest
from .conftest import (
    CLIENT_FIXTURE,
    COMMENT_DELETE_URL_FIXTURE,
    COMMENT_EDIT_URL_FIXTURE,
    HOME_URL_FIXTURE,
    LOGIN_URL_FIXTURE,
    LOGOUT_URL_FIXTURE,
    NEWS_DETAIL_URL_FIXTURE,
    SIGNUP_URL_FIXTURE
)


@pytest.mark.parametrize("url_fixture, client_fixture, expected_status", [
    (HOME_URL_FIXTURE, CLIENT_FIXTURE, HTTPStatus.OK),
    (NEWS_DETAIL_URL_FIXTURE, CLIENT_FIXTURE, HTTPStatus.OK),
    (SIGNUP_URL_FIXTURE, CLIENT_FIXTURE, HTTPStatus.OK),
    (LOGIN_URL_FIXTURE, CLIENT_FIXTURE, HTTPStatus.OK),
    (LOGOUT_URL_FIXTURE, CLIENT_FIXTURE, HTTPStatus.OK),
    (COMMENT_EDIT_URL_FIXTURE, CLIENT_FIXTURE, HTTPStatus.FOUND),
    (COMMENT_DELETE_URL_FIXTURE, CLIENT_FIXTURE, HTTPStatus.FOUND),
])
def test_status_codes_anonymous(
        client_fixture,
        url_fixture,
        expected_status
):
    assert client_fixture.get(url_fixture).status_code == expected_status
