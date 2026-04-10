"""
Tests d'intégration — endpoints REST principaux.
Utilise pytest-django + APIClient DRF + factory-boy.
"""
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .factories import (
    ContactRequestFactory,
    PortfolioProjectFactory,
    TestimonialFactory,
    UserFactory,
)


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(db):
    return UserFactory()


@pytest.fixture
def auth_client(client, user):
    """Client authentifié avec JWT."""
    response = client.post(
        '/api/v1/auth/token/',
        {'email': user.email, 'password': 'TestPassword123!'},
        format='json',
    )
    assert response.status_code == status.HTTP_200_OK
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')
    return client


# ─────────────────────────────────────────────
# Auth
# ─────────────────────────────────────────────

@pytest.mark.django_db
class TestAuth:
    def test_login_valid(self, client, user):
        response = client.post(
            '/api/v1/auth/token/',
            {'email': user.email, 'password': 'TestPassword123!'},
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' not in response.data  # refresh en cookie HttpOnly
        assert 'refresh_token' in response.cookies

    def test_login_invalid_password(self, client, user):
        response = client.post(
            '/api/v1/auth/token/',
            {'email': user.email, 'password': 'mauvais'},
            format='json',
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_unknown_email(self, client):
        response = client.post(
            '/api/v1/auth/token/',
            {'email': 'inconnu@example.com', 'password': 'test'},
            format='json',
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_refresh_via_cookie(self, client, user):
        """Le refresh doit fonctionner via le cookie HttpOnly."""
        login = client.post(
            '/api/v1/auth/token/',
            {'email': user.email, 'password': 'TestPassword123!'},
            format='json',
        )
        assert login.status_code == status.HTTP_200_OK
        # Le cookie est automatiquement renvoyé par le test client DRF
        refresh_response = client.post('/api/v1/auth/token/refresh/')
        assert refresh_response.status_code == status.HTTP_200_OK
        assert 'access' in refresh_response.data

    def test_refresh_without_cookie_returns_401(self, client):
        response = client.post('/api/v1/auth/token/refresh/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_logout_clears_cookie(self, client, user):
        client.post(
            '/api/v1/auth/token/',
            {'email': user.email, 'password': 'TestPassword123!'},
            format='json',
        )
        response = client.post('/api/v1/auth/logout/')
        assert response.status_code == status.HTTP_200_OK
        # Le cookie doit être supprimé (max_age=0 ou absent)
        cookie = response.cookies.get('refresh_token')
        assert cookie is None or cookie['max-age'] == 0

    def test_me_authenticated(self, auth_client, user):
        response = auth_client.get('/api/v1/auth/me/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == user.email

    def test_me_unauthenticated(self, client):
        response = client.get('/api/v1/auth/me/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_register_creates_user(self, client, db):
        response = client.post(
            '/api/v1/auth/register/',
            {
                'email': 'nouveau@example.com',
                'username': 'nouveau',
                'password': 'MotDePasse123!',
                'password2': 'MotDePasse123!',
            },
            format='json',
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_register_password_mismatch(self, client, db):
        response = client.post(
            '/api/v1/auth/register/',
            {
                'email': 'test@example.com',
                'username': 'test',
                'password': 'MotDePasse123!',
                'password2': 'Différent456!',
            },
            format='json',
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


# ─────────────────────────────────────────────
# Portfolio
# ─────────────────────────────────────────────

@pytest.mark.django_db
class TestPortfolio:
    def test_list_only_published(self, client):
        PortfolioProjectFactory(is_published=True)
        PortfolioProjectFactory(is_published=True)
        PortfolioProjectFactory(is_published=False)
        response = client.get('/api/v1/portfolio/projects/')
        assert response.status_code == status.HTTP_200_OK
        data = response.data.get('results', response.data)
        assert len(data) == 2

    def test_list_has_image_webp_field(self, client):
        PortfolioProjectFactory(is_published=True)
        response = client.get('/api/v1/portfolio/projects/')
        data = response.data.get('results', response.data)
        assert 'image_webp' in data[0]

    def test_detail_by_slug(self, client):
        project = PortfolioProjectFactory(is_published=True, title='Mon projet test')
        response = client.get(f'/api/v1/portfolio/projects/{project.slug}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Mon projet test'
        assert 'testimonials' in response.data

    def test_detail_not_found(self, client):
        response = client.get('/api/v1/portfolio/projects/inexistant/')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_detail_unpublished_not_accessible(self, client):
        project = PortfolioProjectFactory(is_published=False)
        response = client.get(f'/api/v1/portfolio/projects/{project.slug}/')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_testimonials_list(self, client):
        TestimonialFactory(is_active=True)
        TestimonialFactory(is_active=False)
        response = client.get('/api/v1/portfolio/testimonials/')
        assert response.status_code == status.HTTP_200_OK
        data = response.data.get('results', response.data)
        assert len(data) == 1


# ─────────────────────────────────────────────
# Contact
# ─────────────────────────────────────────────

@pytest.mark.django_db
class TestContact:
    VALID_PAYLOAD = {
        'name': 'Jean Dupont',
        'email': 'jean@example.com',
        'subject': 'project',
        'message': 'Bonjour, je souhaite un devis pour mon projet.',
    }

    def test_create_contact_success(self, client):
        response = client.post('/api/v1/contacts/', self.VALID_PAYLOAD, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_contact_invalid_email(self, client):
        payload = {**self.VALID_PAYLOAD, 'email': 'pas_un_email'}
        response = client.post('/api/v1/contacts/', payload, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_contact_missing_message(self, client):
        payload = {**self.VALID_PAYLOAD, 'message': ''}
        response = client.post('/api/v1/contacts/', payload, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_contact_invalid_subject(self, client):
        payload = {**self.VALID_PAYLOAD, 'subject': 'invalide'}
        response = client.post('/api/v1/contacts/', payload, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST


# ─────────────────────────────────────────────
# Health check
# ─────────────────────────────────────────────

@pytest.mark.django_db
class TestHealth:
    def test_health_returns_ok(self, client):
        response = client.get('/api/v1/health/')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['status'] == 'ok'
