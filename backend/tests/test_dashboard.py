"""
Tests — Tableau de bord admin (DashboardStatsView) et inscription (RegisterView).
"""
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from .factories import UserFactory, QuoteFactory


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(db):
    return UserFactory()


@pytest.fixture
def staff_user(db):
    return UserFactory(is_staff=True)


@pytest.fixture
def auth_client(client, user):
    r = client.post('/api/v1/auth/token/', {'email': user.email, 'password': 'TestPassword123!'}, format='json')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {r.data["access"]}')
    return client


@pytest.fixture
def staff_client(client, staff_user):
    r = client.post('/api/v1/auth/token/', {'email': staff_user.email, 'password': 'TestPassword123!'}, format='json')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {r.data["access"]}')
    return client


# ─────────────────────────────────────────────
# DashboardStatsView
# ─────────────────────────────────────────────

@pytest.mark.django_db
class TestDashboardStats:

    def test_anonymous_is_forbidden(self, client):
        r = client.get('/api/v1/quotes/dashboard/')
        assert r.status_code == status.HTTP_401_UNAUTHORIZED

    def test_non_staff_is_forbidden(self, auth_client):
        r = auth_client.get('/api/v1/quotes/dashboard/')
        assert r.status_code == status.HTTP_403_FORBIDDEN

    def test_staff_gets_200(self, staff_client):
        r = staff_client.get('/api/v1/quotes/dashboard/')
        assert r.status_code == status.HTTP_200_OK

    def test_response_has_required_keys(self, staff_client):
        r = staff_client.get('/api/v1/quotes/dashboard/')
        assert 'kpis' in r.data
        assert 'recent_quotes' in r.data
        assert 'active_projects' in r.data

    def test_kpis_structure(self, staff_client):
        r = staff_client.get('/api/v1/quotes/dashboard/')
        kpis = r.data['kpis']
        for key in ('quotes_total', 'quotes_this_month', 'quotes_pending',
                    'quotes_accepted', 'conversion_rate',
                    'revenue_total', 'revenue_this_month', 'projects_active'):
            assert key in kpis, f'KPI manquant : {key}'

    def test_kpis_reflect_quotes(self, staff_client, db):
        QuoteFactory(status='accepted', total_ttc=1200)
        QuoteFactory(status='sent')
        QuoteFactory(status='draft')
        r = staff_client.get('/api/v1/quotes/dashboard/')
        kpis = r.data['kpis']
        assert kpis['quotes_total'] >= 3
        assert kpis['quotes_accepted'] >= 1
        assert kpis['quotes_pending'] >= 2

    def test_conversion_rate_is_percentage(self, staff_client, db):
        QuoteFactory(status='accepted')
        QuoteFactory(status='sent')
        r = staff_client.get('/api/v1/quotes/dashboard/')
        rate = r.data['kpis']['conversion_rate']
        assert 0 <= rate <= 100

    def test_recent_quotes_capped_at_ten(self, staff_client, db):
        for _ in range(15):
            QuoteFactory()
        r = staff_client.get('/api/v1/quotes/dashboard/')
        assert len(r.data['recent_quotes']) <= 10

    def test_recent_quote_fields(self, staff_client, db):
        QuoteFactory(status='sent')
        r = staff_client.get('/api/v1/quotes/dashboard/')
        if r.data['recent_quotes']:
            q = r.data['recent_quotes'][0]
            for field in ('uuid', 'quote_number', 'client_name', 'total_ttc', 'status', 'status_display', 'created_at'):
                assert field in q, f'Champ manquant dans recent_quotes : {field}'

    def test_zero_conversion_rate_when_no_quotes(self, staff_client):
        r = staff_client.get('/api/v1/quotes/dashboard/')
        assert r.data['kpis']['conversion_rate'] == 0


# ─────────────────────────────────────────────
# RegisterView + RegisterSerializer
# ─────────────────────────────────────────────

@pytest.mark.django_db
class TestRegister:

    def test_register_creates_user(self, client):
        r = client.post('/api/v1/auth/register/', {
            'email': 'nouveau@example.com',
            'password': 'TestPassword123!',
            'password2': 'TestPassword123!',
            'first_name': 'Alice',
            'last_name': 'Martin',
        }, format='json')
        assert r.status_code == status.HTTP_201_CREATED

    def test_register_auto_generates_username(self, client):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        client.post('/api/v1/auth/register/', {
            'email': 'alice@example.com',
            'password': 'TestPassword123!',
            'password2': 'TestPassword123!',
        }, format='json')
        user = User.objects.get(email='alice@example.com')
        assert user.username == 'alice'

    def test_register_username_collision_gets_suffix(self, client, db):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        # Crée un utilisateur dont l'username = 'bob'
        UserFactory(username='bob', email='bob.existing@example.com')
        client.post('/api/v1/auth/register/', {
            'email': 'bob@example.com',
            'password': 'TestPassword123!',
            'password2': 'TestPassword123!',
        }, format='json')
        user = User.objects.get(email='bob@example.com')
        assert user.username == 'bob_1'

    def test_register_duplicate_email_returns_400(self, client, user):
        r = client.post('/api/v1/auth/register/', {
            'email': user.email,
            'password': 'TestPassword123!',
            'password2': 'TestPassword123!',
        }, format='json')
        assert r.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in r.data

    def test_register_password_mismatch_returns_400(self, client):
        r = client.post('/api/v1/auth/register/', {
            'email': 'mismatch@example.com',
            'password': 'TestPassword123!',
            'password2': 'DifferentPassword!',
        }, format='json')
        assert r.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password2' in r.data

    def test_register_weak_password_returns_400(self, client):
        r = client.post('/api/v1/auth/register/', {
            'email': 'weak@example.com',
            'password': '123',
            'password2': '123',
        }, format='json')
        assert r.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_missing_email_returns_400(self, client):
        r = client.post('/api/v1/auth/register/', {
            'password': 'TestPassword123!',
            'password2': 'TestPassword123!',
        }, format='json')
        assert r.status_code == status.HTTP_400_BAD_REQUEST


# ─────────────────────────────────────────────
# UserSerializer — is_staff exposé
# ─────────────────────────────────────────────

@pytest.mark.django_db
class TestUserSerializerIsStaff:

    def test_me_includes_is_staff_false(self, auth_client):
        r = auth_client.get('/api/v1/auth/me/')
        assert r.status_code == status.HTTP_200_OK
        assert 'is_staff' in r.data
        assert r.data['is_staff'] is False

    def test_me_includes_is_staff_true(self, staff_client):
        r = staff_client.get('/api/v1/auth/me/')
        assert r.status_code == status.HTTP_200_OK
        assert r.data['is_staff'] is True

    def test_is_staff_is_readonly(self, auth_client):
        """Un utilisateur normal ne peut pas s'auto-élever au rang de staff."""
        r = auth_client.patch('/api/v1/auth/me/', {'is_staff': True}, format='json')
        assert r.status_code == status.HTTP_200_OK
        assert r.data['is_staff'] is False
