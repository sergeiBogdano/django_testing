from datetime import timedelta

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News


@pytest.fixture
def user(db):
    return User.objects.create_user(username='user', password='password')


@pytest.fixture
def news_list(db):
    return [
        News.objects.create(
            title=f'News {i}',
            text='Content',
            date=timezone.now() - timedelta(days=i)
        ) for i in range(15)
    ]


@pytest.fixture
def news_with_comments(db, user):
    news = News.objects.create(
        title='News with Comments',
        text='Content'
    )
    for i in range(5):
        Comment.objects.create(
            text=f'Comment {i}',
            author=user,
            news=news,
            created=timezone.now() - timedelta(hours=i)
        )
    return news


@pytest.mark.django_db
def test_news_count_on_home_page(client, news_list):
    response = client.get(reverse('news:home'))
    assert response.status_code == 200
    assert len(response.context['news_list']) <= 10


@pytest.mark.django_db
def test_news_order_on_home_page(client, news_list):
    response = client.get(reverse('news:home'))
    assert response.status_code == 200
    news_dates = [news.date for news in response.context['news_list']]
    assert news_dates == sorted(news_dates, reverse=True)


@pytest.mark.django_db
def test_comments_order_on_news_detail(client, news_with_comments):
    response = client.get(
        reverse('news:detail', args=[news_with_comments.id])
    )
    assert response.status_code == 200
    comment_dates = [
        comment.created
        for comment in response.context['object'].comment_set.all()
    ]
    assert comment_dates == sorted(comment_dates)


@pytest.mark.django_db
def test_comment_form_visibility_for_anonymous(client, news_with_comments):
    response = client.get(
        reverse('news:detail', args=[news_with_comments.id])
    )
    assert response.status_code == 200
    assert 'form' not in response.context


@pytest.mark.django_db
def test_comment_form_visibility_for_authenticated(
    client, user, news_with_comments
):
    client.login(username='user', password='password')
    response = client.get(
        reverse('news:detail', args=[news_with_comments.id])
    )
    assert response.status_code == 200
    assert 'form' in response.context
