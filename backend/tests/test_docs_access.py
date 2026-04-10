import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
class TestDocsAccessInProductionMode:
    """Vérifie que les endpoints de documentation sont protégés hors DEBUG."""

    def setup_method(self):
        self.client = Client()

    def test_anonymous_user_is_redirected_from_docs(self, settings):
        settings.DEBUG = False
        response = self.client.get(reverse('swagger-ui'))
        assert response.status_code == 302
        assert '/admin/login/' in response.url

    def test_anonymous_user_is_redirected_from_schema(self, settings):
        settings.DEBUG = False
        response = self.client.get(reverse('schema'))
        assert response.status_code == 302
        assert '/admin/login/' in response.url

    def test_anonymous_user_is_redirected_from_redoc(self, settings):
        settings.DEBUG = False
        response = self.client.get(reverse('redoc'))
        assert response.status_code == 302
        assert '/admin/login/' in response.url

    def test_non_staff_user_is_redirected_from_docs(self, settings):
        settings.DEBUG = False
        user_model = get_user_model()
        user = user_model.objects.create_user(
            email='user@example.com',
            username='normal-user',
            password='StrongPassword123!',
            is_staff=False,
        )
        self.client.force_login(user)
        response = self.client.get(reverse('swagger-ui'))
        assert response.status_code == 302

    def test_non_staff_user_is_redirected_from_schema(self, settings):
        settings.DEBUG = False
        user_model = get_user_model()
        user = user_model.objects.create_user(
            email='user-schema@example.com',
            username='normal-user-schema',
            password='StrongPassword123!',
            is_staff=False,
        )
        self.client.force_login(user)
        response = self.client.get(reverse('schema'))
        assert response.status_code == 302

    def test_staff_user_can_access_docs(self, settings):
        settings.DEBUG = False
        user_model = get_user_model()
        user = user_model.objects.create_user(
            email='staff@example.com',
            username='staff-user',
            password='StrongPassword123!',
            is_staff=True,
            is_superuser=True,
        )
        self.client.force_login(user)
        response = self.client.get(reverse('swagger-ui'))
        assert response.status_code == 200

    def test_staff_user_can_access_schema_and_redoc(self, settings):
        settings.DEBUG = False
        user_model = get_user_model()
        user = user_model.objects.create_user(
            email='staff-docs@example.com',
            username='staff-docs-user',
            password='StrongPassword123!',
            is_staff=True,
            is_superuser=True,
        )
        self.client.force_login(user)
        schema_response = self.client.get(reverse('schema'))
        redoc_response = self.client.get(reverse('redoc'))
        assert schema_response.status_code == 200
        assert redoc_response.status_code == 200
