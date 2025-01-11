import pytest
from django.urls import reverse

from notes.forms import NoteForm


@pytest.mark.django_db
def test_note_in_object_list(client, user1, note1):
    client.login(username='user1', password='password1')
    response = client.get(reverse('notes:list'))
    assert note1 in response.context['object_list']
    note = response.context['object_list'].get(pk=note1.pk)
    assert note.title == 'Note 1'
    assert note.text == 'Content 1'


@pytest.mark.django_db
def test_notes_list_excludes_other_users_notes(client, user1, note1, note2):
    client.login(username='user1', password='password1')
    response = client.get(reverse('notes:list'))
    assert note1 in response.context['object_list']
    assert note2 not in response.context['object_list']


@pytest.mark.parametrize(
    "url", [reverse('notes:add'), reverse('notes:edit', args=['note-1'])]
)
@pytest.mark.django_db
def test_note_page_contains_form(client, user1, note1, url):
    client.login(username='user1', password='password1')
    response = client.get(url)
    assert isinstance(response.context['form'], NoteForm)
