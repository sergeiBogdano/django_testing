import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from news.forms import BAD_WORDS
from news.models import Comment, News

pytestmark = pytest.mark.django_db


@pytest.fixture
def news_detail_url(news):
    return reverse('news:detail', args=[news.id])


@pytest.fixture
def comment_edit_url(comment):
    return reverse('news:edit', args=[comment.id])


@pytest.fixture
def comment_delete_url(comment):
    return reverse('news:delete', args=[comment.id])


@pytest.fixture
def user(db):
    return User.objects.create_user(username='user', password='password')


@pytest.fixture
def another_user(db):
    return User.objects.create_user(
        username='another_user',
        password='password'
    )


@pytest.fixture
def news(db):
    return News.objects.create(title='Test News', text='Test Content')


@pytest.fixture
def comment(db, user, news):
    return Comment.objects.create(
        text='Test Comment',
        author=user,
        news=news
    )


def test_anonymous_user_cannot_modify_database(client, news_detail_url):
    response = client.post(news_detail_url, {'text': 'Anonymous comment'})
    assert response.status_code == 302
    assert Comment.objects.count() == 0


def test_authenticated_user_can_post_comment(client, user, news):
    client.login(username='user', password='password')
    news_detail_url = reverse('news:detail', args=[news.id])
    response = client.post(news_detail_url, {'text': 'User comment'})
    assert response.status_code == 302
    assert Comment.objects.filter(author=user, news=news).count() == 1


@pytest.mark.parametrize('forbidden_word', BAD_WORDS)
def test_comment_with_forbidden_words(
    client, user, news_detail_url, forbidden_word
):
    client.login(username='user', password='password')
    response = client.post(
        news_detail_url, {'text': f'This comment contains {forbidden_word}'}
    )
    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['form'].errors
    assert Comment.objects.count() == 0


def test_user_can_edit_own_comment(client, user, comment, comment_edit_url):
    client.login(username='user', password='password')
    response = client.post(comment_edit_url, {'text': 'Edited comment'})
    assert response.status_code == 302
    updated_comment = Comment.objects.get(id=comment.id)
    assert updated_comment.text == 'Edited comment'
    assert updated_comment.author == user
    assert updated_comment.news == comment.news


def test_user_cannot_edit_others_comment(
    client, another_user, comment, comment_edit_url
):
    client.login(username='another_user', password='password')
    response = client.post(comment_edit_url, {'text': 'Attempted edit'})
    assert response.status_code == 404
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
    assert response.status_code == 302
    assert not Comment.objects.filter(id=comment.id).exists()


def test_user_cannot_delete_others_comment(
    client, another_user, comment, comment_delete_url
):
    client.login(username='another_user', password='password')
    response = client.post(comment_delete_url)
    assert response.status_code == 404
    assert Comment.objects.filter(id=comment.id).exists()
