from django.urls import reverse

from notes.forms import NoteForm

from .base_test_case import NoteTestBase, LIST_URL


class TestNoteContent(NoteTestBase):
    def setUp(self):
        self.client.login(username='user1', password='password1')

    def test_note_in_object_list(self):
        response = self.client.get(LIST_URL)
        self.assertIn(self.note1, response.context['object_list'])
        self.assertNotIn(self.note2, response.context['object_list'])

    def test_note_page_contains_form(self):
        urls = [
            reverse('notes:add'),
            reverse('notes:edit', args=[self.note1.slug])
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertIsInstance(response.context['form'], NoteForm)
            self.assertContains(response, '<form', status_code=200)
