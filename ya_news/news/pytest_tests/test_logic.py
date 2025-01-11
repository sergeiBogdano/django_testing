from http import HTTPStatus

import pytest

from news.forms import BAD_WORDS
from news.models import Comment

pytestmark = pytest.mark.django_db

ANONYMOUS_COMMENT_DATA = {'text': 'Anonymous comment'}
USER_COMMENT_DATA = {'text': 'User comment'}
UPDATED_COMMENT_DATA = {'text': 'Edited comment'}


def test_anonymous_user_cannot_create_comment(client, news_detail_url):
    initial_comments = set(Comment.objects.all())
    response = client.post(news_detail_url, ANONYMOUS_COMMENT_DATA)
    assert response.status_code == HTTPStatus.FOUND
    assert set(Comment.objects.all()) == initial_comments


def test_authenticated_user_can_create_comment(
        client_logged_in,
        news_detail_url,
        user,
        news
):
    initial_comments = set(Comment.objects.all())
    response = client_logged_in.post(news_detail_url, data=USER_COMMENT_DATA)
    assert response.status_code == HTTPStatus.FOUND
    assert len(Comment.objects.all()) == len(initial_comments) + 1
    new_comment = Comment.objects.exclude(
        id__in=[c.id for c in initial_comments]
    ).get()
    assert new_comment.text == USER_COMMENT_DATA['text']
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
    assert not Comment.objects.filter(text__icontains=forbidden_word).exists()


def test_user_can_edit_own_comment(
        client_logged_in,
        comment,
        comment_edit_url
):
    response = client_logged_in.post(
        comment_edit_url,
        data=UPDATED_COMMENT_DATA
    )
    assert response.status_code == HTTPStatus.FOUND
    updated_comment = Comment.objects.get(id=comment.id)
    assert updated_comment.text == UPDATED_COMMENT_DATA['text']
    assert updated_comment.author == comment.author
    assert updated_comment.news == comment.news


def test_user_cannot_edit_others_comment(
        another_client_logged_in,
        comment,
        comment_edit_url
):
    initial_comment = Comment.objects.get(id=comment.id)
    response = another_client_logged_in.post(comment_edit_url,
                                             {'text': 'Attempted edit'})
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
    assert Comment.objects.filter(id=comment.id).exists()
    response = another_client_logged_in.post(comment_delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    existing_comment = Comment.objects.get(id=comment.id)
    assert existing_comment.text == comment.text
    assert existing_comment.author == comment.author
    assert existing_comment.news == comment.news
