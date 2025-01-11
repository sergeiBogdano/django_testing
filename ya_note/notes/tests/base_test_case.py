from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from notes.models import Note


class NoteTestBase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
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
        cls.client.force_login(cls.user1)
        cls.urls_with_status = [
            (HOME_URL, HTTPStatus.OK),
            (LIST_URL, HTTPStatus.OK),
            (SUCCESS_URL, HTTPStatus.OK),
            (ADD_NOTE_URL, HTTPStatus.OK),
            (get_detail_note_url(cls.note1.slug), HTTPStatus.OK),
            (get_edit_note_url(cls.note1.slug), HTTPStatus.OK),
            (get_delete_note_url(cls.note1.slug), HTTPStatus.OK),
        ]
        cls.protected_urls = [
            LIST_URL, SUCCESS_URL, ADD_NOTE_URL,
            get_detail_note_url(cls.note1.slug),
            get_edit_note_url(cls.note1.slug),
            get_delete_note_url(cls.note1.slug),
        ]
        cls.login_url = reverse('users:login')
        cls.redirect_urls = [
            (url, f'{cls.login_url}?next={url}') for url in cls.protected_urls
        ]
        cls.initial_note_count = Note.objects.count()


def get_edit_note_url(slug):
    return reverse('notes:edit', args=[slug])


def get_delete_note_url(slug):
    return reverse('notes:delete', args=[slug])


def get_detail_note_url(slug):
    return reverse('notes:detail', args=[slug])

# Извините, не понимаю немного,
# вы мне говорите использовать константы,
# но когда я проверяю код он мне пишет.
# E731 do not assign a lambda expression, use a def
# можете, пожалуйста, как то направить на решение


HOME_URL = reverse('notes:home')
LIST_URL = reverse('notes:list')
SUCCESS_URL = reverse('notes:success')
ADD_NOTE_URL = reverse('notes:add')
