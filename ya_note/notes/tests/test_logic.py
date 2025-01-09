from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from pytils.translit import slugify
from notes.models import Note


class TestLogic(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            password='password1'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='password2'
        )

    def test_logged_in_user_can_create_note(self):
        self.client.login(username='user1', password='password1')
        response = self.client.post(reverse('notes:add'), {
            'title': 'New Note',
            'text': 'Some content',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Note.objects.filter(title='New Note').exists())

    def test_anonymous_user_cannot_create_note(self):
        response = self.client.post(reverse('notes:add'), {
            'title': 'Anonymous Note',
            'text': 'Some content',
        })
        login_url = reverse('users:login')
        self.assertRedirects(
            response,
            f'{login_url}?next={reverse("notes:add")}'
        )
        self.assertFalse(Note.objects.filter(title='Anonymous Note').exists())

    def test_cannot_create_notes_with_same_slug(self):
        self.client.login(username='user1', password='password1')
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
        response = self.client.post(reverse('notes:add'), {
            'title': 'Заметка без слага',
            'text': 'Some content',
        })
        self.assertEqual(response.status_code, 302)
        note = Note.objects.get(title='Заметка без слага')
        expected_slug = slugify('Заметка без слага')
        self.assertEqual(note.slug, expected_slug)

    def test_user_can_edit_own_note(self):
        note = Note.objects.create(
            title='Editable Note',
            text='Content',
            author=self.user1
        )
        self.client.login(username='user1', password='password1')
        response = self.client.post(
            reverse('notes:edit', args=[note.slug]), {
                'title': 'Edited Note',
                'text': 'Updated content',
            }
        )
        self.assertEqual(response.status_code, 302)
        note.refresh_from_db()
        self.assertEqual(note.title, 'Edited Note')

    def test_user_cannot_edit_others_note(self):
        note = Note.objects.create(
            title='Uneditable Note',
            text='Content',
            author=self.user2
        )
        self.client.login(username='user1', password='password1')
        response = self.client.post(
            reverse('notes:edit', args=[note.slug]), {
                'title': 'Attempted Edit',
                'text': 'Updated content',
            }
        )
        self.assertEqual(response.status_code, 404)
        note.refresh_from_db()
        self.assertNotEqual(note.title, 'Attempted Edit')

    def test_user_can_delete_own_note(self):
        note = Note.objects.create(
            title='Deletable Note',
            text='Content',
            author=self.user1
        )
        self.client.login(username='user1', password='password1')
        response = self.client.post(
            reverse('notes:delete', args=[note.slug])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Note.objects.filter(id=note.id).exists())

    def test_user_cannot_delete_others_note(self):
        note = Note.objects.create(
            title='Undeletable Note',
            text='Content',
            author=self.user2
        )
        self.client.login(username='user1', password='password1')
        response = self.client.post(
            reverse('notes:delete', args=[note.slug])
        )
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Note.objects.filter(id=note.id).exists())
