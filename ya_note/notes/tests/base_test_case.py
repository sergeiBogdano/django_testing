from django.contrib.auth.models import User
from django.test import TestCase
from notes.models import Note


class NoteTestBase(TestCase):

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
        cls.note1 = Note.objects.create(
            title='Note 1',
            text='Content 1',
            author=cls.user1
        )
        cls.note2 = Note.objects.create(
            title='Note 2',
            text='Content 2',
            author=cls.user2
        )
