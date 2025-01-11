from datetime import timedelta
import time
from http import HTTPStatus

import pytest
from django.urls import reverse

from news.models import Comment, News
from news.forms import CommentForm

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
def test_comment_form_presence(client_logged_in, news_detail_url):
    response = client_logged_in.get(news_detail_url)
    assert response.status_code == HTTPStatus.OK
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)


@pytest.mark.django_db
def test_news_order(client, news):
    news_2 = News.objects.create(
        title='Test News 2',
        text='More Content',
        date=news.date + timedelta(days=1)
    )
    response = client.get(reverse('news:home'))
    news_list = list(response.context['news_list'])
    assert news_list == [news_2, news]


@pytest.mark.django_db
def test_comment_order(client, news, user):
    comment = Comment.objects.create(
        text='First Comment',
        author=user,
        news=news
    )
    time.sleep(1)
    comment_2 = Comment.objects.create(
        text='Another Comment',
        author=user,
        news=news
    )
    response = client.get(reverse('news:detail', args=[news.id]))
    assert 'object' in response.context
    news_object = response.context['object']
    comment_list = list(news_object.comment_set.all())
    assert comment_list == [comment, comment_2]
