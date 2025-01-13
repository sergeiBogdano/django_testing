from http import HTTPStatus

import pytest

from news.forms import BAD_WORDS
from news.models import Comment

pytestmark = pytest.mark.django_db

COMMENT_DATA = {'text': 'Sample comment'}
COMMENT_TEMPLATE = {'text': 'This comment contains {}'}
COMMENT_DATA_WITH_FORBIDDEN_WORDS = [
    {'text': COMMENT_TEMPLATE['text'].format(word)} for word in BAD_WORDS
]


def test_anonymous_user_cannot_create_comment(client, news_detail_url):
    initial_comments = set(Comment.objects.all())
    response = client.post(news_detail_url, COMMENT_DATA)
    assert response.status_code == HTTPStatus.FOUND
    assert set(Comment.objects.all()) == initial_comments


def test_authenticated_user_can_create_comment(
        client_logged_in,
        news_detail_url,
        user,
        news
):
    initial_comments = set(Comment.objects.all())
    response = client_logged_in.post(news_detail_url, data=COMMENT_DATA)
    assert response.status_code == HTTPStatus.FOUND
    all_comments = set(Comment.objects.all())
    assert len(all_comments) == len(initial_comments) + 1
    new_comment = all_comments - initial_comments
    assert len(new_comment) == 1
    new_comment = new_comment.pop()
    assert new_comment.text == COMMENT_DATA['text']
    assert new_comment.author == user
    assert new_comment.news == news


@pytest.mark.parametrize("comment_data", COMMENT_DATA_WITH_FORBIDDEN_WORDS)
def test_comment_with_forbidden_words(
        client_logged_in,
        news_detail_url,
        comment_data
):
    initial_comments = set(Comment.objects.all())
    response = client_logged_in.post(news_detail_url, data=comment_data)
    assert response.status_code == HTTPStatus.OK
    assert 'form' in response.context
    assert response.context['form'].errors
    assert set(Comment.objects.all()) == initial_comments


def test_user_can_edit_own_comment(
        client_logged_in,
        comment,
        comment_edit_url
):
    response = client_logged_in.post(
        comment_edit_url,
        data=COMMENT_DATA
    )
    assert response.status_code == HTTPStatus.FOUND
    updated_comment = Comment.objects.get(id=comment.id)
    assert updated_comment.text == COMMENT_DATA['text']
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
    initial_comment_count = Comment.objects.count()
    response = client_logged_in.post(comment_delete_url)
    assert response.status_code == HTTPStatus.FOUND
    assert not Comment.objects.filter(id=comment.id).exists()
    assert Comment.objects.count() == initial_comment_count - 1


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
