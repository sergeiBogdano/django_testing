from http import HTTPStatus

from .base_test_case import (
    get_delete_note_url,
    get_detail_note_url,
    get_edit_note_url,
    NoteTestBase
)


class TestRoutes(NoteTestBase):

    def test_status_codes(self):
        self.client.force_login(self.user1)
        for url, expected_status in self.urls_with_status:
            response = self.client.get(url)
            self.assertEqual(response.status_code, expected_status)
        self.client.force_login(self.user2)
        for url in [get_detail_note_url(self.note1.slug),
                    get_edit_note_url(self.note1.slug),
                    get_delete_note_url(self.note1.slug)]:
            response = self.client.get(url)
            self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_redirect_urls(self):
        self.client.logout()
        for url, expected_redirect in self.redirect_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, HTTPStatus.FOUND)
            self.assertEqual(response.url, expected_redirect)
