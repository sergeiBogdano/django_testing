from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note


HOME_URL = reverse('notes:home')
LIST_URL = reverse('notes:list')
SUCCESS_URL = reverse('notes:success')
ADD_NOTE_URL = reverse('notes:add')
LOGIN_URL = reverse('users:login')


class NoteTestBase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(
            username='user1', password='password1'
        )
        cls.user2 = User.objects.create_user(
            username='user2', password='password2'
        )
        cls.note1 = Note.objects.create(
            title='Note 1', text='Content 1', author=cls.user1,
            slug='note-1'
        )
        cls.note2 = Note.objects.create(
            title='Note 2', text='Content 2', author=cls.user2,
            slug='note-2'
        )
        cls.note_data = {
            'title': 'New Note',
            'text': 'Some content',
            'slug': 'new-note'
        }
        cls.logged_in_client = Client()
        cls.logged_in_client.force_login(cls.user1)
        cls.logged_in_client_user1 = Client()
        cls.logged_in_client_user1.force_login(cls.user1)
        cls.logged_in_client_user2 = Client()
        cls.logged_in_client_user2.force_login(cls.user2)

    def get_note_urls(self, note):
        return {
            'edit': reverse('notes:edit', args=[note.slug]),
            'delete': reverse('notes:delete', args=[note.slug]),
            'detail': reverse('notes:detail', args=[note.slug]),
        }
