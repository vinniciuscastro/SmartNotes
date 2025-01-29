import pytest
from django.contrib.auth.models import User

def test_home_view(client):
    response = client.get(path='/')
    assert 200 == response.status_code
    assert 'Welcome to SmartNotes' in str(response.content)

def test_signup(client):
    response = client.get(path='/signup/')
    assert 200 == response.status_code
    assert 'home/register.html' in response.template_name

@pytest.mark.django_db
def test_signup_authenticated(client):
    """
    When a user is authentticated and try to access the 
    signup page, it should be redirected to the notes list page. 
    """
    user = User.objects.create_user('Clara','clara@example.com','password')
    client.login(username=user, password='password')
    response = client.get(path='/signup/', follow=True)
    assert 200 == response.status_code
    assert 'notes/notes.html' in response.template_name