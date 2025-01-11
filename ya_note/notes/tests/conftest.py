import pytest
from django.contrib.auth.models import User

from notes.models import Note


@pytest.fixture
def user1(db):
    return User.objects.create_user(username='user1', password='password1')


@pytest.fixture
def user2(db):
    return User.objects.create_user(username='user2', password='password2')


@pytest.fixture
def note1(user1):
    return Note.objects.create(
        title='Note 1', text='Content 1', author=user1, slug='note-1'
    )


@pytest.fixture
def note2(user2):
    return Note.objects.create(
        title='Note 2', text='Content 2', author=user2, slug='note-2'
    )


@pytest.fixture
def note_data():
    return {
        'title': 'New Note',
        'text': 'Some content',
        'slug': 'new-note'
    }
