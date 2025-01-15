from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note


HOME_URL = reverse('notes:home')
LIST_URL = reverse('notes:list')
SUCCESS_URL = reverse('notes:success')
ADD_NOTE_URL = reverse('notes:add')
LOGIN_URL = reverse('users:login')
EDIT_NOTE_ROUTE = 'notes:edit'
DELETE_NOTE_ROUTE = 'notes:delete'
DETAIL_NOTE_ROUTE = 'notes:detail'
EXPECTED_REDIRECT_LIST_URL = f'{LOGIN_URL}?next={LIST_URL}'
EXPECTED_REDIRECT_SUCCESS_URL = f'{LOGIN_URL}?next={SUCCESS_URL}'
EXPECTED_REDIRECT_ADD_NOTE_URL = f'{LOGIN_URL}?next={ADD_NOTE_URL}'


def get_edit_note_url(slug):
    return reverse(EDIT_NOTE_ROUTE, kwargs={'slug': slug})


def get_delete_note_url(slug):
    return reverse(DELETE_NOTE_ROUTE, kwargs={'slug': slug})


def get_detail_note_url(slug):
    return reverse(DETAIL_NOTE_ROUTE, kwargs={'slug': slug})


class NoteTestBase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(
            username='user1', password='password1'
        )
        cls.non_author = User.objects.create_user(
            username='user2', password='password2'
        )
        cls.note = Note.objects.create(
            title='Note 1', text='Content 1', author=cls.author,
            slug='note-1'
        )
        cls.note_data = {
            'title': 'New Note',
            'text': 'Some content',
            'slug': 'new-note'
        }
        cls.add_note_url = ADD_NOTE_URL
        cls.edit_note_url = get_edit_note_url(cls.note.slug)
        cls.delete_note_url = get_delete_note_url(cls.note.slug)
        cls.detail_note_url = get_detail_note_url(cls.note.slug)

        users_and_clients = [
            (cls.author, 'logged_in_client'),
            (cls.author, 'logged_in_client_author'),
            (cls.non_author, 'logged_in_client_non_author'),
            (cls.non_author, 'client_user2')
        ]
        cls.expected_redirects = {
            LIST_URL: f'{LOGIN_URL}?next={LIST_URL}',
            SUCCESS_URL: f'{LOGIN_URL}?next={SUCCESS_URL}',
            ADD_NOTE_URL: f'{LOGIN_URL}?next={ADD_NOTE_URL}',
        }

        for user, client_attr in users_and_clients:
            client = Client()
            client.force_login(user)
            setattr(cls, client_attr, client)
