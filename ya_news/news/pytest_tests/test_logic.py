from http import HTTPStatus

import pytest
from django.urls import reverse

from news.forms import BAD_WORDS
from news.models import Comment, News

pytestmark = pytest.mark.django_db


def test_anonymous_user_cannot_create_comment(
        client,
        news_detail_url,
        anonymous_comment_data
):
    initial_comments = list(Comment.objects.all())
    response = client.post(news_detail_url, anonymous_comment_data)
    assert response.status_code == HTTPStatus.FOUND
    assert list(Comment.objects.all()) == initial_comments


def test_authenticated_user_can_create_comment(
        client_logged_in,
        news_detail_url,
        user_comment_data,
        user, news
):
    initial_comments = list(Comment.objects.all())
    response = client_logged_in.post(news_detail_url, data=user_comment_data)
    assert response.status_code == HTTPStatus.FOUND
    assert len(Comment.objects.all()) == len(initial_comments) + 1
    new_comment = Comment.objects.exclude(
        id__in=[c.id for c in initial_comments]
    ).get()
    assert new_comment.text == user_comment_data['text']
    assert new_comment.author == user
    assert new_comment.news == news


@pytest.mark.parametrize("forbidden_word", BAD_WORDS)
def test_comment_with_forbidden_words(
        client_logged_in,
        news_detail_url,
        forbidden_word
):
    comment_data = {'text': f'This comment contains {forbidden_word}'}
    response = client_logged_in.post(news_detail_url, data=comment_data)
    assert response.status_code == HTTPStatus.OK
    assert 'form' in response.context
    assert response.context['form'].errors
    assert not Comment.objects.filter(text=comment_data['text']).exists()


def test_user_can_edit_own_comment(
        client_logged_in,
        comment,
        comment_edit_url,
        updated_comment_data
):
    response = client_logged_in.post(
        comment_edit_url,
        data=updated_comment_data
    )
    assert response.status_code == HTTPStatus.FOUND
    updated_comment = Comment.objects.get(id=comment.id)
    assert updated_comment.text == updated_comment_data['text']
    assert updated_comment.author == comment.author
    assert updated_comment.news == comment.news


def test_user_cannot_edit_others_comment(
        another_client_logged_in,
        comment,
        comment_edit_url
):
    initial_comment = Comment.objects.get(id=comment.id)
    response = another_client_logged_in.post(
        comment_edit_url,
        {'text': 'Attempted edit'}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    unchanged_comment = Comment.objects.get(id=comment.id)
    assert unchanged_comment.text == initial_comment.text
    assert unchanged_comment.author == initial_comment.author
    assert unchanged_comment.news == initial_comment.news


def test_user_can_delete_own_comment(
        client_logged_in,
        comment,
        comment_delete_url
):
    response = client_logged_in.post(comment_delete_url)
    assert response.status_code == HTTPStatus.FOUND
    assert not Comment.objects.filter(id=comment.id).exists()


def test_user_cannot_delete_others_comment(
        another_client_logged_in,
        comment,
        comment_delete_url
):
    response = another_client_logged_in.post(comment_delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    existing_comment = Comment.objects.get(id=comment.id)
    assert existing_comment.text == comment.text
    assert existing_comment.author == comment.author
    assert existing_comment.news == comment.news


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
