from datetime import timedelta

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News
from news.forms import CommentForm

pytestmark = pytest.mark.django_db

NEWS_COUNT = 10


@pytest.fixture
def user(db):
    return User.objects.create_user(username='user', password='password')


@pytest.fixture
def news_list(db):
    news_items = [
        News(
            title=f'News {i}',
            text='Content',
            date=timezone.now() - timedelta(days=i)
        ) for i in range(NEWS_COUNT + 5)
    ]
    News.objects.bulk_create(news_items)
    return news_items


@pytest.fixture
def news_with_comments(db, user):
    news = News.objects.create(
        title='News with Comments',
        text='Content'
    )
    comments = [
        Comment(
            text=f'Comment {i}',
            author=user,
            news=news,
            created=timezone.now() - timedelta(hours=i)
        ) for i in range(5)
    ]
    Comment.objects.bulk_create(comments)
    return news


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def news_detail_url(news_with_comments):
    return reverse('news:detail', args=[news_with_comments.id])


def test_news_count_on_home_page(client, home_url, news_list):
    response = client.get(home_url)
    assert len(response.context['news_list']) <= NEWS_COUNT


def test_news_order_on_home_page(client, home_url, news_list):
    response = client.get(home_url)
    news_dates = [news.date for news in response.context['news_list']]
    assert news_dates == sorted(news_dates, reverse=True)


def test_comments_order_on_news_detail(client, news_detail_url):
    response = client.get(news_detail_url)
    comment_dates = [
        comment.created
        for comment in response.context['object'].comment_set.all()
    ]
    assert comment_dates == sorted(comment_dates)


def test_comment_form_visibility_for_anonymous(client, news_detail_url):
    response = client.get(news_detail_url)
    assert 'form' not in response.context


def test_comment_form_visibility_for_authenticated(
        client,
        user,
        news_detail_url
):
    client.login(username='user', password='password')
    response = client.get(news_detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
