from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

CLIENT_FIXTURE = pytest.lazy_fixture('client')
HOME_URL_FIXTURE = pytest.lazy_fixture('home_url')
NEWS_DETAIL_URL_FIXTURE = pytest.lazy_fixture('news_detail_url')
SIGNUP_URL_FIXTURE = pytest.lazy_fixture('signup_url')
LOGIN_URL_FIXTURE = pytest.lazy_fixture('login_url')
LOGOUT_URL_FIXTURE = pytest.lazy_fixture('logout_url')
COMMENT_EDIT_URL_FIXTURE = pytest.lazy_fixture('comment_edit_url')
COMMENT_DELETE_URL_FIXTURE = pytest.lazy_fixture('comment_delete_url')
COMMENT_EDIT_REDIRECT_URL_FIXTURE = pytest.lazy_fixture(
    'comment_edit_redirect_url'
)
COMMENT_DELETE_REDIRECT_URL_FIXTURE = pytest.lazy_fixture(
    'comment_delete_redirect_url'
)
COMMENT_DELETE_REDIRECT_URL_FIXTURE_NEXT = pytest.lazy_fixture(
    'comment_delete_redirect_url_with_next'
)
COMMENT_EDIT_REDIRECT_URL_FIXTURE_NEXT = pytest.lazy_fixture(
    'comment_edit_redirect_url_with_next'
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


@pytest.mark.parametrize("url_fixture, expected_redirect_url_fixture", [
    (COMMENT_EDIT_URL_FIXTURE, COMMENT_EDIT_REDIRECT_URL_FIXTURE_NEXT),
    (COMMENT_DELETE_URL_FIXTURE, COMMENT_DELETE_REDIRECT_URL_FIXTURE_NEXT),
])
def test_redirect_final_url_for_anonymous(
        client,
        url_fixture,
        expected_redirect_url_fixture
):
    assertRedirects(
        client.get(url_fixture),
        expected_redirect_url_fixture,
        fetch_redirect_response=False
    )
