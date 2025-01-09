from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from notes.models import Note


class TestRoutes(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            password='password1'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='password2'
        )
        self.note = Note.objects.create(
            title='Test Note',
            text='Test Content',
            author=self.user1
        )

    def test_home_page_accessible_to_anonymous(self):
        response = self.client.get(reverse('notes:home'))
        self.assertEqual(response.status_code, 200)

    def test_notes_list_accessible_to_authenticated_user(self):
        self.client.login(username='user1', password='password1')
        response = self.client.get(reverse('notes:list'))
        self.assertEqual(response.status_code, 200)

    def test_note_success_accessible_to_authenticated_user(self):
        self.client.login(username='user1', password='password1')
        response = self.client.get(reverse('notes:success'))
        self.assertEqual(response.status_code, 200)

    def test_add_note_accessible_to_authenticated_user(self):
        self.client.login(username='user1', password='password1')
        response = self.client.get(reverse('notes:add'))
        self.assertEqual(response.status_code, 200)

    def test_note_detail_accessible_to_author(self):
        self.client.login(username='user1', password='password1')
        response = self.client.get(
            reverse('notes:detail', args=[self.note.slug])
        )
        self.assertEqual(response.status_code, 200)

    def test_note_detail_not_accessible_to_other_user(self):
        self.client.login(username='user2', password='password2')
        response = self.client.get(
            reverse('notes:detail', args=[self.note.slug])
        )
        self.assertEqual(response.status_code, 404)

    def test_note_edit_accessible_to_author(self):
        self.client.login(username='user1', password='password1')
        response = self.client.get(
            reverse('notes:edit', args=[self.note.slug])
        )
        self.assertEqual(response.status_code, 200)

    def test_note_edit_not_accessible_to_other_user(self):
        self.client.login(username='user2', password='password2')
        response = self.client.get(
            reverse('notes:edit', args=[self.note.slug])
        )
        self.assertEqual(response.status_code, 404)

    def test_note_delete_accessible_to_author(self):
        self.client.login(username='user1', password='password1')
        response = self.client.get(
            reverse('notes:delete', args=[self.note.slug])
        )
        self.assertEqual(response.status_code, 200)

    def test_note_delete_not_accessible_to_other_user(self):
        self.client.login(username='user2', password='password2')
        response = self.client.get(
            reverse('notes:delete', args=[self.note.slug])
        )
        self.assertEqual(response.status_code, 404)

    def test_anonymous_user_redirected_to_login(self):
        protected_urls = [
            reverse('notes:list'),
            reverse('notes:success'),
            reverse('notes:add'),
            reverse('notes:detail', args=[self.note.slug]),
            reverse('notes:edit', args=[self.note.slug]),
            reverse('notes:delete', args=[self.note.slug]),
        ]
        for url in protected_urls:
            response = self.client.get(url)
            self.assertRedirects(response, f'/auth/login/?next={url}')

    def test_registration_page_accessible_to_anonymous(self):
        response = self.client.get(reverse('users:signup'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_accessible_to_anonymous(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_page_accessible_to_anonymous(self):
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 200)
