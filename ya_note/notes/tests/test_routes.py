from http import HTTPStatus

from .base_test_case import (
    ADD_NOTE_URL,
    LIST_URL,
    LOGIN_URL,
    NoteTestBase,
    SUCCESS_URL
)


class TestRoutes(NoteTestBase):

    def test_status_codes_and_redirects(self):
        urls_with_status = [
            (LIST_URL, HTTPStatus.OK),
            (SUCCESS_URL, HTTPStatus.OK),
            (ADD_NOTE_URL, HTTPStatus.OK),
        ]
        for client, client_name in [
            (self.logged_in_client_user1, 'logged_in_client_user1'),
            (self.logged_in_client, 'logged_in_client')
        ]:
            for url, expected_status in urls_with_status:
                with self.subTest(client=client_name, url=url):
                    response = client.get(url)
                    self.assertEqual(response.status_code, expected_status)

    def test_protected_urls(self):
        protected_urls = [
            LIST_URL, SUCCESS_URL, ADD_NOTE_URL,
        ]
        for note in [self.note1, self.note2]:
            urls = self.get_note_urls(note)
            protected_urls.extend(urls.values())

        for url in protected_urls:
            response = self.client.get(url)
            self.assertRedirects(response, f'{LOGIN_URL}?next={url}')
