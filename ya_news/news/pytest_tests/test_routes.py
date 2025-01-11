import pytest
from http import HTTPStatus

import pytest_lazyfixture

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("url, expected_status", [
    (pytest_lazyfixture.lazy_fixture('home_url'), HTTPStatus.OK),
    (pytest_lazyfixture.lazy_fixture('news_detail_url'), HTTPStatus.OK),
    (pytest_lazyfixture.lazy_fixture('signup_url'), HTTPStatus.OK),
    (pytest_lazyfixture.lazy_fixture('login_url'), HTTPStatus.OK),
    (pytest_lazyfixture.lazy_fixture('logout_url'), HTTPStatus.OK),
])
def test_status_codes(client, url, expected_status):
    response = client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize("url_fixture", [
    'comment_edit_url',
    'comment_delete_url',
])
def test_redirects_for_anonymous(
        client,
        request,
        url_fixture,
        login_url,
        comment
):
    url = request.getfixturevalue(url_fixture)
    if callable(url):
        url = url(comment)
    response = client.get(url)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url.startswith(f'{login_url}?next=')
