from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase
from pytils.translit import slugify

from notes.models import Note
from notes.constans import (
    ADD_NOTE_URL,
    LOGIN_URL,
    note_edit_url,
    note_delete_url
)


class TestLogic(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(
            username='user1',
            password='password1'
        )
        cls.user2 = User.objects.create_user(
            username='user2',
            password='password2'
        )

    def test_logged_in_user_can_create_note(self):
        self.client.login(username='user1', password='password1')
        form_data = {
            'title': 'New Note',
            'text': 'Some content',
            'slug': 'new-note'
        }
        response = self.client.post(ADD_NOTE_URL, form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        note = Note.objects.get(slug='new-note')
        self.assertEqual(note.title, form_data['title'])
        self.assertEqual(note.text, form_data['text'])
        self.assertEqual(note.author, self.user1)

    def test_anonymous_user_cannot_create_note(self):
        form_data = {
            'title': 'Anonymous Note',
            'text': 'Some content',
            'slug': 'anonymous-note'
        }
        response = self.client.post(ADD_NOTE_URL, form_data)
        self.assertRedirects(response, f'{LOGIN_URL}?next={ADD_NOTE_URL}')
        self.assertFalse(Note.objects.filter(slug='anonymous-note').exists())

    def test_cannot_create_notes_with_same_slug(self):
        Note.objects.create(
            title='Unique Title',
            text='Content',
            author=self.user1,
            slug='unique-slug'
        )
        with self.assertRaises(Exception):
            Note.objects.create(
                title='Another Title',
                text='Content',
                author=self.user1,
                slug='unique-slug'
            )

    def test_slug_is_generated_if_not_provided(self):
        self.client.login(username='user1', password='password1')
        form_data = {
            'title': 'Заметка без слага',
            'text': 'Some content'
        }
        response = self.client.post(ADD_NOTE_URL, form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        note = Note.objects.get(title=form_data['title'])
        self.assertEqual(note.slug, slugify(form_data['title']))
        self.assertEqual(note.text, form_data['text'])
        self.assertEqual(note.author, self.user1)

    def test_user_can_edit_own_note(self):
        note = Note.objects.create(
            title='Editable Note',
            text='Content',
            author=self.user1,
            slug='editable-note'
        )
        self.client.login(username='user1', password='password1')
        form_data = {
            'title': 'Edited Note',
            'text': 'Updated content',
            'slug': 'editable-note'
        }
        response = self.client.post(note_edit_url(note.slug), form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        note.refresh_from_db()
        self.assertEqual(note.title, form_data['title'])
        self.assertEqual(note.text, form_data['text'])

    def test_user_cannot_edit_others_note(self):
        note = Note.objects.create(
            title='Uneditable Note',
            text='Content',
            author=self.user2,
            slug='uneditable-note'
        )
        self.client.login(username='user1', password='password1')
        form_data = {
            'title': 'Attempted Edit',
            'text': 'Updated content',
            'slug': 'uneditable-note'
        }
        response = self.client.post(note_edit_url(note.slug), form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note.refresh_from_db()
        self.assertNotEqual(note.title, form_data['title'])

    def test_user_can_delete_own_note(self):
        note = Note.objects.create(
            title='Deletable Note',
            text='Content',
            author=self.user1,
            slug='deletable-note'
        )
        self.client.login(username='user1', password='password1')
        response = self.client.post(note_delete_url(note.slug))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(Note.objects.filter(id=note.id).exists())

    def test_user_cannot_delete_others_note(self):
        note = Note.objects.create(
            title='Undeletable Note',
            text='Content',
            author=self.user2,
            slug='undeletable-note'
        )
        self.client.login(username='user1', password='password1')
        response = self.client.post(note_delete_url(note.slug))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTrue(Note.objects.filter(id=note.id).exists())
