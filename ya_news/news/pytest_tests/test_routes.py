from http import HTTPStatus

import pytest


CLIENT_FIXTURE = pytest.lazy_fixture('client')
LOGIN_URL_FIXTURE = pytest.lazy_fixture('login_url')


@pytest.mark.parametrize("url_fixture, client_fixture, expected_status", [
    (pytest.lazy_fixture('home_url'), pytest.lazy_fixture('client'),
     HTTPStatus.OK),
    (pytest.lazy_fixture('news_detail_url'), pytest.lazy_fixture('client'),
     HTTPStatus.OK),
    (pytest.lazy_fixture('signup_url'), pytest.lazy_fixture('client'),
     HTTPStatus.OK),
    (pytest.lazy_fixture('login_url'), pytest.lazy_fixture('client'),
     HTTPStatus.OK),
    (pytest.lazy_fixture('logout_url'), pytest.lazy_fixture('client'),
     HTTPStatus.OK),
    (pytest.lazy_fixture('comment_edit_url'), pytest.lazy_fixture('client'),
     HTTPStatus.FOUND),
    (pytest.lazy_fixture('comment_delete_url'), pytest.lazy_fixture('client'),
     HTTPStatus.FOUND),
])
def test_status_codes_anonymous(
        client_fixture,
        url_fixture,
        expected_status,
        login_url
):
    response = client_fixture.get(url_fixture)
    assert response.status_code == expected_status
