from http import HTTPStatus

from .base_test_case import (
    ADD_NOTE_URL,
    LIST_URL,
    LOGIN_URL,
    NoteTestBase,
    SUCCESS_URL,
)


class TestRoutes(NoteTestBase):
    def setUp(self):
        super().setUp()
        self.expected_redirect_list_url =\
            f'{LOGIN_URL}?next={LIST_URL}'
        self.expected_redirect_success_url =\
            f'{LOGIN_URL}?next={SUCCESS_URL}'
        self.expected_redirect_add_note_url =\
            f'{LOGIN_URL}?next={ADD_NOTE_URL}'

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
                    expected_redirect_url = f'{LOGIN_URL}?next={url}'
                    self.assertEqual(response.url, expected_redirect_url)

    def test_final_urls_after_redirects(self):
        redirect_tests = [
            (self.client, LIST_URL, self.expected_redirect_list_url),
            (self.client, SUCCESS_URL, self.expected_redirect_success_url),
            (self.client, ADD_NOTE_URL, self.expected_redirect_add_note_url),
        ]

        for client, initial_url, expected_final_url in redirect_tests:
            with self.subTest(client=client, initial_url=initial_url):
                response = client.get(initial_url, follow=True)
                self.assertEqual(
                    response.redirect_chain[-1][0], expected_final_url
                )
