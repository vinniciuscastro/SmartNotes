import pytest

from django.contrib.auth.models import User
from notes.models import Note

@pytest.mark.django_db
def test_list_endpoint_return_user_notes(client):
    user = User.objects.create_user('Clara', 'clara@test.com', 'password')
    login_response = client.login(username='Clara', password='password')
    assert login_response is True

    note = Note.objects.create(title='Clara what is good?', text='We all in this industry...', user=user)
    note2 = Note.objects.create(title='Clara what is good? Again', text='We all in this industry...', user=user)
    
    response = client.get(path='/smart/notes')
    assert response.status_code == 200
    content = str(response.content)
    assert "Clara what is good?" in content
    assert "Clara what is good? Again" in content
    assert 0 == content.count('<h2>')