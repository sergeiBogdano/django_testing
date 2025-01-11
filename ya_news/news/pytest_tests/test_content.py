from http import HTTPStatus

import pytest

pytestmark = pytest.mark.django_db


def test_news_list_view_status_code(client, home_url):
    response = client.get(home_url)
    assert response.status_code == HTTPStatus.OK


def test_news_list_view_empty(client, home_url):
    response = client.get(home_url)
    assert 'news_list' in response.context
    assert len(response.context['news_list']) == 0


def test_news_detail_view_status_code(client, news_detail_url, news):
    response = client.get(news_detail_url)
    assert response.status_code == HTTPStatus.OK
    assert 'news' in response.context
    assert response.context['news'] == news


def test_comment_form_presence(client, news_detail_url, user):
    client.force_login(user)
    response = client.get(news_detail_url)
    assert response.status_code == HTTPStatus.OK
    assert 'form' in response.context,\
        "Форма комментариев не найдена в контексте"
