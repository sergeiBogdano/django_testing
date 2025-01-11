from django.urls import reverse

from notes.forms import NoteForm
from .base_test_case import NoteTestBase


class TestNoteContent(NoteTestBase):

    def test_note_in_object_list(self):
        self.client.login(username='user1', password='password1')
        response = self.client.get(reverse('notes:list'))
        self.assertIn(self.note1, response.context['object_list'])
        note = response.context['object_list'].get(pk=self.note1.pk)
        self.assertEqual(note.title, 'Note 1')
        self.assertEqual(note.text, 'Content 1')

    def test_notes_list_excludes_other_users_notes(self):
        self.client.login(username='user1', password='password1')
        response = self.client.get(reverse('notes:list'))
        self.assertIn(self.note1, response.context['object_list'])
        self.assertNotIn(self.note2, response.context['object_list'])

    def test_note_page_contains_form(self):
        self.client.login(username='user1', password='password1')
        urls = [
            reverse('notes:add'),
            reverse('notes:edit', args=[self.note1.slug])
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertIsInstance(response.context['form'], NoteForm)
