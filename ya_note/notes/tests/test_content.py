from .base_test_case import (
    ADD_NOTE_URL,
    EDIT_NOTE_URL,
    LIST_URL,
    NoteTestBase
)
from notes.forms import NoteForm


class TestNoteContent(NoteTestBase):

    def test_note_in_object_list(self):
        response = self.logged_in_client.get(LIST_URL)
        note_from_context = response.context['object_list'].get(
            id=self.note.id
        )
        self.assertEqual(note_from_context.title, self.note.title)
        self.assertEqual(note_from_context.text, self.note.text)
        self.assertEqual(note_from_context.slug, self.note.slug)
        self.assertEqual(note_from_context.author, self.note.author)

    def test_note_not_in_object_list_for_non_author(self):
        response = self.logged_in_client_non_author.get(LIST_URL)
        self.assertNotIn(self.note, response.context['object_list'])

    def test_note_form_on_add_and_edit_pages(self):
        for url in [ADD_NOTE_URL, EDIT_NOTE_URL.format(slug=self.note.slug)]:
            with self.subTest(url=url):
                response = self.logged_in_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
