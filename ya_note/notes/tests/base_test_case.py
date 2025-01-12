from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from notes.models import Note


HOME_URL = reverse('notes:home')
LIST_URL = reverse('notes:list')
SUCCESS_URL = reverse('notes:success')
ADD_NOTE_URL = reverse('notes:add')
LOGIN_URL = reverse('users:login')
EDIT_NOTE1_URL = reverse('notes:edit', args=['note-1'])
EDIT_NOTE2_URL = reverse('notes:edit', args=['note-2'])
DELETE_NOTE1_URL = reverse('notes:delete', args=['note-1'])
DELETE_NOTE2_URL = reverse('notes:delete', args=['note-2'])
DETAIL_NOTE1_URL = reverse('notes:detail', args=['note-1'])
DETAIL_NOTE2_URL = reverse('notes:detail', args=['note-2'])


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
        cls.DETAIL_NOTE1_URL = reverse(
            'notes:detail', args=[cls.note1.slug]
        )
        cls.EDIT_NOTE1_URL = reverse(
            'notes:edit', args=[cls.note1.slug]
        )
        cls.DELETE_NOTE1_URL = reverse(
            'notes:delete', args=[cls.note1.slug]
        )
        cls.DELETE_NOTE2_URL = reverse(
            'notes:delete', args=[cls.note2.slug]
        )
        cls.logged_in_client = Client()
        cls.logged_in_client.force_login(cls.user1)
        cls.logged_in_client_user1 = Client()
        cls.logged_in_client_user1.force_login(cls.user1)
        cls.logged_in_client_user2 = Client()
        cls.logged_in_client_user2.force_login(cls.user2)

        cls.urls_with_status = [
            (HOME_URL, HTTPStatus.OK),
            (LIST_URL, HTTPStatus.OK),
            (SUCCESS_URL, HTTPStatus.OK),
            (ADD_NOTE_URL, HTTPStatus.OK),
            (cls.DETAIL_NOTE1_URL, HTTPStatus.OK),
            (cls.EDIT_NOTE1_URL, HTTPStatus.OK),
            (cls.DELETE_NOTE1_URL, HTTPStatus.OK),
        ]
        cls.logged_in_client = Client()
        cls.logged_in_client.force_login(cls.user1)
        cls.logged_in_client_user1 = Client()
        cls.logged_in_client_user1.force_login(cls.user1)
        cls.logged_in_client_user2 = Client()
        cls.logged_in_client_user2.force_login(cls.user2)

    def test_protected_urls(self):
        protected_urls = [
            LIST_URL, SUCCESS_URL, ADD_NOTE_URL,
            self.DETAIL_NOTE1_URL,
            self.EDIT_NOTE1_URL,
            self.DELETE_NOTE1_URL,
        ]
        for url in protected_urls:
            response = self.client.get(url)
            self.assertRedirects(response, f'{LOGIN_URL}?next={url}')
