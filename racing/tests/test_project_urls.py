import pytest
from django.urls import reverse, resolve
from django.test import Client
from django.conf import settings
 
client = Client()
 
 
@pytest.mark.django_db
def test_home_url():
    url = reverse("home")
    response = client.get(url)
    assert response.status_code == 200
 
 
def test_admin_url_resolves():
    resolver = resolve("/admin/")
    assert resolver is not None
 
 
def test_api_root_resolves():
    response = client.get("/api/")
    assert response.status_code in [200, 401, 403]
 
 
def test_auth_login_url():
    response = client.get("/accounts/login/")
    assert response.status_code == 200
 
 
def test_swagger_ui_url():
    response = client.get("/swagger/")
    assert response.status_code == 200
 
 
def test_redoc_ui_url():
    response = client.get("/redoc/")
    assert response.status_code == 200
 
 
def test_swagger_json_url():
    response = client.get("/swagger.json")
    assert response.status_code == 200
 
 
@pytest.mark.skipif(not settings.DEBUG, reason="MEDIA served only in DEBUG")
def test_media_url_exists():
    assert settings.MEDIA_URL.startswith("/")