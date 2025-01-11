from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from notes.models import Note


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

    def setUp(self):
        self.client = Client()


def edit_note_url(slug):
    return reverse('notes:edit', args=[slug])


def delete_note_url(slug):
    return reverse('notes:delete', args=[slug])


def detail_note_url(slug):
    return reverse('notes:detail', args=[slug])


HOME_URL = reverse('notes:home')
LIST_URL = reverse('notes:list')
SUCCESS_URL = reverse('notes:success')
ADD_NOTE_URL = reverse('notes:add')
