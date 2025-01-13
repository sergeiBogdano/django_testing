from http import HTTPStatus

from pytils.translit import slugify

from notes.models import Note

from .base_test_case import ADD_NOTE_URL, LOGIN_URL, NoteTestBase


class TestLogic(NoteTestBase):
    def test_logged_in_user_can_create_note(self):
        initial_note_count = Note.objects.count()
        response = self.logged_in_client.post(ADD_NOTE_URL, self.note_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Note.objects.count(), initial_note_count + 1)
        new_note = Note.objects.get(
            title=self.note_data['title'],
            text=self.note_data['text']
        )
        self.assertEqual(new_note.author, self.user1)
        self.assertEqual(new_note.slug, self.note_data['slug'])

    def test_anonymous_user_cannot_create_note(self):
        initial_notes = set(Note.objects.all())
        response = self.client.post(ADD_NOTE_URL, self.note_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        expected_redirect_url = f'{LOGIN_URL}?next={ADD_NOTE_URL}'
        self.assertEqual(response.url, expected_redirect_url)
        self.assertEqual(set(Note.objects.all()), initial_notes)

    def test_cannot_create_notes_with_same_slug(self):
        initial_notes = set(Note.objects.all())
        self.note_data['slug'] = self.note1.slug
        response = self.logged_in_client.post(ADD_NOTE_URL, self.note_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(set(Note.objects.all()), initial_notes)

    def test_slug_is_generated_if_not_provided(self):
        initial_notes = set(Note.objects.all())
        del self.note_data['slug']
        response = self.logged_in_client.post(ADD_NOTE_URL, self.note_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Note.objects.count(), len(initial_notes) + 1)

        new_note = Note.objects.exclude(
            id__in=[note.id for note in initial_notes]
        ).get()
        self.assertEqual(new_note.title, self.note_data['title'])
        self.assertEqual(new_note.text, self.note_data['text'])
        self.assertEqual(new_note.slug, slugify(self.note_data['title']))
        self.assertEqual(new_note.author, self.user1)

    def test_user_can_edit_own_note(self):
        note_urls = self.get_note_urls(self.note1)
        response = self.logged_in_client.post(
            note_urls['edit'], self.note_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        note = Note.objects.get(id=self.note1.id)
        self.assertEqual(note.title, self.note_data['title'])
        self.assertEqual(note.text, self.note_data['text'])
        self.assertEqual(note.slug, self.note_data['slug'])
        self.assertEqual(note.author, self.note1.author)

    def test_user_can_delete_own_note(self):
        note_urls = self.get_note_urls(self.note1)
        initial_note_count = Note.objects.count()
        response = self.logged_in_client.post(note_urls['delete'])
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(Note.objects.filter(id=self.note1.id).exists())
        self.assertEqual(Note.objects.count(), initial_note_count - 1)

    def test_user_cannot_delete_others_note(self):
        note_urls = self.get_note_urls(self.note2)
        response = self.logged_in_client_user1.post(note_urls['delete'])
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get(id=self.note2.id)
        self.assertEqual(note.title, self.note2.title)
        self.assertEqual(note.text, self.note2.text)
        self.assertEqual(note.slug, self.note2.slug)
        self.assertEqual(note.author, self.note2.author)
