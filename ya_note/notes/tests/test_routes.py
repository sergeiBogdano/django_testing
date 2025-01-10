from django.contrib.auth.models import User
from django.test import TestCase
from http import HTTPStatus

from notes.models import Note
from notes.constans import (
    HOME_URL, NOTES_LIST_URL, NOTE_SUCCESS_URL, ADD_NOTE_URL,
    SIGNUP_URL, LOGIN_URL, LOGOUT_URL,
    note_detail_url, note_edit_url, note_delete_url
)


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(
            username='user1',
            password='password1'
        )
        cls.user2 = User.objects.create_user(
            username='user2',
            password='password2'
        )
        cls.note = Note.objects.create(
            title='Test Note',
            text='Test Content',
            author=cls.user1
        )

    def test_accessible_pages(self):
        self.client.login(username='user1', password='password1')
        urls = [
            (HOME_URL, HTTPStatus.OK),
            (NOTES_LIST_URL, HTTPStatus.OK),
            (NOTE_SUCCESS_URL, HTTPStatus.OK),
            (ADD_NOTE_URL, HTTPStatus.OK),
            (note_detail_url(self.note.slug), HTTPStatus.OK),
            (note_edit_url(self.note.slug), HTTPStatus.OK),
            (note_delete_url(self.note.slug), HTTPStatus.OK),
            (SIGNUP_URL, HTTPStatus.OK),
            (LOGIN_URL, HTTPStatus.OK),
            (LOGOUT_URL, HTTPStatus.OK),
        ]
        for url, expected_status in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, expected_status)

    def test_redirects_for_anonymous(self):
        protected_urls = [
            NOTES_LIST_URL,
            NOTE_SUCCESS_URL,
            ADD_NOTE_URL,
            note_detail_url(self.note.slug),
            note_edit_url(self.note.slug),
            note_delete_url(self.note.slug),
        ]
        for url in protected_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, f'{LOGIN_URL}?next={url}')

    def test_note_detail_not_accessible_to_other_user(self):
        self.client.login(username='user2', password='password2')
        response = self.client.get(note_detail_url(self.note.slug))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_note_edit_not_accessible_to_other_user(self):
        self.client.login(username='user2', password='password2')
        response = self.client.get(note_edit_url(self.note.slug))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_note_delete_not_accessible_to_other_user(self):
        self.client.login(username='user2', password='password2')
        response = self.client.get(note_delete_url(self.note.slug))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
