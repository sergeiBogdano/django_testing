from notes.forms import NoteForm

from .base_test_case import (
    ADD_NOTE_URL,
    EDIT_NOTE1_URL,
    LIST_URL,
    NoteTestBase
)


class TestNoteContent(NoteTestBase):

    def test_note_in_object_list(self):
        response = self.logged_in_client.get(LIST_URL)
        self.assertIn(self.note1, response.context['object_list'])
        note_from_context = next(
            note for note in response.context[
                'object_list'
            ] if note == self.note1
        )
        self.assertEqual(note_from_context.title, self.note1.title)
        self.assertEqual(note_from_context.text, self.note1.text)
        self.assertEqual(note_from_context.slug, self.note1.slug)

    def test_note_not_in_object_list_for_user2(self):
        self.client.force_login(self.user2)
        response = self.client.get(LIST_URL)
        self.assertIn(self.note2, response.context['object_list'])

    def test_note_page_contains_form(self):
        urls = [
            ADD_NOTE_URL,
            EDIT_NOTE1_URL
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.logged_in_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
