from http import HTTPStatus
from django.urls import reverse

from .base_test_case import (
    ADD_NOTE_URL, delete_note_url, detail_note_url, edit_note_url,
    HOME_URL, LIST_URL, SUCCESS_URL, NoteTestBase
)


class TestRoutes(NoteTestBase):

    def test_status_codes(self):
        self.client.force_login(self.user1)
        urls = [
            (HOME_URL, HTTPStatus.OK),
            (LIST_URL, HTTPStatus.OK),
            (SUCCESS_URL, HTTPStatus.OK),
            (ADD_NOTE_URL, HTTPStatus.OK),
            (detail_note_url(self.note1.slug), HTTPStatus.OK),
            (edit_note_url(self.note1.slug), HTTPStatus.OK),
            (delete_note_url(self.note1.slug), HTTPStatus.OK),
        ]

        for url, expected_status in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, expected_status)

        self.client.force_login(self.user2)
        response = self.client.get(detail_note_url(self.note1.slug))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        response = self.client.get(edit_note_url(self.note1.slug))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        response = self.client.get(delete_note_url(self.note1.slug))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_redirect_urls(self):
        protected_urls = [
            LIST_URL, SUCCESS_URL, ADD_NOTE_URL,
            detail_note_url(self.note1.slug), edit_note_url(self.note1.slug),
            delete_note_url(self.note1.slug),
        ]
        for url in protected_urls:
            response = self.client.get(url)
            login_url = reverse('users:login')
            self.assertEqual(response.status_code, HTTPStatus.FOUND)
            self.assertTrue(response.url.startswith(f'{login_url}?next={url}'))
