from http import HTTPStatus

import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from news.models import Comment, News

pytestmark = pytest.mark.django_db


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def news_detail_url(news):
    return reverse('news:detail', args=[news.id])


@pytest.fixture
def comment_edit_url(comment):
    return reverse('news:edit', args=[comment.id])


@pytest.fixture
def comment_delete_url(comment):
    return reverse('news:delete', args=[comment.id])


@pytest.fixture
def login_url():
    return reverse('users:login')


@pytest.fixture
def signup_url():
    return reverse('users:signup')


@pytest.fixture
def logout_url():
    return reverse('users:logout')


@pytest.fixture
def user(db):
    return User.objects.create_user(username='user', password='password')


@pytest.fixture
def another_user(db):
    return User.objects.create_user(
        username='another_user',
        password='password'
    )


@pytest.fixture
def news(db):
    return News.objects.create(title='Test News', text='Test Content')


@pytest.fixture
def comment(db, user, news):
    return Comment.objects.create(
        text='Test Comment',
        author=user,
        news=news
    )


@pytest.mark.parametrize('url', [
    pytest.lazy_fixture('home_url'),
    pytest.lazy_fixture('news_detail_url'),
    pytest.lazy_fixture('signup_url'),
    pytest.lazy_fixture('login_url'),
    pytest.lazy_fixture('logout_url'),
])
def test_accessible_pages(client, url, expected_status=HTTPStatus.OK):
    response = client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize('url', [
    pytest.lazy_fixture('comment_edit_url'),
    pytest.lazy_fixture('comment_delete_url'),
])
def test_redirects_for_anonymous(client, url, login_url):
    response = client.get(url)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url.startswith(f'{login_url}?next=')


def test_comment_edit_accessible_to_author(client, user, comment_edit_url):
    client.login(username='user', password='password')
    response = client.get(comment_edit_url)
    assert response.status_code == HTTPStatus.OK


def test_comment_delete_accessible_to_author(client, user, comment_delete_url):
    client.login(username='user', password='password')
    response = client.get(comment_delete_url)
    assert response.status_code == HTTPStatus.OK


def test_authorized_user_cannot_edit_others_comment(
    client, another_user, comment_edit_url
):
    client.login(username='another_user', password='password')
    response = client.get(comment_edit_url)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_authorized_user_cannot_delete_others_comment(
    client, another_user, comment_delete_url
):
    client.login(username='another_user', password='password')
    response = client.get(comment_delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
