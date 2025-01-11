from django.urls import reverse

HOME_URL = reverse('notes:home')
LIST_URL = reverse('notes:list')
SUCCESS_URL = reverse('notes:success')
ADD_NOTE_URL = reverse('notes:add')


def edit_note_url(slug):
    return reverse('notes:edit', args=[slug])


def delete_note_url(slug):
    return reverse('notes:delete', args=[slug])


def detail_note_url(slug):
    return reverse('notes:detail', args=[slug])
