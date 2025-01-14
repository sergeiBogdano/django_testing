import pytest

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
def test_comment_form_in_context(client_logged_in, news_detail_url):
    response = client_logged_in.get(news_detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)


@pytest.mark.django_db
def test_news_order(client, many_news_entries, home_url):
    response = client.get(home_url)
    news_list = list(response.context['news_list'])
    sorted_news_list = sorted(
        news_list,
        key=lambda news: news.date,
        reverse=True
    )
    assert news_list == sorted_news_list


@pytest.mark.django_db
def test_comment_order(client, news, many_comments, news_detail_url):
    response = client.get(news_detail_url)
    assert 'object' in response.context
    news_object = response.context['object']
    comment_list = list(news_object.comment_set.all())
    assert comment_list == many_comments


@pytest.mark.django_db
def test_comment_form_absent_for_unauthenticated_user(
        client,
        news_detail_url
):
    assert 'form' not in client.get(news_detail_url).context
