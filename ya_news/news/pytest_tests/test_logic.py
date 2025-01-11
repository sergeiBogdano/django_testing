import pytest
from http import HTTPStatus

from news.forms import BAD_WORDS
from news.models import Comment

pytestmark = pytest.mark.django_db


def test_anonymous_user_cannot_create_comment(client, news_detail_url):
    initial_comment_count = Comment.objects.count()
    response = client.post(news_detail_url, {'text': 'Anonymous comment'})
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == initial_comment_count


def test_authenticated_user_can_create_comment(
        client,
        user,
        news_detail_url,
        news
):
    client.login(username='user', password='password')
    comment_data = {'text': 'User comment'}
    initial_comment_count = Comment.objects.count()
    response = client.post(news_detail_url, data=comment_data)
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == initial_comment_count + 1
    new_comment = Comment.objects.latest('id')
    assert new_comment.text == 'User comment'
    assert new_comment.author == user
    assert new_comment.news == news


@pytest.mark.parametrize("forbidden_word", BAD_WORDS)
def test_comment_with_forbidden_words(
        client,
        user,
        news_detail_url,
        forbidden_word
):
    client.login(username='user', password='password')
    comment_data = {'text': f'This comment contains {forbidden_word}'}
    response = client.post(news_detail_url, data=comment_data)
    assert response.status_code == HTTPStatus.OK
    assert 'form' in response.context
    assert response.context['form'].errors
    assert not Comment.objects.filter(text=comment_data['text']).exists()


def test_user_can_edit_own_comment(client, user, comment, comment_edit_url):
    client.login(username='user', password='password')
    updated_comment_data = {'text': 'Edited comment'}
    response = client.post(comment_edit_url, data=updated_comment_data)
    assert response.status_code == HTTPStatus.FOUND
    updated_comment = Comment.objects.get(id=comment.id)
    assert updated_comment.text == 'Edited comment'
    assert updated_comment.author == user
    assert updated_comment.news == comment.news


def test_user_cannot_edit_others_comment(
        client,
        another_user,
        comment,
        comment_edit_url
):
    client.login(username='another_user', password='password')
    response = client.post(comment_edit_url, {'text': 'Attempted edit'})
    assert response.status_code == HTTPStatus.NOT_FOUND
    unchanged_comment = Comment.objects.get(id=comment.id)
    assert unchanged_comment.text == 'Test Comment'


def test_user_can_delete_own_comment(
        client,
        user,
        comment,
        comment_delete_url
):
    client.login(username='user', password='password')
    response = client.post(comment_delete_url)
    assert response.status_code == HTTPStatus.FOUND
    assert not Comment.objects.filter(id=comment.id).exists()


def test_user_cannot_delete_others_comment(
        client,
        another_user,
        comment,
        comment_delete_url
):
    client.login(username='another_user', password='password')
    response = client.post(comment_delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    existing_comment = Comment.objects.get(id=comment.id)
    assert existing_comment.text == 'Test Comment'
    assert existing_comment.author == comment.author
    assert existing_comment.news == comment.news
