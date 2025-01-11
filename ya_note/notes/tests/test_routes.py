import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from http import HTTPStatus

from notes.models import Note

from .constans import (
    ADD_NOTE_URL, delete_note_url, detail_note_url, edit_note_url,
    HOME_URL, LIST_URL, SUCCESS_URL
)


@pytest.mark.django_db
class TestRoutes:

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(
            username='user1', password='password1'
        )
        cls.user2 = User.objects.create_user(
            username='user2', password='password2'
        )
        cls.note = Note.objects.create(
            title='Test Note', text='Test Content',
            author=cls.user1, slug='test-note'
        )

    def test_home_page_accessible_to_anonymous(self, client):
        response = client.get(HOME_URL)
        assert response.status_code == HTTPStatus.OK

    def test_notes_list_accessible_to_authenticated_user(self, client, user1):
        client.force_login(user1)
        response = client.get(LIST_URL)
        assert response.status_code == HTTPStatus.OK

    def test_note_success_accessible_to_authenticated_user(
            self,
            client,
            user1
    ):
        client.force_login(user1)
        response = client.get(SUCCESS_URL)
        assert response.status_code == HTTPStatus.OK

    def test_add_note_accessible_to_authenticated_user(self, client, user1):
        client.force_login(user1)
        response = client.get(ADD_NOTE_URL)
        assert response.status_code == HTTPStatus.OK

    def test_note_detail_accessible_to_author(self, client, user1, note1):
        client.force_login(user1)
        response = client.get(detail_note_url(note1.slug))
        assert response.status_code == HTTPStatus.OK

    def test_note_detail_not_accessible_to_other_user(
            self,
            client,
            user2,
            note1
    ):
        client.force_login(user2)
        response = client.get(detail_note_url(note1.slug))
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_note_edit_accessible_to_author(self, client, user1, note1):
        client.force_login(user1)
        response = client.get(edit_note_url(note1.slug))
        assert response.status_code == HTTPStatus.OK

    def test_note_edit_not_accessible_to_other_user(
            self,
            client,
            user2,
            note1
    ):
        client.force_login(user2)
        response = client.get(edit_note_url(note1.slug))
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_note_delete_accessible_to_author(self, client, user1, note1):
        client.force_login(user1)
        response = client.get(delete_note_url(note1.slug))
        assert response.status_code == HTTPStatus.OK

    def test_note_delete_not_accessible_to_other_user(
            self,
            client,
            user2,
            note1
    ):
        client.force_login(user2)
        response = client.get(delete_note_url(note1.slug))
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_anonymous_user_redirected_to_login(self, client, note1):
        protected_urls = [
            LIST_URL, SUCCESS_URL, ADD_NOTE_URL,
            detail_note_url(note1.slug), edit_note_url(note1.slug),
            delete_note_url(note1.slug),
        ]
        for url in protected_urls:
            response = client.get(url)
            login_url = reverse('users:login')
            assert response.status_code == HTTPStatus.FOUND
            assert response.url.startswith(f'{login_url}?next={url}')

    def test_registration_page_accessible_to_anonymous(self, client):
        response = client.get(reverse('users:signup'))
        assert response.status_code == HTTPStatus.OK

    def test_login_page_accessible_to_anonymous(self, client):
        response = client.get(reverse('users:login'))
        assert response.status_code == HTTPStatus.OK

    def test_logout_page_accessible_to_anonymous(self, client):
        response = client.get(reverse('users:logout'))
        assert response.status_code == HTTPStatus.OK
