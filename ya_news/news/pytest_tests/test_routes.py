import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from news.models import Comment, News


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
    return News.objects.create(
        title='Test News',
        text='Test Content'
    )


@pytest.fixture
def comment(db, user, news):
    return Comment.objects.create(
        text='Test Comment',
        author=user,
        news=news
    )


@pytest.mark.django_db
def test_home_page_accessible_to_anonymous(client):
    response = client.get(reverse('news:home'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_news_detail_accessible_to_anonymous(client, news):
    response = client.get(reverse('news:detail', args=[news.id]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_comment_edit_accessible_to_author(client, user, comment):
    client.login(username='user', password='password')
    response = client.get(reverse('news:edit', args=[comment.id]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_comment_delete_accessible_to_author(client, user, comment):
    client.login(username='user', password='password')
    response = client.get(reverse('news:delete', args=[comment.id]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_anonymous_user_redirected_to_login_on_comment_edit(
    client, comment
):
    response = client.get(reverse('news:edit', args=[comment.id]))
    login_url = reverse('users:login')
    assert response.status_code == 302
    assert response.url.startswith(f'{login_url}?next=')


@pytest.mark.django_db
def test_anonymous_user_redirected_to_login_on_comment_delete(
    client, comment
):
    response = client.get(reverse('news:delete', args=[comment.id]))
    login_url = reverse('users:login')
    assert response.status_code == 302
    assert response.url.startswith(f'{login_url}?next=')


@pytest.mark.django_db
def test_authorized_user_cannot_edit_others_comment(
    client, another_user, comment
):
    client.login(username='another_user', password='password')
    response = client.get(reverse('news:edit', args=[comment.id]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_authorized_user_cannot_delete_others_comment(
    client, another_user, comment
):
    client.login(username='another_user', password='password')
    response = client.get(reverse('news:delete', args=[comment.id]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_registration_page_accessible_to_anonymous(client):
    response = client.get(reverse('users:signup'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_page_accessible_to_anonymous(client):
    response = client.get(reverse('users:login'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_logout_page_accessible_to_anonymous(client):
    response = client.get(reverse('users:logout'))
    assert response.status_code == 200
