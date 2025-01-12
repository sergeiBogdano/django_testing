from .base_test_case import (
    DELETE_NOTE1_URL,
    DETAIL_NOTE1_URL,
    EDIT_NOTE1_URL,
    NoteTestBase,

)


class TestRoutes(NoteTestBase):

    def test_status_codes(self):
        for url, expected_status in self.urls_with_status:
            with self.subTest(user='user1', url=url):
                response = self.logged_in_client_user1.get(url)
                self.assertEqual(response.status_code, expected_status)
        for url in [DETAIL_NOTE1_URL, EDIT_NOTE1_URL, DELETE_NOTE1_URL]:
            with self.subTest(user='user2', url=url):
                response = self.logged_in_client_user2.get(url)
                self.assertEqual(response.status_code, 404)

    def test_status_and_redirects(self):
        for url, expected_status in self.urls_with_status:
            with self.subTest(url=url):
                response = self.logged_in_client.get(url)
                self.assertEqual(response.status_code, expected_status)
