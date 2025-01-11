from http import HTTPStatus

from django.urls import reverse
from pytils.translit import slugify

from notes.models import Note
from .base_test_case import (
    NoteTestBase,
    ADD_NOTE_URL,
    delete_note_url,
    edit_note_url
)


class TestLogic(NoteTestBase):

    def test_logged_in_user_can_create_note(self):
        self.client.force_login(self.user1)
        response = self.client.post(ADD_NOTE_URL, self.note_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(Note.objects.filter(
            slug=self.note_data['slug']).exists())
        note = Note.objects.get(slug=self.note_data['slug'])
        self.assertEqual(note.title, self.note_data['title'])
        self.assertEqual(note.text, self.note_data['text'])
        self.assertEqual(note.author, self.user1)

    def test_anonymous_user_cannot_create_note(self):
        response = self.client.post(ADD_NOTE_URL, self.note_data)
        login_url = reverse('users:login')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(response.url.startswith(
            f'{login_url}?next={ADD_NOTE_URL}'))
        self.assertFalse(Note.objects.filter(
            slug=self.note_data['slug']).exists())

    def test_cannot_create_notes_with_same_slug(self):
        self.client.force_login(self.user1)
        with self.assertRaises(Exception):
            Note.objects.create(
                title='Another Title', text='Content',
                author=self.user1, slug=self.note1.slug
            )

    def test_slug_is_generated_if_not_provided(self):
        self.client.force_login(self.user1)
        note_data = {'title': 'Заметка без слага', 'text': 'Some content'}
        response = self.client.post(ADD_NOTE_URL, note_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        note = Note.objects.get(title=note_data['title'])
        self.assertEqual(note.slug, slugify(note_data['title']))
        self.assertEqual(note.text, note_data['text'])
        self.assertEqual(note.author, self.user1)

    def test_user_can_edit_own_note(self):
        self.client.force_login(self.user1)
        updated_data = {
            'title': 'Edited Note', 'text': 'Updated content',
            'slug': self.note1.slug
        }
        response = self.client.post(
            edit_note_url(self.note1.slug), updated_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.note1.refresh_from_db()
        self.assertEqual(self.note1.title, updated_data['title'])
        self.assertEqual(self.note1.text, updated_data['text'])

    def test_user_can_delete_own_note(self):
        self.client.force_login(self.user1)
        response = self.client.post(delete_note_url(self.note1.slug))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(Note.objects.filter(id=self.note1.id).exists())

    def test_user_cannot_delete_others_note(self):
        self.client.force_login(self.user1)
        response = self.client.post(delete_note_url(self.note2.slug))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTrue(Note.objects.filter(id=self.note2.id).exists())
