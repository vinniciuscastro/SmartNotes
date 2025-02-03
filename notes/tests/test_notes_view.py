import pytest

from django.contrib.auth.models import User # type: ignore
from notes.models import Note
from .factories import UserFactory, NoteFactory

@pytest.fixture
def logged_user(client):
    user = UserFactory()
    client.login(username=user.username, password='password')
    return user

@pytest.mark.django_db
def test_list_endpoint_return_user_notes(client, logged_user):

    # assert logged_user is True
    fac_note = NoteFactory(user=logged_user)
    note = Note.objects.create(title='Clara what is good?', text='We all in this industry...', user=logged_user)
    note2 = Note.objects.create(title='Clara what is good? Again', text='We all in this industry...', user=logged_user)
    
    response = client.get(path='/smart/notes')
    assert response.status_code == 200
    content = str(response.content)

    assert fac_note.title in content
    assert note.title in content
    assert note2.title in content
    assert 0 == content.count('<h2>')

@pytest.mark.django_db
def test_list_endpoint_notes_from_authenticated_users(client, logged_user):
    """
    This test checks if the only notes from authenticated users
    are displayed in the notes list page, making sure that each user
    has access only to their own notes.
    """
    jon = User.objects.create_user('Jon', 'jon@test.com', 'password')
    Note.objects.create(title='You know nothing Jon Snow', text='Dracaris', user=jon)
    
    # assert logged_user is True

    note = Note.objects.create(title='Clara what is good?', text='We all in this industry...', user=logged_user)
    note2 = Note.objects.create(title='Clara what is good? Again', text='We all in this industry...', user=logged_user)
    
    response = client.get(path='/smart/notes')
    assert response.status_code == 200
    content = str(response.content)
    assert "Clara what is good?" in content
    assert "Clara what is good? Again" in content
    assert "You know nothing Jon Snow" not in content
    assert 0 == content.count('<h2>')


@pytest.mark.django_db
def test_create_endpoint_receives_form_data(client, logged_user):
    """
    This test checks if the create endpoint receives the form data
    and creates a new note in the database.
    """
    form_data = {
        'title': 'Clara what is good?',
        'text': 'We are all in this industry...',
    }
    response = client.post(path='/smart/notes/new', data=form_data, follow=True)
    assert 200 == response.status_code
    assert "notes/notes.html" in response.template_name
    assert 1 == logged_user.notes.count()