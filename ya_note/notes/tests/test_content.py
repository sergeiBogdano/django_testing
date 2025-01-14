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
            id=self.note1.id
        )
        self.assertEqual(note_from_context.title, self.note1.title)
        self.assertEqual(note_from_context.text, self.note1.text)
        self.assertEqual(note_from_context.slug, self.note1.slug)
        self.assertEqual(note_from_context.author, self.note1.author)

    def test_note_not_in_object_list_for_user2(self):
        response = self.logged_in_client_user2.get(LIST_URL)
        self.assertNotIn(self.note1, response.context['object_list'])

    def test_note_form_on_add_page(self):
        response = self.logged_in_client.get(ADD_NOTE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)

    def test_note_form_on_edit_page(self):
        edit_url = EDIT_NOTE_URL.format(slug=self.note1.slug)
        response = self.logged_in_client.get(edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)
