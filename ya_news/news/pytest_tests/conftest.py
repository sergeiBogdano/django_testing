from datetime import datetime, timedelta

import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from news.models import Comment, News


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


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def client_logged_in(client, user):
    client.login(username='user', password='password')
    return client


@pytest.fixture
def another_client_logged_in(client, another_user):
    client.login(username='another_user', password='password')
    return client


@pytest.fixture
def many_news_entries(db):
    base_date = datetime.now().date()
    news_list = [
        News(
            title={i + 1},
            text={i + 1},
            date=base_date + timedelta(days=i)
        )
        for i in range(222)
    ]
    News.objects.bulk_create(news_list)


@pytest.fixture
def many_comments(db, user, news):
    base_date = datetime.now()
    comments = [
        Comment(
            text={i + 1},
            author=user,
            news=news,
            created=base_date + timedelta(days=i)
        )
        for i in range(222)
    ]
    for comment in comments:
        comment.save()
    return comments


@pytest.fixture
def comment_edit_redirect_url(login_url):
    return login_url


@pytest.fixture
def comment_delete_redirect_url(login_url):
    return login_url
