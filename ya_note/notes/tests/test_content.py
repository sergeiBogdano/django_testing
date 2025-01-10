from notes.forms import NoteForm
from notes.constans import NOTES_LIST_URL, ADD_NOTE_URL, note_edit_url
from .base_test_case import NoteTestBase


class TestContent(NoteTestBase):

    def test_note_in_object_list(self):
        self.client.login(username='user1', password='password1')
        response = self.client.get(NOTES_LIST_URL)
        self.assertIn(self.note1, response.context['object_list'])
        note_from_response = (
            response.context['object_list'].get(id=self.note1.id)
        )
        self.assertEqual(note_from_response.title, self.note1.title)
        self.assertEqual(note_from_response.text, self.note1.text)
        self.assertEqual(note_from_response.author, self.note1.author)

    def test_notes_list_excludes_other_users_notes(self):
        self.client.login(username='user1', password='password1')
        response = self.client.get(NOTES_LIST_URL)
        self.assertIn(self.note1, response.context['object_list'])
        self.assertNotIn(self.note2, response.context['object_list'])

    def test_create_and_edit_note_page_contains_form(self):
        self.client.login(username='user1', password='password1')
        urls = [ADD_NOTE_URL, note_edit_url(self.note1.slug)]
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertIsInstance(response.context['form'], NoteForm)
