import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from http import HTTPStatus
from pytils.translit import slugify

from notes.models import Note
from .constans import ADD_NOTE_URL, delete_note_url, edit_note_url


@pytest.mark.django_db
class TestLogic:

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(
            username='user1', password='password1'
        )
        cls.user2 = User.objects.create_user(
            username='user2', password='password2'
        )

    def test_logged_in_user_can_create_note(self, client, user1, note_data):
        client.force_login(user1)
        response = client.post(ADD_NOTE_URL, note_data)
        assert response.status_code == HTTPStatus.FOUND
        assert Note.objects.filter(slug=note_data['slug']).exists()
        note = Note.objects.get(slug=note_data['slug'])
        assert note.title == note_data['title']
        assert note.text == note_data['text']
        assert note.author == user1

    def test_anonymous_user_cannot_create_note(self, client, note_data):
        response = client.post(ADD_NOTE_URL, note_data)
        login_url = reverse('users:login')
        assert response.status_code == HTTPStatus.FOUND
        assert response.url.startswith(f'{login_url}?next={ADD_NOTE_URL}')
        assert not Note.objects.filter(slug=note_data['slug']).exists()

    def test_cannot_create_notes_with_same_slug(self, client, user1, note1):
        client.force_login(user1)
        with pytest.raises(Exception):
            Note.objects.create(
                title='Another Title', text='Content',
                author=user1, slug=note1.slug
            )

    def test_slug_is_generated_if_not_provided(self, client, user1):
        client.force_login(user1)
        note_data = {'title': 'Заметка без слага', 'text': 'Some content'}
        response = client.post(ADD_NOTE_URL, note_data)
        assert response.status_code == HTTPStatus.FOUND
        note = Note.objects.get(title=note_data['title'])
        assert note.slug == slugify(note_data['title'])
        assert note.text == note_data['text']
        assert note.author == user1

    def test_user_can_edit_own_note(self, client, user1, note1):
        client.force_login(user1)
        updated_data = {
            'title': 'Edited Note', 'text': 'Updated content',
            'slug': note1.slug
        }
        response = client.post(edit_note_url(note1.slug), updated_data)
        assert response.status_code == HTTPStatus.FOUND
        note1.refresh_from_db()
        assert note1.title == updated_data['title']
        assert note1.text == updated_data['text']

    def test_user_cannot_edit_others_note(self, client, user1, note2):
        client.force_login(user1)
        updated_data = {
            'title': 'Attempted Edit', 'text': 'Updated content',
            'slug': note2.slug
        }
        response = client.post(edit_note_url(note2.slug), updated_data)
        assert response.status_code == HTTPStatus.NOT_FOUND
        note2.refresh_from_db()
        assert note2.title != updated_data['title']

    def test_user_can_delete_own_note(self, client, user1, note1):
        client.force_login(user1)
        response = client.post(delete_note_url(note1.slug))
        assert response.status_code == HTTPStatus.FOUND
        assert not Note.objects.filter(id=note1.id).exists()

    def test_user_cannot_delete_others_note(self, client, user1, note2):
        client.force_login(user1)
        response = client.post(delete_note_url(note2.slug))
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert Note.objects.filter(id=note2.id).exists()
