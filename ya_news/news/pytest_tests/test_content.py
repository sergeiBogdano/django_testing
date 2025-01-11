import pytest
from django.urls import reverse
from http import HTTPStatus

from news.models import News

pytestmark = pytest.mark.django_db


def test_news_list_view(client, home_url):
    response = client.get(home_url)
    assert response.status_code == HTTPStatus.OK
    assert 'news_list' in response.context
    assert len(response.context['news_list']) == 0


def test_news_detail_view(client, news_detail_url, news):
    response = client.get(news_detail_url)
    assert response.status_code == HTTPStatus.OK
    assert 'news' in response.context
    assert response.context['news'] == news


def test_news_creation(client, user):
    client.force_login(user)
    news_data = {
        'title': 'New Test News',
        'text': 'Test Content',
    }
    url = reverse('news:home')
    response = client.post(url, data=news_data)
    assert response.status_code == 405
    assert not News.objects.filter(title='New Test News').exists()


def test_news_update(client, user, news):
    client.force_login(user)
    updated_news_data = {
        'title': 'Updated Test News',
        'text': 'This is updated test news content.',
    }
    url = reverse('news:edit', args=[news.id])
    response = client.post(url, data=updated_news_data)
    assert response.status_code == 404
    news.refresh_from_db()
    assert news.title == 'Test News'
    assert news.text == 'Test Content'


def test_news_deletion(client, user, news):
    client.force_login(user)
    url = reverse('news:delete', args=[news.id])
    response = client.post(url)
    assert response.status_code == 404
    assert News.objects.filter(id=news.id).exists()
