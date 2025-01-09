import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from news.forms import BAD_WORDS
from news.models import Comment, News


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
    return News.objects.create(
        title='Test News',
        text='Test Content'
    )


@pytest.fixture
def comment(db, user, news):
    return Comment.objects.create(
        text='Test Comment',
        author=user,
        news=news
    )


@pytest.mark.django_db
def test_anonymous_user_cannot_post_comment(client, news):
    response = client.post(reverse('news:detail', args=[news.id]), {
        'text': 'Anonymous comment'
    })
    assert response.status_code == 302
    assert not Comment.objects.filter(text='Anonymous comment').exists()


@pytest.mark.django_db
def test_authenticated_user_can_post_comment(client, user, news):
    client.login(username='user', password='password')
    response = client.post(reverse('news:detail', args=[news.id]), {
        'text': 'User comment'
    })
    assert response.status_code == 302
    assert Comment.objects.filter(text='User comment').exists()


@pytest.mark.django_db
def test_comment_with_forbidden_words(client, user, news):
    client.login(username='user', password='password')
    forbidden_word = BAD_WORDS[0]
    response = client.post(reverse('news:detail', args=[news.id]), {
        'text': f'This comment contains {forbidden_word}'
    })
    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['form'].errors
    assert not Comment.objects.filter(
        text=f'This comment contains {forbidden_word}'
    ).exists()


@pytest.mark.django_db
def test_user_can_edit_own_comment(client, user, comment):
    client.login(username='user', password='password')
    client.post(reverse('news:edit', args=[comment.id]), {
        'text': 'Edited comment'
    })
    comment.refresh_from_db()
    assert comment.text == 'Edited comment'


@pytest.mark.django_db
def test_user_cannot_edit_others_comment(client, another_user, comment):
    client.login(username='another_user', password='password')
    client.post(reverse('news:edit', args=[comment.id]), {
        'text': 'Attempted edit'
    })
    comment.refresh_from_db()
    assert comment.text != 'Attempted edit'


@pytest.mark.django_db
def test_user_can_delete_own_comment(client, user, comment):
    client.login(username='user', password='password')
    client.post(reverse('news:delete', args=[comment.id]))
    assert not Comment.objects.filter(id=comment.id).exists()


@pytest.mark.django_db
def test_user_cannot_delete_others_comment(client, another_user, comment):
    client.login(username='another_user', password='password')
    client.post(reverse('news:delete', args=[comment.id]))
    assert Comment.objects.filter(id=comment.id).exists()
