from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note


class TestContent(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            password='password1'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='password2'
        )
        self.note1 = Note.objects.create(
            title='Note 1',
            text='Content 1',
            author=self.user1
        )
        self.note2 = Note.objects.create(
            title='Note 2',
            text='Content 2',
            author=self.user2
        )

    def test_note_in_object_list(self):
        self.client.login(username='user1', password='password1')
        response = self.client.get(reverse('notes:list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.note1, response.context['object_list'])
        self.assertNotIn(self.note2, response.context['object_list'])

    def test_notes_list_excludes_other_users_notes(self):
        self.client.login(username='user1', password='password1')
        response = self.client.get(reverse('notes:list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.note1, response.context['object_list'])
        self.assertNotIn(self.note2, response.context['object_list'])

    def test_create_note_page_contains_form(self):
        self.client.login(username='user1', password='password1')
        response = self.client.get(reverse('notes:add'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(
            response.context['form'],
            NoteForm
        )

    def test_edit_note_page_contains_form(self):
        self.client.login(username='user1', password='password1')
        response = self.client.get(
            reverse('notes:edit', args=[self.note1.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(
            response.context['form'],
            NoteForm
        )
