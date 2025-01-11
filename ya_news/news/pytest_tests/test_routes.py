from http import HTTPStatus
import pytest


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("url_fixture, expected_status", [
    ('home_url', HTTPStatus.OK),
    ('news_detail_url', HTTPStatus.OK),
    ('signup_url', HTTPStatus.OK),
    ('login_url', HTTPStatus.OK),
    ('logout_url', HTTPStatus.OK),
    ('comment_edit_url', HTTPStatus.FOUND),
    ('comment_delete_url', HTTPStatus.FOUND),
])
def test_status_codes_anonymous(
        client,
        request,
        url_fixture,
        expected_status,
        login_url
):
    url = request.getfixturevalue(url_fixture)
    response = client.get(url)
    assert response.status_code == expected_status

    if expected_status == HTTPStatus.FOUND:
        assert response.url == f'{login_url}?next={url}'


@pytest.mark.parametrize("url_fixture, expected_status", [
    ('home_url', HTTPStatus.OK),
    ('news_detail_url', HTTPStatus.OK),
    ('signup_url', HTTPStatus.OK),
    ('login_url', HTTPStatus.OK),
    ('logout_url', HTTPStatus.OK),
    ('comment_edit_url', HTTPStatus.OK),
    ('comment_delete_url', HTTPStatus.OK),
])
def test_status_codes_authenticated(
        client_logged_in,
        request,
        url_fixture,
        expected_status
):
    url = request.getfixturevalue(url_fixture)
    response = client_logged_in.get(url)
    assert response.status_code == expected_status


def test_news_list_view_status_code(client, home_url):
    response = client.get(home_url)
    assert response.status_code == HTTPStatus.OK


def test_news_detail_status_code(client_logged_in, news_detail_url):
    response = client_logged_in.get(news_detail_url)
    assert response.status_code == HTTPStatus.OK
