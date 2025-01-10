from django.urls import reverse

HOME_URL = reverse('notes:home')
NOTES_LIST_URL = reverse('notes:list')
NOTE_SUCCESS_URL = reverse('notes:success')
ADD_NOTE_URL = reverse('notes:add')
SIGNUP_URL = reverse('users:signup')
LOGIN_URL = reverse('users:login')
LOGOUT_URL = reverse('users:logout')


def note_detail_url(slug):
    return reverse('notes:detail', args=[slug])


def note_edit_url(slug):
    return reverse('notes:edit', args=[slug])


def note_delete_url(slug):
    return reverse('notes:delete', args=[slug])
