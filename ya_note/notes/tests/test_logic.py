from http import HTTPStatus

from pytils.translit import slugify

from notes.models import Note

from .base_test_case import (
    NoteTestBase,
    ADD_NOTE_URL,
    get_delete_note_url,
    get_edit_note_url
)


class TestLogic(NoteTestBase):
    def test_logged_in_user_can_create_note(self):
        self.client.force_login(self.user1)
        response = self.client.post(ADD_NOTE_URL, self.note_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Note.objects.count(), self.initial_note_count + 1)
        note = Note.objects.get(title=self.note_data['title'])
        self.assertEqual(note.title, self.note_data['title'])
        self.assertEqual(note.text, self.note_data['text'])
        self.assertEqual(note.author, self.user1)
        self.assertEqual(note.slug, slugify(self.note_data['title']))

    def test_anonymous_user_cannot_create_note(self):
        response = self.client.post(ADD_NOTE_URL, self.note_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(
            response.url.startswith(f'{self.login_url}?next={ADD_NOTE_URL}')
        )
        self.assertEqual(Note.objects.count(), self.initial_note_count)

    def test_cannot_create_notes_with_same_slug(self):
        self.client.force_login(self.user1)
        response = self.client.post(ADD_NOTE_URL, {
            'title': self.note1.title,
            'text': 'Some other content',
            'slug': self.note1.slug
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Note.objects.count(), self.initial_note_count)

    def test_slug_is_generated_if_not_provided(self):
        self.client.force_login(self.user1)
        note_data = {'title': 'Заметка без слага', 'text': 'Some content'}
        response = self.client.post(ADD_NOTE_URL, note_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Note.objects.count(), self.initial_note_count + 1)
        note = Note.objects.get(title=note_data['title'])
        self.assertEqual(note.slug, slugify(note_data['title']))
        self.assertEqual(note.text, note_data['text'])
        self.assertEqual(note.author, self.user1)

    def test_user_can_edit_own_note(self):
        self.client.force_login(self.user1)
        updated_data = {
            'title': 'Edited Note',
            'text': 'Updated content',
            'slug': self.note1.slug
        }
        response = self.client.post(get_edit_note_url(
            self.note1.slug
        ), updated_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        note = Note.objects.get(id=self.note1.id)
        self.assertEqual(note.title, updated_data['title'])
        self.assertEqual(note.text, updated_data['text'])
        self.assertEqual(note.slug, updated_data['slug'])
        self.assertEqual(note.author, self.user1)

    def test_user_can_delete_own_note(self):
        self.client.force_login(self.user1)
        response = self.client.post(get_delete_note_url(self.note1.slug))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(Note.objects.filter(id=self.note1.id).exists())
        self.assertEqual(Note.objects.count(), self.initial_note_count - 1)

    def test_user_cannot_delete_others_note(self):
        self.client.force_login(self.user1)
        response = self.client.post(get_delete_note_url(self.note2.slug))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get(id=self.note2.id)
        self.assertEqual(note.title, self.note2.title)
        self.assertEqual(note.text, self.note2.text)
        self.assertEqual(note.slug, self.note2.slug)
        self.assertEqual(note.author, self.note2.author)
