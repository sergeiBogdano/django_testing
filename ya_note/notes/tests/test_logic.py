from http import HTTPStatus

from pytils.translit import slugify

from notes.models import Note
from .base_test_case import (
    ADD_NOTE_URL,
    NoteTestBase,
)


class TestLogic(NoteTestBase):

    def test_logged_in_user_can_create_note(self):
        initial_notes = set(Note.objects.all())
        response = self.logged_in_client.post(ADD_NOTE_URL, self.note_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Note.objects.count(), len(initial_notes) + 1)
        new_notes = Note.objects.exclude(
            id__in=[note.id for note in initial_notes]
        )
        self.assertEqual(new_notes.count(), 1)
        new_note = new_notes.get()
        self.assertEqual(new_note.title, self.note_data['title'])
        self.assertEqual(new_note.text, self.note_data['text'])
        self.assertEqual(new_note.author, self.author)
        self.assertEqual(new_note.slug, self.note_data['slug'])

    def test_anonymous_user_cannot_create_note(self):
        initial_notes = set(Note.objects.all())
        response = self.client.post(ADD_NOTE_URL, self.note_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.expected_redirects[ADD_NOTE_URL])
        self.assertEqual(set(Note.objects.all()), initial_notes)

    def test_cannot_create_notes_with_same_slug(self):
        initial_notes = set(Note.objects.all())
        self.note_data['slug'] = self.note.slug
        response = self.logged_in_client.post(ADD_NOTE_URL, self.note_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(set(Note.objects.all()), initial_notes)

    def test_slug_is_generated_if_not_provided(self):
        initial_notes = set(Note.objects.all())
        del self.note_data['slug']
        response = self.logged_in_client.post(ADD_NOTE_URL, self.note_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Note.objects.count(), len(initial_notes) + 1)
        new_notes = Note.objects.exclude(id__in=[
            note.id for note in initial_notes
        ])
        self.assertEqual(new_notes.count(), 1)
        new_note = new_notes.get()
        self.assertEqual(new_note.title, self.note_data['title'])
        self.assertEqual(new_note.text, self.note_data['text'])
        self.assertEqual(new_note.author, self.author)
        self.assertEqual(new_note.slug, slugify(self.note_data['title']))

    def test_user_can_edit_own_note(self):
        response = self.logged_in_client.post(
            self.edit_note_url,
            self.note_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, self.note_data['title'])
        self.assertEqual(note.text, self.note_data['text'])
        self.assertEqual(note.slug, self.note_data['slug'])
        self.assertEqual(note.author, self.note.author)

    def test_user_can_delete_own_note(self):
        initial_note_count = Note.objects.count()
        response = self.logged_in_client.post(self.delete_note_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())
        self.assertEqual(Note.objects.count(), initial_note_count - 1)

    def test_user_cannot_delete_others_note(self):
        response = self.logged_in_client_non_author.post(self.delete_note_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)
