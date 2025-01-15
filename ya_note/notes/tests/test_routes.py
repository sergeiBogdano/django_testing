from http import HTTPStatus

from .base_test_case import (
    ADD_NOTE_URL,
    LIST_URL,
    NoteTestBase,
    SUCCESS_URL,
)


class TestRoutes(NoteTestBase):

    def test_status_codes_and_redirects(self):
        client_url_status = [
            (self.logged_in_client_author, LIST_URL, HTTPStatus.OK),
            (self.logged_in_client_author, SUCCESS_URL, HTTPStatus.OK),
            (self.logged_in_client_author, ADD_NOTE_URL, HTTPStatus.OK),
            (self.logged_in_client, LIST_URL, HTTPStatus.OK),
            (self.logged_in_client, SUCCESS_URL, HTTPStatus.OK),
            (self.logged_in_client, ADD_NOTE_URL, HTTPStatus.OK),
            (self.logged_in_client_non_author, LIST_URL, HTTPStatus.OK),
            (self.logged_in_client_non_author, SUCCESS_URL, HTTPStatus.OK),
            (self.logged_in_client_non_author, ADD_NOTE_URL, HTTPStatus.OK),
            (self.client, LIST_URL, HTTPStatus.FOUND),
            (self.client, SUCCESS_URL, HTTPStatus.FOUND),
            (self.client, ADD_NOTE_URL, HTTPStatus.FOUND),
        ]

        for client, url, expected_status in client_url_status:
            with self.subTest(client=client, url=url):
                response = client.get(url)
                self.assertEqual(response.status_code, expected_status)
                if expected_status == HTTPStatus.FOUND:
                    expected_redirect_url = self.expected_redirects[url]
                    self.assertRedirects(response, expected_redirect_url)

    def test_final_urls_after_redirects(self):
        redirect_tests = [
            (self.client, LIST_URL, self.expected_redirects[LIST_URL]),
            (self.client, SUCCESS_URL, self.expected_redirects[SUCCESS_URL]),
            (
                self.client,
                ADD_NOTE_URL,
                self.expected_redirects[ADD_NOTE_URL]
            ),
        ]

        for client, initial_url, expected_final_url in redirect_tests:
            with self.subTest(client=client, initial_url=initial_url):
                response = client.get(initial_url, follow=True)
                self.assertRedirects(response, expected_final_url)
