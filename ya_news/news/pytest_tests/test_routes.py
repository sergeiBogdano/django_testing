import pytest
from http import HTTPStatus


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("url_key, expected_status", [
    ('home_url', HTTPStatus.OK),
    ('news_detail_url', HTTPStatus.OK),
    ('signup_url', HTTPStatus.OK),
    ('login_url', HTTPStatus.OK),
    ('logout_url', HTTPStatus.OK),
    ('comment_edit_url', HTTPStatus.FOUND),
    ('comment_delete_url', HTTPStatus.FOUND),
])
def test_status_codes(client, urls, url_key, expected_status, login_url):
    url = urls[url_key]
    response = client.get(url)
    assert response.status_code == expected_status

    if expected_status == HTTPStatus.FOUND:
        assert response.url == f'{login_url}?next={url}'
