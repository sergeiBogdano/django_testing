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
EDIT_NOTE_URL = reverse('notes:edit', args=['note-1'])
DELETE_NOTE_URL = reverse('notes:delete', args=['note-1'])
DETAIL_NOTE_URL = reverse('notes:detail', args=['note-1'])


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
        cls.edit_note_url = EDIT_NOTE_URL
        cls.delete_note_url = DELETE_NOTE_URL
        cls.detail_note_url = DETAIL_NOTE_URL

        cls.logged_in_client_author = Client()
        cls.logged_in_client_author.force_login(cls.author)

        cls.logged_in_client_non_author = Client()
        cls.logged_in_client_non_author.force_login(cls.non_author)
        cls.expected_redirects = {
            LIST_URL: EXPECTED_REDIRECT_LIST_URL,
            SUCCESS_URL: EXPECTED_REDIRECT_SUCCESS_URL,
            ADD_NOTE_URL: EXPECTED_REDIRECT_ADD_NOTE_URL,
        }
