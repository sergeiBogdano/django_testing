from http import HTTPStatus

from .base_test_case import (
    ADD_NOTE_URL,
    LIST_URL,
    NoteTestBase,
    SUCCESS_URL
)


class TestRoutes(NoteTestBase):

    def test_status_codes_and_redirects(self):
        client_url_status = [
            (
                self.logged_in_client_user1,
                'logged_in_client_user1',
                LIST_URL, HTTPStatus.OK
            ),
            (
                self.logged_in_client_user1,
                'logged_in_client_user1',
                SUCCESS_URL,
                HTTPStatus.OK
            ),
            (
                self.logged_in_client_user1,
                'logged_in_client_user1',
                ADD_NOTE_URL,
                HTTPStatus.OK
            ),
            (
                self.logged_in_client,
                'logged_in_client',
                LIST_URL,
                HTTPStatus.OK
            ),
            (
                self.logged_in_client,
                'logged_in_client',
                SUCCESS_URL,
                HTTPStatus.OK
            ),
            (
                self.logged_in_client,
                'logged_in_client',
                ADD_NOTE_URL,
                HTTPStatus.OK
            ),
            (
                self.logged_in_client_user2,
                'logged_in_client_user2',
                LIST_URL,
                HTTPStatus.OK
            ),
            (
                self.logged_in_client_user2,
                'logged_in_client_user2',
                SUCCESS_URL,
                HTTPStatus.OK
            ),
            (
                self.logged_in_client_user2,
                'logged_in_client_user2',
                ADD_NOTE_URL,
                HTTPStatus.OK
            ),
        ]

        for client, client_name, url, expected_status in client_url_status:
            with self.subTest(client=client_name, url=url):
                response = client.get(url)
                self.assertEqual(response.status_code, expected_status)
