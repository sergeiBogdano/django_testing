import pytest
from django.urls import reverse

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
def test_comment_form(client_logged_in, news_detail_url):
    response = client_logged_in.get(news_detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)


@pytest.mark.django_db
def test_news_order(client, many_news_entries):
    response = client.get(reverse('news:home'))
    news_list = list(response.context['news_list'])
    assert news_list == list(reversed(many_news_entries))[:10]


@pytest.mark.django_db
def test_comment_order(client, news, many_comments):
    response = client.get(reverse('news:detail', args=[news.id]))
    assert 'object' in response.context
    news_object = response.context['object']
    comment_list = list(news_object.comment_set.all())
    assert comment_list == many_comments


@pytest.mark.django_db
def test_comment_form_present_for_authenticated_user(
        client_logged_in,
        news_detail_url
):
    response = client_logged_in.get(news_detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)


@pytest.mark.django_db
def test_comment_form_absent_for_unauthenticated_user(
        client,
        news_detail_url
):
    response = client.get(news_detail_url)
    assert 'form' not in response.context
